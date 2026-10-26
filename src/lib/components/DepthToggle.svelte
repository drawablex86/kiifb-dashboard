<script lang="ts">
	/**
	 * DepthToggle.svelte — the two-gear persona switch (designsystem.md §3.3).
	 *
	 * Segmented `Plain English ⇄ Evidence` control. Persists via depth store
	 * (localStorage + ?depth= URL param). Hydrates the store on mount; SSR
	 * prerenders assume `plain`.
	 */
	import { depth, setDepth, initDepth, type DepthMode } from '$lib/stores/depth.svelte';

	let { compact = false }: { compact?: boolean } = $props();

	$effect(() => {
		initDepth();
	});

	const options: { value: DepthMode; label: string; description: string }[] = [
		{
			value: 'plain',
			label: 'Plain English',
			description: 'Everyday wording, definitions on demand, simplified charts'
		},
		{
			value: 'evidence',
			label: 'Evidence',
			description: 'Source ids, locators, formulas and full technical detail'
		}
	];
</script>

<div
	class="inline-flex items-center rounded-md border border-slate-200 bg-slate-100 p-0.5 {compact
		? 'text-[11px]'
		: 'text-xs'}"
	role="group"
	aria-label="Information depth"
>
	{#each options as option (option.value)}
		<button
			type="button"
			onclick={() => setDepth(option.value)}
			aria-pressed={depth.mode === option.value}
			title={option.description}
			class="rounded px-2.5 py-1 font-medium transition-all outline-2 outline-offset-2 outline-transparent hover:outline-slate-300 {depth.mode === option.value
				? 'bg-white text-slate-900 shadow-sm'
				: 'text-slate-500 hover:text-slate-800 hover:bg-slate-200/60'}"
		>
			{option.label}
		</button>
	{/each}
</div>
