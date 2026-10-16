<script lang="ts">
	let { data } = $props();

	// Tabs for navigation
	let activeTab = $state<'completeness' | 'dimensions' | 'geography'>('completeness');

	// Shorthand derived state
	let dimensions = $derived(data.publicValue.dimensions);
	let completeness = $derived(data.publicValue.evidence_completeness_matrix);
	let dataGaps = $derived(data.publicValue.portfolio_data_gaps || []);
	let districts = $derived(data.publicValue.district_distribution || []);
	let departments = $derived(data.publicValue.department_distribution || []);

	// Severity badge styling helper
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

	function getStatusBadge(status: string) {
		switch (status) {
			case 'fully_documented':
				return 'bg-emerald-50 text-emerald-700 border-emerald-200';
			case 'partially_documented':
				return 'bg-amber-50 text-amber-700 border-amber-200';
			case 'data_gap':
				return 'bg-rose-50 text-rose-700 border-rose-200 font-semibold';
			default:
				return 'bg-slate-50 text-slate-700 border-slate-200';
		}
	}
</script>

<svelte:head>
	<title>Public Value & Evidence Completeness — KIIFB Accountability Dashboard</title>
</svelte:head>

<div class="space-y-6">
	<!-- Page Header Banner -->
	<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
			<div>
				<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 mb-2">
					<span>Milestone 4: Public Value & Outcomes</span>
					<span>•</span>
					<span>Evidence Hierarchy & Data Gaps</span>
				</div>
				<h2 class="text-2xl font-bold tracking-tight text-slate-900">
					Public Value, Evidence Completeness & Data Gaps
				</h2>
				<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
					Rigorous evaluation of public infrastructure value beyond narrow corporate debt servicing. Tracks measurable delivery vs. critical data gaps across 1,240 sanctioned investments.
				</p>
			</div>

			<!-- Summary Stat Counters -->
			<div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-left">
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Financial Coverage</div>
					<div class="text-lg font-bold text-emerald-700 tabular-nums">100%</div>
					<div class="text-3xs text-slate-500">Sanctions & Releases Audited</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Physical Milestones</div>
					<div class="text-lg font-bold text-amber-600 tabular-nums">42.5%</div>
					<div class="text-3xs text-slate-500">Internal PMAS / KTIMS Tracked</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3 col-span-2 sm:col-span-1">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Ex-Post Outcome Data</div>
					<div class="text-lg font-bold text-rose-600 tabular-nums">8.0%</div>
					<div class="text-3xs text-slate-500">92.0% Documented Data Gap</div>
				</div>
			</div>
		</div>

		<!-- Navigation Tabs -->
		<div class="flex items-center space-x-2 border-b border-slate-200 mt-6 -mb-6 overflow-x-auto">
			<button
				onclick={() => (activeTab = 'completeness')}
				class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'completeness' ? 'border-emerald-600 text-emerald-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
			>
				Evidence Completeness & Data Gaps (T041)
			</button>
			<button
				onclick={() => (activeTab = 'dimensions')}
				class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'dimensions' ? 'border-emerald-600 text-emerald-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
			>
				5-Dimensional Public Value (T040)
			</button>
			<button
				onclick={() => (activeTab = 'geography')}
				class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'geography' ? 'border-emerald-600 text-emerald-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
			>
				District & Sector Allocation (T042)
			</button>
		</div>
	</div>

	<!-- TAB 1: EVIDENCE COMPLETENESS & DATA GAPS (T041) -->
	{#if activeTab === 'completeness'}
		<div class="space-y-6">
			<!-- Civic Standard Notice -->
			<div class="bg-amber-50/60 border border-amber-200 rounded-lg p-4 text-xs sm:text-sm text-amber-900 flex items-start gap-3">
				<div class="font-bold text-base leading-none text-amber-600">!</div>
				<div>
					<span class="font-semibold">Civic Tech Audit Standard:</span> Missing evidence is not evidence of absence or zero benefit. In public finance, social infrastructure benefits (e.g. improved learning outcomes in upgraded schools, reduced mortality from diagnostic oncology) accrue over decades. Where official reports or portals lack operational monitoring, we classify them explicitly as <strong class="text-rose-700 bg-rose-50 px-1 py-0.5 rounded border border-rose-200">DATA GAP</strong> rather than zero.
				</div>
			</div>

			<!-- Completeness Ladder -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="flex items-center justify-between mb-4">
					<div>
						<h3 class="text-base font-bold text-slate-900">Portfolio Evidence Completeness Ladder</h3>
						<p class="text-xs text-slate-500">Measurement of documentation depth across the entire portfolio of 1,240 approved projects</p>
					</div>
					<span class="text-xs text-slate-400 font-mono">Source: KIIFB PMAS & Committee Chapter IV</span>
				</div>

				<div class="space-y-4">
					{#each completeness.metrics_tracked as metric}
						<div class="border border-slate-100 rounded-lg p-3.5 hover:bg-slate-50/50 transition">
							<div class="flex items-center justify-between text-xs sm:text-sm font-medium mb-1.5">
								<div class="flex items-center gap-2">
									<span class="text-slate-900 font-semibold">{metric.metric_name}</span>
									<span class="px-2 py-0.5 rounded text-2xs uppercase tracking-wider border {getStatusBadge(metric.status)}">
										{metric.status.replace('_', ' ')}
									</span>
								</div>
								<span class="font-bold tabular-nums text-slate-800">{metric.completeness_pct}%</span>
							</div>

							<!-- Visual Progress Bar -->
							<div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden mb-2">
								<div
									class="h-2.5 rounded-full transition-all {metric.completeness_pct >= 80 ? 'bg-emerald-500' : metric.completeness_pct >= 40 ? 'bg-amber-500' : 'bg-rose-500'}"
									style="width: {metric.completeness_pct}%"
								></div>
							</div>

							<div class="flex items-center justify-between text-2xs text-slate-500">
								<span>Primary Data Source: {metric.primary_source}</span>
								<span>Gestation / Gap: {(100 - metric.completeness_pct).toFixed(1)}%</span>
							</div>
						</div>
					{/each}
				</div>
			</div>

			<!-- Itemized Data Gap Register -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="mb-4">
					<h3 class="text-base font-bold text-slate-900">Itemized Portfolio Data Gap Register</h3>
					<p class="text-xs text-slate-500">Identified institutional, portal, and reporting gaps with measurable impact on public accountability</p>
				</div>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
					{#each dataGaps as gap}
						<div class="border border-slate-200 rounded-lg p-4 bg-slate-50/30 flex flex-col justify-between">
							<div>
								<div class="flex items-center justify-between mb-2">
									<span class="font-mono text-2xs font-bold text-slate-700 bg-slate-200 px-2 py-0.5 rounded">
										{gap.gap_id}
									</span>
									<span class="px-2 py-0.5 rounded text-2xs font-semibold uppercase tracking-wider border {getSeverityBadge(gap.severity)}">
										{gap.severity} severity
									</span>
								</div>
								<h4 class="text-sm font-bold text-slate-900 mb-1">{gap.dimension}</h4>
								<p class="text-xs text-slate-600 mb-2 leading-relaxed">{gap.description}</p>
								<div class="text-2xs text-slate-500 mb-3">
									<strong class="text-slate-700">Affected Scope:</strong> {gap.affected_records}
								</div>
							</div>

							<div class="pt-2 border-t border-slate-200 text-2xs text-emerald-800 bg-emerald-50/50 p-2 rounded border border-emerald-100">
								<span class="font-semibold">Dashboard Audit Remedy:</span> {gap.remedy}
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>

	<!-- TAB 2: 5-DIMENSIONAL PUBLIC VALUE (T040) -->
	{:else if activeTab === 'dimensions'}
		<div class="space-y-6">
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="mb-4">
					<h3 class="text-base font-bold text-slate-900">5-Dimensional Public-Value Evaluation Framework</h3>
					<p class="text-xs text-slate-500">Separates commercial financial return from macro-economic, social, and equity outcomes</p>
				</div>

				<div class="space-y-4">
					<!-- Financial Return -->
					<div class="border border-slate-200 rounded-lg p-5 bg-white">
						<div class="flex items-center justify-between mb-2">
							<h4 class="text-sm font-bold text-slate-900">1. Financial Return (Commercial Cash Receipts)</h4>
							<span class="px-2 py-0.5 rounded text-2xs uppercase tracking-wider border bg-emerald-50 text-emerald-700 border-emerald-200 font-medium">Documented</span>
						</div>
						<p class="text-xs text-slate-500 italic mb-2">{dimensions.financial_return.definition}</p>
						<p class="text-xs text-slate-700 mb-3 leading-relaxed">{dimensions.financial_return.committee_finding_summary}</p>
						<div class="text-2xs text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200">
							<strong class="text-slate-800">Caveat:</strong> {dimensions.financial_return.caveats}
						</div>
					</div>

					<!-- Economic Return -->
					<div class="border border-slate-200 rounded-lg p-5 bg-white">
						<div class="flex items-center justify-between mb-2">
							<h4 class="text-sm font-bold text-slate-900">2. Economic Return (Macroeconomic Impact & Productivity)</h4>
							<span class="px-2 py-0.5 rounded text-2xs uppercase tracking-wider border bg-rose-50 text-rose-700 border-rose-200 font-semibold">Data Gap / Unmodelled</span>
						</div>
						<p class="text-xs text-slate-500 italic mb-2">{dimensions.economic_return.definition}</p>
						<p class="text-xs text-slate-700 mb-3 leading-relaxed">{dimensions.economic_return.committee_finding_summary}</p>
						<div class="text-2xs text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200">
							<strong class="text-slate-800">Caveat:</strong> {dimensions.economic_return.caveats}
						</div>
					</div>

					<!-- Social Return -->
					<div class="border border-slate-200 rounded-lg p-5 bg-white">
						<div class="flex items-center justify-between mb-2">
							<h4 class="text-sm font-bold text-slate-900">3. Social Return (Education, Health & Human Capital)</h4>
							<span class="px-2 py-0.5 rounded text-2xs uppercase tracking-wider border bg-amber-50 text-amber-700 border-amber-200 font-medium">Documented Official Delivery</span>
						</div>
						<p class="text-xs text-slate-500 italic mb-2">{dimensions.social_return.definition}</p>
						<p class="text-xs text-slate-700 mb-2 leading-relaxed">{dimensions.social_return.committee_finding_summary}</p>
						
						<!-- Documented delivery details -->
						<div class="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-3">
							<div class="bg-blue-50/50 border border-blue-200 p-2.5 rounded text-2xs text-blue-900">
								<strong>General Education:</strong> {dimensions.social_return.documented_official_delivery.education}
							</div>
							<div class="bg-emerald-50/50 border border-emerald-200 p-2.5 rounded text-2xs text-emerald-900">
								<strong>Healthcare:</strong> {dimensions.social_return.documented_official_delivery.health}
							</div>
						</div>

						<div class="text-2xs text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200">
							<strong class="text-slate-800">Caveat:</strong> {dimensions.social_return.caveats}
						</div>
					</div>

					<!-- Distributional Return -->
					<div class="border border-slate-200 rounded-lg p-5 bg-white">
						<div class="flex items-center justify-between mb-2">
							<h4 class="text-sm font-bold text-slate-900">4. Distributional Return (Geographic & Social Equity)</h4>
							<span class="px-2 py-0.5 rounded text-2xs uppercase tracking-wider border bg-amber-50 text-amber-700 border-amber-200 font-medium">Skewness Identified</span>
						</div>
						<p class="text-xs text-slate-500 italic mb-2">{dimensions.distributional_return.definition}</p>
						<p class="text-xs text-slate-700 mb-3 leading-relaxed">{dimensions.distributional_return.committee_finding_summary}</p>
						<div class="text-2xs text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200">
							<strong class="text-slate-800">Caveat:</strong> {dimensions.distributional_return.caveats}
						</div>
					</div>

					<!-- Financing Suitability -->
					<div class="border border-slate-200 rounded-lg p-5 bg-white">
						<div class="flex items-center justify-between mb-2">
							<h4 class="text-sm font-bold text-slate-900">5. Financing Suitability (Instrument & Cash Flow Matching)</h4>
							<span class="px-2 py-0.5 rounded text-2xs uppercase tracking-wider border bg-rose-50 text-rose-700 border-rose-200 font-medium">Structural Mismatch</span>
						</div>
						<p class="text-xs text-slate-500 italic mb-2">{dimensions.financing_suitability.definition}</p>
						<p class="text-xs text-slate-700 mb-3 leading-relaxed">{dimensions.financing_suitability.committee_finding_summary}</p>
						<div class="text-2xs text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200">
							<strong class="text-slate-800">Caveat:</strong> {dimensions.financing_suitability.caveats}
						</div>
					</div>
				</div>
			</div>
		</div>

	<!-- TAB 3: DISTRICT & SECTOR ALLOCATION (T042) Placeholder (Expanded in T042) -->
	{:else if activeTab === 'geography'}
		<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
			<div class="mb-4">
				<h3 class="text-base font-bold text-slate-900">District & Sector Allocation</h3>
				<p class="text-xs text-slate-500">Comparative spatial and sectoral distributions (Category A Infrastructure & Category B Land Acquisition)</p>
			</div>

			<!-- District Table Preview -->
			<div class="overflow-x-auto border border-slate-200 rounded-lg">
				<table class="w-full text-xs text-left text-slate-700">
					<thead class="text-2xs text-slate-500 uppercase bg-slate-50 border-b border-slate-200">
						<tr>
							<th class="px-4 py-3">District / Region</th>
							<th class="px-4 py-3 text-right">Infra Outlay (₹ Cr)</th>
							<th class="px-4 py-3 text-right">Infra Share (%)</th>
							<th class="px-4 py-3 text-right">Land Acquisition (₹ Cr)</th>
							<th class="px-4 py-3 text-right">Total Approved (₹ Cr)</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-slate-200">
						{#each districts as dist}
							<tr class="hover:bg-slate-50/80 transition">
								<td class="px-4 py-2.5 font-medium text-slate-900">{dist.district}</td>
								<td class="px-4 py-2.5 text-right font-mono tabular-nums">₹{dist.infrastructure_outlay_cr.toLocaleString('en-IN', { minimumFractionDigits: 2 })} Cr</td>
								<td class="px-4 py-2.5 text-right font-mono tabular-nums">{dist.infrastructure_share_pct.toFixed(2)}%</td>
								<td class="px-4 py-2.5 text-right font-mono tabular-nums">
									{dist.land_acquisition_outlay_cr > 0 ? `₹${dist.land_acquisition_outlay_cr.toLocaleString('en-IN', { minimumFractionDigits: 2 })} Cr` : '—'}
								</td>
								<td class="px-4 py-2.5 text-right font-bold text-slate-900 font-mono tabular-nums">
									₹{dist.total_approved_cr.toLocaleString('en-IN', { minimumFractionDigits: 2 })} Cr
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	{/if}
</div>
