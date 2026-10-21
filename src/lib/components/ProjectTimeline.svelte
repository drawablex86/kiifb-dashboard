<script lang="ts">
	/**
	 * ProjectTimeline.svelte — T100 (Milestone 10)
	 *
	 * Collapsible per-project milestone ladder (Sanction → Tender →
	 * Contract → Milestones → Handover → DLP) rendered inside the
	 * project explorer inspection drawer.
	 *
	 * Data sources:
	 *   - DS010 (KIIFB portal) — record status + provenance.
	 *   - DS030 (Kerala Kanakku, CC BY 4.0) — matched package statuses
	 *     used to place the record on the Kanakku lifecycle ladder.
	 *
	 * Honesty rule: a stage is marked "reached" only when a source
	 * explicitly discloses a status at or beyond that stage. Every other
	 * stage is rendered as an explicit GAP with the reason recorded —
	 * unrecorded milestones are never invented.
	 */
	import { LADDER, furthestLadderStage, ladderIndex, type LadderStageId } from '$lib/data/lifecycle';

	type KanakkuPackageRef = {
		code: string;
		status: string;
	};

	type TimelineRecord = {
		status?: { source_status_text?: string; normalised_status?: string; as_of_date?: string };
		source_id?: string;
		source_locator?: string;
		record_id?: string;
	};

	let {
		record,
		kanakkuPackages = []
	}: {
		record: TimelineRecord;
		kanakkuPackages?: KanakkuPackageRef[];
	} = $props();

	let expanded = $state(true);

	const asOf = $derived(record.status?.as_of_date ?? '2026-10');

	// Furthest stage disclosed by any matched Kanakku package (DS030)
	const bestKanakkuPackage = $derived.by(() => {
		let best: { pkg: KanakkuPackageRef; index: number } | null = null;
		for (const pkg of kanakkuPackages) {
			const mapped = furthestLadderStage({ status: { source_status_text: pkg.status } } as any);
			if (mapped) {
				const idx = ladderIndex(mapped);
				if (!best || idx > best.index) best = { pkg, index: idx };
			}
		}
		return best?.pkg ?? null;
	});

	// Stage furthest reached per the record's own portal status (DS010)
	const recordStage = $derived(furthestLadderStage(record as any));
	const recordIdx = $derived(ladderIndex(recordStage));
	const kanakkuIdx = $derived(
		bestKanakkuPackage
			? ladderIndex(
					furthestLadderStage({ status: { source_status_text: bestKanakkuPackage.status } } as any)
				)
			: -1
	);
	const furthestIdx = $derived(Math.max(recordIdx, kanakkuIdx));

	type Row = {
		id: LadderStageId;
		label: string;
		description: string;
		reached: boolean;
		current: boolean;
		reason: string;
		sourceId: string;
		sourceLocator: string;
		asOf: string;
	};

	const rows = $derived.by<Row[]>(() => {
		return LADDER.map((stage, idx) => {
			const reached = idx <= furthestIdx && furthestIdx >= 0;
			const current = idx === furthestIdx;
			let reason = '';
			let sourceId = record.source_id ?? '—';
			let sourceLocator = record.source_locator ?? '—';
			let rowAsOf = asOf;

			if (reached) {
				if (kanakkuIdx >= 0 && idx >= recordIdx && bestKanakkuPackage) {
					sourceId = 'DS030';
					sourceLocator = `Kanakku package ${bestKanakkuPackage.code} — status field`;
					rowAsOf = asOf;
					reason = bestKanakkuPackage.status || record.status?.source_status_text || 'Disclosed delivery stage';
				} else {
					reason = record.status?.source_status_text || record.status?.normalised_status || 'Disclosed';
				}
			} else {
				reason = 'GAP — not recorded in KIIFB portal or Kanakku disclosures as of ' + asOf;
				sourceId = '—';
				sourceLocator = 'no source discloses this stage for this record';
			}
			return {
				id: stage.id,
				label: stage.label,
				description: stage.description,
				reached,
				current,
				reason,
				sourceId,
				sourceLocator,
				asOf: rowAsOf
			};
		});
	});

	const reachedCount = $derived(rows.filter((r) => r.reached).length);
</script>

<div class="border border-slate-200 rounded overflow-hidden">
	<button
		type="button"
		onclick={() => (expanded = !expanded)}
		aria-expanded={expanded}
		class="w-full flex items-center justify-between px-3 py-2.5 bg-slate-50 border-b border-slate-200 text-left hover:bg-slate-100 transition"
	>
		<div>
			<h4 class="text-2xs font-bold uppercase text-slate-500">Delivery Milestone Ladder (T100)</h4>
			<p class="text-3xs text-slate-400 font-mono">
				{reachedCount}/6 stages disclosed
				{#if bestKanakkuPackage}&nbsp;• Kanakku package {bestKanakkuPackage.code}{/if}
			</p>
		</div>
		<span class="text-slate-400 text-xs">{expanded ? '▾' : '▸'}</span>
	</button>

	{#if expanded}
		<ol class="divide-y divide-slate-100">
			{#each rows as row}
				<li class="flex gap-3 px-3 py-2.5 text-xs">
					<!-- Step indicator -->
					<span
						class="mt-0.5 w-2 h-2 rounded-full shrink-0 {row.reached
							? (row.current ? 'bg-indigo-600 ring-2 ring-indigo-200' : 'bg-emerald-500')
							: 'bg-slate-200 ring-1 ring-slate-300'}"
						aria-hidden="true"
					></span>
					<div class="min-w-0 flex-1">
						<div class="flex items-center gap-1.5 flex-wrap">
							<span class="font-semibold {row.reached ? 'text-slate-900' : 'text-slate-400'}">
								{row.label}
							</span>
							{#if row.current}
								<span class="px-1.5 py-0.5 rounded text-3xs font-bold uppercase bg-indigo-50 text-indigo-800 border border-indigo-200">
									current stage
								</span>
							{:else if row.reached}
								<span class="px-1.5 py-0.5 rounded text-3xs font-bold uppercase bg-emerald-50 text-emerald-800 border border-emerald-200">
									reached
								</span>
							{:else}
								<span class="px-1.5 py-0.5 rounded text-3xs font-bold uppercase bg-rose-50 text-rose-700 border border-rose-200">
									gap — unrecorded
								</span>
							{/if}
						</div>
						<p class="text-3xs text-slate-500 mt-0.5">{row.reason}</p>
						<div class="font-mono text-3xs text-slate-400 mt-0.5 break-words">
							source_id: {row.sourceId} · source_locator: {row.sourceLocator} · as-of: {row.asOf}
						</div>
					</div>
				</li>
			{/each}
		</ol>
		<div class="px-3 py-2 bg-slate-50 border-t border-slate-100 text-3xs text-slate-400 font-mono leading-relaxed">
			* Ladder derived from disclosed status fields only ({'DS010'} portal status
			{#if bestKanakkuPackage}, {'DS030'} Kanakku package status{/if}). Stages the sources do not
			record remain explicit gaps (not invented). DLP stage is not individually disclosed by
			{'DS030'} — it is only inferred once the record discloses an operational status.
		</div>
	{/if}
</div>
