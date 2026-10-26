<script lang="ts">
	/**
	 * NudgeCallout.svelte — the "thought nudge" note (designsystem.md §6).
	 *
	 * Three kinds: situate (scale anchor), interpret (misread guard), ask
	 * (forward question). Single reserved indigo treatment — deliberately NOT
	 * badge-tinted, so a nudge can never masquerade as an evidence state.
	 * Dismissible per browser session (sessionStorage), non-data-changing note.
	 */
	import type { Snippet } from 'svelte';

	let {
		kind,
		id,
		heading = undefined,
		dismissible = true,
		children
	}: {
		kind: 'situate' | 'interpret' | 'ask';
		/** Stable per-instance id for the session-dismissal storage key. */
		id: string;
		/** Optional bolded lead-in from the author. */
		heading?: string;
		dismissible?: boolean;
		children: Snippet;
	} = $props();

	const meta: { label: string; icon: 'pin' | 'alert' | 'arrow' } = $derived(
		kind === 'situate'
			? { label: 'Situate', icon: 'pin' }
			: kind === 'interpret'
				? { label: 'Interpret carefully', icon: 'alert' }
				: { label: 'Worth asking', icon: 'arrow' }
	);

	const STORAGE_PREFIX = 'kiifb-nudge-';

	let hidden = $state(false);

	$effect(() => {
		if (dismissible && typeof window !== 'undefined') {
			try {
				hidden = window.sessionStorage.getItem(STORAGE_PREFIX + id) === '1';
			} catch {
				/* storage unavailable — always render */
			}
		}
	});

	function dismiss() {
		hidden = true;
		try {
			window.sessionStorage.setItem(STORAGE_PREFIX + id, '1');
		} catch {
			/* ignore */
		}
	}
</script>

{#if !hidden}
	<aside
		role="note"
		aria-label="{meta.label} — reading note"
		class="flex items-start gap-2.5 rounded-md border-l-4 border-indigo-300 bg-indigo-50/70 px-4 py-3"
	>
		{#if meta.icon === 'pin'}
			<svg class="w-4 h-4 mt-0.5 shrink-0 text-indigo-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
				<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" /><circle cx="12" cy="10" r="3" />
			</svg>
		{:else if meta.icon === 'alert'}
			<svg class="w-4 h-4 mt-0.5 shrink-0 text-indigo-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
				<circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
			</svg>
		{:else}
			<svg class="w-4 h-4 mt-0.5 shrink-0 text-indigo-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
				<path d="M5 12h14" /><path d="M13 6l6 6-6 6" />
			</svg>
		{/if}
		<div class="min-w-0 flex-1 text-sm text-slate-700 leading-relaxed">
			<span class="font-semibold text-indigo-900">{meta.label}</span>{heading ? ` — ${heading}` : ''} {@render children()}
		</div>
		{#if dismissible}
			<button
				type="button"
				onclick={dismiss}
				aria-label="Dismiss this note"
				title="Hide this note"
				class="shrink-0 mt-0.5 -mr-1 p-1 rounded text-slate-400 hover:text-slate-700 hover:bg-indigo-100 transition"
			>
				<svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
					<path d="M18 6L6 18M6 6l12 12" />
				</svg>
			</button>
		{/if}
	</aside>
{/if}
