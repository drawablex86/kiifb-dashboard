/**
 * flags.ts — T102 (Milestone 10)
 *
 * Flag metadata registry for the delay & anomaly register (/flags).
 * Criteria text is objective: each entry states the exact measured
 * condition of Kanakku Rule Engine v2 (DS030) / T092 divergence logic
 * that must be true for the flag to be raised. Nothing is invented —
 * unrecorded fields are disclosed as data gaps, not flags.
 */

export type FlagMeta = {
	id: string;
	label: string;
	/** Objective criterion that triggers the flag. */
	criterion: string;
	severity: 'high' | 'medium' | 'info';
	primarySource: string;
};

export const FLAG_REGISTRY: FlagMeta[] = [
	{
		id: 'overdue',
		label: 'Overdue',
		criterion:
			'Kanakku package status remains below execution/contract-completion stages while the disclosed disbursement window reported by DS010/DS030 has elapsed without a recorded advancement (status trail shows no forward migration in change_log.json).',
		severity: 'high',
		primarySource: 'DS030 (Kanakku Rule Engine v2 status trail; change_log.json status_migrations)'
	},
	{
		id: 'payment_vs_progress',
		label: 'Payment vs Progress divergence',
		criterion:
			'Funds released (DS010 released_crore) exceed the physical progress disclosed at the corresponding lifecycle stage — measured as release advance beyond the stage midpoint of the Kanakku ladder with no completion status disclosed (physical progress % itself is a disclosed data gap).',
		severity: 'high',
		primarySource: 'DS030 + DS010 (Rule Engine v2 divergence rule; T092 scatter divergence zone)'
	},
	{
		id: 'cost_escalation',
		label: 'Cost escalation',
		criterion:
			'Disclosed expenditure (Kanakku expenditure_inr) exceeds the approved outlay carried for the record in DS010, i.e. spending crosses the sanctioned ceiling without a corresponding approval revision being recorded.',
		severity: 'medium',
		primarySource: 'DS030 expenditure field vs DS010 approved outlay (Rule Engine v2)'
	},
	{
		id: 'stale',
		label: 'Stale update',
		criterion:
			'No status or financial field for the record has changed between the last two processed snapshots according to change_log.json (no status_migrations, no financial_deltas, no added flags) — the record’s as-of disclosure is aged.',
		severity: 'medium',
		primarySource: 'change_log.json (T082 snapshot diff engine)'
	},
	{
		id: 'above_approved',
		label: 'Released above approved',
		criterion:
			'Released or recorded expenditure for the record exceeds its sanctioned approved outlay (released_inr > approved_inr in DS010 / expenditure > approved in DS030), indicating draw beyond sanction.',
		severity: 'high',
		primarySource: 'DS010 financials + DS030 expenditure (Rule Engine v2)'
	}
];

export function getFlagMeta(id: string): FlagMeta | undefined {
	return FLAG_REGISTRY.find((f) => f.id === id);
}
