<script lang="ts">
	/**
	 * /glossary — "Glossary & Sources" (designsystem.md §4.1, §5.4).
	 *
	 * Searchable plain-words A–Z of every term used on the site, plus the
	 * verification entry points (sources register, raw data, exports).
	 * Depth-aware: technical definitions lead in Evidence gear, plain first
	 * in Plain gear. Anchors match GlossaryTerm popover deep-links (#id).
	 */
	import PageIntro from '$lib/components/PageIntro.svelte';
	import ResultCount from '$lib/components/ResultCount.svelte';
	import { GLOSSARY, searchGlossary, type GlossaryEntry } from '$lib/data/glossary';
	import { depth } from '$lib/stores/depth.svelte';

	let query = $state('');

	const matches = $derived(searchGlossary(query));
	const groups = $derived.by(() => {
		const byLetter = new Map<string, GlossaryEntry[]>();
		for (const entry of matches) {
			const letter = entry.term[0].toUpperCase();
			const bucket = byLetter.get(letter) ?? [];
			bucket.push(entry);
			byLetter.set(letter, bucket);
		}
		return [...byLetter.entries()].sort(([a], [b]) => a.localeCompare(b));
	});
</script>

<svelte:head>
	<title>Glossary & Sources — KIIFB Accountability Dashboard</title>
</svelte:head>

