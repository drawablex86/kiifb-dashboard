<script lang="ts">
	/**
	 * /portfolio — T101 (Milestone 10)
	 *
	 * Portfolio → Sector → District → Project drill-down funnel with
	 * summary tiles at every level (count, approved ₹, released ₹,
	 * % physically complete). All drill-down state lives in the URL
	 * (`?sector=&district=`) so any view is shareable and restores
	 * exactly. Approved outlay is never conflated with completion —
	 * the two appear as separate tiles.
	 */
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import {
		applyFunnel,
		listDistricts,
		listSectors,
		summarise,
		belongsToDistrict,
		type FunnelSummary
	} from '$lib/data/funnel';
	import PageIntro from '$lib/components/PageIntro.svelte';
	import NudgeCallout from '$lib/components/NudgeCallout.svelte';
	import PlainBadge from '$lib/components/PlainBadge.svelte';
	import ResultCount from '$lib/components/ResultCount.svelte';
	import GlossaryTerm from '$lib/components/GlossaryTerm.svelte';

	let { data } = $props();

	// URL-shared funnel state, restored exactly from the address bar.
	let sectorParam = $derived(page.url.searchParams.get('sector'));
	let districtParam = $derived(page.url.searchParams.get('district'));

	function setParams(params: Record<string, string | null>) {
		const next = new URLSearchParams(page.url.searchParams);
		for (const [k, v] of Object.entries(params)) {
			if (v === null || v === '') next.delete(k);
			else next.set(k, v);
		}
		goto(`/portfolio?${next.toString()}`, { replaceState: true, noScroll: false, keepFocus: true });
	}

	function drillSector(sector: string) {
		setParams({ sector, district: null });
	}
	function drillDistrict(district: string) {
		setParams({ district });
	}
	function clearSector() {
		setParams({ sector: null });
	}
	function clearDistrict() {
		setParams({ district: null });
	}
	function resetAll() {
		goto('/portfolio', { replaceState: true, keepFocus: true });
	}

	// Funnel levels
	let allRecords = $derived(data.records as any[]);
	let sectorLevel = $derived((sectorParam ?? null) as string | null);
	let districtLevel = $derived((districtParam ?? null) as string | null);

	let afterSector = $derived(applyFunnel(allRecords, sectorLevel, null));
	let afterDistrict = $derived(applyFunnel(afterSector, null, districtLevel));

	let portfolioSummary = $derived(summarise(allRecords));
	let sectorSummary = $derived(summarise(afterSector));
	let districtSummary = $derived(summarise(afterDistrict));

	let sectorBreakdown = $derived.by(() => {
		return listSectors(allRecords)
			.map((s) => ({ sector: s, summary: summarise(allRecords.filter((r: any) => r.sector === s)) }))
			.sort((a, b) => b.summary.approved_crore - a.summary.approved_crore);
	});
	let districtBreakdown = $derived.by(() => {
		return listDistricts(allRecords, afterSector)
			.map((d) => ({
				district: d,
				summary: summarise(afterSector.filter((r: any) => belongsToDistrict(r, d)))
			}))
			.sort((a, b) => b.summary.approved_crore - a.summary.approved_crore);
	});
	let projectList = $derived(afterDistrict.slice());

	function formatCrore(val: number): string {
		return (
			'₹' +
			val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) +
			' Cr'
		);
	}

	function tiles(summary: FunnelSummary) {
		return [
			{ label: 'Records', value: summary.count.toLocaleString('en-IN') },
			{ label: 'Approved outlay', value: formatCrore(summary.approved_crore) },
			{ label: 'Released funds', value: formatCrore(summary.released_crore) },
			{ label: '% physically complete', value: summary.pct_physically_complete.toFixed(1) + '%' }
		];
	}
</script>

<svelte:head>
	<title>Portfolio Drill-Down Funnel — KIIFB Accountability Dashboard</title>
</svelte:head>

<PageIntro
	title="Where the Money Goes"
	question="How does ₹100 of approved money move through the delivery pipeline?"
	lead="Drill Portfolio → Sector → District → Project with summary tiles at every level. Approved outlay and physical completion are separate tiles — approval is never conflated with completion. Filter state is URL-shared."
	shows={[
		'Portfolio-level tiles (count, approved, released, % complete)',
		'Sector breakdown table with drill-down',
		'District breakdown within selected sector with drill-down',
		'Project list at the deepest level with per-record financials and status',
		'URL-shareable funnel state (`?sector=&district=`)'
	]}
	doesnt={[
		'Searchable project table with 7 filters (see Projects)',
		'Sankey flow of Kanakku lifecycle stages (see Projects)',
		'Funds vs. Progress scatter (see Projects)',
		'District map with geo-tagged projects (see Districts & Map)'
	]}
/>

<NudgeCallout kind="situate" id="portfolio-start" heading="Follow the money">
	This funnel reconciles exactly with <code class="font-mono">unified_project_explorer.json</code> — 2,377 records, ₹81,161 Cr approved. The four tiles at each level are: Records, Approved Outlay, Released Funds, % Physically Complete. <strong>Approved is permission to spend; physically complete is delivery.</strong> They are separate tiles by design.
