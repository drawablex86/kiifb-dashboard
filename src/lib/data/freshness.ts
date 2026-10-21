import manifestJson from '../../../data/manifest.json';
import changeLogJson from '../../../data/processed/change_log.json';

/**
 * T095 (Milestone 9) — Data freshness resolution.
 *
 * Dates are derived from `data/manifest.json` retrieval records only:
 *   1. a source's `retrieved_at` (archived baseline registration date), and
 *   2. any T080 live-crawl history (`manifest.live_crawls` — success/unchanged
 *      entries mean the content was re-verified against the live source on
 *      that date).
 * The "mode" label therefore reflects reality:
 *   - `archived` → the evidence is the checksum-verified pinned baseline
 *     (never re-fetched, still reproducible), while
 *   - `live-verified` → a later crawl confirmed the content (or recorded an
 *     update from) the live source.
 * No date on any badge is hardcoded; everything traces to the manifest.
 */

type ManifestSource = {
	source_id: string;
	title?: string;
	retrieved_at?: string;
};

type ManifestCrawl = {
	source_id: string;
	retrieved_at: string;
	status: string;
	arc_dir?: string;
};

type ManifestShape = {
	last_updated?: string;
	sources?: ManifestSource[];
	live_crawls?: ManifestCrawl[];
};

export const manifest = manifestJson as unknown as ManifestShape;

/** Server-side import of the deterministic change log (snapshot-run provenance). */
type ChangeLogMetaShape = {
	computed_from?: { prev?: string; curr?: string; dataset_root?: string };
};
export const changeLogMeta = changeLogJson as unknown as ChangeLogMetaShape;

export type Freshness = {
	sourceId: string;
	/** YYYY-MM-DD, from manifest retrieval records. */
	asOfDate: string;
	mode: 'archived' | 'live-verified';
	/** True when a later live crawl saw content change vs the baseline. */
	crawlUpdated: boolean;
};

const LIVE_VERIFIED_STATUSES = new Set(['success', 'unchanged']);

function isoDate(full?: string | null): string {
	return full ? String(full).slice(0, 10) : 'unknown';
}

export function freshnessFor(sourceId: string): Freshness {
	const src = manifest.sources?.find((s) => s.source_id === sourceId);
	const crawls = (manifest.live_crawls ?? [])
		.filter((c) => c.source_id === sourceId && LIVE_VERIFIED_STATUSES.has(c.status))
		.sort((a, b) => (a.retrieved_at < b.retrieved_at ? -1 : 1));
	const lastCrawl = crawls.length > 0 ? crawls[crawls.length - 1] : null;

	// Prefer the later of (baseline registration, newest successful crawl) —
	// the date at which this dashboard's copy was most recently confirmed.
	const base = isoDate(src?.retrieved_at);
	const live = lastCrawl ? isoDate(lastCrawl.retrieved_at) : null;
	const asOfDate = live && base !== 'unknown' && live > base ? live : base !== 'unknown' ? base : live ?? 'unknown';

	return {
		sourceId,
		asOfDate,
		mode: lastCrawl ? 'live-verified' : 'archived',
		crawlUpdated: lastCrawl?.status === 'success'
	};
}

/**
 * Route → primary evidence sources. Used by the persistent layout badge;
 * individual pages may pass their own narrower set (e.g. /trends).
 */
export function routeSources(pathname: string): string[] {
	const table: Record<string, string[]> = {
		'/': ['DS001'],
		'/projects': ['DS010', 'DS021', 'DS030'],
		'/financials': ['DS001', 'DS010'],
		'/outcomes': ['DS010', 'DS021', 'DS030'],
		'/governance': ['DS001', 'DS010'],
		'/committee': ['DS001'],
		'/genesis': ['DS001'],
		'/trends': ['DS010', 'DS030']
	};
	return table[pathname] ?? ['DS001'];
}

/** Aggregated freshness across a route's sources. */
export function routeFreshness(pathname: string): Freshness[] {
	return routeSources(pathname).map(freshnessFor);
}

/** Snapshot-run date parsed from the change log's computed_from pointer (for /trends et-al). */
export function snapshotAsOf(): { run: string; isoDate: string } {
	const run = changeLogMeta.computed_from?.curr ?? '';
	const stamp = run.split('__')[1] ?? '';
	const m = stamp.match(/^(\d{4})(\d{2})(\d{2})/);
	const base = run.split('__')[0];
	return { run, isoDate: m ? `${m[1]}-${m[2]}-${m[3]}` : base };
}
