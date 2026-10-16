import genesisData from '../../../data/processed/kiifb_genesis.json';
import federalData from '../../../data/processed/opposing_pillars_and_federalism.json';
import tablesData from '../../../data/processed/committee_financial_tables.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		statutoryEvolution: genesisData.statutory_evolution,
		keyArchitects: genesisData.key_architects,
		fiduciaryCommission: genesisData.fiduciary_trust_commission,
		theoreticalPremise: genesisData.theoretical_premise,
		opposingPillars: federalData.opposing_pillars_matrix,
		federalismContext: federalData.federalism_context,
		financialTables: tablesData.tables,
		manifest: manifestData
	};
};
