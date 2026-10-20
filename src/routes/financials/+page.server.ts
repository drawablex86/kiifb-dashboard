import tablesData from '../../../data/processed/committee_financial_tables.json';
import explorerData from '../../../data/processed/unified_project_explorer.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		tables: tablesData.tables,
		records: explorerData.records,
		manifest: manifestData
	};
};
