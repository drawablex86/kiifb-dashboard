<script lang="ts">
	import PageIntro from '$lib/components/PageIntro.svelte';
	import NudgeCallout from '$lib/components/NudgeCallout.svelte';
	import PlainBadge from '$lib/components/PlainBadge.svelte';
	import GlossaryTerm from '$lib/components/GlossaryTerm.svelte';

	let { data } = $props();

	// Tab state
	let activeTab = $state<'evolution' | 'architects' | 'premise' | 'hypothecation' | 'dialectic'>('evolution');

	let evolution = $derived(data.statutoryEvolution || []);
	let architects = $derived(data.keyArchitects || []);
	let ftac = $derived(data.fiduciaryCommission || { distinguished_trustees: [] });
	let premise = $derived(data.theoreticalPremise || { core_economic_challenge: {}, fiscal_trap: {}, economic_rationale: { principles: [] } });
	let opposingPillars = $derived(data.opposingPillars || []);
	let federalism = $derived(data.federalismContext || {});
	let tables = $derived(data.financialTables || {});

	function formatCrore(val: number): string {
		return '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Cr';
	}
</script>

<svelte:head>
	<title>KIIFB Genesis & Theoretical Premise — Architecture, People & Capital Rationale</title>
</svelte:head>

<PageIntro
	title="Background: What is KIIFB"
	question="How was KIIFB created, what is its capital theory, and who built it?"
	lead="Comprehensive documentation of KIIFB's statutory evolution, key architects, independent fiduciary oversight by former national regulators, and the economic rationale of sub-national capital mobilisation. Five tabs: Statutory Evolution, Key People & FTAC, Theoretical Premise, Revenue Hypothecation, Opposing Pillars. Cross-links to /committee for the scrutiny layer."
	shows={[
		'Three phases of statutory evolution (1999–2016) with governing instruments and outcomes',
		'Key architects (Isaac, Abraham, Vijayan, Vinod Rai) with roles, contributions, and key quotes',
		'FTAC (Fiduciary Commission) — statutory shield under Section 6D with distinguished trustees',
		'Keynesian theoretical premise: structural dilemma, fiscal trap, economic principles (k > 1.5–2.0)',
		'Section 7 revenue hypothecation mechanics (MVT 10%→50% scaling, Petroleum Cess 100% ring-fenced)',
		'Opposing pillars matrix (shared with /committee) + federalism squeeze (Art.293, Union double standards, SC Constitution Bench)'
	]}
	doesnt={[
		'Project-level search & filters (see Projects)',
		'Portfolio funnel drill-down (see Where the Money Goes)',
		'Debt amortisation schedule (see Debt & Repayments)',
		'District map (see Districts & Map)',
		'Committee scrutiny: legality, lapses, member conflicts (see The Committee\'s Claims)'
	]}
/>

<NudgeCallout kind="situate" id="gen-start" heading="KIIFB-first, analyses-as-layers">
	This is the <strong>L1 KIIFB story</strong> — the subject matter. The October 2026 Committee is an <strong>analytical layer (L2)</strong> scrutinising KIIFB. Cross-links between both pages maintain the dialectic: the Committee's fiscal orthodoxy vs. KIIFB's Keynesian developmentalism.
</NudgeCallout>

