<script lang="ts">
	import PageIntro from '$lib/components/PageIntro.svelte';
	import NudgeCallout from '$lib/components/NudgeCallout.svelte';
	import PlainBadge from '$lib/components/PlainBadge.svelte';
	import GlossaryTerm from '$lib/components/GlossaryTerm.svelte';

	let { data } = $props();

	// Tab state
	let activeTab = $state<'recommendations' | 'legal_register' | 'liability' | 'methodology'>('recommendations');

	let recommendations = $derived(data.recommendations || []);
	let legalIssues = $derived(data.legalIssues || []);
	let civicNote = $derived(data.civicStandardNote);
	let methodology = $derived(data.methodology || { sources: [], counting_units: [], discrepancies: [], limitations: [] });
	let contractorLiability = $derived(data.contractorLiability?.records || []);

	// Liability filter
	let liabilitySearch = $state('');
	let selectedLiabilityDistrict = $state('ALL');
	let liabilityDistricts = $derived([
		'ALL',
		...Array.from(new Set(contractorLiability.map((l: any) => l.district).filter(Boolean))).sort()
	]);
	let filteredLiability = $derived(
		contractorLiability.filter((l: any) => {
			const matchesSearch =
				liabilitySearch === '' ||
				l.work.toLowerCase().includes(liabilitySearch.toLowerCase()) ||
				l.contractor.toLowerCase().includes(liabilitySearch.toLowerCase()) ||
				l.division.toLowerCase().includes(liabilitySearch.toLowerCase());
			const matchesDist = selectedLiabilityDistrict === 'ALL' || l.district === selectedLiabilityDistrict;
			return matchesSearch && matchesDist;
		})
	);

	function getStatusBadge(status: string) {
		switch (status) {
			case 'implemented':
				return 'bg-emerald-50 text-emerald-800 border-emerald-200';
			case 'partially_budgeted':
				return 'bg-amber-50 text-amber-800 border-amber-200 font-semibold';
			case 'advisory_pending_action':
				return 'bg-slate-50 text-slate-700 border-slate-200';
			default:
				return 'bg-slate-50 text-slate-700 border-slate-200';
		}
	}

	function getSeverityBadge(severity: string) {
		switch (severity) {
			case 'critical':
				return 'bg-red-50 text-red-700 border-red-200';
			case 'high':
				return 'bg-amber-50 text-amber-700 border-amber-200';
			case 'medium':
				return 'bg-blue-50 text-blue-700 border-blue-200';
			default:
				return 'bg-slate-50 text-slate-700 border-slate-200';
		}
	}
</script>

<svelte:head>
	<title>Governance, Legal Issues & Recommendations — KIIFB Accountability Dashboard</title>
</svelte:head>

<PageIntro
	title="Recommendations & Law"
	question="What did the committee recommend, what are the legal positions, and how are they tracked?"
	lead="Rigorous analysis of constitutional questions (Articles 266, 293, List I Entry 37), tracking of the 8 Committee recommendations, contractor defect liability from Kerala Kanakku, and full source reproducibility methodology. Four tabs: Recommendations, Legal Register, Contractor Liability, Methodology."
	shows={[
		'8 restructuring recommendations tracked to target authority, legal instrument, and official action status',
		'Legal & constitutional register: Articles 266/293, Entry 37, SCSP/TSP — committee view vs. court status',
		'Contractor Defect Liability Period register from Kerala Kanakku (DS030)',
		'Methodology: primary sources with SHA-256, counting units protocol, discrepancy log (DISC-001–006), reproducibility commands'
	]}
	doesnt={[
		'Project-level search & filters (see Projects)',
		'Portfolio funnel drill-down (see Where the Money Goes)',
		'Debt amortisation schedule (see Debt & Repayments)',
		'District map (see Districts & Map)',
		'Committee scrutiny of legality/lapses/members (see The Committee\'s Claims)'
	]}
/>

