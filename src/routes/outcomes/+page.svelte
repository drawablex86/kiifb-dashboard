<script lang="ts">
	import KeralaGeographyMap from '$lib/components/KeralaGeographyMap.svelte';

	let { data } = $props();

	// Tabs for navigation
	let activeTab = $state<'completeness' | 'dimensions' | 'geography' | 'factsheets'>('geography');

	// Shorthand derived state
	let dimensions = $derived(data.publicValue.dimensions);
	let completeness = $derived(data.publicValue.evidence_completeness_matrix);
	let dataGaps = $derived(data.publicValue.portfolio_data_gaps || []);
	let districts = $derived(data.publicValue.district_distribution || []);
	let departments = $derived(data.publicValue.department_distribution || []);

	// State for Geography & Sectoral tab (T042) - now shared with KeralaGeographyMap
	let selectedDistrict = $state<string>('Kannur');
	let districtSort = $state<'outlay_desc' | 'outlay_asc' | 'alpha' | 'share_desc'>('outlay_desc');
	let selectedDenominator = $state<'infra' | 'land' | 'total'>('infra');
	let mapMode = $state<'districts' | 'dots' | 'both'>('districts');
	let deptSearch = $state('');
	let deptSort = $state<'approved_desc' | 'released_desc' | 'absorption_desc' | 'projects_desc'>('approved_desc');

	// Geotagged records for the map dot layer (from DS030 enriched data)
	let geotaggedRecords = $derived.by(() => {
		return (data.kanakkuPackages || []).filter((p: any) =>
			p.lat && p.lng && Number.isFinite(p.lat) && Number.isFinite(p.lng)
		);
	});

	let sortedDistricts = $derived.by(() => {
		const list = [...districts];
		if (districtSort === 'outlay_desc') {
			return list.sort((a, b) => b.infrastructure_outlay_cr - a.infrastructure_outlay_cr);
		} else if (districtSort === 'outlay_asc') {
			return list.sort((a, b) => a.infrastructure_outlay_cr - b.infrastructure_outlay_cr);
		} else if (districtSort === 'share_desc') {
			return list.sort((a, b) => b.infrastructure_share_pct - a.infrastructure_share_pct);
		} else {
			return list.sort((a, b) => a.district.localeCompare(b.district));
		}
	});

	let activeDistrictData = $derived(
		districts.find((d: any) => d.district === selectedDistrict) || districts[0]
	);

	let filteredDepartments = $derived.by(() => {
		let list = departments.filter((d: any) =>
			d.department.toLowerCase().includes(deptSearch.toLowerCase())
		);
		if (deptSort === 'approved_desc') {
			return list.sort((a: any, b: any) => b.approved_cr - a.approved_cr);
		} else if (deptSort === 'released_desc') {
			return list.sort((a: any, b: any) => b.released_cr - a.released_cr);
		} else if (deptSort === 'absorption_desc') {
			return list.sort((a: any, b: any) => b.absorption_rate_pct - a.absorption_rate_pct);
		} else {
			return list.sort((a: any, b: any) => b.projects_count - a.projects_count);
		}
	});

	// Formatting helper
	function formatCrore(val: number | null | undefined): string {
		if (val === null || val === undefined) return '—';
		return '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Cr';
	}

	// Severity and status badges
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

	// Color coding for district bars (used in the comparison section)
	function getDistrictFillColor(dist: any, isSelected: boolean): string {
		if (isSelected) return '#059669'; // Emerald-600 highlight
		if (dist.infrastructure_share_pct >= 10.0) return '#065f46'; // Emerald-800
		if (dist.infrastructure_share_pct >= 5.0) return '#0284c7'; // Sky-600
		if (dist.infrastructure_share_pct >= 3.0) return '#64748b'; // Slate-500
		return '#f59e0b'; // Amber-500 (Underserved)
	}

	// T103 (Milestone 10): print-ready district fact sheets
	let activeFactSheetDistrict = $state<string>('Kannur');
	let showAllFactSheets = $state(false);

	const factSheetDistricts = $derived(districts);

	let activeFactSheet = $derived(
		factSheetDistricts.find((d: any) => d.district === activeFactSheetDistrict) || factSheetDistricts[0]
	);

	function printFactSheets() {
		print();
	}
</script>

