<script lang="ts">
	import SankeyFlow from '$lib/components/SankeyFlow.svelte';
	import FundsProgressScatter from '$lib/components/FundsProgressScatter.svelte';

	let { data } = $props();

	// Sankey/Scatter view state
	let showSankey = $state(false);
	let showScatter = $state(false);

	// Search & Filter State
	let searchQuery = $state('');
	let selectedSector = $state('ALL');
	let selectedDistrict = $state('ALL');
	let selectedFlag = $state('ALL');
	let selectedStatus = $state('ALL');
	let selectedEntityType = $state('ALL');
	let currentPage = $state(1);
	const pageSize = 25;

	// Modal / Inspection Drawer state
	let activeRecord = $state<any>(null);

	// Collect unique sectors, districts, statuses
	let sectors = $derived(['ALL', ...Array.from(new Set(data.records.map((r: any) => r.sector))).sort()]);
	let districts = $derived([
		'ALL',
		...Array.from(
			new Set(
				data.records
					.map((r: any) => r.district)
					.filter((d: any) => d)
					.flatMap((d: string) => d.split(',').map((s) => s.trim()))
			)
		).sort()
	]);
	let flags = $derived(['ALL', 'FLAGGED', 'overdue', 'payment_vs_progress', 'cost_escalation', 'stale', 'above_approved']);
	let statuses = $derived(['ALL', ...Array.from(new Set(data.records.map((r: any) => r.status.normalised_status))).sort()]);
	let entityTypes = $derived(['ALL', 'project_sanction', 'educational_institution']);

	// Filtered records
	let filteredRecords = $derived(
		data.records.filter((r: any) => {
			const matchesSearch = searchQuery === '' || 
				r.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				(r.spv && r.spv.toLowerCase().includes(searchQuery.toLowerCase())) ||
				(r.department && r.department.toLowerCase().includes(searchQuery.toLowerCase())) ||
				(r.district && r.district.toLowerCase().includes(searchQuery.toLowerCase())) ||
				(r.constituency && r.constituency.toLowerCase().includes(searchQuery.toLowerCase())) ||
				(r.school_code && r.school_code.includes(searchQuery));

			const matchesSector = selectedSector === 'ALL' || r.sector === selectedSector;
			const matchesDistrict = selectedDistrict === 'ALL' || (r.district && r.district.includes(selectedDistrict));
			const matchesStatus = selectedStatus === 'ALL' || r.status.normalised_status === selectedStatus;
			const matchesEntity = selectedEntityType === 'ALL' || r.entity_type === selectedEntityType;
			
			let matchesFlag = true;
			if (selectedFlag === 'FLAGGED') {
				matchesFlag = r.open_flags && r.open_flags.length > 0;
			} else if (selectedFlag !== 'ALL') {
				matchesFlag = r.open_flags && r.open_flags.includes(selectedFlag);
			}

			return matchesSearch && matchesSector && matchesDistrict && matchesStatus && matchesEntity && matchesFlag;
		})
	);

	let totalPages = $derived(Math.max(1, Math.ceil(filteredRecords.length / pageSize)));
	let paginatedRecords = $derived(
		filteredRecords.slice((currentPage - 1) * pageSize, currentPage * pageSize)
	);

	function openRecordModal(rec: any) {
		activeRecord = rec;
	}

	function closeRecordModal() {
		activeRecord = null;
	}

	function formatCrore(val: number | null | undefined): string {
		if (val === null || val === undefined) return '—';
		return '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Cr';
	}

	// Badge styling based on design-system.md
	function getStatusBadge(status: string) {
		switch (status) {
			case 'approved':
				return 'bg-slate-100 text-slate-800 border-slate-300';
			case 'tendered':
				return 'bg-sky-50 text-sky-800 border-sky-200';
			case 'in_progress':
				return 'bg-indigo-50 text-indigo-800 border-indigo-200';
			case 'physically_complete':
				return 'bg-cyan-50 text-cyan-800 border-cyan-200';
			case 'handed_over':
				return 'bg-teal-50 text-teal-800 border-teal-200';
			case 'operational':
				return 'bg-emerald-50 text-emerald-800 border-emerald-200';
			case 'delayed':
				return 'bg-amber-50 text-amber-800 border-amber-200';
			case 'cancelled':
				return 'bg-red-50 text-red-800 border-red-200';
			default:
				return 'bg-slate-50 text-slate-700 border-slate-200';
		}
	}
