import tablesData from '../../../data/processed/committee_financial_tables.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		tables: tablesData.tables,
		manifest: manifestData
	};
};
