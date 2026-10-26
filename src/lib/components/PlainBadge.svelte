<script lang="ts">
	/**
	 * PlainBadge.svelte — centralized humanized label badge (designsystem.md §8).
	 *
	 * Plain gear: humanized label only ("Committee finding"). Evidence gear:
	 * humanized + raw id in mono so experts keep their cross-reference shortcut.
	 * The parent may pass `showId` to force the id visible. Tooltip carries the
	 * authoritative description; the description is also exposed to screen
	 * readers via sr-only text.
	 */
	import { humanizeLabel, type LabelKind } from '$lib/data/vocabulary';
	import { depth } from '$lib/stores/depth.svelte';

	let {
		label,
		kind = 'evidence',
		showId = false,
		class: extraClass = ''
	}: {
		label: string;
		kind?: LabelKind;
		showId?: boolean;
		/** Additional Tailwind classes for the badge surface. */
		class?: string;
	} = $props();

	const meta = $derived(humanizeLabel(kind, label));
	const showRaw = $derived(depth.mode === 'evidence' || showId);
</script>

<span
	class="inline-flex items-baseline gap-1.5 text-xs font-medium px-2.5 py-0.5 rounded border {meta.tint} {extraClass}"
>
	<span>{meta.humanized}</span>
	{#if showRaw}
		<span class="font-mono text-[10px] opacity-70">{label}</span>
	{/if}
</span>
<span class="sr-only"> — {meta.description}</span>
