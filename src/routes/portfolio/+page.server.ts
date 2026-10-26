import explorerData from '../../../data/processed/unified_project_explorer.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

/**
 * T101 (Milestone 10) — portfolio drill-down funnel (Portfolio →
 * Sector → District → Project). Only processed public data from
 * `unified_project_explorer.json` is exposed. Filter state is carried
 * in shareable URL search params (`?sector=&district=`) and restored
 * exactly on reload / link sharing.
 */
export const prerender = false;
export const load: PageServerLoad = async () => {
	return {
		summary: explorerData.summary,
		records: explorerData.records,
		generatedAt: explorerData.generated_at,
		manifest: manifestData
	};
};
