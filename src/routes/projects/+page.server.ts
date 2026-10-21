import explorerData from '../../../data/processed/unified_project_explorer.json';
import matchLog from '../../../data/processed/kanakku_match_log.json';
import kanakkuPackages from '../../../data/processed/kanakku_packages.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

/**
 * T100 (Milestone 10): resolve matched Kanakku package codes per explorer
 * record so the inspection drawer can render the Kanakku lifecycle ladder
 * (Sanction → Tender → Contract → Milestones → Handover → DLP) with
 * per-milestone provenance.
 */
function buildMatchesByRecord(): Record<string, { code: string; status: string }[]> {
	const byCode = new Map(kanakkuPackages.packages.map((p: any) => [p.code, p]));
	const matches: Record<string, { code: string; status: string }[]> = {};
	for (const entry of matchLog.entries as any[]) {
		if (!entry.pkg_codes || entry.pkg_codes.length === 0) continue;
		matches[entry.project_id] = entry.pkg_codes
			.map((code: string) => byCode.get(code))
			.filter(Boolean)
			.map((p: any) => ({ code: p.code, status: p.status }));
	}
	return matches;
}

export const load: PageServerLoad = async () => {
	return {
		summary: explorerData.summary,
		records: explorerData.records,
		matchesByRecord: buildMatchesByRecord() as Record<string, { code: string; status: string }[]>,
		manifest: manifestData
	};
};
