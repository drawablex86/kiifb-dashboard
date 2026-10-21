import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import changeLogJson from '../../../data/processed/change_log.json';
import type { PageServerLoad } from './$types';

/**
 * T094 (Milestone 9) — `/trends` server load.
 *
 * Timeline data is derived ONLY from `data/snapshots/` (archived canonical
 * snapshot runs written by scripts/diff_snapshots.py, T082) plus
 * `data/processed/change_log.json`. Nothing is hardcoded: every as-of label
 * comes from the snapshot run directory names, and every aggregate is
 * recomputed from the archived datasets by `scripts/refresh_pipeline.py`.
 *
 * Timeline granularity disclosure: snapshot cadence is monthly at minimum
 * (`<YYYY-MM>`), with intra-month re-runs suffixed `__<YYYYMMDDTHHMMSSZ>`.
 * The page states how many points exist and what interval they span.
 */

type SnapshotPoint = {
	/** Snapshot run directory name (unique key). */
	run: string;
	/** Human label, e.g. "2026-10 (monthly baseline)" or "2026-10-21 03:18 UTC". */
	asOfLabel: string;
	/** Date-only ISO label, e.g. "2026-10" / "2026-10-21". */
	asOfDate: string;
	approvedCrore: number;
	releasedCrore: number;
	records: number;
	districtedRecords: number;
	coordRecords: number;
	flaggedRecords: number;
	/** <normalised_status, count[]> via record counts. */
	statusHistogram: Record<string, number>;
	/** Districts with >0 crore released, sorted desc; multi-district splits credit each district. */
	perDistrict: { district: string; releasedCrore: number; records: number }[];
	/** Share of district-attributed released funds held by the top-3 districts (%). */
	top3SharePct: number;
};

type DistrictPoint = { district: string; releasedCrore: number; records: number };

const SNAPSHOTS_DIR = 'data/snapshots';
const KIIFB_FILE = 'kiifb_projects.json';

function listSnapshotRuns(): string[] {
	try {
		return readdirSync(SNAPSHOTS_DIR)
			.filter(
				(d: string) =>
					!d.startsWith('.') &&
					existsSync(join(SNAPSHOTS_DIR, d, KIIFB_FILE))
			)
			.sort();
	} catch {
		return [];
	}
}

/** Run directory name → point-in-time labels. */function labelsFor(run: string): { asOfLabel: string; asOfDate: string } {
	const [base, stamp] = run.split('__');
	if (stamp) {
		const m = stamp.match(/^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})/);
		if (m) {
			const [, y, mo, d, hh, mm] = m;
			return {
				asOfDate: `${y}-${mo}-${d}`,
				asOfLabel: `${y}-${mo}-${d} ${hh}:${mm} UTC (${base} cycle)`
			};
		}
	}
	return { asOfDate: base, asOfLabel: `${base} (monthly baseline)` };
}

/** Multi-district values are comma-joined by the matcher — credit each district share, counting records with a split-cap of 1 each (documented on the page). */
function districtBuckets(projs: Record<string, unknown>[]): Map<string, DistrictPoint> {
	const byD = new Map<string, DistrictPoint>();
	for (const p of projs) {
		const d = (p as { district?: string | null }).district;
		if (!d) continue;
		const record = p as {
			financials?: { released_crore?: number };
			open_flags?: string[];
		};
		const rel = record.financials?.released_crore ?? 0;
		const parts = [...new Set(d.split(',').map((s) => s.trim()))];
		const credit = parts.length > 0 ? rel / parts.length : 0;
		for (const part of parts) {
			const cur = byD.get(part) ?? { district: part, releasedCrore: 0, records: 0 };
			cur.releasedCrore += credit;
			cur.records += 1;
			byD.set(part, cur);
		}
	}
	return byD;
}

function pointFor(run: string): SnapshotPoint {
	const projs = (<{ projects: Record<string, unknown>[] }>(
		JSON.parse(readFileSync(join(SNAPSHOTS_DIR, run, KIIFB_FILE), 'utf-8'))
	)).projects;

	let approvedCrore = 0;
	let releasedCrore = 0;
	let districtedRecords = 0;
	let coordRecords = 0;
	let flaggedRecords = 0;
	const statusHistogram: Record<string, number> = {};

	for (const raw of projs) {
		const p = raw as {
			financials?: { approved_crore?: number; released_crore?: number };
			district?: string | null;
			coordinates?: { lat?: number; lng?: number } | null;
			open_flags?: string[];
			status?: { normalised_status?: string };
		};
		approvedCrore += p.financials?.approved_crore ?? 0;
		releasedCrore += p.financials?.released_crore ?? 0;
		if (p.district) districtedRecords += 1;
		if (p.coordinates && p.coordinates.lat != null && p.coordinates.lng != null) coordRecords += 1;
		if (p.open_flags && p.open_flags.length > 0) flaggedRecords += 1;
		const st = p.status?.normalised_status ?? 'unknown';
		statusHistogram[st] = (statusHistogram[st] ?? 0) + 1;
	}

	const byD = districtBuckets(projs);
	const districts = [...byD.values()].sort((a, b) => b.releasedCrore - a.releasedCrore);
	const attributed = districts.reduce((s, d) => s + d.releasedCrore, 0);
	const top3 = districts.slice(0, 3);
	const top3SharePct =
		attributed > 0 ? (top3.reduce((s, d) => s + d.releasedCrore, 0) / attributed) * 100 : 0;

	return {
		run,
		...labelsFor(run),
		approvedCrore,
		releasedCrore,
		records: projs.length,
		districtedRecords,
		coordRecords,
		flaggedRecords,
		statusHistogram,
		perDistrict: districts,
		top3SharePct
	};
}

type ChangeLogShape = {
	note?: string;
	datasets?: Record<
		string,
		{
			status_migrations?: { id: string; from: string | null; to: string | null }[];
			totals?: { flags_added?: number; flags_resolved?: number };
			coverage?: { district_prev?: number; district_curr?: number; total_curr?: number };
		}
	>;
};

const changeLogData = changeLogJson as unknown as ChangeLogShape;

export const load: PageServerLoad = async () => {
	const runs = listSnapshotRuns();
	const points: SnapshotPoint[] = runs.map(pointFor);

	// District series keeps a consistent top-N across snapshots (union of top 8).
	const topDistricts = [...new Set(points.flatMap((p) => p.perDistrict.slice(0, 8).map((d) => d.district)))].slice(
		0,
		8
	);

	return {
		points,
		topDistricts,
		statusMigrations:
			changeLogData.datasets?.['kiifb_projects.json']?.status_migrations ?? [],
		flagTrend: {
			added: changeLogData.datasets?.['kiifb_projects.json']?.totals?.flags_added ?? 0,
			resolved: changeLogData.datasets?.['kiifb_projects.json']?.totals?.flags_resolved ?? 0
		},
		coverageDelta: {
			prev: changeLogData.datasets?.['kiifb_projects.json']?.coverage?.district_prev ?? null,
			curr: changeLogData.datasets?.['kiifb_projects.json']?.coverage?.district_curr ?? null,
			total: changeLogData.datasets?.['kiifb_projects.json']?.coverage?.total_curr ?? null
		},
		changeLogNote: changeLogData.note ?? ''
	};
};
