import explorerData from '../../../data/processed/unified_project_explorer.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		summary: explorerData.summary,
		records: explorerData.records,
		manifest: manifestData
	};
};
