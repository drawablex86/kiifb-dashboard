<script lang="ts">
	import SankeyFlow from '$lib/components/SankeyFlow.svelte';
	import CompletionTrajectoryOverlay from '$lib/components/CompletionTrajectoryOverlay.svelte';

	let { data } = $props();

	// Active tab inside Financials view
	let activeTab = $state<'debt_profile' | 'land_pool' | 'amortisation' | 'transfers' | 'deployment_flow'>('debt_profile');

	// Tables shorthand
	let t3 = $derived(data.tables.table_3_3_aggregate_borrowing);
	let t4 = $derived(data.tables.table_3_4_bank_loans);
	let t5 = $derived(data.tables.table_3_5_institution_loans);
	let t7 = $derived(data.tables.table_3_7_bse_bonds);
	let t11 = $derived(data.tables.table_3_11_space_deduction);
	let t45 = $derived(data.tables.table_4_5_land_acquisition);
	let t61 = $derived(data.tables.table_6_1_debt_servicing_schedule);
	let t_req = $derived(data.tables.table_6_2_and_3_completion_requirements);
	let t63 = $derived(t_req);
	let t31 = $derived(data.tables.table_3_1_transfers);
	let t32 = $derived(data.tables.table_3_2_servicing_ratio);

	function formatCrore(val: number | null | undefined): string {
		if (val === null || val === undefined) return '—';
		return '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Cr';
	}
</script>

