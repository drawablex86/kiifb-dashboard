import changeLog from '../../../../../data/processed/change_log.json';
import type { RequestHandler } from './$types';

/**
 * /api/v1/change-log.json — T103 (Milestone 10)
 *
 * Read-only JSON endpoint exposing ONLY the processed public change log
 * (`data/processed/change_log.json`, produced by T082 snapshot diffing).
 * Resolved and added flags are retained here permanently — history is
 * never deleted.
 */
export const GET: RequestHandler = async () => {
	return new Response(
		JSON.stringify(
			{
				licence: {
					default: 'Processed public data (dashboard-derived change log)',
					'note': 'Reuse must cite datasource.md and preserve provenance fields.'
				},
				...changeLog
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
