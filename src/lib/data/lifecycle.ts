/**
 * lifecycle.ts — T100 (Milestone 10)
 *
 * Shared Kanakku lifecycle mapping: source status fields → the
 * delivery ladder (Sanction → Tender → Contract → Milestones →
 * Handover → DLP) together with per-stage provenance labels.
 *
 * Only statuses that a source actually discloses are ever treated as
 * "reached"; everything the sources do not record stays an explicit
 * GAP — nothing is invented or interpolated.
 */

export type LadderStageId =
	| 'sanction'
	| 'tender'
	| 'contract'
	| 'milestones'
	| 'handover'
	| 'dlp';

export type LadderStage = {
	id: LadderStageId;
	label: string;
	description: string;
};

export const LADDER: LadderStage[] = [
	{
		id: 'sanction',
		label: 'Sanction',
		description: 'Project sanctioned; financial outlay approved by KIIFB.'
	},
	{
		id: 'tender',
		label: 'Tender',
		description: 'Technical sanction and tender process initiated / completed.'
	},
	{
		id: 'contract',
		label: 'Contract',
		description: 'Contract process created / completed; work agreement executed.'
	},
	{
		id: 'milestones',
		label: 'Milestones',
		description: 'Execution underway; payment milestones recorded in Kanakku WBS.'
	},
	{
		id: 'handover',
		label: 'Handover',
		description: 'Physically complete and officially handed over to the department.'
	},
	{
		id: 'dlp',
		label: 'DLP',
		description: 'Defect liability period (typically 3–5 years post-handover).'
	}
];

/** Highest ladder index reached for a Kanakku portal / package status. */
export const KANAKKU_STATUS_TO_LADDER_STAGE: Record<string, LadderStageId> = {
	// Sanction-level disclosures
	'Project Approved': 'sanction',
	'Project Under Evaluation': 'sanction',
	'Project Created': 'sanction',
	'Project Initiated': 'sanction',
	'Design Basis Report Created': 'sanction',
	'Design Basis Report Approved': 'sanction',
	'WBS Approval Created': 'sanction',
	'WBS Base Zero Approved': 'sanction',
	'WBS Base One Approved': 'sanction',
	// Tender-level disclosures
	'Technical Sanction Created': 'tender',
	'Technical Sanction Completed': 'tender',
	'Tender Created': 'tender',
	'Tender Completed': 'tender',
	// Contract-level disclosures
	'Contract Process Created': 'contract',
	'Contract Process Completed': 'contract',
	'Project Execution Document Stage 1 Created': 'contract',
	'Project Execution Document Stage 1 Approved': 'contract',
	// Executing / milestone-level disclosures
	'Project Execution Document Stage 2 Initiated': 'milestones',
	'Project Execution Document Stage 2 Approved': 'milestones',
	'Submitted for Confirmation by KIIFB': 'milestones',
	'Return to SPV': 'milestones',
	'Payment milestone finalization pending base 0': 'milestones',
	'Payment milestone finalization pending base 1': 'milestones'
};

/** Highest ladder index reached for a normalised KIIFB-portal status. */
export const NORMALISED_STATUS_TO_LADDER_STAGE: Record<string, LadderStageId> = {
	approved: 'sanction',
	tendered: 'tender',
	in_progress: 'milestones',
	delayed: 'milestones',
	physically_complete: 'handover',
	handed_over: 'handover',
	operational: 'dlp',
	cancelled: 'sanction'
};

/** Resolve the furthest ladder stage a record discloses (null = none). */
export function furthestLadderStage(record: {
	status?: { normalised_status?: string; source_status_text?: string };
	kanakku_status?: string;
	kanakku_statuses?: string[];
}): LadderStageId | null {
	const candidates: LadderStageId[] = [];
	for (const stage of record.kanakku_statuses ?? []) {
		const mapped = KANAKKU_STATUS_TO_LADDER_STAGE[stage];
		if (mapped) candidates.push(mapped);
	}
	if (record.kanakku_status) {
		const mapped = KANAKKU_STATUS_TO_LADDER_STAGE[record.kanakku_status];
		if (mapped) candidates.push(mapped);
	}
	if (record.status?.normalised_status) {
		const mapped = NORMALISED_STATUS_TO_LADDER_STAGE[record.status.normalised_status];
		if (mapped) candidates.push(mapped);
	}
	if (record.status?.source_status_text) {
		const mapped = KANAKKU_STATUS_TO_LADDER_STAGE[record.status.source_status_text];
		if (mapped) candidates.push(mapped);
	}
	if (candidates.length === 0) return null;
	return LADDER.find((s) => candidates.includes(s.id))!.id;
}

/** Index of a stage within the ladder (or -1). */
export function ladderIndex(stageId: LadderStageId | null): number {
	if (!stageId) return -1;
	return LADDER.findIndex((s) => s.id === stageId);
}
