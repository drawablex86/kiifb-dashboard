<script lang="ts">
	/**
	 * NavGroup.svelte — disclosure-style dropdown for one nav group
	 * (WAI-ARIA disclosure navigation pattern: button + aria-expanded +
	 * aria-controls; panel holds plain links — no menu-role machinery).
	 *
	 * Signifiers (designsystem.md §9.1): active group shows a filled dot +
	 * tinted pill; chevron rotates when open; each item carries its one-line
	 * scent description (P11 information scent). Esc closes and returns focus
	 * to the trigger; outside click closes; route change closes.
	 */
	import { page } from '$app/state';
	import type { NavGroupData } from '$lib/nav';

	let { group }: { group: NavGroupData } = $props();

	let open = $state(false);
	let root: HTMLDivElement | null = $state(null);
	let trigger: HTMLButtonElement | null = $state(null);
	const panelId = `nav-panel-${group.id}`;
	const currentPath = $derived(page.url.pathname);
	const active = $derived(group.items.some((i) => i.href === currentPath));

	// Route change = deliberate navigation: always collapse (P4 feedback).
	$effect(() => {
		void currentPath;
		open = false;
	});

	function onDocumentClick(e: MouseEvent) {
		if (open && root && !root.contains(e.target as Node)) open = false;
	}

	function onRootKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape' && open) {
			open = false;
			trigger?.focus();
		}
	}
</script>

<svelte:document onclick={onDocumentClick} />

<div class="relative" bind:this={root} onkeydown={onRootKeydown}>
	<button
		bind:this={trigger}
		type="button"
		aria-expanded={open}
		aria-controls={panelId}
		onclick={() => (open = !open)}
		class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-md text-sm font-medium transition-all outline-2 outline-offset-2 outline-transparent hover:outline-slate-300 {active
			? 'bg-slate-100 text-slate-900'
			: 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'}"
	>
		{#if active}
			<span aria-hidden="true" class="w-1.5 h-1.5 rounded-full bg-slate-900"></span>
		{/if}
		{group.label}
		<svg
			class="w-3.5 h-3.5 transition-transform {open ? 'rotate-180' : ''}"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
			aria-hidden="true"
		>
			<path d="M6 9l6 6 6-6" />
		</svg>
	</button>

	{#if open}
		<div id={panelId} class="absolute left-0 top-full mt-2 w-72 max-w-[85vw] rounded-md border border-border bg-popover shadow-md p-1.5 z-40">
			{#each group.items as item (item.href)}
				<a
					href={item.href}
					aria-current={item.href === currentPath ? 'page' : undefined}
					class="block rounded-md px-3 py-2 transition-colors hover:bg-slate-100 {item.href === currentPath
						? 'bg-slate-50'
						: ''}"
				>
					<span class="block text-sm font-medium text-slate-900 {item.href === currentPath ? 'underline decoration-slate-300 underline-offset-2' : ''}">
						{item.label}
					</span>
					<span class="block text-xs text-muted-foreground mt-0.5">{item.description}</span>
				</a>
			{/each}
		</div>
	{/if}
</div>
