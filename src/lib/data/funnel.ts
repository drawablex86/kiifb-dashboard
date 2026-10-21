/**
 * funnel.ts — T101 (Milestone 10)
 *
 * Pure helpers for the Portfolio → Sector → District → Project drill-down
 * funnel. Kept framework-free so the same aggregation maths can be
 * reconciled against `unified_project_explorer.json` in unit tests
 * (tests/test_portfolio_funnel.py).
 */

export type FunnelRecord = {
	record_id: string;
	name?: string;
	department?: string;
	entity_type?: string;
	sector?: string;
	district?: string;
	financials?: { approved_crore?: number; released_crore?: number };
	status?: { normalised_status?: string };
};

export type FunnelSummary = {
	count: number;
	approved_crore: number;
	released_crore: number;
	/** Share of records whose normalised status discloses physical completion. */
	pct_physically_complete: number;
};

/** Statuses that count as physically complete in the funnel tiles. */
const PHYSICALLY_COMPLETE_STATUSES = ['physically_complete', 'handed_over', 'operational'];

/** Records having any disclosed financial figures (denominator for sums). */
export function summarise(records: FunnelRecord[]): FunnelSummary {
	let approved = 0;
	let released = 0;
	let complete = 0;
	for (const r of records) {
		approved += r.financials?.approved_crore ?? 0;
		released += r.financials?.released_crore ?? 0;
		if (PHYSICALLY_COMPLETE_STATUSES.includes(r.status?.normalised_status ?? '')) complete += 1;
	}
	return {
		count: records.length,
		approved_crore: Math.round(approved * 100) / 100,
		released_crore: Math.round(released * 100) / 100,
		pct_physically_complete: records.length === 0 ? 0 : Math.round((complete / records.length) * 1000) / 10
	};
}

/** Records belonging to a district (multi-district fields split on ','), prefixed 'ALL'-safe. */
export function belongsToDistrict(rec: FunnelRecord, district: string): boolean {
	if (!rec.district) return false;
	return rec.district.split(',').some((s) => s.trim() === district);
}

export function listSectors(records: FunnelRecord[], parent?: FunnelRecord[]): string[] {
	const src = parent ?? records;
	return Array.from(new Set(src.map((r) => r.sector).filter((s): s is string => Boolean(s)))).sort();
}

export function listDistricts(records: FunnelRecord[], parent?: FunnelRecord[]): string[] {
	const src = parent ?? records;
	return Array.from(
		new Set(
			src
				.map((r) => r.district)
				.filter(Boolean)
				.flatMap((d) => d!.split(',').map((s) => s.trim()))
		)
	).sort();
}

/** Funnel path filters: null entry = level not yet drilled. */
export function applyFunnel(
	records: FunnelRecord[],
	sector: string | null,
	district: string|null
): FunnelRecord[] {
	let out = records;
	if (sector) out = out.filter((r) => r.sector === sector);
	if (district) out = out.filter((r) => belongsToDistrict(r, district));
	return out;
}