<svelte:head>
	<title>Financial Liabilities & Baseline Model — KIIFB Accountability Dashboard</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header / Key Totals Banner -->
	<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
			<div>
				<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-50 text-purple-800 border border-purple-200 mb-2">
					<span>Milestone 3 Baseline</span>
					<span>•</span>
					<span>Committee Report Tables (Audited)</span>
				</div>
				<h2 class="text-2xl font-bold tracking-tight text-slate-900">
					Financial Liabilities & Future Obligations Baseline
				</h2>
				<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
					Audited extraction and reconciliation of KIIFB's borrowing position, bank loans, listed bonds, land acquisition commitments, and scheduled debt service up to 2041-42.
				</p>
			</div>

			<!-- Top Summary Stat Cards -->
			<div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-left">
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Outstanding Debt (Stock)</div>
					<div class="text-lg font-bold text-slate-900 tabular-nums">₹31,681.15 Cr</div>
					<div class="text-3xs text-slate-500">As of 30 June 2026 (Table 3.3)</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Borrowing Space Deducted</div>
					<div class="text-lg font-bold text-amber-800 tabular-nums">₹25,932.55 Cr</div>
					<div class="text-3xs text-slate-500">Article 293(3) (Table 3.11)</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3 col-span-2 sm:col-span-1">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Total Scheduled Debt Service</div>
					<div class="text-lg font-bold text-purple-900 tabular-nums">₹47,532.54 Cr</div>
					<div class="text-3xs text-slate-500">Principal + Interest to 2041-42</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Navigation Tabs -->
	<div class="flex border-b border-slate-200 bg-white rounded-t-lg px-4 pt-2 gap-2 text-xs font-medium">
		<button 
			onclick={() => activeTab = 'debt_profile'} 
			class="px-4 py-2.5 border-b-2 font-semibold transition cursor-pointer {activeTab === 'debt_profile' ? 'border-slate-900 text-slate-900' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			Debt Structure & Lenders
		</button>
		<button 
			onclick={() => activeTab = 'land_pool'} 
			class="px-4 py-2.5 border-b-2 font-semibold transition cursor-pointer {activeTab === 'land_pool' ? 'border-slate-900 text-slate-900' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			Land Acquisition Liabilities (Table 4.5)
		</button>
		<button 
			onclick={() => activeTab = 'amortisation'} 
			class="px-4 py-2.5 border-b-2 font-semibold transition cursor-pointer {activeTab === 'amortisation' ? 'border-slate-900 text-slate-900' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			Debt Servicing Schedule to 2041-42 (Table 6.1)
		</button>
		<button 
			onclick={() => activeTab = 'transfers'} 
			class="px-4 py-2.5 border-b-2 font-semibold transition cursor-pointer {activeTab === 'transfers' ? 'border-slate-900 text-slate-900' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			State Budget Transfers (99.4% Ratio)
		</button>
		<button 
			onclick={() => activeTab = 'deployment_flow'} 
			class="px-4 py-2.5 border-b-2 font-semibold transition cursor-pointer {activeTab === 'deployment_flow' ? 'border-slate-900 text-slate-900' : 'border-transparent text-slate-500 hover:text-slate-800'}"
		>
			Deployment Flow (Sankey)
		</button>
	</div>

	<!-- Tab 1: Debt Structure & Lenders -->
	{#if activeTab === 'debt_profile'}
		<div class="space-y-6">
			<!-- Aggregate Borrowing Reconciliation -->
			<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
				<h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider mb-3">
					Table 3.3 — Aggregate Borrowing Reconciliation (as of 30 June 2026)
				</h3>
				<div class="grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs mb-3">
					{#each t3.particulars as item}
						<div class="bg-slate-50 p-3 rounded border border-slate-200">
							<div class="text-2xs text-slate-500">{item.label}</div>
							<div class="text-sm font-bold text-slate-900 mt-1 tabular-nums">
								{formatCrore(item.amount_crore)}
							</div>
						</div>
					{/each}
				</div>
				<p class="text-2xs text-slate-500 italic">
					Sanctioned (₹48,559.69 Cr) = Availed (₹42,193.45 Cr) + Undrawn (₹6,366.24 Cr). Outstanding = Availed - Repaid (₹10,512.30 Cr) = ₹31,681.15 Cr.
				</p>
			</div>

			<!-- Two Columns: Bank Loans & Financial Institutions -->
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<!-- Commercial Banks Table -->
				<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
					<div class="flex items-center justify-between mb-3">
						<h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider">
							Table 3.4 — Commercial Bank Loans
						</h4>
						<span class="text-2xs font-mono text-slate-500">Total: {formatCrore(t4.total.outstanding)}</span>
					</div>
					<div class="overflow-x-auto">
						<table class="w-full text-left text-xs">
							<thead class="bg-slate-50 border-b border-slate-200 text-2xs text-slate-500 uppercase">
								<tr>
									<th class="py-2 px-3">Bank Name</th>
									<th class="py-2 px-3 text-right">Raised</th>
									<th class="py-2 px-3 text-right">Outstanding</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-slate-100">
								{#each t4.rows as b}
									<tr class="hover:bg-slate-50">
										<td class="py-2 px-3 font-medium text-slate-800">{b.bank_name}</td>
										<td class="py-2 px-3 text-right font-mono tabular-nums">{formatCrore(b.amount_raised)}</td>
										<td class="py-2 px-3 text-right font-mono font-bold text-slate-900 tabular-nums">{formatCrore(b.outstanding)}</td>
									</tr>
								{/each}
								<tr class="bg-slate-50/80 font-bold border-t border-slate-200">
									<td class="py-2 px-3">Total</td>
									<td class="py-2 px-3 text-right font-mono tabular-nums">{formatCrore(t4.total.amount_raised)}</td>
									<td class="py-2 px-3 text-right font-mono text-slate-900 tabular-nums">{formatCrore(t4.total.outstanding)}</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<!-- Financial Institutions Table -->
				<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
					<div class="flex items-center justify-between mb-3">
						<h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider">
							Table 3.5 — Financial Institutions
						</h4>
						<span class="text-2xs font-mono text-slate-500">Total: {formatCrore(t5.total.outstanding)}</span>
					</div>
					<div class="overflow-x-auto">
						<table class="w-full text-left text-xs">
							<thead class="bg-slate-50 border-b border-slate-200 text-2xs text-slate-500 uppercase">
								<tr>
									<th class="py-2 px-3">Institution</th>
									<th class="py-2 px-3 text-right">Sanctioned</th>
									<th class="py-2 px-3 text-right">Outstanding</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-slate-100">
								{#each t5.rows as inst}
									<tr class="hover:bg-slate-50">
										<td class="py-2 px-3 font-medium text-slate-800">{inst.institution}</td>
										<td class="py-2 px-3 text-right font-mono tabular-nums">{formatCrore(inst.sanctioned)}</td>
										<td class="py-2 px-3 text-right font-mono font-bold text-slate-900 tabular-nums">{formatCrore(inst.outstanding)}</td>
									</tr>
								{/each}
								<tr class="bg-slate-50/80 font-bold border-t border-slate-200">
									<td class="py-2 px-3">Total</td>
									<td class="py-2 px-3 text-right font-mono tabular-nums">{formatCrore(t5.total.sanctioned)}</td>
									<td class="py-2 px-3 text-right font-mono text-slate-900 tabular-nums">{formatCrore(t5.total.outstanding)}</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>

			<!-- BSE Listed Domestic Bonds -->
			<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
				<div class="flex items-center justify-between mb-3">
					<h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider">
						Table 3.7 — BSE-Listed Domestic Bonds Issued ({formatCrore(t7.total.amount)})
					</h4>
					<span class="text-2xs text-slate-500">Structured as 7 Separately Transferable Redeemable Principal Parts (STRPP)</span>
				</div>
				<div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
					{#each t7.rows as bond}
						<div class="bg-slate-50 p-3 rounded border border-slate-200">
							<div class="flex items-center justify-between">
								<span class="font-bold text-slate-800">{bond.series}</span>
								<span class="font-mono text-2xs text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200">{bond.coupon_rate}</span>
							</div>
							<div class="text-sm font-bold text-slate-900 mt-2 font-mono tabular-nums">
								{formatCrore(bond.amount)}
							</div>
							<div class="text-3xs text-slate-400 mt-0.5">FY {bond.year_of_issue}</div>
						</div>
					{/each}
				</div>
			</div>
		</div>
	{/if}

	<!-- Tab 2: Land Acquisition Pool -->
	{#if activeTab === 'land_pool'}
		<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm space-y-4">
			<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-3">
				<div>
					<h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider">
						Table 4.5 — Land Acquisition Pool Projects (as on 15 September 2026)
					</h3>
					<p class="text-xs text-slate-500 mt-0.5">
						Total Approved Outlay: {formatCrore(t45.total.outlay)} | Amount Paid: {formatCrore(t45.total.amount_paid)} | Unpaid Balance: {formatCrore(t45.total.balance)}
					</p>
				</div>
				<div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-amber-50 text-amber-800 border border-amber-200 text-xs font-medium">
					<span>Audit Discrepancy: Repaid Sum ₹1,401.07 Cr vs Footer ₹1,386.64 Cr (Δ ₹14.43 Cr)</span>
				</div>
			</div>

			<div class="overflow-x-auto">
				<table class="w-full text-left text-xs text-slate-700">
					<thead class="bg-slate-50 border-b border-slate-200 text-2xs text-slate-500 uppercase">
						<tr>
							<th class="py-2.5 px-3">Project Name</th>
							<th class="py-2.5 px-3">SPV</th>
							<th class="py-2.5 px-3 text-right">Project Outlay</th>
							<th class="py-2.5 px-3 text-right">Amount Paid</th>
							<th class="py-2.5 px-3 text-right">Unpaid Balance</th>
							<th class="py-2.5 px-3 text-right">Amount Repaid</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-slate-100">
						{#each t45.rows as p}
							<tr class="hover:bg-slate-50">
								<td class="py-2.5 px-3 font-semibold text-slate-900 max-w-xs">{p.project_name}</td>
								<td class="py-2.5 px-3 font-medium text-slate-600">{p.spv}</td>
								<td class="py-2.5 px-3 text-right font-mono tabular-nums">{formatCrore(p.outlay)}</td>
								<td class="py-2.5 px-3 text-right font-mono text-emerald-800 font-medium tabular-nums">{formatCrore(p.amount_paid)}</td>
								<td class="py-2.5 px-3 text-right font-mono text-amber-800 font-medium tabular-nums">{formatCrore(p.balance)}</td>
								<td class="py-2.5 px-3 text-right font-mono text-blue-800 tabular-nums">{formatCrore(p.repaid)}</td>
							</tr>
						{/each}
						<tr class="bg-slate-50 font-bold border-t-2 border-slate-200">
							<td class="py-3 px-3">Grand Total (Reported Table Footer)</td>
							<td class="py-3 px-3"></td>
							<td class="py-3 px-3 text-right font-mono tabular-nums">{formatCrore(t45.total.outlay)}</td>
							<td class="py-3 px-3 text-right font-mono tabular-nums">{formatCrore(t45.total.amount_paid)}</td>
							<td class="py-3 px-3 text-right font-mono text-amber-900 tabular-nums">{formatCrore(t45.total.balance)}</td>
							<td class="py-3 px-3 text-right font-mono text-blue-900 tabular-nums">{formatCrore(t45.total.repaid)}</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	{/if}

	<!-- Tab 3: Debt Servicing Schedule to 2041-42 -->
	{#if activeTab === 'amortisation'}
		<div class="space-y-6">
			<!-- Future Fiscal Requirement Summary -->
			<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
				<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
					<h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider">
						Grand Future Fiscal Burden: ₹70,415.54 Crore (Tables 6.1, 6.2, 6.3)
					</h3>
					<span class="text-xs text-slate-500 font-mono">Excludes Land Acquisition Liabilities</span>
				</div>
				<div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs mb-2">
					<div class="bg-purple-50 p-3 rounded border border-purple-200">
						<div class="text-2xs text-purple-700 font-semibold">Scheduled Debt Servicing (Table 6.1)</div>
						<div class="text-base font-bold text-purple-950 font-mono mt-1 tabular-nums">
							{formatCrore(t_req.grand_future_fiscal_requirement.debt_servicing_crore)}
						</div>
						<div class="text-3xs text-purple-600 mt-0.5">Principal (₹31,857.20 Cr) + Interest (₹15,675.34 Cr)</div>
					</div>
					<div class="bg-blue-50 p-3 rounded border border-blue-200">
						<div class="text-2xs text-blue-700 font-semibold">Project Completion Funding (Table 6.2)</div>
						<div class="text-base font-bold text-blue-950 font-mono mt-1 tabular-nums">
							{formatCrore(t_req.grand_future_fiscal_requirement.project_completion_crore)}
						</div>
						<div class="text-3xs text-blue-600 mt-0.5">To complete started & priority tendered projects</div>
					</div>
					<div class="bg-amber-50 p-3 rounded border border-amber-200">
						<div class="text-2xs text-amber-700 font-semibold">Additional Unpaid Land Balance</div>
						<div class="text-base font-bold text-amber-950 font-mono mt-1 tabular-nums">
							{formatCrore(t_req.grand_future_fiscal_requirement.unpaid_land_balance_crore)}
						</div>
						<div class="text-3xs text-amber-600 mt-0.5">Pending under LARR Act notifications (Table 4.5)</div>
					</div>
				</div>
			</div>

			<!-- Year-wise Amortisation Table -->
			<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
				<h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3">
					Table 6.1 — Year-Wise Amortisation Schedule (2026-27 to 2041-42)
				</h4>
				<div class="overflow-x-auto">
					<table class="w-full text-left text-xs">
						<thead class="bg-slate-50 border-b border-slate-200 text-2xs text-slate-500 uppercase">
							<tr>
								<th class="py-2 px-3">Financial Year</th>
								<th class="py-2 px-3 text-right">Principal Repayment</th>
								<th class="py-2 px-3 text-right">Interest Payment</th>
								<th class="py-2 px-3 text-right">Total Debt Service</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-slate-100 font-mono tabular-nums">
							{#each t61.rows as row}
								<tr class="hover:bg-slate-50">
									<td class="py-2 px-3 font-sans font-medium text-slate-800">{row.year}</td>
									<td class="py-2 px-3 text-right">{formatCrore(row.principal)}</td>
									<td class="py-2 px-3 text-right text-slate-600">{formatCrore(row.interest)}</td>
									<td class="py-2 px-3 text-right font-bold text-slate-900">{formatCrore(row.total)}</td>
								</tr>
							{/each}
							<tr class="bg-slate-50 font-bold border-t-2 border-slate-300 font-mono">
								<td class="py-3 px-3 font-sans">Total Debt Service</td>
								<td class="py-3 px-3 text-right">{formatCrore(t61.total.principal)}</td>
								<td class="py-3 px-3 text-right">{formatCrore(t61.total.interest)}</td>
								<td class="py-3 px-3 text-right text-purple-900">{formatCrore(t61.total.total_debt_service)}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			<!-- Completion Trajectory Overlay (T093) -->
			<CompletionTrajectoryOverlay {t31} {t61} {t63} />

		</div>
	{/if}

	<!-- Tab 4: State Budget Transfers -->
	{#if activeTab === 'transfers'}
		<div class="space-y-6">
			<!-- Table 3.2 Servicing Ratio Card -->
			<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
				<h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2">
					Table 3.2 — State Transfers vs. Debt Servicing (99.4% Ratio)
				</h3>
				<p class="text-xs text-slate-600 mb-4">
					Between 2021-22 and 2024-25, GoK transferred ₹11,869.28 crore to KIIFB, while KIIFB's debt service was ₹11,944.18 crore. State transfers met 99.4% of all debt servicing.
				</p>
				<div class="overflow-x-auto">
					<table class="w-full text-left text-xs">
						<thead class="bg-slate-50 border-b border-slate-200 text-2xs text-slate-500 uppercase">
							<tr>
								<th class="py-2 px-3">Year</th>
								<th class="py-2 px-3 text-right">Principal Repaid</th>
								<th class="py-2 px-3 text-right">Interest Paid</th>
								<th class="py-2 px-3 text-right">Total Debt Service</th>
								<th class="py-2 px-3 text-right">Transfers from GoK</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-slate-100 font-mono tabular-nums">
							{#each t32.rows as r}
								<tr class="hover:bg-slate-50">
									<td class="py-2 px-3 font-sans font-medium text-slate-800">{r.year}</td>
									<td class="py-2 px-3 text-right">{formatCrore(r.principal_repaid)}</td>
									<td class="py-2 px-3 text-right">{formatCrore(r.interest_paid)}</td>
									<td class="py-2 px-3 text-right font-bold text-slate-900">{formatCrore(r.total_debt_service)}</td>
									<td class="py-2 px-3 text-right font-bold text-emerald-800">{formatCrore(r.transfers_from_gok)}</td>
								</tr>
							{/each}
							<tr class="bg-slate-50 font-bold border-t-2 border-slate-300">
								<td class="py-3 px-3 font-sans">Total</td>
								<td class="py-3 px-3 text-right">{formatCrore(t32.total.principal_repaid)}</td>
								<td class="py-3 px-3 text-right">{formatCrore(t32.total.interest_paid)}</td>
								<td class="py-3 px-3 text-right text-slate-900">{formatCrore(t32.total.total_debt_service)}</td>
								<td class="py-3 px-3 text-right text-emerald-900">{formatCrore(t32.total.transfers_from_gok)}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			<!-- Historical Transfers Table 3.1 -->
			<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
				<h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2">
					Table 3.1 — Annual Revenue Transfers Under Section 7 (2016-17 to 2026-27)
				</h3>
				<p class="text-xs text-slate-600 mb-4">
					Total cumulative statutory revenue transferred to KIIFB: ₹24,764.64 Crore (Motor Vehicles Tax + Petroleum Cess).
				</p>
				<div class="overflow-x-auto">
					<table class="w-full text-left text-xs">
						<thead class="bg-slate-50 border-b border-slate-200 text-2xs text-slate-500 uppercase">
							<tr>
								<th class="py-2 px-3">Financial Year</th>
								<th class="py-2 px-3 text-right">Motor Vehicles Tax Share</th>
								<th class="py-2 px-3 text-right">Petroleum Cess</th>
								<th class="py-2 px-3 text-right">Total Transferred</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-slate-100 font-mono tabular-nums">
							{#each t31.rows as row}
								<tr class="hover:bg-slate-50">
									<td class="py-2 px-3 font-sans font-medium text-slate-800">{row.year}</td>
									<td class="py-2 px-3 text-right">{formatCrore(row.mvt_share)}</td>
									<td class="py-2 px-3 text-right text-slate-600">{formatCrore(row.petroleum_cess)}</td>
									<td class="py-2 px-3 text-right font-bold text-slate-900">{formatCrore(row.total)}</td>
								</tr>
							{/each}
							<tr class="bg-slate-50 font-bold border-t-2 border-slate-300">
								<td class="py-3 px-3 font-sans">Total Transferred</td>
								<td class="py-3 px-3 text-right">{formatCrore(t31.total.mvt_share)}</td>
								<td class="py-3 px-3 text-right">{formatCrore(t31.total.petroleum_cess)}</td>
								<td class="py-3 px-3 text-right text-emerald-900">{formatCrore(t31.total.total_transferred)}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</div>
	{/if}

	<!-- Tab 5: Deployment Flow (Sankey) -->
	{#if activeTab === 'deployment_flow'}
		<div class="space-y-6">
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<h2 class="text-lg font-bold text-slate-900 mb-2">Portfolio Deployment Flow (Sankey)</h2>
				<p class="text-xs text-slate-500 mb-4">
					Flow of approved capital through Kanakku lifecycle stages. Data from DS010/DS030 enriched project records.
				</p>
				<SankeyFlow records={data.records} />
			</div>
		</div>
	{/if}
</div>