</script>

<svelte:head>
	<title>Project Explorer — KIIFB Accountability Dashboard</title>
</svelte:head>

<div class="space-y-6">
	<!-- Page Header / Metric Cards -->
	<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
			<div>
				<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-800 border border-blue-200 mb-2">
					<span>Milestone 2 Explorer</span>
					<span>•</span>
					<span>Official Disclosed Delivery</span>
				</div>
				<h2 class="text-2xl font-bold tracking-tight text-slate-900">
					Official Project & Delivery Explorer
				</h2>
				<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
					Exploration of 1,408 KIIFB project sanctions joined with 969 KITE public school institutions. Distinguishes umbrella project sanctions from delivery institutions.
				</p>
			</div>
			<div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-left">
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Total Records</div>
					<div class="text-lg font-bold text-slate-900 tabular-nums">{data.summary.total_records.toLocaleString('en-IN')}</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Project Sanctions (DS010)</div>
					<div class="text-lg font-bold text-slate-900 tabular-nums">{data.summary.kiifb_project_sanctions.toLocaleString('en-IN')}</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3 col-span-2 sm:col-span-1">
					<div class="text-2xs text-slate-500 uppercase font-semibold">KITE Schools (DS021)</div>
					<div class="text-lg font-bold text-emerald-800 tabular-nums">{data.summary.kite_school_institutions.toLocaleString('en-IN')}</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Filter Controls -->
	<div class="bg-white rounded-lg border border-slate-200 p-4 shadow-sm space-y-3">
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3">
			<div class="lg:col-span-2">
				<label for="search" class="block text-2xs font-semibold uppercase text-slate-500 mb-1">Search Keyword / ID</label>
				<input 
					id="search"
					type="text" 
					bind:value={searchQuery}
					oninput={() => currentPage = 1}
					placeholder="Search project, school, constituency, SPV..." 
					class="w-full text-xs px-3 py-2 border border-slate-300 rounded focus:ring-1 focus:ring-slate-900 focus:outline-none"
				/>
			</div>
			<div>
				<label for="district" class="block text-2xs font-semibold uppercase text-slate-500 mb-1">District (Enriched)</label>
				<select 
					id="district"
					bind:value={selectedDistrict}
					onchange={() => currentPage = 1}
					class="w-full text-xs px-3 py-2 border border-slate-300 rounded focus:ring-1 focus:ring-slate-900 focus:outline-none bg-white"
				>
					{#each districts as dist}
						<option value={dist}>{dist}</option>
					{/each}
				</select>
			</div>
			<div>
				<label for="flag" class="block text-2xs font-semibold uppercase text-slate-500 mb-1">Rule Flags (Kanakku)</label>
				<select 
					id="flag"
					bind:value={selectedFlag}
					onchange={() => currentPage = 1}
					class="w-full text-xs px-3 py-2 border border-slate-300 rounded focus:ring-1 focus:ring-slate-900 focus:outline-none bg-white font-medium text-slate-800"
				>
					{#each flags as flg}
						<option value={flg}>{flg === 'ALL' ? 'ALL PROJECTS' : flg === 'FLAGGED' ? '🚩 ANY OPEN FLAG' : flg}</option>
					{/each}
				</select>
			</div>
			<div>
				<label for="sector" class="block text-2xs font-semibold uppercase text-slate-500 mb-1">Sector</label>
				<select 
					id="sector"
					bind:value={selectedSector}
					onchange={() => currentPage = 1}
					class="w-full text-xs px-3 py-2 border border-slate-300 rounded focus:ring-1 focus:ring-slate-900 focus:outline-none bg-white"
				>
					{#each sectors as sec}
						<option value={sec}>{sec}</option>
					{/each}
				</select>
			</div>
			<div>
				<label for="status" class="block text-2xs font-semibold uppercase text-slate-500 mb-1">Normalised Status</label>
				<select 
					id="status"
					bind:value={selectedStatus}
					onchange={() => currentPage = 1}
					class="w-full text-xs px-3 py-2 border border-slate-300 rounded focus:ring-1 focus:ring-slate-900 focus:outline-none bg-white"
				>
					{#each statuses as st}
						<option value={st}>{st}</option>
					{/each}
				</select>
			</div>
		</div>

		<div class="flex flex-col sm:flex-row sm:items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-100 gap-2">
			<div class="flex items-center gap-2">
				<span>Showing <strong>{filteredRecords.length.toLocaleString('en-IN')}</strong> matching records</span>
				<span class="text-slate-300">|</span>
				<span class="inline-flex items-center gap-1 text-2xs px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">
					<span>✨ Enriched with Kerala Kanakku (DS030)</span>
				</span>
			</div>
			{#if searchQuery || selectedSector !== 'ALL' || selectedDistrict !== 'ALL' || selectedFlag !== 'ALL' || selectedStatus !== 'ALL' || selectedEntityType !== 'ALL'}
				<button 
					onclick={() => { searchQuery = ''; selectedSector = 'ALL'; selectedDistrict = 'ALL'; selectedFlag = 'ALL'; selectedStatus = 'ALL'; selectedEntityType = 'ALL'; currentPage = 1; }}
					class="text-blue-600 hover:underline cursor-pointer font-medium"
				>
					Reset all filters
				</button>
			{/if}
		</div>
	</div>

	<!-- Sankey Flow View Toggle -->
	<div class="bg-white rounded-lg border border-slate-200 p-4 shadow-sm">
		<div class="flex items-center justify-between">
			<div>
				<h3 class="text-sm font-bold text-slate-900">Portfolio Deployment Flow (Sankey)</h3>
				<p class="text-2xs text-slate-500">Visualize capital flow through Kanakku lifecycle stages</p>
			</div>
			<button
				onclick={() => showSankey = !showSankey}
				class="px-3 py-1.5 text-xs font-medium rounded border transition {showSankey ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}"
			>
				{showSankey ? 'Hide Sankey' : 'Show Sankey'}
			</button>
		</div>
		{#if showSankey}
			<SankeyFlow records={data.records} />
		{/if}
	</div>

	<!-- Funds vs Progress Scatter (T092) -->
	<div class="bg-white rounded-lg border border-slate-200 p-4 shadow-sm">
		<div class="flex items-center justify-between">
			<div>
				<h3 class="text-sm font-bold text-slate-900">Funds Released vs Physical Progress Scatter</h3>
				<p class="text-2xs text-slate-500">Scatter of % released vs % progress with divergence zone and anomaly markers</p>
			</div>
			<button
				onclick={() => showScatter = !showScatter}
				class="px-3 py-1.5 text-xs font-medium rounded border transition {showScatter ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}"
			>
				{showScatter ? 'Hide Scatter' : 'Show Scatter'}
			</button>
		</div>
		{#if showScatter}
			<FundsProgressScatter records={data.records} />
		{/if}
	</div>

	<!-- Project Explorer Table -->
	<div class="bg-white rounded-lg border border-slate-200 overflow-hidden shadow-sm">
		<div class="overflow-x-auto">
			<table class="w-full text-left text-xs text-slate-700">
				<thead class="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase text-2xs tracking-wider">
					<tr>
						<th class="px-4 py-3">ID & Entity</th>
						<th class="px-4 py-3">Project / School Name</th>
						<th class="px-4 py-3">Sector & SPV</th>
						<th class="px-4 py-3 text-right">Approved Outlay</th>
						<th class="px-4 py-3 text-right">Disbursed</th>
						<th class="px-4 py-3 text-center">Status</th>
						<th class="px-4 py-3 text-center">Actions</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-slate-100">
					{#if paginatedRecords.length === 0}
						<tr>
							<td colspan="7" class="text-center py-8 text-slate-400">
								No matching records found.
							</td>
						</tr>
					{:else}
						{#each paginatedRecords as rec}
							<tr class="hover:bg-slate-50/80 transition">
								<td class="px-4 py-3 font-mono">
									<div class="font-bold text-slate-900">{rec.record_id}</div>
									<div class="text-2xs text-slate-400">
										{rec.entity_type === 'project_sanction' ? 'Project Sanction' : 'School Campus'}
									</div>
								</td>
								<td class="px-4 py-3 max-w-sm">
									<div class="font-semibold text-slate-900 leading-snug">{rec.name}</div>
									{#if rec.district || rec.constituency}
										<div class="text-2xs text-slate-500 mt-0.5">
											{rec.district || ''}{rec.constituency ? ` (${rec.constituency})` : ''}
										</div>
									{/if}
									{#if rec.open_flags && rec.open_flags.length > 0}
										<div class="flex flex-wrap gap-1 mt-1">
											{#each rec.open_flags as flg}
												<span class="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-3xs font-bold uppercase bg-amber-100 text-amber-900 border border-amber-300">
													<span>🚩 {flg.replace('_', ' ')}</span>
												</span>
											{/each}
										</div>
									{/if}
									{#if rec.school_code}
										<div class="text-2xs font-mono text-emerald-700 mt-0.5">
											School Code: {rec.school_code}
										</div>
									{/if}
								</td>
								<td class="px-4 py-3">
									<div class="font-medium text-slate-800">{rec.sector}</div>
									<div class="text-2xs text-slate-500 truncate max-w-xs">{rec.spv || rec.department}</div>
								</td>
								<td class="px-4 py-3 text-right font-mono tabular-nums">
									{formatCrore(rec.financials?.approved_crore)}
								</td>
								<td class="px-4 py-3 text-right font-mono tabular-nums">
									{#if rec.financials?.released_crore !== undefined}
										<span class="font-medium text-slate-900">{formatCrore(rec.financials.released_crore)}</span>
										{#if rec.financials.release_ratio_pct > 0}
											<div class="text-2xs text-slate-400">({rec.financials.release_ratio_pct}%)</div>
										{/if}
									{:else}
										<span class="text-slate-400">—</span>
									{/if}
								</td>
								<td class="px-4 py-3 text-center">
									<span class="inline-block px-2 py-0.5 rounded text-2xs font-semibold border {getStatusBadge(rec.status.normalised_status)}">
										{rec.status.normalised_status}
									</span>
								</td>
								<td class="px-4 py-3 text-center">
									<button 
										onclick={() => openRecordModal(rec)}
										class="px-2.5 py-1 text-2xs font-medium text-blue-700 bg-blue-50 border border-blue-200 rounded hover:bg-blue-100 transition cursor-pointer"
									>
										Inspect
									</button>
								</td>
							</tr>
						{/each}
					{/if}
				</tbody>
			</table>
		</div>

		<!-- Pagination Footer -->
		{#if totalPages > 1}
			<div class="bg-slate-50 px-4 py-3 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600">
				<div>
					Page {currentPage} of {totalPages}
				</div>
				<div class="flex items-center space-x-2">
					<button 
						disabled={currentPage === 1}
						onclick={() => currentPage = Math.max(1, currentPage - 1)}
						class="px-3 py-1 border border-slate-300 rounded bg-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-100"
					>
						Previous
					</button>
					<button 
						disabled={currentPage === totalPages}
						onclick={() => currentPage = Math.min(totalPages, currentPage + 1)}
						class="px-3 py-1 border border-slate-300 rounded bg-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-100"
					>
						Next
					</button>
				</div>
			</div>
		{/if}
	</div>
</div>

<!-- Detailed Record Inspection Modal -->
{#if activeRecord}
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<div 
		class="fixed inset-0 z-50 overflow-hidden bg-slate-900/50 backdrop-blur-xs flex justify-end transition-opacity"
		onclick={closeRecordModal}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
		onkeydown={(e) => e.key === 'Escape' && closeRecordModal()}
	>
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
		<div 
			class="w-full max-w-xl bg-white h-full shadow-2xl p-6 overflow-y-auto flex flex-col justify-between"
			onclick={(e) => e.stopPropagation()}
			role="document"
		>
			<div class="space-y-6">
				<!-- Header -->
				<div class="flex items-start justify-between pb-4 border-b border-slate-200">
					<div>
						<div class="flex items-center gap-2 mb-1">
							<span class="font-mono text-xs font-bold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
								{activeRecord.record_id}
							</span>
							<span class="text-2xs font-semibold px-2 py-0.5 rounded border {getStatusBadge(activeRecord.status.normalised_status)}">
								{activeRecord.status.normalised_status}
							</span>
						</div>
						<h3 class="text-base font-bold text-slate-900 leading-snug">
							{activeRecord.name}
						</h3>
					</div>
					<button 
						onclick={closeRecordModal}
						class="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition text-lg"
						aria-label="Close modal"
					>
						✕
					</button>
				</div>

				<!-- Provenance & Source Locator -->
				<div class="bg-blue-50/60 rounded p-3.5 border border-blue-200/70 text-xs">
					<div class="font-bold text-blue-900 mb-1">Source & Provenance</div>
					<div class="font-mono text-blue-800 text-2xs space-y-0.5">
						<div>Source ID: {activeRecord.source_id}</div>
						<div>Locator: {activeRecord.source_locator}</div>
						<div>Counting Unit: {activeRecord.counting_unit}</div>
						{#if activeRecord.school_code}
							<div>Official School Code: {activeRecord.school_code}</div>
						{/if}
					</div>
				</div>

				<!-- Normalised Status Explanation -->
				<div>
					<h4 class="text-2xs font-bold uppercase text-slate-500 mb-1">Status Disambiguation</h4>
					<div class="bg-slate-50 p-3 rounded border border-slate-200/80 text-xs space-y-1">
						<div><strong>Source Portal Label:</strong> "{activeRecord.status.source_status_text}"</div>
						<div><strong>Normalised Status:</strong> {activeRecord.status.normalised_status}</div>
						{#if activeRecord.status.normalisation_rule}
							<div class="text-slate-500 text-2xs pt-1 border-t border-slate-200">
								Rule: {activeRecord.status.normalisation_rule}
							</div>
						{/if}
					</div>
				</div>

				<!-- Financial Details -->
				{#if activeRecord.financials}
					<div>
						<h4 class="text-2xs font-bold uppercase text-slate-500 mb-1">Disclosed Financials</h4>
						<div class="grid grid-cols-2 gap-2 text-xs">
							<div class="bg-slate-50 p-2.5 rounded border border-slate-200">
								<div class="text-2xs text-slate-500">Approved Outlay</div>
								<div class="font-mono font-bold text-slate-900 mt-0.5">
									{formatCrore(activeRecord.financials.approved_crore)}
								</div>
								<div class="text-3xs text-slate-400">₹{activeRecord.financials.approved_inr.toLocaleString('en-IN')}</div>
							</div>
							<div class="bg-slate-50 p-2.5 rounded border border-slate-200">
								<div class="text-2xs text-slate-500">Released Funds</div>
								<div class="font-mono font-bold text-slate-900 mt-0.5">
									{formatCrore(activeRecord.financials.released_crore)}
								</div>
								<div class="text-3xs text-slate-400">₹{activeRecord.financials.released_inr.toLocaleString('en-IN')}</div>
							</div>
						</div>
					</div>
				{/if}

				<!-- Administrative Metadata -->
				<div>
					<h4 class="text-2xs font-bold uppercase text-slate-500 mb-1">Administrative Scope</h4>
					<div class="space-y-1 text-xs text-slate-700 bg-slate-50 p-3 rounded border border-slate-200">
						<div><strong>Sector:</strong> {activeRecord.sector}</div>
						<div><strong>Department:</strong> {activeRecord.department}</div>
						<div><strong>Implementing Agency / SPV:</strong> {activeRecord.spv || '—'}</div>
						{#if activeRecord.district}
							<div><strong>District:</strong> {activeRecord.district}</div>
						{/if}
						{#if activeRecord.constituency}
							<div><strong>Constituency:</strong> {activeRecord.constituency}</div>
						{/if}
					</div>
				</div>
			</div>

			<!-- Footer -->
			<div class="pt-4 border-t border-slate-200 mt-6 flex justify-end">
				<button 
					onclick={closeRecordModal}
					class="px-4 py-2 bg-slate-900 text-white rounded text-xs font-medium hover:bg-slate-800 transition"
				>
					Close
				</button>
			</div>
		</div>
	</div>
{/if}