<div class="space-y-8">
	<PageIntro
		title="Glossary & Sources"
		question="What exactly does this word mean, and where do I check it?"
		lead="Every term this site uses, in plain words first and technical detail underneath. Any dotted-underlined word anywhere on the site opens a version of these definitions right in place."
		shows={[
			`${GLOSSARY.length} defined terms, searchable`,
			`Plain-words and technical definitions side by side`,
			'Links back to the pages where each term matters'
		]}
		doesnt={[
			'Primary documents themselves — sources live in the linked register',
			'New values or claims (this page only explains words)'
		]}
	/>

	<!-- Search + results -->
	<section aria-label="Search glossary terms" class="space-y-3">
		<div class="flex flex-col sm:flex-row sm:items-end gap-2">
			<div class="flex-1">
				<label for="glossary-search" class="block text-xs font-medium text-slate-700 mb-1">Search terms</label>
				<input
					id="glossary-search"
					type="search"
					bind:value={query}
					placeholder="e.g. masala bond, crore, debt service…"
					autocomplete="off"
					spellcheck="false"
					class="w-full h-9 rounded-md border border-border bg-card px-3 text-sm text-foreground placeholder:text-slate-400 focus-visible:outline-2 focus-visible:outline-ring"
				/>
			</div>
			{#if query}
				<button
					type="button"
					class="h-9 px-3 self-start rounded-md border border-border bg-card text-sm font-medium text-slate-700 hover:bg-slate-50 transition-all outline-2 outline-offset-2 outline-transparent hover:outline-slate-300"
					onclick={() => (query = '')}
				>
					Clear search
				</button>
			{/if}
		</div>
		<ResultCount shown={matches.length} total={GLOSSARY.length} noun="terms" />
	</section>

	<!-- A–Z definition list -->
	{#if matches.length === 0}
		<section class="rounded-lg border border-border bg-card p-8 text-center">
			<p class="text-sm font-medium text-slate-800">No terms matched “{query}”.</p>
			<p class="text-xs text-muted-foreground mt-1">
				Try a shorter term — or if this word appears on the site unexplained, that's a bug we'd want to fix.
				<a
					class="underline underline-offset-2 text-blue-700 hover:text-blue-900"
					href="https://github.com/drawablex86/kiifb-dashboard/issues"
					target="_blank"
					rel="noopener noreferrer">Report it →</a
				>
			</p>
		</section>
	{:else}
		<section class="space-y-8">
			{#each groups as [letter, entries], gi (letter + gi)}
				<div>
					<h2 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-2" aria-hidden="true">{letter}</h2>
					<div class="space-y-3">
						{#each entries as entry (entry.id)}
							<article
								id={entry.id}
								aria-labelledby={`term-${entry.id}`}
								class="scroll-mt-28 rounded-lg border border-border bg-card p-5"
							>
								<h3 id={`term-${entry.id}`} class="text-base font-semibold text-foreground">{entry.term}</h3>

								<p class="mt-2 text-sm text-slate-700 leading-relaxed">
									{#if depth.mode === 'evidence'}
										<span class="text-xs font-semibold uppercase tracking-wide text-slate-400 block mb-0.5">Technical definition</span>
										{entry.expert}
									{:else}
										<span class="text-xs font-semibold uppercase tracking-wide text-slate-400 block mb-0.5">In plain words</span>
										{entry.plain}
									{/if}
								</p>
								<p class="mt-2 text-sm text-slate-600 leading-relaxed">
									{#if depth.mode === 'evidence'}
										<span class="text-xs font-semibold uppercase tracking-wide text-slate-400 block mb-0.5">In plain words</span>
									{:else}
										<span class="text-xs font-semibold uppercase tracking-wide text-slate-400 block mb-0.5">Technical definition</span>
									{/if}
									{depth.mode === 'evidence' ? entry.plain : entry.expert}
								</p>

								<p class="mt-3 pt-3 border-t border-border text-xs text-slate-600 leading-relaxed">
									<span class="font-semibold text-slate-700">Why it matters here: </span>{entry.why}
								</p>

								{#if entry.seeAlso?.length}
									<p class="mt-2 flex flex-wrap items-center gap-1.5 text-xs">
										<span class="text-slate-400">See also:</span>
										{#each entry.seeAlso as link (link)}
											<a href="/glossary#{link}" class="rounded-none underline decoration-dotted decoration-slate-400 underline-offset-2 text-blue-700 hover:text-blue-900">
												{GLOSSARY.find((g) => g.id === link)?.term ?? link}
											</a>
										{/each}
									</p>
								{/if}
							</article>
						{/each}
					</div>
				</div>
			{/each}
		</section>
	{/if}

	<!-- Sources & verification entry points -->
	<section aria-labelledby="sources-heading" class="rounded-lg border border-border bg-card p-5">
		<h2 id="sources-heading" class="text-base font-semibold text-foreground mb-1">Where the data comes from</h2>
		<p class="text-sm text-slate-600 mb-4 max-w-3xl">
			Every figure traces to a checksummed primary source (the committee report PDF, KIIFB's own portals,
			Kerala PWD's public ledger, statutory registers). Experts can rebuild the dataset end-to-end.
		</p>
		<ul class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
			<li class="rounded-md border border-border bg-slate-50/60 p-3">
				<a
					href="https://github.com/drawablex86/kiifb-dashboard/blob/master/datasources.md"
					target="_blank"
					rel="noopener noreferrer"
					class="font-medium text-slate-900 hover:text-blue-700 hover:underline underline-offset-2"
				>
					Source register & licences <span aria-hidden="true">↗</span>
				</a>
				<p class="text-xs text-muted-foreground mt-1">Publishers, retrieval dates, SHA-256 checksums, licence terms</p>
			</li>
			<li class="rounded-md border border-border bg-slate-50/60 p-3">
				<a
					href="/api/v1/projects.csv"
					class="font-medium text-slate-900 hover:text-blue-700 hover:underline underline-offset-2"
				>
					Download the full record set
				</a>
				<p class="text-xs text-muted-foreground mt-1">CSV with provenance columns; also <a class="underline underline-offset-2 text-slate-600 hover:text-blue-700" href="/api/v1/projects.json">JSON</a> and <a class="underline underline-offset-2 text-slate-600 hover:text-blue-700" href="/api/v1/change-log.json">change-log</a></p>
			</li>
			<li class="rounded-md border border-border bg-slate-50/60 p-3">
				<a
					href="https://github.com/drawablex86/kiifb-dashboard/blob/master/design-system.md"
					target="_blank"
					rel="noopener noreferrer"
					class="font-medium text-slate-900 hover:text-blue-700 hover:underline underline-offset-2"
				>
					How evidence states are defined <span aria-hidden="true">↗</span>
				</a>
				<p class="text-xs text-muted-foreground mt-1">The seven-state taxonomy and what each badge is allowed to claim</p>
			</li>
		</ul>
	</section>
</div>
