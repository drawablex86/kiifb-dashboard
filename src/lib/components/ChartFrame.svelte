<script lang="ts">
	/**
	 * ChartFrame.svelte — standard narrative wrapper for every visualization
	 * (designsystem.md §7): Question → Key takeaway → How to read → Chart →
	 * View as data table → Provenance (depth-aware).
	 *
	 * The chart itself is the `children` snippet and keeps its own aria;
	 * `ariaNote` adds a long text alternative. `table` slot powers the data
	 * table disclosure (the a11y alternative and the expert extraction path).
	 * `controls` slot sits between the header and the chart (scale toggles,
	 * view switches) so every chart-level action is labelled, not icon-only.
	 */
	import type { Snippet } from 'svelte';
	import { depth } from '$lib/stores/depth.svelte';

	let {
		question,
		takeaway = undefined,
		howToRead = undefined,
		provenance = undefined,
		ariaNote = undefined,
		controls,
		table,
		children
	}: {
		/** The plain-language question this chart answers (also the section's aria-label). */
		question: string;
		/** One sentence carrying the number: the "so what". */
		takeaway?: string;
		/** One-liner explaining the visual encoding for the lay reader. */
		howToRead?: string;
		/** Provenance string, e.g. "Source: DS001, Table 3.3, as of 30 Jun 2026". */
		provenance?: string;
		/** Optional visible-beyond-the-canvas text for assistive tech. */
		ariaNote?: string;
		controls?: Snippet;
		table?: Snippet;
		children: Snippet;
	} = $props();
</script>

<section class="bg-white rounded-lg border border-slate-200 shadow-sm" aria-label={question}>
	<header class="px-4 sm:px-5 pt-4 sm:pt-5">
		<h3 class="text-base sm:text-lg font-semibold text-slate-900 leading-snug">{question}</h3>
		{#if takeaway}
			<p class="mt-1.5 text-sm text-slate-700 leading-relaxed">
				<span class="font-bold text-slate-900">Key takeaway: </span>{takeaway}
			</p>
		{/if}
		{#if howToRead}
			<details class="chevron mt-2">
				<summary class="cursor-pointer inline-flex items-center gap-1 text-xs font-medium text-slate-500 hover:text-slate-900 select-none">
					<span class="marker-chevron" aria-hidden="true">▸</span> How to read this
				</summary>
				<p class="mt-1 text-xs text-slate-600 leading-relaxed max-w-prose">{howToRead}</p>
			</details>
		{/if}
	</header>

	{#if controls}
		<div class="px-4 sm:px-5 pt-3 flex flex-wrap items-center gap-2">
			{@render controls()}
		</div>
	{/if}

	<div class="px-4 sm:px-5 py-4 sm:py-5">
		{#if ariaNote}<p class="sr-only">{ariaNote}</p>{/if}
		{@render children()}
	</div>

	{#if table}
		<div class="border-t border-slate-100 px-4 sm:px-5 py-3">
			<details>
				<summary class="cursor-pointer text-xs font-medium text-slate-600 hover:text-slate-900 select-none">
					View as data table
				</summary>
				<div class="mt-3 overflow-x-auto">
					{@render table()}
				</div>
			</details>
		</div>
	{/if}

	{#if provenance}
		<footer class="border-t border-slate-100 bg-slate-50/60 px-4 sm:px-5 py-2.5 text-[11px]">
			{#if depth.mode === 'evidence'}
				<span class="sr-only">Data provenance: </span>
				<span class="font-mono text-slate-500">{provenance}</span>
			{:else}
				<details>
					<summary class="cursor-pointer inline-flex items-center gap-1 font-medium text-slate-600 hover:text-slate-900 select-none">
						Where's this from?
					</summary>
					<span class="font-mono text-slate-500 mt-1 block">{provenance}</span>
				</details>
			{/if}
		</footer>
	{/if}
</section>

<style>
	/* Custom chevron summary: standard marker hidden, rotation gives open state feedback. */
	.chevron > summary::-webkit-details-marker,
	.chevron summary::marker {
		display: none;
	}
	.chevron summary .marker-chevron {
		display: inline-block;
		transition: transform 120ms ease-out;
	}
	.chevron[open] > summary .marker-chevron {
		transform: rotate(90deg);
	}
</style>
