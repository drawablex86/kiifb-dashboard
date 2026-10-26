<script lang="ts">
	import { depth } from '$lib/stores/depth.svelte';
	import { initDepth } from '$lib/stores/depth.svelte';
	import PageIntro from '$lib/components/PageIntro.svelte';
	import NudgeCallout from '$lib/components/NudgeCallout.svelte';
	import DepthToggle from '$lib/components/DepthToggle.svelte';
	import PlainBadge from '$lib/components/PlainBadge.svelte';
	import GlossaryTerm from '$lib/components/GlossaryTerm.svelte';

	let { data } = $props();

	// Initialize depth store on client mount
	$effect.pre(() => {
		initDepth();
	});

	// State for citation drawer
	let selectedAssertion = $state<any>(null);
	let activeEvidenceLinks = $derived(
		selectedAssertion
			? data.evidenceLinks.filter((ev: any) => ev.assertion_id === selectedAssertion.assertion_id)
			: []
	);

	function openEvidenceDrawer(assertion: any) {
		selectedAssertion = assertion;
	}

	function closeEvidenceDrawer() {
		selectedAssertion = null;
	}

	// Welcome dismiss state
	let welcomeDismissed = $state(false);
	$effect.pre(() => {
		welcomeDismissed = typeof localStorage !== 'undefined' && localStorage.getItem('welcomeDismissed') === 'true';
	});

	function dismissWelcome() {
		welcomeDismissed = true;
		if (typeof localStorage !== 'undefined') {
			localStorage.setItem('welcomeDismissed', 'true');
		}
	}

	// Five plain-language questions = site map
	const siteQuestions = [
		{
			id: 'what-is-kiifb',
			question: 'What is KIIFB, and how does it borrow?',
			answer: 'KIIFB is Kerala\'s off-budget infrastructure company. It borrows in its own name (banks, bonds, masala bonds), but the state services 99.4% of its debt from the budget. The Committee says this consumes ₹25,932.55 Cr of Kerala\'s borrowing space.',
			route: '/genesis',
			linkLabel: 'Read the origin story →',
			badge: 'Analytical layer'
		},
		{
			id: 'where-money-goes',
			question: 'Where does the money go — project by project?',
			answer: '1,408 sanctioned projects across 35 departments. Search by district, sector, status, or keyword. See approved vs. released vs. physically complete — with evidence badges on every record.',
			route: '/projects',
			linkLabel: 'Explore projects →',
			badge: 'Record base'
		},
		{
			id: 'money-pipeline',
			question: 'How does ₹100 of approved money move through the pipeline?',
			answer: 'Track the flow: Approved → Tendered → Contracted → In Progress → Complete → Handed Over → Operational. The funnel shows where money gets stuck and which sectors deliver.',
			route: '/portfolio',
			linkLabel: 'Follow the funnel →',
			badge: 'Record base'
		},
		{
			id: 'debt-repayments',
			question: 'Who does KIIFB owe, and when is it repaid?',
			answer: 'Banks, institutions, and bondholders — ₹16,290 Cr outstanding, with a 16-year amortisation schedule to FY 2041-42. See the borrowing cost premium (≈₹910 Cr over state rates) and the land acquisition liability pool.',
			route: '/financials',
			linkLabel: 'View debt schedule →',
			badge: 'Record base'
		},
		{
			id: 'districts-map',
			question: 'Where did the money land across Kerala\'s 14 districts?',
			answer: 'Top 3 districts receive 41.6% of approved outlay. Kannur holds 74.7% of the land acquisition pool. See the interactive map, district bars, and the evidence gaps (GAP-001: 309 projects lack district tags).',
			route: '/outcomes',
			linkLabel: 'See the map →',
			badge: 'Record base'
		}
	];

	// Helper to format currency
	function formatIndianCrore(val: number): string {
		return '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Cr';
	}
</script>

<svelte:head>
	<title>KIIFB Accountability Dashboard — Start Here</title>