<NudgeCallout kind="interpret" id="gov-start" heading="Advisory ≠ binding">
	The Committee's recommendations are <strong>advisory proposals</strong> — not statutes. 0 of 8 are fully implemented. The legal register separates committee/CAG advisory opinions from binding judicial proceedings (SC Constitution Bench referral pending). Contractor liability is from Kerala Kanakku (CC BY 4.0), not the Committee.
</NudgeCallout>

<div class="space-y-6">
	<!-- Navigation Tabs -->
	<div class="flex items-center space-x-2 border-b border-slate-200 mb-6 overflow-x-auto">
		<button
			onclick={() => (activeTab = 'recommendations')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'recommendations' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			Recommendation Tracker (T051)
		</button>
		<button
			onclick={() => (activeTab = 'legal_register')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'legal_register' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			Legal & Constitutional Register (T050)
		</button>
		<button
			onclick={() => (activeTab = 'liability')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'liability' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			Contractor Defect Liability (DS030)
		</button>
		<button
			onclick={() => (activeTab = 'methodology')}
			class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'methodology' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			Methodology & Discrepancies (T052)
		</button>
	</div>

	<!-- TAB 1: RECOMMENDATIONS TRACKER (T051) -->
	{#if activeTab === 'recommendations'}
		<div class="space-y-6">
			<!-- Critical Civic Notice -->
			<NudgeCallout kind="interpret" id="gov-recs" heading="Civic Standard on Advisory Recommendations">
				{civicNote}
			</NudgeCallout>

			<!-- Recommendations Grid / Table -->
			<div class="space-y-4">
				{#each recommendations as rec}
					<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm hover:border-slate-300 transition">
						<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-3">
							<div class="flex items-center gap-2">
								<span class="font-mono text-2xs font-bold text-slate-700 bg-slate-100 px-2.5 py-0.5 rounded border border-slate-200">
									{rec.rec_id}
								</span>
								<h3 class="text-sm font-bold text-slate-900">{rec.title}</h3>
							</div>
							<div>
								<span class="px-2.5 py-0.5 rounded-full text-2xs font-semibold uppercase tracking-wider border {getStatusBadge(rec.implementation_status)}">
									{rec.status_label}
								</span>
							</div>
						</div>

						<p class="text-xs text-slate-700 mb-3 leading-relaxed">
							{rec.summary}
						</p>

						<div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-2xs mb-3">
							<div class="bg-slate-50 p-2.5 rounded border border-slate-200">
								<strong class="text-slate-800">Target Authority:</strong>
								<span class="text-slate-600 block mt-0.5">{rec.target_entity}</span>
							</div>
							<div class="bg-slate-50 p-2.5 rounded border border-slate-200">
								<strong class="text-slate-800">Required Legal Instrument:</strong>
								<span class="text-slate-600 block mt-0.5">{rec.required_instrument}</span>
							</div>
						</div>

						<div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-2xs">
							<div class="bg-red-50/40 p-2.5 rounded border border-red-100 text-red-900">
								<strong>Official Action Evidence:</strong>
								<span class="block mt-0.5 text-slate-700">{rec.official_evidence}</span>
							</div>
							<div class="bg-emerald-50/40 p-2.5 rounded border border-emerald-100 text-emerald-950">
								<strong>Structural Impact If Enacted:</strong>
								<span class="block mt-0.5 text-slate-700">{rec.impact_if_implemented}</span>
							</div>
						</div>

						<div class="mt-3 pt-2 border-t border-slate-100 text-3xs text-slate-400 font-mono flex justify-between">
							<span>Source Citation: {rec.report_reference}</span>
							<span>Audit Standard: Verified Official Actions Only</span>
						</div>
					</div>
				{/each}
			</div>
		</div>

	<!-- TAB 2: LEGAL & CONSTITUTIONAL REGISTER (T050) -->
	{:else if activeTab === 'legal_register'}
		<div class="space-y-6">
			<!-- Civic Alert on Court Separation -->
			<NudgeCallout kind="interpret" id="gov-legal" heading="Judicial separation: advisory ≠ binding">
				An executive committee's interpretation is an advisory opinion, not a binding judicial ruling. In matters involving Article 293, Article 266, and Entry 37 of List I, the Committee itself noted that key questions have not been definitively adjudicated by the courts, or remain sub judice before a Constitution Bench of the Supreme Court of India.
			</NudgeCallout>

			<!-- Legal Issues Cards -->
			<div class="space-y-5">
				{#each legalIssues as issue}
					<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
						<div class="flex flex-col sm:flex-row sm:items-start justify-between gap-2 border-b border-slate-100 pb-3 mb-4">
							<div>
								<div class="flex items-center gap-2 mb-1">
									<span class="font-mono text-2xs font-bold text-slate-800 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
										{issue.issue_id}
									</span>
									<h3 class="text-base font-bold text-slate-900">{issue.title}</h3>
								</div>
								<div class="flex flex-wrap gap-1.5 text-3xs font-mono text-slate-600">
									{#each issue.provisions as prov}
										<span class="bg-slate-100 px-2 py-0.5 rounded border border-slate-200">{prov}</span>
									{/each}
								</div>
							</div>
							<div class="text-left sm:text-right">
								<span class="px-2.5 py-1 rounded text-2xs font-semibold uppercase tracking-wider bg-indigo-50 text-indigo-800 border border-indigo-200 block sm:inline-block">
									{issue.judicial_proceedings.binding_status.split(';')[0]}
								</span>
							</div>
						</div>

						<!-- Two Column Breakdown: Committee View vs Court Adjudication -->
						<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs mb-4">
							<!-- Left Column: Committee & CAG Interpretation -->
							<div class="border border-slate-200 rounded-lg p-4 bg-slate-50/40">
								<h4 class="text-2xs uppercase font-bold text-slate-700 tracking-wider mb-2 flex items-center gap-1.5">
									<PlainBadge label="committee_finding" />
									<span>Committee & Audit Interpretation</span>
								</h4>
								<p class="text-slate-700 mb-3 leading-relaxed">
									{issue.committee_interpretation}
								</p>
								<div class="text-2xs text-slate-600 border-t border-slate-200 pt-2 space-y-1">
									<div><strong class="text-slate-800">Executive Action:</strong> {issue.executive_action}</div>
									<div><strong class="text-slate-800">CAG Audit View:</strong> {issue.cag_audit_view}</div>
								</div>
							</div>

							<!-- Right Column: Judicial Status & Court Proceedings -->
							<div class="border border-indigo-200 rounded-lg p-4 bg-indigo-50/20">
								<h4 class="text-2xs uppercase font-bold text-indigo-900 tracking-wider mb-2 flex items-center gap-1.5">
									<PlainBadge label="official_record" />
									<span>Judicial Status & Court Findings</span>
								</h4>
								<div class="text-2xs font-semibold text-indigo-800 mb-1">
									{issue.judicial_proceedings.forum}: {issue.judicial_proceedings.case_citation}
								</div>
								<p class="text-slate-700 mb-3 leading-relaxed">
									{issue.judicial_proceedings.adjudication_summary}
								</p>
								<div class="border-t border-indigo-100 pt-2 text-2xs text-indigo-950 bg-indigo-50/50 p-2 rounded">
									<strong>Advisory vs. Binding Court Distinction:</strong>
									<span class="block mt-0.5 text-slate-700">
										{issue.judicial_proceedings.committee_vs_court_distinction}
									</span>
								</div>
							</div>
						</div>

						<div class="text-2xs text-slate-500 bg-slate-50 p-2 rounded border border-slate-100 flex items-center justify-between">
							<span>Subject: {issue.statutory_subject}</span>
							<span class="font-mono">Evidence Standard: Strict Legal Provenance</span>
						</div>
					</div>
				{/each}
			</div>
		</div>

	<!-- TAB 3: CONTRACTOR DEFECT LIABILITY (DS030 via Kerala Kanakku) -->
	{:else if activeTab === 'liability'}
		<div class="space-y-6">
			<!-- Banner -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
					<div>
						<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 mb-2">
							<span>Source: Kerala Kanakku (DS030)</span>
							<span>•</span>
							<span>Kerala PWD Defect Liability Period Register</span>
						</div>
						<h3 class="text-xl font-bold tracking-tight text-slate-900">
							Contractor Defect Liability Period (DLP) Register
						</h3>
						<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
							For finished public works, contractors are legally required to repair any defects at their own cost during the guarantee period. Tracked directly from PWD office records and compiled by Kerala Kanakku under CC BY 4.0.
						</p>
					</div>
					<div class="flex gap-3 text-left">
						<div class="bg-slate-50 border border-slate-200/80 rounded p-3 min-w-[120px]">
							<div class="text-2xs text-slate-500 uppercase font-semibold">Active Works</div>
							<div class="text-lg font-bold text-slate-900 tabular-nums">{contractorLiability.length.toLocaleString('en-IN')}</div>
							<div class="text-3xs text-slate-400">Under Liability</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Filters -->
			<div class="bg-white rounded-lg border border-slate-200 p-4 shadow-sm flex flex-col sm:flex-row gap-3">
				<div class="flex-1">
					<label for="lsearch" class="block text-2xs font-semibold uppercase text-slate-500 mb-1">Search Work, Contractor, Division</label>
					<input 
						id="lsearch"
						type="text"
						bind:value={liabilitySearch}
						placeholder="Search road, bridge, contractor name..."
						class="w-full text-xs px-3 py-2 border border-slate-300 rounded focus:ring-1 focus:ring-slate-900 focus:outline-none"
					/>
				</div>
				<div class="sm:w-64">
					<label for="ldist" class="block text-2xs font-semibold uppercase text-slate-500 mb-1">Office District</label>
					<select 
						id="ldist"
						bind:value={selectedLiabilityDistrict}
						class="w-full text-xs px-3 py-2 border border-slate-300 rounded focus:ring-1 focus:ring-slate-900 focus:outline-none bg-white"
					>
						{#each liabilityDistricts as dist}
							<option value={dist}>{dist}</option>
						{/each}
					</select>
				</div>
			</div>

			<!-- Liability Table -->
			<div class="bg-white rounded-lg border border-slate-200 overflow-hidden shadow-sm">
				<div class="overflow-x-auto">
					<table class="w-full text-left text-xs text-slate-700">
						<thead class="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase text-2xs tracking-wider">
							<tr>
								<th class="px-4 py-3">Work Name & Division</th>
								<th class="px-4 py-3">Contractor</th>
								<th class="px-4 py-3">Office District</th>
								<th class="px-4 py-3 text-right">Agreed Outlay</th>
								<th class="px-4 py-3 text-center">Liability Period</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-slate-100">
							{#if filteredLiability.length === 0}
								<tr>
									<td colspan="5" class="text-center py-8 text-slate-400">No matching liability records found.</td>
								</tr>
							{:else}
								{#each filteredLiability.slice(0, 50) as item}
									<tr class="hover:bg-slate-50/80 transition">
										<td class="px-4 py-3 max-w-md">
											<div class="font-semibold text-slate-900 leading-snug">{item.work}</div>
											<div class="text-2xs text-slate-500 mt-0.5">
												{item.wing} · {item.division}{item.subdivision ? ` · ${item.subdivision}` : ''}
											</div>
										</td>
										<td class="px-4 py-3 font-medium text-slate-800 max-w-xs truncate">
											{item.contractor}
										</td>
										<td class="px-4 py-3">
											<span class="inline-block px-2 py-0.5 rounded text-2xs font-medium bg-slate-100 text-slate-800 border border-slate-200">
												{item.district}
											</span>
										</td>
										<td class="px-4 py-3 text-right font-mono tabular-nums">
											{#if item.agreed_amount_inr > 0}
												₹{(item.agreed_amount_inr / 10000000).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} Cr
											{:else}
												—
											{/if}
										</td>
										<td class="px-4 py-3 text-center font-mono text-2xs">
											<div class="text-slate-900 font-semibold">{item.liability_ends}</div>
											<div class="text-3xs text-slate-400">Starts: {item.liability_starts}</div>
										</td>
									</tr>
								{/each}
							{/if}
						</tbody>
					</table>
				</div>
				{#if filteredLiability.length > 50}
					<div class="bg-slate-50 px-4 py-3 border-t border-slate-200 text-2xs text-slate-500 text-center font-medium">
						Showing first 50 of {filteredLiability.length.toLocaleString('en-IN')} matching liability works. Filter by district or search to narrow down.
					</div>
				{/if}
			</div>
		</div>

	<!-- TAB 4: METHODOLOGY & DISCREPANCIES (T052) -->
	{:else if activeTab === 'methodology'}
		<div class="space-y-6">
			<!-- Provenance & Sources Table -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="mb-4">
					<h3 class="text-base font-bold text-slate-900">Primary Data Sources & Archive Integrity</h3>
					<p class="text-xs text-slate-500">Official custodians, dates of extraction, and SHA-256 integrity hashes</p>
				</div>

				<div class="overflow-x-auto border border-slate-200 rounded-lg">
					<table class="w-full text-xs text-left text-slate-700">
						<thead class="text-2xs text-slate-500 uppercase bg-slate-50 border-b border-slate-200">
							<tr>
								<th class="px-4 py-3">Source ID</th>
								<th class="px-4 py-3">Source Name</th>
								<th class="px-4 py-3">Custodian</th>
								<th class="px-4 py-3 text-center">As-Of Date</th>
								<th class="px-4 py-3">Coverage Scope</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-slate-200">
							{#each methodology.sources as src}
								<tr class="hover:bg-slate-50 transition">
									<td class="px-4 py-2.5 font-mono font-bold text-slate-900">{src.source_id}</td>
									<td class="px-4 py-2.5">
										<div class="font-semibold text-slate-900">{src.name}</div>
										<div class="text-3xs text-slate-400 font-mono mt-0.5 truncate max-w-sm">{src.local_path}</div>
									</td>
									<td class="px-4 py-2.5 text-slate-600">{src.custodian}</td>
									<td class="px-4 py-2.5 text-center font-mono tabular-nums">{src.as_of_date}</td>
									<td class="px-4 py-2.5 text-slate-600 text-2xs">{src.coverage}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>

			<!-- Counting Units Protocol -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="mb-4">
					<h3 class="text-base font-bold text-slate-900">Counting Units & Reconciliation Protocol</h3>
					<p class="text-xs text-slate-500">Resolving the structural mismatch between umbrella project sanctions and physical institutions</p>
				</div>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					{#each methodology.counting_units as unit}
						<div class="border border-slate-200 rounded-lg p-4 bg-slate-50/50">
							<div class="flex items-center justify-between mb-2">
								<span class="font-mono text-xs font-bold text-slate-900 bg-white px-2.5 py-0.5 rounded border border-slate-200">
									{unit.unit}
								</span>
								<span class="text-xs font-bold text-indigo-700 tabular-nums">
									{unit.count} records
								</span>
							</div>
							<div class="text-2xs text-slate-500 mb-2">Dataset: <strong>{unit.dataset}</strong></div>
							<p class="text-xs text-slate-700 leading-relaxed">{unit.definition}</p>
						</div>
					{/each}
				</div>
			</div>

			<!-- Documented Discrepancy Log -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="mb-4">
					<h3 class="text-base font-bold text-slate-900">Itemized Source Discrepancy Log</h3>
					<p class="text-xs text-slate-500">Exact arithmetic, reporting, and spatial discrepancies reconciled and documented across official records</p>
				</div>

				<div class="space-y-4">
					{#each methodology.discrepancies as disc}
						<div class="border border-slate-200 rounded-lg p-4 bg-white hover:border-slate-300 transition">
							<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-2 mb-2">
								<div class="flex items-center gap-2">
									<span class="font-mono text-2xs font-bold text-slate-700 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
										{disc.discrepancy_id}
									</span>
									<h4 class="text-sm font-bold text-slate-900">{disc.title}</h4>
								</div>
								<div class="flex items-center gap-2">
									<PlainBadge label={disc.severity} kind="flag" />
									<span class="text-2xs text-slate-400 font-mono">{disc.source_location}</span>
								</div>
							</div>

							<p class="text-xs text-slate-700 mb-2">{disc.description}</p>
							<div class="bg-slate-50 p-2.5 rounded border border-slate-200 text-2xs text-slate-800 font-mono mb-2">
								<strong>Mathematical Check:</strong> {disc.mathematical_reconciliation}
							</div>
							<div class="text-2xs text-emerald-800 bg-emerald-50/50 p-2 rounded border border-emerald-100">
								<strong>Dashboard Handling:</strong> {disc.dashboard_treatment}
							</div>
						</div>
					{/each}
				</div>
			</div>

			<!-- Limitations and Caveats -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="mb-4">
					<h3 class="text-base font-bold text-slate-900">Data Limitations & Interpretive Caveats</h3>
					<p class="text-xs text-slate-500">Methodological caveats preserving analytical neutrality and civic rigor</p>
				</div>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					{#each methodology.limitations as lim}
						<div class="border border-slate-200 rounded-lg p-4 bg-slate-50/30">
							<div class="font-mono text-2xs font-bold text-slate-500 mb-1">{lim.id}</div>
							<h4 class="text-xs font-bold text-slate-900 mb-1">{lim.title}</h4>
							<p class="text-xs text-slate-600 leading-relaxed">{lim.description}</p>
						</div>
					{/each}
				</div>
			</div>

			<!-- Reproducibility Guide -->
			<div class="bg-slate-900 text-slate-100 rounded-lg p-6 shadow-sm">
				<div class="flex items-center gap-2 mb-2">
					<span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
					<h3 class="text-sm font-bold text-white tracking-wide uppercase">Open Civic Reproducibility Standard</h3>
				</div>
				<p class="text-xs text-slate-300 mb-4">
					Any citizen or independent researcher can reproduce every calculation and verify all tables directly from the command line:
				</p>
				<div class="bg-slate-950 p-4 rounded-lg font-mono text-2xs text-emerald-400 space-y-1.5 overflow-x-auto border border-slate-800">
					<div><span class="text-slate-500"># 1. Run all 23 mathematical reconciliation & legal tests:</span></div>
					<div>python3 -m unittest discover tests</div>
					<div class="pt-2"><span class="text-slate-500"># 2. Check TypeScript and Svelte accessibility diagnostics:</span></div>
					<div>npm run check</div>
					<div class="pt-2"><span class="text-slate-500"># 3. Build optimized production bundle:</span></div>
					<div>npm run build</div>
				</div>
			</div>
		</div>
	{/if}

	<!-- Provenance banner -->
	<div class="bg-slate-100 border border-slate-200 rounded-lg p-4 text-xs text-slate-600 mt-6">
		<span class="font-bold text-slate-900">Provenance:</span> Recommendations from DS001 Ch-VI; Legal issues from DS001 Ch-III/V + court records (SC Original Suit No. 1/2024); Liability from DS030 (CC BY 4.0). All sources in <code class="font-mono">data/manifest.json</code>. Reproducibility: <code class="font-mono">python3 -m unittest discover tests</code> + <code class="font-mono">npm run check</code> + <code class="font-mono">npm run build</code>.
	</div>
</div>