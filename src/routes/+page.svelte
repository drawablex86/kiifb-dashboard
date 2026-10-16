<script lang="ts">
	let { data } = $props();

	// State for citation popover / drawer
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

	// Helper to format currency numbers to Indian notation
	function formatIndianCrore(val: number): string {
		return '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Cr';
	}

	// Badge styling based on design-system.md
	function getEvidenceBadgeClass(label: string): string {
		switch (label) {
			case 'committee_finding':
				return 'bg-purple-50 text-purple-800 border-purple-200';
			case 'official_record':
				return 'bg-emerald-50 text-emerald-800 border-emerald-200';
			case 'verified_outcome':
				return 'bg-blue-50 text-blue-800 border-blue-200';
			case 'analytical_inference':
				return 'bg-green-50 text-green-800 border-green-200';
			case 'contested_interpretation':
				return 'bg-amber-50 text-amber-800 border-amber-200';
			case 'unverified_claim':
				return 'bg-orange-50 text-orange-800 border-orange-200';
			default:
				return 'bg-slate-100 text-slate-700 border-slate-200';
		}
	}
</script>

<svelte:head>
	<title>KIIFB Accountability Dashboard — Committee Assertions</title>
</svelte:head>

<div class="space-y-8">
	<!-- Hero / Overview Banner -->
	<section class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<div class="max-w-3xl">
			<div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-semibold bg-purple-50 text-purple-800 border border-purple-200 mb-3">
				<span>Milestone 1 Prototype</span>
				<span class="text-purple-300">•</span>
				<span>October 2026 Committee Baseline</span>
			</div>
			<h2 class="text-2xl font-bold tracking-tight text-slate-900 mb-2">
				Five Key Committee Assertions Under Investigation
			</h2>
			<p class="text-slate-600 text-sm leading-relaxed mb-4">
				The October 2026 Expert Committee Report (chaired by Sudha Pillai) presents major findings on Kerala's fiscal exposure, debt servicing, and project classifications. Below, each assertion is linked to verified source locators, primary figures, and corroborating/qualifying evidence.
			</p>
			<div class="flex flex-wrap items-center gap-4 text-xs text-slate-500 pt-2 border-t border-slate-100">
				<div>
					<span class="font-medium text-slate-700">Primary Source:</span> DS001 (Niyamasabha Combined PDF)
				</div>
				<div>
					<span class="font-medium text-slate-700">Local Verified Extract:</span> DS001-LOCAL
				</div>
				<div>
					<span class="font-medium text-slate-700">Total Assertions Tracked:</span> {data.assertions.length}
				</div>
			</div>
		</div>
	</section>

	<!-- Assertions Grid / List -->
	<section class="space-y-4">
		<h3 class="text-lg font-semibold text-slate-900 flex items-center justify-between">
			<span>Detailed Assertion Records</span>
			<span class="text-xs font-normal text-slate-500">Click any card to inspect full source citations</span>
		</h3>

		<div class="grid grid-cols-1 gap-5">
			{#each data.assertions as assertion}
				<div 
					class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm hover:border-slate-300 transition cursor-pointer relative group"
					onclick={() => openEvidenceDrawer(assertion)}
					role="button"
					tabindex="0"
					onkeydown={(e) => e.key === 'Enter' && openEvidenceDrawer(assertion)}
				>
					<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
						<div class="flex items-center gap-2">
							<span class="font-mono text-xs font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
								{assertion.assertion_id}
							</span>
							<span class="inline-block text-xs font-medium px-2.5 py-0.5 rounded border {getEvidenceBadgeClass(assertion.evidence_label)}">
								{assertion.evidence_label}
							</span>
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
						<span class="font-medium text-blue-600 group-hover:underline whitespace-nowrap ml-2">
							View Evidence & Citations →
						</span>
					</div>
				</div>
			{/each}
		</div>
	</section>
</div>

<!-- Slide-over Citation & Evidence Drawer -->
{#if selectedAssertion}
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<div 
		class="fixed inset-0 z-50 overflow-hidden bg-slate-900/50 backdrop-blur-xs flex justify-end transition-opacity"
		onclick={closeEvidenceDrawer}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
		onkeydown={(e) => e.key === 'Escape' && closeEvidenceDrawer()}
	>
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
		<div 
			class="w-full max-w-2xl bg-white h-full shadow-2xl p-6 overflow-y-auto flex flex-col justify-between"
			onclick={(e) => e.stopPropagation()}
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
							<span class="text-xs font-medium px-2.5 py-0.5 rounded border {getEvidenceBadgeClass(selectedAssertion.evidence_label)}">
								{selectedAssertion.evidence_label}
							</span>
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
										<span class="text-xs font-semibold px-2 py-0.5 rounded border {getEvidenceBadgeClass(ev.evidence_label)}">
											{ev.evidence_label}
										</span>
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
