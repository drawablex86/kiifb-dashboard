import legalData from '../../../data/processed/legal_issues_register.json';
import recsData from '../../../data/processed/committee_recommendations.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		legalIssues: legalData.issues,
		recommendations: recsData.recommendations,
		civicStandardNote: recsData.civic_standard_note,
		manifest: manifestData
	};
};
