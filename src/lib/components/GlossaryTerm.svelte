<script lang="ts">
	/**
	 * GlossaryTerm.svelte — inline definitional popover (designsystem.md §8).
	 *
	 * Renders a dotted-underlined term (the site's sanctioned glossary signifier)
	 * that expands via native <details>: zero-JS disclosure, Esc-aware, 
	 * depth-aware (Plain shows `plain` first; Evidence prepends `expert`).
	 * Unknown ids throw via getEntry — fail loud at build time, not silently.
	 */
	import { getEntry } from '$lib/data/glossary';
	import { depth } from '$lib/stores/depth.svelte';

	let { id, display = undefined }: { id: string; display?: string } = $props();

	let open = $state(false);
	const entry = $derived(getEntry(id));

	function onkeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') open = false;
	}
</script>

<details bind:open class="glossary-term">
	<summary {onkeydown}>
		<span class="term-label">{display ?? entry.term}</span>
		<span class="term-marker" aria-hidden="true">ⓘ</span>
		<span class="sr-only">— open glossary definition</span>
	</summary>
	<div class="glossary-popover" role="region" aria-label="{entry.term} — glossary definition">
		{#if depth.mode === 'evidence'}
			<p class="text-sm text-slate-700 leading-relaxed attach-tight">{entry.expert}</p>
		{/if}
		<p class="text-sm text-slate-700 leading-relaxed">
			{#if depth.mode === 'evidence'}
				<span class="text-xs font-semibold uppercase tracking-wide text-slate-400 block mb-0.5">In plain words</span>
				{entry.plain}
			{:else}
				{entry.plain}
			{/if}
		</p>
		<p class="mt-2 text-xs text-slate-600 leading-relaxed">
			<span class="font-semibold text-slate-700">Why it matters here: </span>{entry.why}
		</p>
		<div class="mt-2 pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
			<a href="/glossary#{id}" class="font-medium text-blue-700 hover:text-blue-900 hover:underline underline-offset-2">
				All terms →
			</a>
			{#if depth.mode === 'evidence'}
				<span class="font-mono text-[10px] text-slate-400" title="glossary id">{id}</span>
			{/if}
		</div>
	</div>
</details>

<style>
	.glossary-term {
		position: relative;
		display: inline-block;
		z-index: 10;
	}
	.glossary-term summary {
		list-style: none;
		cursor: help;
		display: inline-flex;
		align-items: baseline;
		gap: 2px;
	}
	.glossary-term summary::-webkit-details-marker {
		display: none;
	}
	.term-label {
		color: #334155;
		text-decoration: underline dotted;
		text-decoration-color: #94a3b8;
		text-decoration-thickness: 1px;
		text-underline-offset: 3px;
	}
	.term-label:hover,
	.term-label:focus-visible {
		color: #0f172a;
		text-decoration-color: #334155;
	}
	.term-marker {
		font-size: 9px;
		color: #94a3b8;
		transform: translateY(-2px);
	}
	.glossary-popover {
		position: absolute;
		top: calc(100% + 6px);
		left: 50%;
		transform: translateX(-50%);
		width: 19rem;
		max-width: 85vw;
		background: #ffffff;
		border: 1px solid #e2e8f0;
		border-radius: 6px;
		box-shadow:
			0 4px 6px -1px rgb(0 0 0 / 0.08),
			0 10px 15px -3px rgb(0 0 0 / 0.1);
		padding: 0.75rem;
		text-align: left;
		z-index: 30;
	}
	.attach-tight {
		margin-top: 0;
	}
</style>
