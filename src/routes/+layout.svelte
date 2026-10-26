<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';
	import FreshnessBadge from '$lib/components/FreshnessBadge.svelte';
	import DepthToggle from '$lib/components/DepthToggle.svelte';
	import NavGroup from '$lib/components/NavGroup.svelte';
	import { NAV_GROUPS } from '$lib/nav';
	import { routeFreshness } from '$lib/data/freshness';

	let { children } = $props();

	// T095: persistent route-aware freshness badge — dates derive from
	// data/manifest.json retrieval records (never hardcoded per route).
	const freshness = $derived(routeFreshness(page.url.pathname));

	// Mobile disclosure menu; closes on navigation (route-change effect below).
	let mobileOpen = $state(false);
	const currentPath = $derived(page.url.pathname);
	$effect(() => {
		void currentPath;
		mobileOpen = false;
	});
	function onMobileKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') mobileOpen = false;
	}
</script>

<div class="min-h-screen flex flex-col bg-background text-foreground">
	<a
		href="#main-content"
		class="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:top-2 focus:left-2 focus:bg-white focus:text-slate-900 focus:border focus:border-slate-300 focus:rounded-md focus:px-3 focus:py-2 focus:shadow-md focus:text-sm focus:font-medium"
	>
		Skip to main content
	</a>

	<!-- Civic Tech Header — grouped navigation (UX v2, designsystem.md §4.1) -->
	<header class="border-b border-border bg-card sticky top-0 z-30">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5 flex items-center justify-between gap-3">
			<a href="/" class="flex items-center space-x-3 min-w-0 group">
				<div class="w-8 h-8 shrink-0 rounded-md bg-primary text-primary-foreground flex items-center justify-center font-bold text-sm tracking-wider">
					KL
				</div>
				<div class="min-w-0">
					<h1 class="text-sm sm:text-base font-semibold leading-tight text-foreground truncate">
						KIIFB Accountability & Public Value Dashboard
					</h1>
					<p class="hidden sm:block text-xs text-muted-foreground truncate">
						Source-linked investigation of the 2026 Expert Committee Report vs. documented delivery
					</p>
				</div>
			</a>

			<!-- Desktop: grouped disclosure nav + depth toggle -->
			<nav class="hidden md:flex flex-wrap items-center justify-end gap-1" aria-label="Main">
				{#each NAV_GROUPS as navGroup (navGroup.id)}
					<NavGroup group={navGroup} />
				{/each}
				<div class="ml-1.5">
					<DepthToggle compact />
				</div>
			</nav>

			<!-- Mobile: single disclosure button -->
			<button
				type="button"
				class="md:hidden inline-flex items-center gap-1.5 px-3 py-2 rounded-md border border-border bg-card text-sm font-medium text-slate-700 hover:bg-slate-50 transition-all outline-2 outline-offset-2 outline-transparent hover:outline-slate-300"
				aria-expanded={mobileOpen}
				aria-controls="mobile-menu"
				onclick={() => (mobileOpen = !mobileOpen)}
			>
				Menu
				<svg
					class="w-3.5 h-3.5 transition-transform {mobileOpen ? 'rotate-180' : ''}"
					viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"
				>
					<path d="M6 9l6 6 6-6" />
				</svg>
			</button>
		</div>

		<!-- Mobile menu panel: full inventory with scent descriptions -->
		{#if mobileOpen}
			<div
				id="mobile-menu"
				role="dialog"
				aria-modal="true"
				aria-label="Main navigation"
				tabindex="-1"
				class="md:hidden border-t border-border bg-popover px-4 py-3 space-y-4 max-h-[70vh] overflow-y-auto"
				onkeydown={onMobileKeydown}
			>
				<nav aria-label="Mobile main">
				{#each NAV_GROUPS as navGroup (navGroup.id)}
					<div>
						<p class="text-[11px] font-semibold uppercase tracking-wide text-slate-400 px-2 mb-1">{navGroup.label}</p>
						{#each navGroup.items as item (item.href)}
							<a
								href={item.href}
								aria-current={item.href === currentPath ? 'page' : undefined}
								class="block rounded-md px-2.5 py-2 hover:bg-slate-100 {item.href === currentPath ? 'bg-slate-50' : ''}"
							>
								<div class="flex items-center justify-between">
									<span class="block text-sm font-medium text-slate-900">{item.label}</span>
									{#if item.badge}
										<span class="text-[10px] font-semibold px-1.5 py-0.5 rounded border bg-slate-100 text-slate-600 border-slate-200 whitespace-nowrap flex-shrink-0">
											{item.badge}
										</span>
									{/if}
								</div>
								<span class="block text-xs text-muted-foreground mt-0.5">{item.description}</span>
							</a>
						{/each}
					</div>
				{/each}
				<div class="flex items-center justify-between gap-3 border-t border-border pt-3 px-2">
					<span class="text-xs font-medium text-slate-500">Information depth</span>
					<DepthToggle compact />
				</div>
			</nav>
			</div>
		{/if}

		<!-- T095: data-freshness strip — always visible in the sticky header -->
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-2 flex flex-wrap items-center">
			<FreshnessBadge sources={freshness.map((f) => f.sourceId)} compact note="route-scoped evidence" />
		</div>
	</header>

	<!-- Main Content Area -->
	<main id="main-content" class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
		{@render children()}
	</main>

	<!-- Standard Civic Footer -->
	<footer class="border-t border-border bg-card py-8 mt-16 text-xs text-slate-600">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
			<div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
				<div class="md:col-span-7 space-y-2">
					<div class="flex items-center space-x-2">
						<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
							Open Source Civic Tech
						</span>
						<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
							Strict Provenance Standard
						</span>
					</div>
					<p class="text-slate-700 leading-relaxed font-normal">
						KIIFB Accountability & Public Value Dashboard is an independent, public-interest research tool cross-referencing statutory audits, official project databases, and the 2026 High-Level Committee Report.
					</p>
					<p class="text-slate-500 text-[11px]">
						All underlying code, synthesis scripts, and structured JSON datasets are publicly auditable and reproducible under open source terms.
					</p>
				</div>

				<div class="md:col-span-5 flex flex-col md:items-end space-y-3">
					<a
						href="https://github.com/drawablex86/kiifb-dashboard"
						target="_blank"
						rel="noopener noreferrer"
						class="inline-flex items-center gap-2 px-3 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary-hover transition font-medium text-xs shadow-sm group"
					>
						<svg class="w-4 h-4 fill-current transition group-hover:scale-105" viewBox="0 0 24 24" aria-hidden="true">
							<path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
						</svg>
						<span>View Source on GitHub</span>
						<span class="text-slate-400 group-hover:text-slate-200 text-[10px]">↗</span>
					</a>
					<div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-slate-500 text-[11px] md:justify-end">
						<a
							href="https://github.com/drawablex86/kiifb-dashboard/issues"
							target="_blank"
							rel="noopener noreferrer"
							class="hover:text-slate-900 underline underline-offset-2 transition"
						>
							Submit Data Correction
						</a>
						<span>•</span>
						<a
							href="https://github.com/drawablex86/kiifb-dashboard/blob/master/datasources.md"
							target="_blank"
							rel="noopener noreferrer"
							class="hover:text-slate-900 underline underline-offset-2 transition"
						>
							Data Sources & Provenance
						</a>
						<span>•</span>
						<span>Oct 2026 Baseline</span>
					</div>
				</div>
			</div>

			<div class="pt-4 border-t border-border flex flex-col sm:flex-row justify-between items-center gap-2 text-slate-400 text-[11px]">
				<p>© 2026 KIIFB Accountability Project • Published under open civic research guidelines.</p>
				<p>Every assertion is linked to verified public record locators.</p>
			</div>
		</div>
	</footer>
</div>
