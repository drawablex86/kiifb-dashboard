<script lang="ts">
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

<div class="space-y-6">
	<!-- Page Header Banner -->
	<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
			<div>
				<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-800 border border-rose-200 mb-2">
					<span>Pillar 1: Institutional Scrutiny</span>
					<span>•</span>
					<span>G.O.(P) No.80/2026/FIN</span>
					<span>•</span>
					<span>October 2026 Report</span>
				</div>
				<h2 class="text-2xl font-bold tracking-tight text-slate-900">
					Scrutiny of the Expert Review Committee
				</h2>
				<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
					Forensic examination of the Committee’s legal constitution, procedural and positional lapses by the Government, member dossiers exposing conflicts of interest, and the fiscal origins of the report.
				</p>
			</div>

			<!-- Quick Summary Counters -->
			<div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-left">
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Legal Category</div>
					<div class="text-sm font-bold text-slate-900">Executive Advisory</div>
					<div class="text-3xs text-rose-600">Non-Statutory (No Inquiry Act)</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Procedural Lapses</div>
					<div class="text-sm font-bold text-rose-700">4 Documented</div>
					<div class="text-3xs text-slate-500">ToR Bias & Conflicts</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3 col-span-2 sm:col-span-1">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Sub Judice Overreach</div>
					<div class="text-sm font-bold text-indigo-700">Article 293</div>
					<div class="text-3xs text-slate-500">SC Constitution Bench</div>
				</div>
			</div>
		</div>

		<!-- Navigation Tabs -->
		<div class="flex items-center space-x-2 border-b border-slate-200 mt-6 -mb-6 overflow-x-auto">
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
	</div>

	<!-- Cross-Link Perspective Callout -->
	<div class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200/80 rounded-lg p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs sm:text-sm">
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
			<div class="bg-rose-50/70 border border-rose-200 rounded-lg p-5 text-slate-800">
				<h3 class="text-base font-bold text-rose-900 mb-2 flex items-center gap-2">
					<span class="w-2.5 h-2.5 rounded-full bg-rose-600"></span>
					The Jurisdictional Paradox: Executive Fiat vs Statutory Law
				</h3>
				<p class="text-xs sm:text-sm text-rose-950 leading-relaxed">
					{legal.jurisdictional_paradox}
				</p>
			</div>

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
						{legal.mandate_summary} The Committee was tasked with reviewing KIIFB’s deviation from the 2014 SBI Caps model, resource mobilisation costs (including Masala Bonds), compliance with Constitutional provisions (Articles 266, 293, and Entry 37 of List I), regional distribution, establishment costs, and recommending a future restructuring path.
					</p>
				</div>
			</div>
		</div>

	<!-- TAB 2: PROCEDURAL & POSITIONAL LAPSES -->
	{:else if activeTab === 'lapses'}
		<div class="space-y-6">
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
									<span class="text-xs font-semibold uppercase text-slate-500 tracking-wide">
										{lapse.category}
									</span>
								</div>
								<span class="text-3xs font-mono uppercase px-2 py-0.5 rounded border {lapse.severity === 'critical' ? 'bg-rose-100 border-rose-300 text-rose-800' : 'bg-amber-100 border-amber-300 text-amber-800'}">
									Severity: {lapse.severity}
								</span>
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
			<!-- Explanatory note -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<h3 class="text-lg font-bold text-slate-900 mb-2">
					Member Dossiers & Documented Conflicts of Interest
				</h3>
				<p class="text-xs sm:text-sm text-slate-600 mb-6">
					Rigorous analysis of each panel member's career trajectory, institutional worldview, and specific positional conflicts—demonstrating how personal records grounded the conclusions of the report.
				</p>

				<!-- Members Grid -->
				<div class="space-y-6">
					{#each members as m}
						<div class="border border-slate-200 rounded-lg p-5 bg-white shadow-sm hover:border-slate-300 transition">
							<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-4">
								<div>
									<div class="flex items-center gap-2">
										<span class="font-mono text-xs font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded">{m.member_id}</span>
										<h4 class="text-lg font-bold text-slate-900">{m.name}</h4>
										<span class="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">{m.designation}</span>
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
				<div class="mt-8 pt-6 border-t border-slate-200">
					<h4 class="text-base font-bold text-slate-900 mb-3">
						The Advisory Secretariat & External Mentorship
					</h4>
					<p class="text-xs text-slate-600 mb-4">
						The Committee’s Foreword explicitly acknowledges external guidance from key architects of past restructuring committees:
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
						<span class="text-xs font-semibold px-2 py-0.5 bg-slate-100 rounded text-slate-800">{origins.nature_of_the_report.genre}</span>
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
						<span class="text-xs font-bold uppercase text-rose-800 bg-rose-100 px-2 py-0.5 rounded">Article 293(3) Net Borrowing Ceiling Penalty</span>
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
						<span class="text-xs font-bold uppercase text-indigo-900 bg-indigo-100 px-2 py-0.5 rounded">Supreme Court of India (Article 131)</span>
						<span class="text-xs font-semibold text-indigo-800">5-Judge Constitution Bench</span>
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
</div>
