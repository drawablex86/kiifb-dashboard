import explorerData from '../../../../../data/processed/unified_project_explorer.json';
import type { RequestHandler } from './$types';

/**
 * /api/v1/projects.json — T103 (Milestone 10)
 *
 * Read-only JSON endpoint exposing ONLY the processed public dataset
 * (`data/processed/unified_project_explorer.json`). No raw, private or
 * unprocessed data is served.
 *
 * Licence inheritance: records derived from Kerala Kanakku (DS030) inherit
 * CC BY 4.0; KIIFB-portal records (DS010) follow the official portal's
 * disclosed terms; KITE data (DS021) follows Sametham's disclosed terms.
 */
export const GET: RequestHandler = async () => {
	return new Response(
		JSON.stringify(
			{
				licence: {
					default: 'Processed public data',
					'DS030': 'CC BY 4.0 (Kerala Kanakku derivative — inherited)',
					'DS010': 'KIIFB official portal disclosure terms',
					'DS021': 'KITE Sametham disclosure terms',
					'note': 'Reuse must preserve source_id and source_locator attribution.'
				},
				generated_at: explorerData.generated_at,
				summary: explorerData.summary,
				records: explorerData.records
			},
			null,
			1
		),
		{
			headers: {
				'Content-Type': 'application/json; charset=utf-8',
				'Cache-Control': 'public, max-age=3600'
			}
		}
	);
};
