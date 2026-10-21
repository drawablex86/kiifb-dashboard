import explorerData from '../../../data/processed/unified_project_explorer.json';
import changeLog from '../../../data/processed/change_log.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

/**
 * T102 (Milestone 10) — delay & anomaly register. Only processed public
 * data is exposed: open flags from `unified_project_explorer.json` and
 * the per-flag trend history retained in `change_log.json` (T082).
 * Resolved flags are never deleted — they remain in the change log.
 */
export const load: PageServerLoad = async () => {
	return {
		records: explorerData.records,
		changeLog: {
			computed_from: changeLog.computed_from,
			note: changeLog.note,
			portfolio_totals_delta_inr: changeLog.portfolio_totals_delta_inr,
			// Per-dataset flag history (added/resolved) — retained permanently.
			datasets: changeLog.datasets
		},
		manifest: manifestData
	};
};