<div class="space-y-6">
	<!-- Navigation Tabs -->
	<div class="flex items-center space-x-2 border-b border-slate-200 mb-6 overflow-x-auto">
		<button
			onclick={() => (activeTab = 'evolution')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'evolution' ? 'border-blue-600 text-blue-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			1. Statutory Evolution (1999–2016)
		</button>
		<button
			onclick={() => (activeTab = 'architects')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'architects' ? 'border-blue-600 text-blue-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			2. Key People & Fiduciary Commission
		</button>
		<button
			onclick={() => (activeTab = 'premise')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'premise' ? 'border-blue-600 text-blue-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			3. Theoretical Premise & Multiplier
		</button>
		<button
			onclick={() => (activeTab = 'hypothecation')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'hypothecation' ? 'border-blue-600 text-blue-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			4. Revenue Hypothecation (Section 7)
		</button>
		<button
			onclick={() => (activeTab = 'dialectic')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'dialectic' ? 'border-blue-600 text-blue-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			5. Opposing Pillars & Federal Squeeze
		</button>
	</div>

	<!-- Cross-Link Perspective Callout -->
	<div class="bg-gradient-to-r from-rose-50 to-amber-50 border border-rose-200/80 rounded-lg p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs sm:text-sm mb-6">
		<div>
			<span class="font-bold text-rose-900">Explore the Opposing Pillar:</span>
			<span class="text-rose-800 ml-1">Scrutinise the Review Committee's legality, procedural lapses, and member conflicts of interest.</span>
		</div>
		<a
			href="/committee"
			class="inline-flex items-center justify-center px-4 py-1.5 rounded-md bg-rose-600 text-white font-medium hover:bg-rose-700 transition shadow-sm text-xs whitespace-nowrap"
		>
			View Review Committee Scrutiny & Dossiers &rarr;
		</a>
	</div>

	<!-- TAB 1: STATUTORY EVOLUTION (1999 TO 2016) -->
	{#if activeTab === 'evolution'}
		<div class="space-y-6">
			<NudgeCallout kind="situate" id="gen-evolution" heading="From dormant vehicle to market-banking body corporate">
				Phase 1 (1999–2003): Kerala Act 4/2000 created KIIFB as a dormant vehicle under the Finance Department. Phase 2 (2014): SBI Caps advisory proposed market-banking model. Phase 3 (2016): Act 8/2016 established KIIFB as a body corporate with Section 7 hypothecation and Section 6D fiduciary commission.
			</NudgeCallout>

			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<h3 class="text-lg font-bold text-slate-900 mb-2">
					Three Phases of Statutory and Institutional Evolution
				</h3>
				<p class="text-xs sm:text-sm text-slate-600 mb-6">
					From a dormant vehicle in 1999 to a market-banking advisory proposal in 2014, and finally to a comprehensive statutory body corporate financing physical and social infrastructure in 2016.
				</p>

				<div class="space-y-6">
					{#each evolution as phase}
						<div class="border border-slate-200 rounded-lg p-5 bg-white shadow-sm hover:border-slate-300 transition">
							<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-3">
								<div class="flex items-center gap-2">
									<PlainBadge label="official_record" />
									<h4 class="text-base font-bold text-slate-900">{phase.phase_name}</h4>
								</div>
								<div class="text-xs font-semibold text-slate-500 bg-slate-50 px-2.5 py-1 rounded border border-slate-200/80">
									{phase.period} • {phase.political_administration.split('(')[0].trim()}
								</div>
							</div>

							<div class="text-xs text-slate-500 font-mono mb-3">
								<span class="font-bold text-slate-700">Legal Instrument:</span> {phase.governing_instrument}
							</div>

							<p class="text-xs sm:text-sm text-slate-700 leading-relaxed mb-3">
								<span class="font-semibold text-slate-900">Legislative Intent:</span> {phase.intent}
							</p>

							<p class="text-xs sm:text-sm text-slate-700 leading-relaxed mb-4">
								<span class="font-semibold text-slate-900">Historical Outcome:</span> {phase.outcome}
							</p>

							{#if phase.structural_limitation}
								<div class="p-3 bg-amber-50 rounded border border-amber-200 text-xs text-amber-950 font-medium">
									<span class="font-bold">Structural Limitation:</span> {phase.structural_limitation}
								</div>
							{/if}

							{#if phase.structural_breakthrough}
								<div class="p-3 bg-emerald-50 rounded border border-emerald-200 text-xs text-emerald-950 font-medium">
									<span class="font-bold">The 2016 Breakthrough:</span> {phase.structural_breakthrough}
								</div>
							{/if}
						</div>
					{/each}
				</div>
			</div>
		</div>

	<!-- TAB 2: KEY PEOPLE & FIDUCIARY COMMISSION -->
	{:else if activeTab === 'architects'}
		<div class="space-y-6">
			<NudgeCallout kind="situate" id="gen-architects" heading="Political, academic, and technocratic leadership">
				Thomas Isaac (academic architect), K.M. Abraham (implementation lead), Pinarayi Vijayan (political sponsor), Vinod Rai (fiduciary chair). The FTAC under former CAG Vinod Rai provides statutory independent oversight — a governance layer the Committee overlooked.
			</NudgeCallout>

			<!-- Key Architects Grid -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<h3 class="text-lg font-bold text-slate-900 mb-2">
					Key Architects of the KIIFB Architecture
				</h3>
				<p class="text-xs sm:text-sm text-slate-600 mb-6">
					The political, academic, and technocratic leadership that conceived, designed, and executed Kerala's off-budget infrastructure financing framework.
				</p>

				<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
					{#each architects as arc}
						<div class="border border-slate-200 rounded-lg p-5 bg-white shadow-sm flex flex-col justify-between hover:border-slate-300 transition">
							<div>
								<div class="flex items-center gap-2 mb-1">
									<PlainBadge label="official_record" />
									<h4 class="text-base font-bold text-slate-900">{arc.name}</h4>
								</div>
								<div class="text-xs font-semibold text-blue-700 mb-2">{arc.role}</div>
								<div class="text-2xs text-slate-500 mb-3">{arc.position_held}</div>
								<div class="text-xs text-slate-600 mb-3 bg-slate-50 p-2 rounded border border-slate-100">
									<span class="font-semibold text-slate-800">Background:</span> {arc.academic_background}
								</div>
								<div class="text-xs text-slate-700 leading-relaxed mb-4">
									<span class="font-semibold text-slate-900">Contribution:</span> {arc.contribution_to_kiifb}
								</div>
							</div>
							<div class="p-3 bg-blue-50/60 rounded border border-blue-100 text-2xs italic text-blue-950">
								&ldquo;{arc.key_quote}&rdquo;
							</div>
						</div>
					{/each}
				</div>
			</div>

			<!-- Fund Trustee and Advisory Commission (FTAC) -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 mb-4 border-b border-slate-100">
					<div>
						<PlainBadge label="official_record" />
						<h3 class="text-lg font-bold text-slate-900 mt-1">{ftac.commission_name}</h3>
					</div>
					<PlainBadge label="official_record" />
				</div>

				<p class="text-xs sm:text-sm text-slate-700 leading-relaxed mb-3">
					{ftac.statutory_mandate}
				</p>
				<p class="text-xs text-slate-500 mb-6">
					{ftac.institutional_significance}
				</p>

				<!-- Distinguished Trustees -->
				<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
					{#each ftac.distinguished_trustees as t}
						<div class="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
							<div class="font-bold text-slate-900 text-base">{t.name}</div>
							<div class="text-xs font-semibold text-indigo-700">{t.role}</div>
							<div class="text-xs text-slate-600">{t.background}</div>
							<div class="p-2.5 bg-white rounded border border-slate-200 text-3xs text-slate-700">
								<span class="font-semibold text-slate-900">Institutional Credibility:</span> {t.credibility_weight}
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>

	<!-- TAB 3: THEORETICAL PREMISE & MULTIPLIER -->
	{:else if activeTab === 'premise'}
		<div class="space-y-6">
			<NudgeCallout kind="interpret" id="gen-premise" heading="The Keynesian multiplier claim">
				KIIFB's model asserts k > 1.5–2.0 for public capital in Kerala — i.e., every ₹1 of infrastructure spending generates ₹1.5–2.0 of GDP. The Committee contests this as unmodelled for Kerala. The truth is a <PlainBadge label="data_gap" /> — no ex-post CGE model exists for Kerala's KIIFB capital.
			</NudgeCallout>

			<!-- Dilemma & Fiscal Trap -->
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
					<PlainBadge label="contested_interpretation" />
					<h4 class="text-base font-bold text-slate-900 mt-2 mb-2">{premise.core_economic_challenge.name}</h4>
					<p class="text-xs sm:text-sm text-slate-700 leading-relaxed">
						{premise.core_economic_challenge.description}
					</p>
				</div>
				<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
					<PlainBadge label="contested_interpretation" />
					<h4 class="text-base font-bold text-slate-900 mt-2 mb-2">{premise.fiscal_trap.name}</h4>
					<p class="text-xs sm:text-sm text-slate-700 leading-relaxed">
						{premise.fiscal_trap.description}
					</p>
				</div>
			</div>

			<!-- Economic Principles -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="mb-4 pb-2 border-b border-slate-100 flex items-center justify-between">
					<h3 class="text-lg font-bold text-slate-900">
						Economic Principles Underpinning KIIFB's Model
					</h3>
					<PlainBadge label="committee_finding" />
				</div>

				<div class="space-y-4">
					{#each premise.economic_rationale.principles as p}
						<div class="p-4 bg-slate-50 rounded-lg border border-slate-200/80 hover:border-slate-300 transition">
							<h4 class="text-sm font-bold text-slate-900 mb-1 flex items-center gap-2">
								<PlainBadge label="verified_outcome" />
								{p.principle_name}
							</h4>
							<p class="text-xs sm:text-sm text-slate-700 leading-relaxed">
								{p.explanation}
							</p>
						</div>
					{/each}
				</div>
			</div>
		</div>

	<!-- TAB 4: REVENUE HYPOTHECATION (SECTION 7) -->
	{:else if activeTab === 'hypothecation'}
		<div class="space-y-6">
			<NudgeCallout kind="situate" id="gen-hypothecation" heading="How the escrow works">
				Section 7 hypothecates Motor Vehicles Tax (scaling 10%→50% over 5 years) + Petroleum Cess (100% ring-fenced) to KIIFB. Total statutory transfers to June 2026: ₹24,764.64 Cr. State transfers met 99.4% of debt service (Table 3.2). This is the credit enhancement that enabled market borrowing.
			</NudgeCallout>

			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<h3 class="text-lg font-bold text-slate-900 mb-2">
					Section 7 Statutory Revenue Hypothecation Mechanics
				</h3>
				<p class="text-xs sm:text-sm text-slate-600 mb-6">
					How dedicating a statutory share of growing fuel and motor vehicle taxes created an escrowed, ring-fenced credit enhancement to service market borrowings.
				</p>

				<!-- Mechanism Cards -->
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
					<div class="p-5 bg-blue-50/50 rounded-lg border border-blue-200">
						<PlainBadge label="official_record" />
						<div class="text-base font-bold text-slate-900 mb-2">10% Scaling to 50% Statutory Share</div>
						<p class="text-xs sm:text-sm text-slate-700 leading-relaxed mb-3">
							Under Section 7(1) of the 2016 Act, 10% of MVT collected in the previous year was contributed in Year 1, increasing by 10% each year up to 50% in the fifth year.
						</p>
						<div class="font-mono text-xs font-bold text-blue-900 bg-white p-2 rounded border border-blue-100">
							Total MVT Transferred (up to June 2026): ₹19,404.52 Crore
						</div>
					</div>

					<div class="p-5 bg-indigo-50/50 rounded-lg border border-indigo-200">
						<PlainBadge label="official_record" />
						<div class="text-base font-bold text-slate-900 mb-2">100% Ring-Fenced Statutory Cess</div>
						<p class="text-xs sm:text-sm text-slate-700 leading-relaxed mb-3">
							Under Section 7(2), the entire cess levied on petroleum products (₹1/litre) was contributed directly to the Fund to service infrastructure liabilities.
						</p>
						<div class="font-mono text-xs font-bold text-indigo-900 bg-white p-2 rounded border border-indigo-100">
							Total Cess Transferred (up to June 2026): ₹5,038.04 Crore
						</div>
					</div>
				</div>

				<!-- Total Transfer vs Debt Servicing Callout -->
				<div class="p-4 bg-slate-50 rounded-lg border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs sm:text-sm">
					<div>
						<span class="font-bold text-slate-900">Total Statutory Transfers to KIIFB:</span>
						<span class="font-mono font-bold text-slate-900 text-base ml-2">₹24,764.64 Cr</span>
						<span class="text-slate-500 text-xs ml-1">(Includes ₹322.07 Cr Govt contributions)</span>
					</div>
					<div class="text-slate-600 text-xs">
						<span>Historical Debt Service Met:</span>
						<span class="font-bold text-slate-900 ml-1">99.4% from State Transfers</span>
					</div>
				</div>
			</div>
		</div>

	<!-- TAB 5: OPPOSING PILLARS & FEDERAL SQUEEZE -->
	{:else if activeTab === 'dialectic'}
		<div class="space-y-6">
			<!-- The Two Opposing Pillars Matrix -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="flex items-center justify-between gap-4 mb-4 pb-2 border-b border-slate-100">
					<div>
						<h3 class="text-lg font-bold text-slate-900">The Two Opposing Pillars: Ideological Confrontation Matrix</h3>
						<p class="text-xs text-slate-600 mt-0.5">
							Direct side-by-side contrast between the Review Committee's fiscal conservatism and KIIFB's sub-national Keynesian developmentalism.
						</p>
					</div>
				</div>

				<div class="overflow-x-auto">
					<table class="w-full text-left text-xs sm:text-sm border-collapse">
						<thead>
							<tr class="bg-slate-50 border-b border-slate-200 text-2xs uppercase tracking-wider text-slate-600">
								<th class="py-3 px-4 font-semibold w-1/4">Dimension</th>
								<th class="py-3 px-4 font-semibold w-3/8 text-rose-900 bg-rose-50/50">Pillar 1: Review Committee (Fiscal Orthodoxy)</th>
								<th class="py-3 px-4 font-semibold w-3/8 text-blue-900 bg-blue-50/50">Pillar 2: KIIFB Leadership (Keynesian Model)</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-slate-100">
							{#each opposingPillars as row}
								<tr class="hover:bg-slate-50/50 transition">
									<td class="py-3 px-4 font-bold text-slate-900 bg-slate-50/30 align-top">
										{row.dimension}
									</td>
									<td class="py-3 px-4 text-slate-700 bg-rose-50/20 align-top">
										<div class="font-bold text-rose-950 mb-1">{row.pillar_1_committee.title}</div>
										<div class="text-xs leading-relaxed">{row.pillar_1_committee.description}</div>
									</td>
									<td class="py-3 px-4 text-slate-700 bg-blue-50/20 align-top">
										<div class="font-bold text-blue-950 mb-1">{row.pillar_2_kiifb.title}</div>
										<div class="text-xs leading-relaxed">{row.pillar_2_kiifb.description}</div>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>

			<!-- Indian Federalism Squeeze Deep Dive -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm space-y-6">
				<h3 class="text-lg font-bold text-slate-900 pb-2 border-b border-slate-100">
					The Larger Indian Federalism Squeeze on Kerala
				</h3>

				<!-- Article 293 Deductions Card -->
				<div class="bg-slate-50 rounded-lg border border-slate-200 p-5">
					<div class="flex items-center justify-between mb-2">
						<PlainBadge label="contested_interpretation" />
						<span class="font-mono font-bold text-rose-700 text-base">{formatCrore(federalism.article_293_weaponisation?.total_deduction_crore || 25932.55)}</span>
					</div>
					<h4 class="text-base font-bold text-slate-900 mb-2">
						{federalism.article_293_weaponisation?.title}
					</h4>
					<p class="text-xs sm:text-sm text-slate-700 leading-relaxed mb-4">
						{federalism.article_293_weaponisation?.march_2022_policy_rupture}
					</p>

					<!-- Table of yearly deductions -->
					<div class="grid grid-cols-2 sm:grid-cols-5 gap-2 text-center text-xs">
						{#each federalism.article_293_weaponisation?.yearly_deductions_in_crores || [] as yr}
							<div class="bg-white p-2.5 rounded border border-slate-200">
								<div class="text-2xs text-slate-500 font-mono">{yr.year}</div>
								<div class="font-bold text-slate-900 mt-1">{formatCrore(yr.deduction_amount)}</div>
							</div>
						{/each}
					</div>
				</div>

				<!-- Union Off-Budget Double Standards -->
				<div class="border border-slate-200 rounded-lg p-5">
					<h4 class="text-base font-bold text-slate-900 mb-2">
						{federalism.union_double_standard?.title}
					</h4>
					<p class="text-xs sm:text-sm text-slate-600 mb-4">
						{federalism.union_double_standard?.description}
					</p>

					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						{#each federalism.union_double_standard?.central_off_budget_entities || [] as entity}
							<div class="p-3.5 bg-slate-50 rounded border border-slate-200/80 space-y-1">
								<div class="font-bold text-slate-900 text-sm">{entity.entity}</div>
								<div class="text-xs font-mono font-semibold text-indigo-700">{entity.borrowing_scale}</div>
								<div class="text-xs text-slate-600 leading-relaxed pt-1">{entity.servicing_mechanism}</div>
							</div>
						{/each}
					</div>
					<div class="mt-4 p-3 bg-amber-50 rounded border border-amber-200 text-xs text-amber-950 font-medium">
						{federalism.union_double_standard?.analytical_conclusion}
					</div>
				</div>

				<!-- Supreme Court Constitution Bench Case -->
				<div class="bg-indigo-50/50 rounded-lg border border-indigo-200 p-5">
					<div class="flex items-center justify-between mb-2">
						<PlainBadge label="official_record" />
						<PlainBadge label="committee_finding" />
					</div>
					<h4 class="text-base font-bold text-slate-900 mb-2">
						{federalism.supreme_court_constitution_bench?.title}
					</h4>
					<div class="text-xs font-mono text-slate-600 mb-3">{federalism.supreme_court_constitution_bench?.case_details}</div>
					<p class="text-xs sm:text-sm text-slate-700 mb-3">
						{federalism.supreme_court_constitution_bench?.significance}
					</p>
					<div class="space-y-1.5 text-xs text-slate-800 bg-white p-3 rounded border border-indigo-100">
						<div class="font-semibold text-indigo-900">Core Undecided Constitutional Questions:</div>
						{#each federalism.supreme_court_constitution_bench?.core_constitutional_questions || [] as q}
							<div class="flex items-start gap-2">
								<span class="text-indigo-600 font-bold">&bull;</span>
								<span>{q}</span>
							</div>
						{/each}
					</div>
				</div>
			</div>
		</div>
	{/if}

	<!-- Provenance banner -->
	<div class="bg-slate-100 border border-slate-200 rounded-lg p-4 text-xs text-slate-600 mt-6">
		<span class="font-bold text-slate-900">Provenance:</span> All datasets from DS001 (Committee Report Oct 2026) + KIIF Act legislative history + FTAC records + public official records. Cryptographic hashes in <code class="font-mono">data/manifest.json</code>. Unit tests in <code class="font-mono">tests/test_committee_and_genesis.py</code> (12 tests, 41 total). This page is the <strong>L1 KIIFB story</strong> — the opposing analytical layer (L2) is at <a href="/committee" class="underline">The Committee's Claims</a>.
	</div>
</div>