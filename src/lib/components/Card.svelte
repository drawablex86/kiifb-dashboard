<script lang="ts">
	/**
	 * Card.svelte — primitive surface container, shadcn-svelte-aligned
	 * (designsystem.md §13.3).
	 *
	 * Open composition via optional `header` / `footer` snippets, so callers
	 * own typography and content rather than the card prescribing it. The
	 * provenance-footer / metric-card patterns compose on top of this, not
	 * instead of it.
	 *
	 * A card that is clickable must carry an explicit "View evidence →"
	 * signifier in its content (designsystem.md §9.1) — never rely on cursor
	 * alone. For truly interactive cards, prefer explicit links/buttons in the
	 * content over making the whole card clickable.
	 */
	import type { Snippet } from 'svelte';

	let {
		header,
		footer,
		class: extra = '',
		children
	}: {
		/** Optional top slot: title + description typography owned by caller. */
		header?: Snippet;
		/** Optional bottom slot, separated by a hairline (e.g. provenance rows). */
		footer?: Snippet;
		/** Extra Tailwind classes merged last. */
		class?: string;
		children?: Snippet;
	} = $props();
</script>

<div class="rounded-lg border border-border bg-card text-card-foreground shadow-sm {extra}">
	{#if header}
		<div class="p-5 pb-2">
			{@render header()}
		</div>
	{/if}
	<div class="p-5">
		{@render children?.()}
	</div>
	{#if footer}
		<div class="px-5 pb-5">
			{@render footer()}
		</div>
	{/if}
</div>
