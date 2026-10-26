<script lang="ts">
	import PageIntro from '$lib/components/PageIntro.svelte';
	import NudgeCallout from '$lib/components/NudgeCallout.svelte';
	import PlainBadge from '$lib/components/PlainBadge.svelte';
	import GlossaryTerm from '$lib/components/GlossaryTerm.svelte';

	let { data } = $props();

	// Tab state
	let activeTab = $state<'legality' | 'lapses' | 'members' | 'origins' | 'dialectic'>('legality');

	let legal = $derived(data.legalConstitution);
	let lapses = $derived(data.proceduralLapses || []);
	let members = $derived(data.members || []);
	let advisors = $derived(data.advisoryApparatus?.key_advisors || []);
	let origins = $derived(data.originsAndTiming || { political_and_fiscal_timing: { factors: [] }, nature_of_the_report: {} });
	let opposingPillars = $derived(data.opposingPillars || []);
	let federalism = $derived(data.federalismContext || {});

	function formatCrore(val: number): string {
		return '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Cr';
	}
</script>

<svelte:head>
	<title>Scrutiny of the Review Committee — Legality, Lapses & Member Records</title>
</svelte:head>

<PageIntro
	title="The Committee's Claims"
	question="Was the October 2026 Expert Committee itself above board — and how do its findings hold up?"
	lead="Forensic examination of the Committee's legal constitution, procedural and positional lapses by the Government, member dossiers exposing conflicts of interest, and the fiscal origins of the report. Five tabs: Constitution & Legality, Procedural Lapses, Member Dossiers & Conflicts, Report Origins & Timing, Opposing Pillars & Federal Squeeze. Cross-links to /genesis for the opposing pillar."
	shows={[
		'Constituting order G.O.(P) No.80/2026/FIN — executive advisory, no statutory inquiry powers',
		'4 documented procedural lapses: ToR bias, sub judice overreach, appointment conflicts, assembly bypass',
		'5 member dossiers with career trajectories, positional biases, and specific conflicts (Tarun Bajaj MoF Art.293; Shyam Srinivasan Federal Bank KIFML equity)',
		'Report origins: July 2026 fiscal squeeze convergence, epistemic character as advisory opinion',
		'7-dimension opposing pillars matrix + federalism squeeze (Art.293 deductions, Union off-budget double standards, SC Constitution Bench)'
	]}
	doesnt={[
		'Project-level search & filters (see Projects)',
		'Portfolio funnel drill-down (see Where the Money Goes)',
		'Debt amortisation schedule (see Debt & Repayments)',
		'District map (see Districts & Map)',
		"KIIFB's own story: statutory evolution, architects, Keynesian premise (see Background: What is KIIFB)"
	]}
/>