</NudgeCallout>

<!-- Header -->
<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm mb-6">
	<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-violet-50 text-violet-800 border border-violet-200 mb-2">
		<span>Record Base (L0)</span>
		<span>•</span>
		<span>T101</span>
	</div>
	<h2 class="text-2xl font-bold tracking-tight text-slate-900">Portfolio Drill-Down Funnel</h2>
	<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
		Drill Portfolio → Sector → District → Project. Reconciles exactly with
		<code class="font-mono text-2xs bg-slate-100 px-1 rounded">unified_project_explorer.json</code>.
		Filter state is URL-shared — copy the address to share the exact view.
	</p>
	<div class="mt-3 flex flex-wrap items-center gap-2 text-xs">
		<span class="text-2xs uppercase text-slate-500">Funnel path:</span>
		<nav aria-label="funnel breadcrumb" class="flex flex-wrap items-center gap-1.5">
			<button
				onclick={resetAll}
				class="px-2 py-0.5 rounded border font-semibold {(!sectorLevel && !districtLevel)
					? 'bg-slate-900 text-white border-slate-900'
					: 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}"
			>
				Portfolio
			</button>
			{#if sectorLevel}
				<span class="text-slate-300">→</span>
				<button
					onclick={clearDistrict}
					class="px-2 py-0.5 rounded border font-semibold {(!districtLevel && sectorLevel)
						? 'bg-slate-900 text-white border-slate-900'
						: 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}"
				>
					{sectorLevel}
				</button>
			{/if}
			{#if districtLevel}
				<span class="text-slate-300">→</span>
				<span class="px-2 py-0.5 rounded border font-semibold bg-slate-900 text-white border-slate-900">
					{districtLevel}
				</span>
			{/if}
		</nav>
		{#if sectorLevel || districtLevel}
			<button onclick={resetAll} class="text-blue-600 hover:underline font-medium">Reset funnel</button>
		{/if}
	</div>
</div>

<!-- LEVEL 1: PORTFOLIO -->
<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm mb-6">
	<h3 class="text-sm font-bold text-slate-900 mb-3">Level 1 — Whole Portfolio</h3>
	<div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
		{#each tiles(portfolioSummary) as t}
			<div class="bg-slate-50 p-3 rounded border border-slate-200">
				<div class="text-2xs text-slate-500 uppercase font-semibold">{t.label}</div>
				<div class="text-base font-bold text-slate-900 tabular-nums">{t.value}</div>
			</div>
		{/each}
	</div>
	<NudgeCallout kind="interpret" id="portfolio-level1" heading="Read the tiles correctly">
		Approved outlay = total sanctioned (permission). Released = cash disbursed. % Physically complete = Kanakku lifecycle stages that indicate physical delivery. These are <strong>different dimensions</strong> — a project can be 100% approved and 0% complete.
	</NudgeCallout>
	<ResultCount shown={allRecords.length} total={allRecords.length} noun="records" />
	<table class="w-full text-xs text-left text-slate-700 border-t border-slate-100 mt-4">
		<caption class="sr-only">Sector breakdown of the portfolio</caption>
		<thead class="bg-slate-50 text-2xs text-slate-500 uppercase border-b border-slate-200">
			<tr>
				<th class="px-3 py-2">Sector</th>
				<th class="px-3 py-2 text-center">Records</th>
				<th class="px-3 py-2 text-right">Approved (₹ Cr)</th>
				<th class="px-3 py-2 text-right">Released (₹ Cr)</th>
				<th class="px-3 py-2 text-right">% Complete</th>
				<th class="px-3 py-2"></th>
			</tr>
		</thead>
		<tbody class="divide-y divide-slate-100">
			{#each sectorBreakdown as row}
				<tr>
					<td class="px-3 py-2 font-medium text-slate-900">{row.sector}</td>
					<td class="px-3 py-2 text-center font-mono tabular-nums">{row.summary.count}</td>
					<td class="px-3 py-2 text-right font-mono tabular-nums">{formatCrore(row.summary.approved_crore)}</td>
					<td class="px-3 py-2 text-right font-mono tabular-nums">{formatCrore(row.summary.released_crore)}</td>
					<td class="px-3 py-2 text-right font-mono tabular-nums">{row.summary.pct_physically_complete.toFixed(1)}%</td>
					<td class="px-3 py-2 text-right">
						<button
							onclick={() => drillSector(row.sector)}
							class="px-2 py-0.5 text-2xs font-medium text-blue-700 bg-blue-50 border border-blue-200 rounded hover:bg-blue-100 transition"
						>
							Drill down
						</button>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>

{#if sectorLevel}
	<!-- LEVEL 2: DISTRICTS within sector -->
	<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm mb-6">
		<h3 class="text-sm font-bold text-slate-900 mb-3">Level 2 — Districts within “{sectorLevel}”</h3>
		<div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
			{#each tiles(sectorSummary) as t}
				<div class="bg-violet-50/60 p-3 rounded border border-violet-200">
					<div class="text-2xs text-violet-700 uppercase font-semibold">{t.label}</div>
					<div class="text-base font-bold text-slate-900 tabular-nums">{t.value}</div>
				</div>
			{/each}
		</div>
		<NudgeCallout kind="interpret" id="portfolio-level2" heading="District attribution is enriched">
			District tags come from the Kanakku matching pipeline (T083) — 78.3% coverage (1,103/1,408). Unattributed records are excluded from district tiles, not counted as zero. See <GlossaryTerm id="kanakku" /> matching log for provenance.
		</NudgeCallout>
		<ResultCount shown={afterSector.length} total={allRecords.length} noun="records" />
		<table class="w-full text-xs text-left text-slate-700 border-t border-slate-100 mt-4">
			<caption class="sr-only">District breakdown within selected sector</caption>
			<thead class="bg-slate-50 text-2xs text-slate-500 uppercase border-b border-slate-200">
				<tr>
					<th class="px-3 py-2">District</th>
					<th class="px-3 py-2 text-center">Records</th>
					<th class="px-3 py-2 text-right">Approved (₹ Cr)</th>
					<th class="px-3 py-2 text-right">Released (₹ Cr)</th>
					<th class="px-3 py-2 text-right">% Complete</th>
					<th class="px-3 py-2"></th>
				</tr>
			</thead>
			<tbody class="divide-y divide-slate-100">
				{#each districtBreakdown as row}
					<tr>
						<td class="px-3 py-2 font-medium text-slate-900">{row.district}</td>
						<td class="px-3 py-2 text-center font-mono tabular-nums">{row.summary.count}</td>
						<td class="px-3 py-2 text-right font-mono tabular-nums">{formatCrore(row.summary.approved_crore)}</td>
						<td class="px-3 py-2 text-right font-mono tabular-nums">{formatCrore(row.summary.released_crore)}</td>
						<td class="px-3 py-2 text-right font-mono tabular-nums">{row.summary.pct_physically_complete.toFixed(1)}%</td>
						<td class="px-3 py-2 text-right">
							<button
								onclick={() => drillDistrict(row.district)}
								class="px-2 py-0.5 text-2xs font-medium text-blue-700 bg-blue-50 border border-blue-200 rounded hover:bg-blue-100 transition"
							>
								Drill down
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

{#if districtLevel}
	<!-- LEVEL 3: PROJECT LIST -->
	<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm mb-6">
		<h3 class="text-sm font-bold text-slate-900 mb-3">
			Level 3 — Projects in {districtLevel} ({sectorLevel ?? 'all sectors'})
		</h3>
		<div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
			{#each tiles(districtSummary) as t}
				<div class="bg-emerald-50/60 p-3 rounded border border-emerald-200">
					<div class="text-2xs text-emerald-700 uppercase font-semibold">{t.label}</div>
					<div class="text-base font-bold text-slate-900 tabular-nums">{t.value}</div>
				</div>
			{/each}
		</div>
		<ResultCount shown={projectList.length} total={allRecords.length} noun="records" />
		<div class="border-t border-slate-100 divide-y divide-slate-100">
			{#each projectList as rec}
				<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 py-2 text-xs">
					<div>
						<a
							href="/projects"
							class="font-semibold text-slate-900 hover:text-blue-700"
						>{rec.name}</a>
						<span class="font-mono text-3xs text-slate-400 ml-1">{rec.record_id}</span>
						<div class="text-2xs text-slate-500">
							{rec.sector || '—'}{rec.department ? ` · ${rec.department}` : ''}
						</div>
					</div>
					<div class="flex items-center gap-3 font-mono tabular-nums text-2xs">
						<span class="text-slate-600">Approved {formatCrore(rec.financials?.approved_crore ?? 0)}</span>
						<span class="text-slate-600">Released {formatCrore(rec.financials?.released_crore ?? 0)}</span>
						<PlainBadge label={rec.status?.normalised_status ?? 'unrecorded'} />
					</div>
				</div>
			{/each}
			{#if projectList.length === 0}
				<div class="py-4 text-center text-slate-400 text-xs">No records at this funnel level.</div>
			{/if}
		</div>
		<div class="mt-3 text-3xs text-slate-400 font-mono">
			* Per-record provenance (source_id / source_locator) is available via the Project
			Explorer inspection drawer; this list shows the funnel reconciliation figures only.
		</div>
	</div>
{/if}

<!-- Provenance banner -->
<div class="bg-slate-100 border border-slate-200 rounded-lg p-4 text-xs text-slate-600">
	<span class="font-bold text-slate-900">Reconciliation standard (T101):</span> tile counts and
	sums aggregate <code class="font-mono">records[]</code> of
	<code class="font-mono">unified_project_explorer.json</code> without any additional filtering
	rules; they are asserted equal to dataset-level totals in
	<code class="font-mono">tests/test_portfolio_funnel.py</code>. "Approved outlay" tiles are
	entirely separate from the "% physically complete" tile — approval is never conflated with
	completion. Data: DS010/DS021/DS030 processed derivatives; as-of
	<code class="font-mono">{data.generatedAt}</code>.
</div>