<script lang="ts">
	let { data } = $props();

	// Tab state
	let activeTab = $state<'recommendations' | 'legal_register' | 'methodology'>('recommendations');

	let recommendations = $derived(data.recommendations || []);
	let legalIssues = $derived(data.legalIssues || []);
	let civicNote = $derived(data.civicStandardNote);

	// Status badge helper
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
</script>

<svelte:head>
	<title>Governance, Legal Issues & Recommendations — KIIFB Accountability Dashboard</title>
</svelte:head>

<div class="space-y-6">
	<!-- Page Header Banner -->
	<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
			<div>
				<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200 mb-2">
					<span>Milestone 5: Legal & Governance</span>
					<span>•</span>
					<span>Constitutional Issues & Recommendation Tracker</span>
				</div>
				<h2 class="text-2xl font-bold tracking-tight text-slate-900">
					Governance, Legal Issues & Recommendation Tracker
				</h2>
				<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
					Rigorous analysis of constitutional questions (Articles 266, 293, List I Entry 37) and status tracking of the 8 Expert Committee restructuring recommendations.
				</p>
			</div>

			<!-- Top Summary Counters -->
			<div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-left">
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Recommendations</div>
					<div class="text-lg font-bold text-slate-900 tabular-nums">8 Tracked</div>
					<div class="text-3xs text-slate-500">Chapter VI Restructuring</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Implemented</div>
					<div class="text-lg font-bold text-amber-700 tabular-nums">0 of 8</div>
					<div class="text-3xs text-slate-500">Advisory Proposals Only</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3 col-span-2 sm:col-span-1">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Sub Judice Issues</div>
					<div class="text-lg font-bold text-indigo-700 tabular-nums">Article 293</div>
					<div class="text-3xs text-slate-500">Supreme Court Constitution Bench</div>
				</div>
			</div>
		</div>

		<!-- Navigation Tabs -->
		<div class="flex items-center space-x-2 border-b border-slate-200 mt-6 -mb-6 overflow-x-auto">
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
		</div>
	</div>

	<!-- TAB 1: RECOMMENDATIONS TRACKER (T051) -->
	{#if activeTab === 'recommendations'}
		<div class="space-y-6">
			<!-- Critical Civic Notice -->
			<div class="bg-amber-50/70 border border-amber-200 rounded-lg p-4 text-xs sm:text-sm text-amber-950 flex items-start gap-3">
				<div class="font-bold text-base leading-none text-amber-700">!</div>
				<div>
					<span class="font-semibold">Civic Standard on Advisory Recommendations:</span> {civicNote}
				</div>
			</div>

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
			<div class="bg-blue-50/70 border border-blue-200 rounded-lg p-4 text-xs sm:text-sm text-blue-950 flex items-start gap-3">
				<div class="font-bold text-base leading-none text-blue-700">§</div>
				<div>
					<span class="font-semibold">Civic Standard on Judicial Separation:</span> An executive committee's interpretation is an advisory opinion, not a binding judicial ruling. In matters involving Article 293, Article 266, and Entry 37 of List I, the Committee itself noted that key questions have not been definitively adjudicated by the courts, or remain sub judice before a Constitution Bench of the Supreme Court of India.
				</div>
			</div>

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
									<span class="w-2 h-2 rounded-full bg-amber-500"></span>
									Committee & Audit Interpretation
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
									<span class="w-2 h-2 rounded-full bg-indigo-600"></span>
									Judicial Status & Court Findings
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
	{/if}
</div>
