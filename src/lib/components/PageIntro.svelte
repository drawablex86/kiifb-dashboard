<script lang="ts">
	/**
	 * PageIntro.svelte — the standard page spine's opening (designsystem.md §4.2):
	 * breadcrumb → h1 → standing question → plain lead →
	 * "On this page / Not on this page (yet)" honesty panel.
	 *
	 * Answers Norman's gulf-of-evaluation from the top: every page opens by
	 * saying what it is for and what it cannot tell you.
	 */
	let {
		crumbs = [],
		title,
		question = undefined,
		lead = undefined,
		shows = [],
		doesnt = []
	}: {
		/** Intermediate trail items; "Home" is always prepended. */
		crumbs?: { label: string; href: string }[];
		title: string;
		/** The page's guiding question, stated in plain words. */
		question?: string;
		/** 1–3 sentence plain answer / orientation. */
		lead?: string;
		/** What the reader will find on this page. */
		shows?: string[];
		/** What the reader will NOT find — honest-gap disclosure. */
		doesnt?: string[];
	} = $props();
</script>

<div class="mb-8">
	{#if crumbs.length}
		<nav aria-label="Breadcrumb" class="mb-2">
			<ol class="flex flex-wrap items-center gap-1.5 text-xs text-slate-500">
				<li><a href="/" class="hover:text-slate-900 hover:underline underline-offset-2">Home</a></li>
				{#each crumbs as c (c.href)}
					<li aria-hidden="true" class="text-slate-300">/</li>
					<li><a href={c.href} class="hover:text-slate-900 hover:underline underline-offset-2">{c.label}</a></li>
				{/each}
			</ol>
		</nav>
	{/if}

	<h1 class="text-2xl font-bold tracking-tight text-slate-900">{title}</h1>

	{#if question}
		<p class="mt-1.5 text-sm text-slate-500">
			<span class="font-medium text-slate-600">Standing question:</span>
			<span class="italic">“{question}”</span>
		</p>
	{/if}

	{#if lead}
		<p class="mt-3 text-sm sm:text-base text-slate-700 leading-relaxed max-w-3xl">{@html lead}</p>
	{/if}

	{#if shows.length || doesnt.length}
		<div class="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3">
			{#if shows.length}
				<div class="rounded-md border border-emerald-200 bg-emerald-50/50 p-3">
					<p class="text-xs font-semibold text-emerald-800 mb-1.5">On this page</p>
					<ul class="space-y-1 text-xs text-slate-700 list-disc pl-4 marker:text-emerald-600">
						{#each shows as item (item)}<li>{item}</li>{/each}
					</ul>
				</div>
			{/if}
			{#if doesnt.length}
				<div class="rounded-md border border-slate-200 bg-slate-50 p-3">
					<p class="text-xs font-semibold text-slate-700 mb-1.5">Not on this page (yet)</p>
					<ul class="space-y-1 text-xs text-slate-700 list-disc pl-4 marker:text-slate-400">
						{#each doesnt as item (item)}<li>{item}</li>{/each}
					</ul>
				</div>
			{/if}
		</div>
	{/if}
</div>
