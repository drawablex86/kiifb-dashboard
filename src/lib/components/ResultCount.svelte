<script lang="ts">
	/**
	 * ResultCount.svelte — live filter feedback (designsystem.md P4).
	 *
	 * "Showing N of M {noun}" with tabular numerals; announced as a polite
	 * status so filter results are perceivable without re-scanning the list.
	 * Optional `children` renders inline next to the count (e.g. clear-filters).
	 */
	import type { Snippet } from 'svelte';

	let {
		shown,
		total,
		noun = 'records',
		children
	}: {
		shown: number;
		total: number;
		noun?: string;
		children?: Snippet;
	} = $props();
</script>

<p role="status" aria-live="polite" class="flex flex-wrap items-center gap-2 text-xs text-slate-600">
	<span>
		Showing
		<span class="tabular-nums font-medium text-slate-800">{shown.toLocaleString('en-IN')}</span>
		of
		<span class="tabular-nums font-medium text-slate-800">{total.toLocaleString('en-IN')}</span>
		{noun}
	</span>
	{#if children}
		<span aria-hidden="true" class="text-slate-300">•</span>
		{@render children()}
	{/if}
</p>