<NudgeCallout kind="interpret" id="comm-start" heading="This is the scrutiny layer">
	This page treats the October 2026 Committee as an <strong>analytical layer (L2)</strong> — not the record base. Its findings are claims to be checked against the record. The "opposing pillar" (KIIFB's own architecture, Keynesian premise, architects) lives at <a href="/genesis" class="underline">Background: What is KIIFB</a>. Cross-links between both pages maintain the dialectic.
</NudgeCallout>

<div class="space-y-6">
	<!-- Navigation Tabs -->
	<div class="flex items-center space-x-2 border-b border-slate-200 mb-6 overflow-x-auto">
		<button
			onclick={() => (activeTab = 'legality')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'legality' ? 'border-rose-600 text-rose-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			1. Constitution & Legality
		</button>
		<button
			onclick={() => (activeTab = 'lapses')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'lapses' ? 'border-rose-600 text-rose-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			2. Procedural Lapses
		</button>
		<button
			onclick={() => (activeTab = 'members')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'members' ? 'border-rose-600 text-rose-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			3. Member Dossiers & Conflicts
		</button>
		<button
			onclick={() => (activeTab = 'origins')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'origins' ? 'border-rose-600 text-rose-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			4. Report Origins & Timing
		</button>
		<button
			onclick={() => (activeTab = 'dialectic')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'dialectic' ? 'border-rose-600 text-rose-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			5. Opposing Pillars & Federal Squeeze
		</button>
	</div>

	<!-- Cross-Link Perspective Callout -->
	<div class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200/80 rounded-lg p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs sm:text-sm mb-6">
		<div>
			<span class="font-bold text-blue-900">Explore the Opposing Pillar:</span>
			<span class="text-blue-800 ml-1">Understand the Keynesian theoretical premise, revenue hypothecation, and architects of KIIFB.</span>
		</div>
		<a
			href="/genesis"
			class="inline-flex items-center justify-center px-4 py-1.5 rounded-md bg-blue-600 text-white font-medium hover:bg-blue-700 transition shadow-sm text-xs whitespace-nowrap"
		>
			View KIIFB Genesis & Theoretical Architecture &rarr;
		</a>
	</div>

	<!-- TAB 1: CONSTITUTION & LEGAL STATUS -->
	{#if activeTab === 'legality'}
		<div class="space-y-6">
			<!-- Critical Legal Alert -->
			<NudgeCallout kind="interpret" id="comm-legality" heading="The Jurisdictional Paradox: Executive Fiat vs Statutory Law">
				{legal.jurisdictional_paradox}
			</NudgeCallout>

			<!-- Legal Order Details Card -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<h3 class="text-base font-bold text-slate-900 mb-4 pb-2 border-b border-slate-100">
					Constituting Instrument & Legal Mandate
				</h3>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
					<div class="p-4 bg-slate-50 rounded border border-slate-100 space-y-2">
						<div class="text-2xs text-slate-500 uppercase font-semibold">Government Order</div>
						<div class="font-mono font-bold text-slate-900 text-base">{legal.constituting_order}</div>
						<div class="text-slate-600"><span class="font-medium">Date of Notification:</span> {legal.order_date}</div>
						<div class="text-slate-600"><span class="font-medium">Issuing Authority:</span> {legal.issuing_authority}</div>
					</div>
					<div class="p-4 bg-slate-50 rounded border border-slate-100 space-y-2">
						<div class="text-2xs text-slate-500 uppercase font-semibold">Statutory Classification</div>
						<div class="font-bold text-slate-900 text-base">{legal.legal_status}</div>
						<div class="text-slate-600"><span class="font-medium">Inquiry Status:</span> {legal.statutory_inquiry_status}</div>
						<div class="text-rose-700 font-medium">Subpoena Powers: No • Evidentiary Immunity: None</div>
					</div>
				</div>

				<div class="mt-6 pt-4 border-t border-slate-100">
					<h4 class="text-xs uppercase font-semibold text-slate-500 mb-2">Executive Order Terms of Reference (ToR) Scope</h4>
					<p class="text-xs sm:text-sm text-slate-700 leading-relaxed">
						{legal.mandate_summary} The Committee was tasked with reviewing KIIFB's deviation from the 2014 SBI Caps model, resource mobilisation costs (including Masala Bonds), compliance with Constitutional provisions (Articles 266, 293, and Entry 37 of List I), regional distribution, establishment costs, and recommending a future restructuring path.
					</p>
				</div>
			</div>
		</div>

	<!-- TAB 2: PROCEDURAL & POSITIONAL LAPSES -->
	{:else if activeTab === 'lapses'}
		<div class="space-y-6">
			<NudgeCallout kind="situate" id="comm-lapses" heading="Four structural lapses">
				These are not minor procedural errors — they are structural choices by the Government that shaped the Committee's conclusions before it began work. Each lapse is sourced to an official record.
			</NudgeCallout>

			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<h3 class="text-lg font-bold text-slate-900 mb-2">
					Documented Procedural and Positional Lapses
				</h3>
				<p class="text-xs sm:text-sm text-slate-600 mb-6">
					Four major structural and procedural lapses committed by the Government in the constitution, scoping, and deployment of the Review Committee.
				</p>

				<div class="space-y-5">
					{#each lapses as lapse}
						<div class="border rounded-lg p-5 transition {lapse.severity === 'critical' ? 'border-rose-200 bg-rose-50/30' : 'border-amber-200 bg-amber-50/20'}">
							<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
								<div class="flex items-center gap-2">
									<span class="font-mono text-xs font-bold px-2 py-0.5 rounded {lapse.severity === 'critical' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'}">
										{lapse.lapse_id}
									</span>
									<PlainBadge label={lapse.category} />
								</div>
								<PlainBadge label={lapse.severity} />
							</div>

							<h4 class="text-base font-bold text-slate-900 mb-2">
								{lapse.title}
							</h4>
							<p class="text-xs sm:text-sm text-slate-700 leading-relaxed mb-3">
								{lapse.description}
							</p>

							<div class="bg-white/80 rounded border border-slate-200 p-3 text-xs space-y-1">
								<div class="text-rose-900 font-medium">
									<span class="font-bold">Constitutional / Institutional Implication:</span> {lapse.implication}
								</div>
								<div class="text-slate-500 text-3xs font-mono pt-1">
									Source: {lapse.official_record}
								</div>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>

	<!-- TAB 3: MEMBER DOSSIERS & CONFLICTS -->
	{:else if activeTab === 'members'}
		<div class="space-y-6">
			<NudgeCallout kind="situate" id="comm-members" heading="Positional bias is not personal bias">
				Each member's career trajectory and institutional worldview grounded the Committee's conclusions. Conflicts are documented from public records (MoF Art.293 deduction policy; Federal Bank KIFML equity in Table 5.6). This is forensic transparency, not ad hominem.
			</NudgeCallout>

			<!-- Members Grid -->
			<div class="space-y-6">
				{#each members as m}
					<div class="border border-slate-200 rounded-lg p-5 bg-white shadow-sm hover:border-slate-300 transition">
						<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-4">
							<div>
								<div class="flex items-center gap-2">
									<span class="font-mono text-xs font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded">{m.member_id}</span>
									<h4 class="text-lg font-bold text-slate-900">{m.name}</h4>
									<PlainBadge label="committee_finding" />
								</div>
								<div class="text-xs text-slate-500 mt-1">{m.service_cadre}</div>
							</div>
							<div class="text-2xs font-semibold uppercase tracking-wider text-slate-500 bg-slate-50 px-2.5 py-1 rounded border border-slate-200/80">
								Expertise: {m.primary_expertise.split(',')[0]}
							</div>
						</div>

						<!-- Career Background -->
						<div class="mb-4 text-xs sm:text-sm text-slate-700">
							<span class="font-semibold text-slate-900">Career Trajectory:</span> {m.career_background}
						</div>

						<!-- Positional Bias -->
						<div class="mb-4 text-xs sm:text-sm text-slate-700 bg-slate-50 p-3 rounded border border-slate-100">
							<span class="font-semibold text-slate-900">Documented Positional Bias:</span> {m.positional_bias}
						</div>

						<!-- Conflict of Interest Callout -->
						<div class="rounded-lg p-3.5 text-xs sm:text-sm {m.documented_conflict.includes('CONFLICT') ? 'bg-rose-50 border border-rose-200 text-rose-950' : 'bg-slate-50 border border-slate-200 text-slate-700'}">
							<span class="font-bold {m.documented_conflict.includes('CONFLICT') ? 'text-rose-800' : 'text-slate-800'}">Positional Record & Conflict Analysis:</span>
							<div class="mt-1 leading-relaxed">{m.documented_conflict}</div>
						</div>
					</div>
				{/each}
			</div>

			<!-- Advisory Apparatus Behind the Scenes -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm mt-6">
				<div class="mt-8 pt-6 border-t border-slate-200">
					<h4 class="text-base font-bold text-slate-900 mb-3">
						The Advisory Secretariat & External Mentorship
					</h4>
					<p class="text-xs text-slate-600 mb-4">
						The Committee's Foreword explicitly acknowledges external guidance from key architects of past restructuring committees:
					</p>

					<div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs sm:text-sm">
						{#each advisors as adv}
							<div class="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
								<div class="font-bold text-slate-900 text-base">{adv.name}</div>
								<div class="text-xs font-semibold text-indigo-700">{adv.role}</div>
								<div class="text-xs text-slate-600">{adv.background}</div>
								{#if adv.notable_context}
									<div class="p-2 bg-amber-50 border border-amber-200 rounded text-3xs text-amber-950 font-medium">
										{adv.notable_context}
									</div>
								{/if}
							</div>
						{/each}
					</div>
				</div>
			</div>
		</div>

	<!-- TAB 4: ORIGINS, TIMING & NATURE OF REPORT -->
	{:else if activeTab === 'origins'}
		<div class="space-y-6">
			<NudgeCallout kind="interpret" id="comm-origins" heading="Why July 2026?">
				The Committee was constituted in July 2026 amid a converging fiscal squeeze: Article 293 deductions mounting, Union off-budget double standards visible, and state elections approaching. The report's epistemic character is an advisory opinion — not a statutory inquiry finding.
			</NudgeCallout>

			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<h3 class="text-lg font-bold text-slate-900 mb-2">
					Origins, Political Timing & Nature of the Report
				</h3>
				<p class="text-xs sm:text-sm text-slate-600 mb-6">
					Why was the Committee constituted in July 2026, and what is the epistemic nature of its final document?
				</p>

				<!-- Timing Factors -->
				<div class="bg-indigo-50/50 border border-indigo-200 rounded-lg p-5 mb-6">
					<h4 class="text-sm font-bold text-indigo-900 mb-3 uppercase tracking-wider">
						The July–October 2026 Fiscal Squeeze Convergence
					</h4>
					<p class="text-xs sm:text-sm text-indigo-950 mb-3">
						{origins.political_and_fiscal_timing.context}
					</p>
					<ul class="space-y-2 text-xs sm:text-sm text-slate-800">
						{#each origins.political_and_fiscal_timing.factors as factor}
							<li class="flex items-start gap-2">
								<span class="text-indigo-600 font-bold">&bull;</span>
								<span>{factor}</span>
							</li>
						{/each}
					</ul>
				</div>

				<!-- Nature of the Report -->
				<div class="border border-slate-200 rounded-lg p-5 bg-white space-y-3">
					<div class="flex items-center justify-between">
						<span class="text-xs font-bold uppercase text-slate-500">Document Genre</span>
						<PlainBadge label="committee_finding" />
					</div>
					<h4 class="text-base font-bold text-slate-900">
						Epistemic Character & Political Utility
					</h4>
					<p class="text-xs sm:text-sm text-slate-700 leading-relaxed">
						{origins.nature_of_the_report.epistemic_character}
					</p>
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
		<span class="font-bold text-slate-900">Provenance:</span> All datasets from DS001 (Committee Report Oct 2026) + court records (SC Original Suit No. 1/2024) + public member records. Cryptographic hashes in <code class="font-mono">data/manifest.json</code>. Unit tests in <code class="font-mono">tests/test_committee_and_genesis.py</code> (12 tests, 41 total). This page is an <strong>analytical layer (L2)</strong> — the opposing pillar is at <a href="/genesis" class="underline">Background: What is KIIFB</a>.
	</div>
</div>