<script lang="ts">
	/**
	 * FreshnessBadge.svelte — T095 (Milestone 9).
	 *
	 * "Data as of <date> • archived / live-verified" pill derived from
	 * data/manifest.json retrieval records via $lib/data/freshness.ts.
	 * Nothing is hardcoded: dates come from `sources[].retrieved_at` and the
	 * T080 live-crawl history in `manifest.live_crawls`.
	 */

	import { freshnessFor, type Freshness } from '$lib/data/freshness';

	type Props = {
		/** Manifest source ids whose retrieval records to disclose (first is most prominent). */
		sources: string[];
		/** Optional trailing note, e.g. "snapshot runs denoted below". */
		note?: string;
		/** Compact variant for tight surfaces (sticky header). */
		compact?: boolean;
	};

	let { sources, note = undefined, compact = false }: Props = $props();

	const badges: Freshness[] = $derived(sources.map(freshnessFor));

	function dateOnly(f: Freshness): string {
		return f.asOfDate;
	}
</script>

<span
	class="{compact
		? 'text-[10px] px-1.5 py-0.5 gap-1'
		: 'text-[11px] px-2 py-1 gap-1.5'} inline-flex flex-wrap items-center rounded-full border font-medium traceability-pill"
	role="status"
	aria-label="Data freshness disclosure"
>
	<span class="text-slate-500">Data as of</span>
	{#each badges as f, i (f.sourceId)}
		{#if i > 0}
			<span class="text-slate-300">|</span>
		{/if}
		<span
			class="inline-flex items-center gap-1 {f.mode === 'live-verified'
				? 'text-emerald-800 bg-emerald-50 border-emerald-200'
				: 'text-slate-600 bg-slate-100 border-slate-200'} px-1.5 py-0.5 rounded border {compact
				? 'text-[10px]'
				: 'text-[11px]'}"
		>
			<span class="tabular-nums">{dateOnly(f)}</span>
			<span class="font-semibold">{f.sourceId}</span>
			<span class="normal-case">{f.mode === 'live-verified' ? 'live-verified' : 'archived'}</span>
		</span>
	{/each}
	{#if note}
		<span class="text-slate-400">• {note}</span>
	{/if}
</span>

<style>
	.traceability-pill {
		background-color: #fff;
	}
</style>
