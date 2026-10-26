/**
 * vocabulary.ts — single source of truth for humanized labels (UX rework v2).
 *
 * Raw snake_case ids live in the data JSONs; the UI never renders them bare in
 * Plain mode. PlainBadge.svelte consumes `humanizeLabel`. Wording here is
 * authoritative: designsystem.md §5 is the written spec, this file is the code.
 */

export type LabelKind = 'evidence' | 'lifecycle' | 'flag';

export type LabelMeta = {
	/** Sentence-case humanized label shown in Plain mode. */
	humanized: string;
	/** Authoritative one-line description (tooltip / sr-only text). */
	description: string;
	/** Tailwind classes: bg / border / text (design-system.md §2.2–2.3 semantics). */
	tint: string;
};

export const EVIDENCE_LABELS: Record<string, LabelMeta> = {
	official_record: {
		humanized: 'Official record',
		description:
			'Published in an official or statutory document held by this site (gazette, budget, audited report).',
		tint: 'bg-emerald-50 text-emerald-800 border-emerald-200'
	},
	verified_outcome: {
		humanized: 'Independently verified',
		description: 'Checked against more than one independent record — the strongest evidence state.',
		tint: 'bg-blue-50 text-blue-800 border-blue-200'
	},
	committee_finding: {
		humanized: 'Committee finding',
		description:
			'A claim made in the October 2026 Expert Committee Report. Treated as a claim, not as fact.',
		tint: 'bg-purple-50 text-purple-800 border-purple-200'
	},
	analytical_inference: {
		humanized: 'Calculated estimate',
		description:
			'Not published anywhere — derived by this dashboard from published numbers, with the formula disclosed.',
		tint: 'bg-green-50 text-green-800 border-green-200'
	},
	contested_interpretation: {
		humanized: 'Disputed interpretation',
		description:
			'More than one reasonable reading exists — records or law are construed differently by competent parties.',
		tint: 'bg-amber-50 text-amber-800 border-amber-200'
	},
	unverified_claim: {
		humanized: 'Unverified claim',
		description:
			'Reported in media or by officials, but not corroborated by an official document held here.',
		tint: 'bg-orange-50 text-orange-800 border-orange-200'
	},
	data_gap: {
		humanized: 'Data gap',
		description: 'Nobody publishes this number. It is shown as a gap, never as zero.',
		tint: 'bg-slate-100 text-slate-700 border-slate-200'
	},
	unknown: {
		humanized: 'Not documented',
		description: 'No record of this value is available. Absence of evidence is not evidence of absence.',
		tint: 'bg-slate-100 text-slate-700 border-slate-200'
	}
};

export const LIFECYCLE_LABELS: Record<string, LabelMeta> = {
	approved: {
		humanized: 'Approved',
		description: 'Permission granted on paper. No ground work is implied yet.',
		tint: 'bg-slate-100 text-slate-700 border-slate-200'
	},
	tendered: {
		humanized: 'Tendered',
		description: 'Work has been put out to tender — contractors are invited to bid.',
		tint: 'bg-sky-50 text-sky-800 border-sky-200'
	},
	in_progress: {
		humanized: 'In progress',
		description: 'Construction or execution is under way.',
		tint: 'bg-indigo-50 text-indigo-800 border-indigo-200'
	},
	physically_complete: {
		humanized: 'Physically complete',
		description: 'Built, but not yet inspected, tested, or handed over.',
		tint: 'bg-cyan-50 text-cyan-800 border-cyan-200'
	},
	handed_over: {
		humanized: 'Handed over',
		description: 'Officially transferred to the department that will use it.',
		tint: 'bg-teal-50 text-teal-800 border-teal-200'
	},
	operational: {
		humanized: 'Operational',
		description: 'Open and serving the public.',
		tint: 'bg-emerald-50 text-emerald-800 border-emerald-200'
	},
	delayed: {
		humanized: 'Delayed',
		description: 'Running behind an agreed schedule, or stalled.',
		tint: 'bg-amber-50 text-amber-800 border-amber-200'
	},
	cancelled: {
		humanized: 'Cancelled',
		description: 'Dropped or revoked.',
		tint: 'bg-red-50 text-red-800 border-red-200'
	},
	conflicting_evidence: {
		humanized: 'Sources disagree',
		description: 'Different records disagree about this status. All versions are shown when you verify.',
		tint: 'bg-rose-50 text-rose-800 border-rose-200'
	}
};

export const FLAG_LABELS: Record<string, LabelMeta> = {
	overdue: {
		humanized: 'Overdue',
		description: 'Past an expected completion deadline with no recorded completion.',
		tint: 'bg-amber-50 text-amber-800 border-amber-200'
	},
	payment_vs_progress: {
		humanized: 'Money paid, work not done',
		description:
			'Share of money paid maps poorly onto share of physical work done. This is an indicator, not a proven finding.',
		tint: 'bg-amber-50 text-amber-800 border-amber-200'
	},
	cost_escalation: {
		humanized: 'Cost rose above approval',
		description: 'Current sanctioned cost has risen above the original approved cost.',
		tint: 'bg-amber-50 text-amber-800 border-amber-200'
	},
	stale: {
		humanized: 'Record not refreshed recently',
		description: "This record hasn't been updated in a long time — treat it with extra care.",
		tint: 'bg-slate-100 text-slate-700 border-slate-200'
	},
	above_approved: {
		humanized: 'Spending above approved cost',
		description: 'Observed spending or sanctioned amount now exceeds the approved outlay.',
		tint: 'bg-amber-50 text-amber-800 border-amber-200'
	}
};

const FALLOUT: LabelMeta = {
	humanized: '',
	description: '',
	tint: 'bg-slate-100 text-slate-700 border-slate-200'
};

/** Humanize a raw label with tooltip description. Falls back to the raw label (never blank). */
export function humanizeLabel(kind: LabelKind, label: string): LabelMeta {
	const map = kind === 'evidence' ? EVIDENCE_LABELS : kind === 'lifecycle' ? LIFECYCLE_LABELS : FLAG_LABELS;
	const meta = map[label];
	if (!meta) {
		return { ...FALLOUT, humanized: label, description: label };
	}
	return meta;
}