</svelte:head>

<PageIntro
	title="Start Here"
	question="What is this dashboard, and what five questions can it answer?"
	lead="This site lets you follow KIIFB's money from sanction to handover, see the debt schedule to 2041, and check the October 2026 Expert Committee's claims against the underlying records. Two reading gears: <strong>Plain English</strong> (default) and <strong>Evidence</strong> (locators, IDs, formulas)."
	shows={[
		'Five plain-language questions that map to the site\'s main sections',
		'Depth switch: Plain English ⇄ Evidence (top-right, remembers your choice)',
		'The Committee\'s five assertions — checked against official records',
		'How this site works: sources, evidence labels, glossary, and exports'
	]}
	doesnt={[
		'Project-level progress charts (see Projects and Portfolio)',
		'Debt amortisation detail (see Debt & Repayments)',
		'District map with geo-tagged projects (see Districts & Map)',
		'Change-over-time trends (see Change Over Time)',
		'Delay/cost-overrun register (see Alerts & Delays)',
		'Legal scrutiny of the committee process (see The Committee\'s Claims)'
	]}
/>

{#if !welcomeDismissed}
	<div class="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3" role="status">
		<div class="flex-1">
			<div class="text-sm text-amber-900">
				<strong>Welcome.</strong> This dashboard covers KIIFB's finances, projects, and the October 2026 Expert Committee's findings. The <DepthToggle compact /> switch in the header (and below) lets you toggle between Plain English and Evidence modes at any time.
			</div>
		</div>
		<button
			onclick={dismissWelcome}
			class="px-3 py-1.5 text-xs font-medium text-amber-800 bg-amber-100 border border-amber-300 rounded hover:bg-amber-200 transition flex-shrink-0"
		>
			Got it — don't show again
		</button>
	</div>
{/if}

<!-- How this site works -->
<section class="mb-8">
	<div class="bg-card border border-border rounded-lg p-5 shadow-sm">
		<h2 class="text-lg font-semibold text-slate-900 mb-3 flex items-center gap-2">
			<svg class="w-5 h-5 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>
			How this site works
		</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
			<div class="p-3 bg-slate-50 rounded border border-border">
				<div class="font-medium text-slate-900 mb-1">Sources are documented</div>
				<div class="text-slate-600">Every figure cites a source ID (DS001, DS010, DS030…), a table/page locator, and an as-of date. <a href="/glossary" class="text-indigo-600 hover:underline">Glossary → Sources</a> lists them all.</div>
			</div>
			<div class="p-3 bg-slate-50 rounded border border-border">
				<div class="font-medium text-slate-900 mb-1">Evidence labels on every fact</div>
				<div class="text-slate-600"><PlainBadge label="official_record" /> = published in an official document. <PlainBadge label="committee_finding" /> = the committee's claim. <PlainBadge label="data_gap" /> = nobody publishes this. <a href="/glossary#evidence_label" class="text-indigo-600 hover:underline">Evidence taxonomy →</a></div>
			</div>
			<div class="p-3 bg-slate-50 rounded border border-border">
				<div class="font-medium text-slate-900 mb-1">Glossary at point of use</div>
				<div class="text-slate-600">Dotted-underlined terms like <GlossaryTerm id="borrowing_space" /> and <GlossaryTerm id="article_293" /> open plain definitions. Switch to Evidence gear for the technical definition. <a href="/glossary" class="text-indigo-600 hover:underline">Full glossary →</a></div>
			</div>
			<div class="p-3 bg-slate-50 rounded border border-border">
				<div class="font-medium text-slate-900 mb-1">Download & verify</div>
				<div class="text-slate-600">CSV/JSON exports on <a href="/projects" class="text-indigo-600 hover:underline">Projects</a>, <a href="/api/v1/projects.json" class="text-indigo-600 hover:underline">API endpoints</a>, and district fact sheets on <a href="/outcomes" class="text-indigo-600 hover:underline">Districts & Map</a>. All inherit CC BY 4.0 where Kanakku data is used.</div>
			</div>
		</div>
	</div>
</section>

<!-- Five questions = site map -->
<section class="mb-8">
	<h2 class="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
		<svg class="w-5 h-5 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
		Five questions this site answers
	</h2>

	<NudgeCallout kind="situate" id="home-start-here" heading="Start with one question">
		Each card below is a doorway. Click through to the section that matches what you want to know. The depth switch (top-right) changes how every page reads — not just this one.
	</NudgeCallout>

	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
		{#each siteQuestions as q}
			<a
				href={q.route}
				class="group bg-white border border-slate-200 rounded-lg p-5 shadow-sm hover:border-indigo-300 hover:shadow-md transition-all duration-200 flex flex-col h-full"
			>
				<div class="flex items-center justify-between mb-2">
					<span class="text-xs font-semibold px-2 py-0.5 rounded border border-slate-200 bg-slate-50 text-slate-600">
						{q.badge}
					</span>
				</div>
				<h3 class="text-base font-semibold text-slate-900 group-hover:text-indigo-700 transition mb-2">
					{q.question}
				</h3>
				<p class="text-sm text-slate-600 leading-relaxed flex-1 mb-3">
					{q.answer}
				</p>
				<span class="text-sm font-medium text-indigo-600 group-hover:underline flex items-center gap-1">
					{q.linkLabel}
					<svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
				</span>
			</a>
		{/each}
	</div>
</section>

<!-- Committee Assertions Section (V3 framing: analyses as layers) -->
<section class="mb-8">
	<div class="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden">
		<div class="p-5 border-b border-slate-200 bg-slate-50/50">
			<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
				<div>
					<h2 class="text-lg font-semibold text-slate-900 flex items-center gap-2">
						<svg class="w-5 h-5 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>
						The Committee's Claims — checked against the record
					</h2>
					<p class="text-sm text-slate-600 mt-1">
						The October 2026 Expert Committee (chaired by Sudha Pillai) made five major assertions about KIIFB's borrowing, debt service, project classification, and delivery reporting. Each card below links the claim to its source locator and to corroborating or qualifying official records.
					</p>
				</div>
				<a href="/committee" class="text-sm font-medium text-indigo-600 hover:underline whitespace-nowrap self-center">
					Full scrutiny: legality, lapses, members, federalism →
				</a>
			</div>
		</div>

		<NudgeCallout kind="interpret" id="home-committee-layer" heading="Read this layer correctly">
			This is an <strong>analytical layer</strong> (the October 2026 Committee's view), not the record base. The committee's findings are treated as claims — corroborated, qualified, or contested by the official records linked in each drawer. KIIFB's own data (projects, financials, districts) lives in the "Follow the money" sections above.
		</NudgeCallout>

		<div class="p-5 space-y-4">
			{#each data.assertions as assertion}
				<div
					class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm hover:border-slate-300 transition cursor-pointer relative group"
					onclick={() => openEvidenceDrawer(assertion)}
					role="button"
					tabindex="0"
					onkeydown={(e) => e.key === 'Enter' && openEvidenceDrawer(assertion)}
				>
					<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
						<div class="flex items-center gap-2 flex-wrap">
							<span class="font-mono text-xs font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
								{assertion.assertion_id}
							</span>
							<PlainBadge label={assertion.evidence_label} />
							<span class="text-xs text-slate-500 font-mono">
								{assertion.reporting_period}
							</span>
						</div>
						<div class="text-xs text-slate-500 font-mono flex items-center gap-1.5">
							<span>Source: Chapter {assertion.report_locator.chapter}, {assertion.report_locator.table}</span>
						</div>
					</div>

					<h4 class="text-base font-bold text-slate-900 group-hover:text-blue-700 transition mb-2">
						{assertion.headline}
					</h4>

					<p class="text-sm text-slate-700 leading-relaxed mb-4">
						{assertion.report_claim}
					</p>

					<!-- Key Quantitative Metrics Preview -->
					<div class="bg-slate-50 rounded border border-slate-200/70 p-3 mb-3 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
						{#if assertion.cited_values.total_amount_crore}
							<div>
								<div class="text-slate-500">Deducted Space</div>
								<div class="text-sm font-bold text-slate-900 tabular-nums">
									{formatIndianCrore(assertion.cited_values.total_amount_crore)}
								</div>
							</div>
						{/if}
						{#if assertion.cited_values.servicing_ratio_percentage}
							<div>
								<div class="text-slate-500">Transfers / Debt Service</div>
								<div class="text-sm font-bold text-slate-900 tabular-nums">
									{assertion.cited_values.servicing_ratio_percentage}%
								</div>
							</div>
							<div>
								<div class="text-slate-500">Total Debt Servicing</div>
								<div class="text-sm font-bold text-slate-900 tabular-nums">
									{formatIndianCrore(assertion.cited_values.total_debt_service_crore)}
								</div>
							</div>
						{/if}
						{#if assertion.cited_values.estimated_premium_crore}
							<div>
								<div class="text-slate-500">Borrowing Premium</div>
								<div class="text-sm font-bold text-slate-900 tabular-nums">
									~{formatIndianCrore(assertion.cited_values.estimated_premium_crore)}
								</div>
							</div>
							<div>
								<div class="text-slate-500">Spread Over State OMB</div>
								<div class="text-sm font-bold text-slate-900 tabular-nums">
									{assertion.cited_values.spread_bps_range}
								</div>
							</div>
						{/if}
						{#if assertion.cited_values.total_revenue_projects_sanctioned}
							<div>
								<div class="text-slate-500">Sanctioned Revenue Projects</div>
								<div class="text-sm font-bold text-slate-900 tabular-nums">
									{assertion.cited_values.total_revenue_projects_sanctioned} ({formatIndianCrore(assertion.cited_values.total_sanctioned_amount_crore)})
								</div>
							</div>
							<div>
								<div class="text-slate-500">True Revenue Repayments</div>
								<div class="text-sm font-bold text-emerald-800 tabular-nums">
									{assertion.cited_values.projects_with_project_revenue_repayments} projects ({formatIndianCrore(assertion.cited_values.verified_project_revenue_repayment_crore)})
								</div>
							</div>
						{/if}
						{#if assertion.cited_values.total_approved_crore}
							<div>
								<div class="text-slate-500">Total Approved Outlay</div>
								<div class="text-sm font-bold text-slate-900 tabular-nums">
									{formatIndianCrore(assertion.cited_values.total_approved_crore)}
								</div>
							</div>
							<div>
								<div class="text-slate-500">Released (42.2%)</div>
								<div class="text-sm font-bold text-slate-900 tabular-nums">
									{formatIndianCrore(assertion.cited_values.total_released_crore)}
								</div>
							</div>
							<div>
								<div class="text-slate-500">Further Funding Needed</div>
								<div class="text-sm font-bold text-amber-800 tabular-nums">
									{formatIndianCrore(assertion.cited_values.further_completion_funding_needed_crore)}
								</div>
							</div>
						{/if}
					</div>

					<div class="flex items-center justify-between pt-2 text-xs text-slate-500 border-t border-slate-100">
						<span class="italic text-slate-500">
							<strong>Caveat:</strong> {assertion.caveats.slice(0, 110)}...
						</span>
						<span class="font-medium text-blue-600 group-hover:underline whitespace-nowrap ml-2 flex items-center gap-1">
							View Evidence & Citations
							<svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
						</span>
					</div>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- Before you conclude footer -->
<section class="mb-8">
	<NudgeCallout kind="interpret" id="home-before-conclude" heading="Before you conclude…">
		<ul class="list-disc list-inside space-y-1 text-sm text-slate-700 mt-2">
			<li><strong>Approved ≠ built.</strong> "Sanctioned" means permission to spend; physical completion and handover are separate stages tracked in <a href="/projects" class="underline">Projects</a> and <a href="/portfolio" class="underline">Portfolio</a>.</li>
			<li><strong>Committee = one study.</strong> The Oct 2026 report is an analytical layer (L2). The record base (L0) and KIIFB's own story (L1) are in the sections above.</li>
			<li><strong>Data gaps are explicit.</strong> Where evidence is missing, you'll see <PlainBadge label="data_gap" /> badges — not zeros.</li>
		</ul>
	</NudgeCallout>
</section>

<!-- Next questions -->
<section class="mb-8">
	<h2 class="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
		<svg class="w-5 h-5 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M17 18a5 5 0 0 0-10 0"/><path d="M12 2v20M12 12l-2 2 2 2"/></svg>
		Next questions to explore
	</h2>
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
		<a href="/trends" class="bg-white border border-slate-200 rounded-lg p-4 hover:border-indigo-300 transition">
			<h3 class="font-medium text-slate-900 mb-1">How have the numbers changed over time?</h3>
			<p class="text-sm text-slate-600">Snapshot history of released funds, status migrations, and district concentration — from the live fetch pipeline.</p>
		</a>
		<a href="/flags" class="bg-white border border-slate-200 rounded-lg p-4 hover:border-indigo-300 transition">
			<h3 class="font-medium text-slate-900 mb-1">Which projects are delayed or over budget?</h3>
			<p class="text-sm text-slate-600">Register of overdue, cost-escalation, and paid-but-idle flags with trend history from change logs.</p>
		</a>
		<a href="/governance" class="bg-white border border-slate-200 rounded-lg p-4 hover:border-indigo-300 transition">
			<h3 class="font-medium text-slate-900 mb-1">What did the committee recommend, and what happened?</h3>
			<p class="text-sm text-slate-600">8 restructuring recommendations mapped to authorities, legal instruments, and implementation status (0 of 8 fully implemented).</p>
		</a>
		<a href="/glossary" class="bg-white border border-slate-200 rounded-lg p-4 hover:border-indigo-300 transition">
			<h3 class="font-medium text-slate-900 mb-1">What does that term mean?</h3>
			<p class="text-sm text-slate-600">37 terms in plain English and expert definitions — searchable, with source locators and see-also links.</p>
		</a>
		<a href="/committee" class="bg-white border border-slate-200 rounded-lg p-4 hover:border-indigo-300 transition">
			<h3 class="font-medium text-slate-900 mb-1">Was the committee itself above board?</h3>
			<p class="text-sm text-slate-600">Constitution & legality, 4 procedural lapses, member dossiers & conflicts, federal squeeze matrix — with cryptographic provenance.</p>
		</a>
		<a href="/genesis" class="bg-white border border-slate-200 rounded-lg p-4 hover:border-indigo-300 transition">
			<h3 class="font-medium text-slate-900 mb-1">How was KIIFB created and why?</h3>
			<p class="text-sm text-slate-600">Statutory evolution 1999–2016, key people, Keynesian capital premise, Section 7 hypothecation, opposing pillars matrix.</p>
		</a>
	</div>
</section>

<!-- Slide-over Citation & Evidence Drawer -->
{#if selectedAssertion}
	<div
		class="fixed inset-0 z-50 overflow-hidden bg-slate-900/50 backdrop-blur-xs flex justify-end transition-opacity"
		onclick={closeEvidenceDrawer}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
		onkeydown={(e) => { e.key === 'Escape' && closeEvidenceDrawer(); e.stopPropagation(); }}
	>
		<div
			class="w-full max-w-2xl bg-white h-full shadow-2xl p-6 overflow-y-auto flex flex-col justify-between"
			role="document"
		>
			<div class="space-y-6">
				<!-- Drawer Header -->
				<div class="flex items-start justify-between pb-4 border-b border-slate-200">
					<div>
						<div class="flex items-center gap-2 mb-1">
							<span class="font-mono text-xs font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
								{selectedAssertion.assertion_id}
							</span>
							<PlainBadge label={selectedAssertion.evidence_label} />
						</div>
						<h3 class="text-lg font-bold text-slate-900">
							{selectedAssertion.headline}
						</h3>
					</div>
					<button
						onclick={closeEvidenceDrawer}
						class="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition text-lg"
						aria-label="Close drawer"
					>
						✕
					</button>
				</div>

				<!-- Source Citation Locator -->
				<div class="bg-purple-50/60 rounded-lg p-4 border border-purple-200/80">
					<div class="text-xs font-semibold text-purple-900 uppercase tracking-wider mb-2">
						Primary Committee Report Citation
					</div>
					<div class="text-sm text-purple-950 font-medium mb-1">
						{data.manifest.sources.find((s: any) => s.source_id === 'DS001')?.title || 'Committee Report Oct 2026'}
					</div>
					<div class="grid grid-cols-2 gap-2 text-xs text-purple-900/80 mt-2 font-mono">
						<div><strong>Chapter:</strong> {selectedAssertion.report_locator.chapter}</div>
						<div><strong>Section/Table:</strong> {selectedAssertion.report_locator.table}</div>
						<div><strong>Pages:</strong> {selectedAssertion.report_locator.pages.join(', ')}</div>
						<div><strong>Local Extract:</strong> DS001-LOCAL</div>
					</div>
				</div>

				<!-- Primary Report Claim Text -->
				<div>
					<h4 class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">
						Complete Committee Statement
					</h4>
					<blockquote class="text-sm text-slate-800 bg-slate-50 border-l-4 border-slate-400 p-3 italic leading-relaxed rounded-r">
						"{selectedAssertion.report_claim}"
					</blockquote>
				</div>

				<!-- Caveats & Context -->
				<div>
					<h4 class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">
						Methodology Caveats & Limitations
					</h4>
					<p class="text-xs text-slate-700 bg-amber-50/60 border border-amber-200/70 p-3 rounded leading-relaxed">
						{selectedAssertion.caveats}
					</p>
				</div>

				<!-- Linked Counter-Evidence / Corroboration -->
				<div>
					<h4 class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-3 flex items-center justify-between">
						<span>Corroborating & Qualifying Records</span>
						<span class="text-xs text-slate-400 font-mono">({activeEvidenceLinks.length} records)</span>
					</h4>

					<div class="space-y-3">
						{#each activeEvidenceLinks as ev}
							<div class="bg-white border border-slate-200 rounded-lg p-3.5 shadow-2xs space-y-2">
								<div class="flex items-center justify-between gap-2">
									<div class="flex items-center gap-1.5">
										<span class="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
											{ev.source_id}
										</span>
										<PlainBadge label={ev.evidence_label} />
									</div>
									<span class="text-xs font-mono capitalize px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">
										Relationship: {ev.relationship}
									</span>
								</div>
								<div class="text-xs font-bold text-slate-900">
									{ev.source_title}
								</div>
								<div class="text-xs text-slate-500 font-mono">
									Locator: {ev.source_locator} • Publisher: {ev.publisher}
								</div>
								<p class="text-xs text-slate-700 leading-relaxed pt-1">
									{ev.summary_finding}
								</p>
								<div class="text-2xs text-slate-500 italic bg-slate-50 p-2 rounded">
									<strong>Note:</strong> {ev.caveat_notes}
								</div>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- Drawer Footer -->
			<div class="pt-6 border-t border-slate-200 mt-6 flex justify-end">
				<button
					onclick={closeEvidenceDrawer}
					class="px-4 py-2 bg-slate-900 text-white rounded text-xs font-medium hover:bg-slate-800 transition"
				>
					Close Drawer
				</button>
			</div>
		</div>
	</div>
{/if}