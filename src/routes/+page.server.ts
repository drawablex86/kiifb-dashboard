import assertionsData from '../../data/processed/committee_assertions.json';
import evidenceLinksData from '../../data/processed/evidence_links.json';
import manifestData from '../../data/manifest.json';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		assertions: assertionsData.assertions,
		evidenceLinks: evidenceLinksData.evidence_links,
		manifest: manifestData
	};
};
