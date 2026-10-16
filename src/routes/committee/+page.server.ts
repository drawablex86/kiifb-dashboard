import scrutinyData from '../../../data/processed/committee_scrutiny.json';
import federalData from '../../../data/processed/opposing_pillars_and_federalism.json';
import tablesData from '../../../data/processed/committee_financial_tables.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		legalConstitution: scrutinyData.legal_constitution,
		proceduralLapses: scrutinyData.procedural_and_positional_lapses,
		members: scrutinyData.members,
		advisoryApparatus: scrutinyData.advisory_apparatus,
		originsAndTiming: scrutinyData.origins_timing_and_nature,
		opposingPillars: federalData.opposing_pillars_matrix,
		federalismContext: federalData.federalism_context,
		financialTables: tablesData.tables,
		manifest: manifestData
	};
};
