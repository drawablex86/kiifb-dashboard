import explorerData from '../../../../../data/processed/unified_project_explorer.json';
import type { RequestHandler } from './$types';

/**
 * /api/v1/projects.csv — T103 (Milestone 10)
 *
 * CSV export of the processed public dataset with provenance preserved:
 * every row carries `source_id` and `source_locator`. Derived from
 * Kerala Kanakku (DS030) — CC BY 4.0 inheritance applies.
 */
function csvEscape(value: unknown): string {
	const s =
		value === null || value === undefined
			? ''
			: typeof value === 'object'
				? JSON.stringify(value)
				: String(value);
	return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

export const GET: RequestHandler = async () => {
	const header = [
		'record_id',
		'name',
		'entity_type',
		'sector',
		'department',
		'spv',
		'district',
		'constituency',
		'counting_unit',
		'approved_inr',
		'approved_crore',
		'released_inr',
		'released_crore',
		'release_ratio_pct',
		'source_status_text',
		'normalised_status',
		'status_as_of',
		'open_flags',
		'source_id',
		'source_locator',
		'evidence_label'
	];
	const lines = [header.join(',')];
	for (const r of explorerData.records as any[]) {
		const f = r.financials ?? {};
		const s = r.status ?? {};
		lines.push(
			[
				r.record_id,
				r.name,
				r.entity_type,
				r.sector,
				r.department,
				r.spv,
				r.district,
				r.constituency,
				r.counting_unit,
				f.approved_inr,
				f.approved_crore,
				f.released_inr,
				f.released_crore,
				f.release_ratio_pct,
				s.source_status_text,
				s.normalised_status,
				s.as_of_date,
				(r.open_flags ?? []).join(';'),
				r.source_id,
				r.source_locator,
				r.evidence_label
			]
				.map(csvEscape)
				.join(',')
		);
	}
	return new Response(lines.join('\n'), {
		headers: {
			'Content-Type': 'text/csv; charset=utf-8',
			'Content-Disposition': 'attachment; filename="kiifb_unified_project_explorer.csv"',
			'Cache-Control': 'public, max-age=3600',
			'X-Data-Licence': 'CC BY 4.0 for Kanakku (DS030) derivatives — preserve source_id/source_locator'
		}
	});
};