<style>
	@media print {
		:global(header),
		:global(footer),
		:global(nav) {
			display: none !important;
		}
		:global(body) {
			background: #fff !important;
		}
		.fact-sheet {
			break-inside: avoid;
			page-break-inside: avoid;
			border: 1px solid #cbd5e1 !important;
			box-shadow: none !important;
		}
		:global(main) {
			max-width: none !important;
			padding: 0 !important;
		}
	}
</style>

<svelte:head>
	<title>Public Value, Geography & Evidence Completeness — KIIFB Accountability Dashboard</title>
</svelte:head>

<div class="space-y-6">
	<!-- Page Header Banner -->
	<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
			<div>
				<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 mb-2">
					<span>Milestone 4: Outcomes & Geography</span>
					<span>•</span>
					<span>5 Dimensions, Evidence Completeness & Spatial Allocation</span>
				</div>
				<h2 class="text-2xl font-bold tracking-tight text-slate-900">
					Public Value, Evidence Completeness & Geographic Allocation
				</h2>
				<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
					Multidimensional civic evaluation of KIIFB capital allocations: separating narrow fiscal debt servicing from social returns, mapping 14-district spatial concentration, and tracking portfolio data gaps.
				</p>
			</div>

			<!-- Summary Stat Counters -->
			<div class="grid grid-cols-2 sm:grid-cols-3 gap-3 text-left">
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Total Approved Capital</div>
					<div class="text-lg font-bold text-slate-900 tabular-nums">₹100,341 Cr</div>
					<div class="text-3xs text-slate-500">1,240 Projects (Table 4.1)</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Top 3 Districts Outlay</div>
					<div class="text-lg font-bold text-emerald-800 tabular-nums">41.6%</div>
					<div class="text-3xs text-slate-500">TVM + Kannur + EKM (Table 4.2)</div>
				</div>
				<div class="bg-slate-50 border border-slate-200/80 rounded p-3 col-span-2 sm:col-span-1">
					<div class="text-2xs text-slate-500 uppercase font-semibold">Kannur Industrial LA</div>
					<div class="text-lg font-bold text-amber-700 tabular-nums">74.7%</div>
					<div class="text-3xs text-slate-500">₹12,257.50 Cr (Table 4.3)</div>
				</div>
			</div>
		</div>

		<!-- Navigation Tabs -->
		<div class="flex items-center space-x-2 border-b border-slate-200 mt-6 -mb-6 overflow-x-auto">
			<button
				onclick={() => (activeTab = 'geography')}
				class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'geography' ? 'border-emerald-600 text-emerald-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
			>
				District & Sector Allocation (T042)
			</button>
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
				onclick={() => (activeTab = 'factsheets')}
				class="px-4 py-2 text-xs sm:text-sm font-semibold border-b-2 transition whitespace-nowrap {activeTab === 'factsheets' ? 'border-emerald-600 text-emerald-700' : 'border-transparent text-slate-500 hover:text-slate-800'}"
			>
				District Fact Sheets (T103)
			</button>
		</div>
	</div>

	<!-- TAB 1: DISTRICT & SECTOR ALLOCATION (T042) -->
	{#if activeTab === 'geography'}
		<div class="space-y-6">
			<!-- Spatial Findings Callout Banner -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
				<div class="bg-emerald-50/50 border border-emerald-200 rounded-lg p-4">
					<div class="text-2xs uppercase tracking-wider font-semibold text-emerald-800 mb-1">
						High Spatial Concentration
					</div>
					<div class="text-sm font-bold text-slate-900 mb-1">Top 3 Districts: 41.6% Outlay</div>
					<p class="text-xs text-slate-600 leading-relaxed">
						Thiruvananthapuram (₹10,819.75 Cr), Kannur (₹10,767.35 Cr), and Ernakulam (₹10,513.72 Cr) together account for 41.6% of approved infrastructure outlay.
					</p>
				</div>

				<div class="bg-amber-50/50 border border-amber-200 rounded-lg p-4">
					<div class="text-2xs uppercase tracking-wider font-semibold text-amber-800 mb-1">
						Underserved Highlands & Periphery
					</div>
					<div class="text-sm font-bold text-slate-900 mb-1">Bottom 4 Districts: 9.7% Combined</div>
					<p class="text-xs text-slate-600 leading-relaxed">
						Idukki (1.87%), Pathanamthitta (1.96%), Wayanad (2.93%), and Kasargod (2.93%) receive only ₹7,480.29 Cr combined across all infrastructure projects.
					</p>
				</div>

				<div class="bg-purple-50/50 border border-purple-200 rounded-lg p-4">
					<div class="text-2xs uppercase tracking-wider font-semibold text-purple-800 mb-1">
						Industrial Land Skewness
					</div>
					<div class="text-sm font-bold text-slate-900 mb-1">Kannur: 74.7% of Industrial LA</div>
					<p class="text-xs text-slate-600 leading-relaxed">
						Kannur alone accounts for ₹12,257.50 Cr in industrial land acquisition — nearly three-quarters of the state's total industrial land pool (Table 4.3).
					</p>
				</div>
			</div>

			<!-- Main Map & District Explorer Grid -->
			<div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
				<!-- Interactive Kerala Map Visualizer -->
				<div class="lg:col-span-5 bg-white rounded-lg border border-slate-200 p-5 shadow-sm flex flex-col justify-between">
					<div>
						<div class="flex items-center justify-between mb-2">
							<h3 class="text-sm font-bold text-slate-900">Kerala Spatial Distribution Map</h3>
							<div class="inline-flex rounded-md shadow-sm border border-slate-300 p-0.5 bg-slate-100 text-3xs font-semibold">
								<button 
									onclick={() => mapMode = 'districts'}
									class="px-2 py-0.5 rounded transition {mapMode === 'districts' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'}"
								>
									Districts
								</button>
								<button 
									onclick={() => mapMode = 'dots'}
									class="px-2 py-0.5 rounded transition {mapMode === 'dots' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'}"
								>
									GPS Dots (DS030)
								</button>
							</div>
						</div>
						<p class="text-xs text-slate-500 mb-4">
							{#if mapMode === 'districts'}
								Geographic layout of all 14 districts positioned from North to South, color-coded by share of infrastructure outlay.
							{:else}
								Pinpointing 3,600+ KIIFB contract packages from Kerala Kanakku (DS030) across exact GPS coordinates.
							{/if}
						</p>

						<!-- Kerala Geography Map (T090) — MapLibre GL choropleth + dot layer with schematic fallback -->
						<KeralaGeographyMap
							{districts}
							geotagged={geotaggedRecords}
							bind:selected={selectedDistrict}
							bind:mode={mapMode}
						/>

					</div>

					<div class="mt-3 text-3xs text-slate-400 font-mono">
						* Map data provenance: Committee Report Table 4.2 (June 30, 2026).
					</div>
				</div>
				<!-- Active District Details & Comparative Bar Visualizer -->
				<div class="lg:col-span-7 space-y-4">
					<!-- Active District Selected Card -->
					<div class="bg-white rounded-lg border-2 border-emerald-500/80 p-5 shadow-sm">
						<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-4">
							<div>
								<div class="flex items-center gap-2">
									<h4 class="text-xl font-bold text-slate-900">{activeDistrictData.district}</h4>
									<span class="text-2xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
										{activeDistrictData.category}
									</span>
								</div>
								<div class="text-xs text-slate-500 mt-0.5">
									Detailed financial & land pool allocation
								</div>
							</div>
							<div class="text-left sm:text-right">
								<div class="text-3xs text-slate-400 uppercase font-semibold">Total Approved Capital</div>
								<div class="text-lg font-bold text-slate-900 tabular-nums">
									{formatCrore(activeDistrictData.total_approved_cr)}
								</div>
							</div>
						</div>

						<div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
							<div class="bg-slate-50 p-3 rounded border border-slate-200">
								<div class="text-3xs uppercase font-semibold text-slate-500">Infrastructure Outlay</div>
								<div class="text-base font-bold text-slate-900 tabular-nums">
									{formatCrore(activeDistrictData.infrastructure_outlay_cr)}
								</div>
								<div class="text-2xs text-slate-500 font-mono">
									{activeDistrictData.infrastructure_share_pct.toFixed(2)}% of state pool
								</div>
							</div>

							<div class="bg-slate-50 p-3 rounded border border-slate-200">
								<div class="text-3xs uppercase font-semibold text-slate-500">Land Acquisition Pool</div>
								<div class="text-base font-bold text-slate-900 tabular-nums">
									{formatCrore(activeDistrictData.land_acquisition_outlay_cr)}
								</div>
								<div class="text-2xs text-slate-500 font-mono">
									{activeDistrictData.land_acquisition_outlay_cr > 0 ? 'KINFRA / KSIDC' : 'None allocated'}
								</div>
							</div>

							<div class="bg-slate-50 p-3 rounded border border-slate-200 col-span-2 sm:col-span-1">
								<div class="text-3xs uppercase font-semibold text-slate-500">Spatial Tier</div>
								<div class="text-sm font-bold text-slate-800">
									{activeDistrictData.category.split('(')[0]}
								</div>
								<div class="text-2xs text-slate-500">
									Rank #{sortedDistricts.findIndex((d: any) => d.district === activeDistrictData.district) + 1} of 15
								</div>
							</div>
						</div>

						<!-- Special District Notes -->
						{#if activeDistrictData.district === 'Kannur'}
							<div class="mt-3 text-xs bg-purple-50 text-purple-900 p-2.5 rounded border border-purple-200">
								<strong>Chapter IV Audit Observation:</strong> Kannur received ₹12,257.50 Cr for industrial land acquisition, representing 74.65% of the state's total industrial land acquisition pool. The Committee noted that KIIFB did not submit a comparative economic appraisal explaining why three-quarters of industrial land funding was concentrated in a single district.
							</div>
						{:else if activeDistrictData.district === 'Thiruvananthapuram'}
							<div class="mt-3 text-xs bg-blue-50 text-blue-900 p-2.5 rounded border border-blue-200">
								<strong>Capital City Portfolio:</strong> Received ₹10,819.75 Cr (14.02%), the single highest infrastructure outlay, covering major transport flyovers, Technopark expansion, medical college superspecialty blocks, and coastal protection.
							</div>
						{:else if ['Idukki', 'Pathanamthitta', 'Wayanad', 'Kasargod'].includes(activeDistrictData.district)}
							<div class="mt-3 text-xs bg-amber-50 text-amber-900 p-2.5 rounded border border-amber-200">
								<strong>Equity Concern:</strong> This peripheral/highland district is among the bottom four in capital outlay, receiving less than 3% of the infrastructure budget.
							</div>
						{/if}
					</div>

					<!-- Comparative Distribution Bars -->
					<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
						<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
							<h4 class="text-sm font-bold text-slate-900">
								District Comparison ({selectedDenominator === 'infra' ? 'Category A: Infrastructure Outlay' : 'Total Approved Capital'})
							</h4>
							
							<!-- Denominator & Sort Controls -->
							<div class="flex items-center gap-2">
								<select
									bind:value={districtSort}
									class="text-xs bg-slate-50 border border-slate-200 rounded px-2 py-1 text-slate-700"
								>
									<option value="outlay_desc">Sort: Outlay (High to Low)</option>
									<option value="outlay_asc">Sort: Outlay (Low to High)</option>
									<option value="share_desc">Sort: State Share (%)</option>
									<option value="alpha">Sort: Alphabetical</option>
								</select>
							</div>
						</div>

						<div class="space-y-2 max-h-[340px] overflow-y-auto pr-1">
							{#each sortedDistricts as dist}
								{@const isSelected = selectedDistrict === dist.district}
								<button
									type="button"
									onclick={() => (selectedDistrict = dist.district)}
									class="w-full text-left p-2 rounded transition flex items-center justify-between gap-3 text-xs border {isSelected ? 'bg-emerald-50/80 border-emerald-300' : 'bg-slate-50/40 border-slate-100 hover:bg-slate-100/70'}"
								>
									<div class="w-36 font-medium text-slate-900 truncate flex items-center gap-1.5">
										<span class="w-2 h-2 rounded-full" style="background-color: {getDistrictFillColor(dist, false)}"></span>
										<span class="{isSelected ? 'font-bold text-emerald-950' : ''}">{dist.district}</span>
									</div>

									<!-- Proportional bar -->
									<div class="flex-1 bg-slate-200 rounded-full h-2 overflow-hidden mx-2">
										<div
											class="h-2 rounded-full transition-all"
											style="width: {dist.infrastructure_share_pct * 4}%; background-color: {getDistrictFillColor(dist, isSelected)}"
										></div>
									</div>

									<div class="w-16 text-right font-mono font-bold tabular-nums text-slate-800">
										{dist.infrastructure_share_pct.toFixed(2)}%
									</div>

									<div class="w-24 text-right font-mono tabular-nums text-slate-600">
										{formatCrore(dist.infrastructure_outlay_cr)}
									</div>
								</button>
							{/each}
						</div>
					</div>
				</div>
			</div>

			<!-- Sectoral & Departmental Distribution (Table 4.4) -->
			<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
				<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
					<div>
						<h3 class="text-base font-bold text-slate-900">
							Department-Wise Distribution of Approved & Released Funds (Table 4.4)
						</h3>
						<p class="text-xs text-slate-500">
							Analysis of all 26 departments: identifying capital concentration and disbursement absorption rates
						</p>
					</div>

					<div class="flex items-center gap-2">
						<input
							type="text"
							placeholder="Search department..."
							bind:value={deptSearch}
							class="text-xs bg-slate-50 border border-slate-200 rounded px-2.5 py-1.5 text-slate-700 w-40 sm:w-48"
						/>
						<select
							bind:value={deptSort}
							class="text-xs bg-slate-50 border border-slate-200 rounded px-2 py-1.5 text-slate-700"
						>
							<option value="approved_desc">Approved Outlay</option>
							<option value="released_desc">Released Funds</option>
							<option value="absorption_desc">Absorption Rate (%)</option>
							<option value="projects_desc">Project Count</option>
						</select>
					</div>
				</div>

				<!-- Sector Table -->
				<div class="overflow-x-auto border border-slate-200 rounded-lg">
					<table class="w-full text-xs text-left text-slate-700">
						<thead class="text-2xs text-slate-500 uppercase bg-slate-50 border-b border-slate-200">
							<tr>
								<th class="px-4 py-3">Department / Sector</th>
								<th class="px-3 py-3 text-center">Projects</th>
								<th class="px-4 py-3 text-right">Approved (₹ Cr)</th>
								<th class="px-3 py-3 text-right">Approved Share</th>
								<th class="px-4 py-3 text-right">Released (₹ Cr)</th>
								<th class="px-3 py-3 text-right">Released Share</th>
								<th class="px-4 py-3 text-right">Absorption Rate</th>
								<th class="px-4 py-3">Progress Dual-Bar</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-slate-200">
							{#each filteredDepartments as dept}
								{@const isPWD = dept.department.includes('Public Works')}
								{@const isEducation = dept.department.includes('General Education')}
								{@const isSCST = dept.department.includes('SC/ST')}
								<tr class="hover:bg-slate-50/80 transition {isPWD ? 'bg-amber-50/30' : isSCST ? 'bg-red-50/30' : ''}">
									<td class="px-4 py-2.5 font-medium text-slate-900">
										<div class="flex items-center gap-1.5">
											<span>{dept.department}</span>
											{#if isPWD}
												<span class="px-1.5 py-0.2 rounded text-3xs font-semibold bg-amber-100 text-amber-800">52.6% Share</span>
											{:else if isEducation}
												<span class="px-1.5 py-0.2 rounded text-3xs font-semibold bg-emerald-100 text-emerald-800">73.7% Absorbed</span>
											{:else if isSCST}
												<span class="px-1.5 py-0.2 rounded text-3xs font-semibold bg-red-100 text-red-800">0.24% Underfunded</span>
											{/if}
										</div>
									</td>
									<td class="px-3 py-2.5 text-center font-mono tabular-nums">{dept.projects_count}</td>
									<td class="px-4 py-2.5 text-right font-mono tabular-nums font-semibold">{formatCrore(dept.approved_cr)}</td>
									<td class="px-3 py-2.5 text-right font-mono tabular-nums">{dept.approved_share_pct.toFixed(2)}%</td>
									<td class="px-4 py-2.5 text-right font-mono tabular-nums">{formatCrore(dept.released_cr)}</td>
									<td class="px-3 py-2.5 text-right font-mono tabular-nums">{dept.released_share_pct.toFixed(2)}%</td>
									<td class="px-4 py-2.5 text-right font-mono font-bold tabular-nums text-slate-900">
										{dept.absorption_rate_pct.toFixed(1)}%
									</td>
									<td class="px-4 py-2.5 w-36">
										<div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
											<div
												class="h-2 rounded-full {dept.absorption_rate_pct >= 60 ? 'bg-emerald-500' : dept.absorption_rate_pct >= 30 ? 'bg-amber-500' : 'bg-rose-400'}"
												style="width: {Math.min(dept.absorption_rate_pct, 100)}%"
											></div>
										</div>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>

				<!-- Sectoral Insights Box -->
				<div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
					<div class="bg-slate-50 p-3 rounded border border-slate-200">
						<div class="font-bold text-slate-900 mb-1">PWD Dominance:</div>
						<p class="text-slate-600">
							Public Works Department alone commands 52.59% of all infrastructure project funding (₹40,577 Cr). Together with Water Resources and Health, three departments take 72.24% of all approved infrastructure funding.
						</p>
					</div>

					<div class="bg-red-50/50 p-3 rounded border border-red-200">
						<div class="font-bold text-red-900 mb-1">SC/ST Development Statutory Deficit:</div>
						<p class="text-slate-700">
							SC/ST Development received only ₹182 Cr (0.24% of approved infrastructure) and ₹87 Cr released (0.28%). By comparison, Kerala's statutory benchmark for Special Component Plan and Tribal Sub Plan (SCSP/TSP) is 12.64% of state capital outlays.
						</p>
					</div>
				</div>
			</div>

			<!-- Explicit Denominators, Provenance & Methodology Banner (T042 Acceptance Requirement) -->
			<div class="bg-slate-100 border border-slate-200 rounded-lg p-5 text-xs text-slate-600 space-y-2">
				<div class="font-bold text-slate-900 flex items-center gap-2">
					<span class="w-2 h-2 rounded-full bg-emerald-600"></span>
					Data Provenance & Explicit Denominator Standards (T042)
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
					<div>
						<strong class="text-slate-800">1. Reporting As-Of Date & Primary Source:</strong>
						<p class="text-2xs text-slate-600 mt-0.5">
							All figures reflect the audited baseline as on <strong>June 30, 2026</strong> from Chapter IV of the Official Expert Committee Report (DS001), specifically Tables 4.1, 4.2, 4.3, 4.4, and 4.5.
						</p>
					</div>
					<div>
						<strong class="text-slate-800">2. Geographic Denominator Definitions:</strong>
						<p class="text-2xs text-slate-600 mt-0.5">
							- Category A: Total Infrastructure Outlay denominator = <strong>₹77,150.87 Cr</strong> (1,233 projects).<br>
							- Category B: Total Land Acquisition Pool denominator = <strong>₹23,189.74 Cr</strong> (7 projects).<br>
							- Industrial Land Acquisition Pool denominator = <strong>₹16,420.73 Cr</strong> (6 projects).<br>
							- Grand Total Portfolio Outlay = <strong>₹100,340.61 Cr</strong> (1,240 projects).
						</p>
					</div>
				</div>
			</div>
		</div>

	<!-- TAB 2: EVIDENCE COMPLETENESS & DATA GAPS (T041) -->
	{:else if activeTab === 'completeness'}
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

	<!-- TAB 3: 5-DIMENSIONAL PUBLIC VALUE (T040) -->
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
	{/if}

<!-- TAB 4: DISTRICT FACT SHEETS (T103) -->
{#if activeTab === 'factsheets'}
	<div class="space-y-6">
		<!-- Controls (hidden in print) -->
		<div class="no-print bg-white rounded-lg border border-slate-200 p-4 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
			<div class="flex items-center gap-2 flex-wrap">
				<button
					onclick={() => (showAllFactSheets = false)}
					class="px-3 py-1.5 text-xs font-medium rounded border transition {showAllFactSheets ? 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50' : 'bg-slate-900 text-white border-slate-900'}"
				>
					Single district
				</button>
				<button
					onclick={() => (showAllFactSheets = true)}
					class="px-3 py-1.5 text-xs font-medium rounded border transition {showAllFactSheets ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}"
				>
					All 15 districts
				</button>
				{#if !showAllFactSheets}
					<select
						bind:value={activeFactSheetDistrict}
						class="text-xs px-2 py-1.5 border border-slate-300 rounded bg-white"
						aria-label="Select district fact sheet"
					>
						{#each factSheetDistricts as d (d.district)}
							<option value={d.district}>{d.district}</option>
						{/each}
					</select>
				{/if}
			</div>
			<button
				onclick={printFactSheets}
				class="px-3 py-1.5 text-xs font-medium rounded bg-emerald-600 text-white hover:bg-emerald-700 transition"
			>
				🖨 Print fact sheets
			</button>
		</div>

		{#each (showAllFactSheets ? factSheetDistricts : [activeFactSheet]) as district (district.district)}
			<article class="fact-sheet bg-white rounded-lg border border-slate-300 p-6 shadow-sm max-w-3xl">
				<header class="border-b-2 border-slate-900 pb-2 mb-3">
					<div class="no-print text-3xs font-mono text-slate-400 uppercase tracking-widest">
						Official District Fact Sheet · print-ready (T103)
					</div>
					<h3 class="text-xl font-bold text-slate-900">{district.district} — KIIFB Evidence Fact Sheet</h3>
					<p class="text-2xs text-slate-500 font-semibold uppercase">{district.category}</p>
				</header>

				<dl class="grid grid-cols-2 gap-2 text-xs mb-4">
					<div class="border border-slate-200 rounded p-2.5">
						<dt class="text-3xs uppercase font-semibold text-slate-500">Total approved capital</dt>
						<dd class="text-base font-bold text-slate-900 tabular-nums">{formatCrore(district.total_approved_cr)}</dd>
						<dd class="text-3xs text-slate-400 font-mono">Source: DS001 Committee Report Ch-IV Table 4.2 (as on June 30, 2026)</dd>
					</div>
					<div class="border border-slate-200 rounded p-2.5">
						<dt class="text-3xs uppercase font-semibold text-slate-500">Infrastructure outlay</dt>
						<dd class="text-base font-bold text-slate-900 tabular-nums">{formatCrore(district.infrastructure_outlay_cr)}</dd>
						<dd class="text-3xs text-slate-400 font-mono">{district.infrastructure_share_pct.toFixed(2)}% of ₹77,150.87 Cr state pool — DS001 Table 4.2 / Table 4.5</dd>
					</div>
					<div class="border border-slate-200 rounded p-2.5">
						<dt class="text-3xs uppercase font-semibold text-slate-500">Land acquisition pool</dt>
						<dd class="text-base font-bold text-slate-900 tabular-nums">{formatCrore(district.land_acquisition_outlay_cr)}</dd>
						<dd class="text-3xs text-slate-400 font-mono">{district.land_acquisition_outlay_cr > 0 ? 'DS001 Tables 4.3 (KINFRA / KSIDC projects)' : 'No land-acquisition allocation disclosed'}</dd>
					</div>
					<div class="border border-slate-200 rounded p-2.5">
						<dt class="text-3xs uppercase font-semibold text-slate-500">Documented delivery disclosures</dt>
						<dd class="text-base font-bold text-slate-900 tabular-nums">DS010 / DS021 / DS030</dd>
						<dd class="text-3xs text-slate-400 font-mono">KIIFB portal · KITE Sametham · Kerala Kanakku (CC BY 4.0)</dd>
					</div>
				</dl>

				{#if district.district === 'Kannur'}
					<div class="text-2xs text-slate-700 bg-amber-50 p-2.5 rounded border border-amber-200 mb-3 print:mb-3">
						<strong>Audit observation:</strong> 74.65% of the state's industrial land acquisition (₹12,257.50 Cr) is concentrated in Kannur with no comparative economic appraisal on record (DS001 Chapter IV, Table 4.3).
					</div>
				{:else if ['Idukki', 'Pathanamthitta', 'Wayanad', 'Kasargod'].includes(district.district)}
					<div class="text-2xs text-slate-700 bg-amber-50 p-2.5 rounded border border-amber-200 mb-3 print:mb-3">
						<strong>Equity note:</strong> Bottom-4 district: below 3% share of infrastructure outlay (DS001 Table 4.2).
					</div>
				{:else if district.district === 'Thiruvananthapuram'}
					<div class="text-2xs text-slate-700 bg-blue-50 p-2.5 rounded border border-blue-200 mb-3 print:mb-3">
						<strong>Capital city note:</strong> Highest single-district infrastructure outlay ₹10,819.75 Cr = 14.02% share (DS001 Table 4.2).
					</div>
				{/if}

				<footer class="pt-2 text-2xs text-slate-500 leading-relaxed">
					<strong class="text-slate-700">Provenance standard:</strong> every figure above is cited to its official table or processed dataset row.
					Physical-milestone and benefit outcome figures for this district remain a disclosed data gap (GAP-001 / GAP-003) and are printed as gaps, not estimates.
					Generated from <code class="font-mono">data/processed/public_value_and_geography.json</code> · dashboard baseline Oct 2026.
					Reuse: Kanakku-derived content inherits CC BY 4.0 with attribution of <code class="font-mono">source_id</code>/<code class="font-mono">source_locator</code>.
				</footer>
			</article>
		{/each}
	</div>
{/if}
</div>
