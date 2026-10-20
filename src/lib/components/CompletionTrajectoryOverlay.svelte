<script lang="ts">
	/**
	 * CompletionTrajectoryOverlay.svelte — T093 (Milestone 9)
	 *
	 * Overlays actual cumulative released funds on the existing Table 6.1 debt-service
	 * schedule and Table 6.3 completion-need timeline within /financials.
	 *
	 * Shows release pace vs future fiscal need in a single comparable timeline.
	 * Stock vs flow distinction preserved per architecture.md §8.
	 *
	 * Data sources:
	 *   - Historical releases: Table 3.1 (annual MVT + Petroleum Cess transfers) — FLOW
	 *   - Debt service schedule: Table 6.1 (annual principal + interest to 2041-42) — STOCK service
	 *   - Completion phasing: Table 6.3 (annual completion need 2026-27 to 2030-31) — FLOW need
	 *   - Grand future requirement: debt service ₹47,532.54 Cr + completion ₹22,883 Cr = ₹70,415.54 Cr
	 *
	 * Key principle: overlay data strictly sourced and dated; no conflation of
	 * future commitments with outstanding debt (per architecture.md §8).
	 */

	type TransferRow = {
		year: string;
		mvt_share: number;
		petroleum_cess: number;
		total: number;
	};

	type DebtServiceRow = {
		year: string;
		principal: number;
		interest: number;
		total: number;
	};

	type CompletionPhasingRow = {
		year: string;
		amount_required: number;
	};

	let {
		t31,
		t61,
		t63
	} = $props();

	// ----------------------------------------------------------- derived series

	// Cumulative historical releases (from Table 3.1)
	const cumulativeReleases = $derived.by(() => {
		const rows = (t31.rows || []) as Array<{ year: string; total: number }>;
		const result: Array<{ year: string; annual: number; cumulative: number }> = [];
		let cum = 0;
		for (const row of rows) {
			cum += row.total;
			result.push({ year: row.year, annual: row.total, cumulative: cum });
		}
		return result;
	});

	// Debt service schedule (Table 6.1)
	const debtService = $derived.by(() => {
		return (t61.rows || []) as Array<{ year: string; principal: number; interest: number; total: number }>;
	});

	// Completion phasing (Table 6.3)
	const completionPhasing = $derived.by(() => {
		return (t63.phasing || []) as Array<{ year: string; amount_required: number }>;
	});

	// Grand totals from Table 6.3
	const grandTotals = $derived.by(() => {
		return {
			debtService: t63.grand_future_fiscal_requirement?.debt_servicing_crore || 47532.54,
			completion: t63.grand_future_fiscal_requirement?.project_completion_crore || 22883,
			total: t63.grand_future_fiscal_requirement?.total_fiscal_requirement_crore || 70415.54,
			excludesLand: t63.grand_future_fiscal_requirement?.excludes_land_acquisition || true,
			unpaidLand: t63.grand_future_fiscal_requirement?.unpaid_land_balance_crore || 11787.37
		};
	});

	// Combined future obligations timeline
	const futureTimeline = $derived.by(() => {
		const debtRows = debtService;
		const completionRows = completionPhasing;

		// Combine by year
		const yearMap = new Map<string, { debtService: number; completionNeed: number }>();

		for (const row of debtRows) {
			yearMap.set(row.year, { debtService: row.total, completionNeed: 0 });
		}
		for (const row of completionRows) {
			const existing = yearMap.get(row.year) || { debtService: 0, completionNeed: 0 };
			existing.completionNeed = row.amount_required;
			yearMap.set(row.year, existing);
		}

		// Convert to sorted array
		return Array.from(yearMap.entries())
			.map(([year, vals]) => ({ year, ...vals }))
			.sort((a, b) => a.year.localeCompare(b.year));
	});

	function formatCrore(val: number): string {
		return '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Cr';
	}
</script>

<div class="space-y-4">
	<!-- Section header -->
	<div class="bg-white rounded-lg border border-slate-200 p-4 shadow-sm">
		<h3 class="text-sm font-bold text-slate-900 mb-1">Completion Trajectory Overlay (T093)</h3>
		<p class="text-2xs text-slate-500 mb-3">
			Overlay of actual cumulative State transfers on the Table 6.1 debt-service schedule
			and Table 6.3 completion-need timeline. Stock vs flow distinction preserved.
		</p>

		<!-- Key totals row -->
		<div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs mb-4">
			<div class="bg-slate-50 p-2 rounded border border-slate-200">
				<div class="text-2xs text-slate-500">Cumulative Transfers (to 2026-27)</div>
				<div class="font-bold text-slate-900 tabular-nums">{formatCrore(cumulativeReleases[cumulativeReleases.length - 1]?.cumulative || 0)}</div>
			</div>
			<div class="bg-slate-50 p-2 rounded border border-slate-200">
				<div class="text-2xs text-slate-500">Future Debt Service (to 2041-42)</div>
				<div class="font-bold text-purple-900 tabular-nums">{formatCrore(grandTotals.debtService)}</div>
			</div>
			<div class="bg-slate-50 p-2 rounded border border-slate-200">
				<div class="text-2xs text-slate-500">Future Completion Need (to 2030-31)</div>
				<div class="font-bold text-emerald-900 tabular-nums">{formatCrore(grandTotals.completion)}</div>
			</div>
			<div class="bg-slate-50 p-2 rounded border border-slate-200">
				<div class="text-2xs text-slate-500">Grand Future Requirement</div>
				<div class="font-bold text-rose-900 tabular-nums">{formatCrore(grandTotals.total)}</div>
			</div>
		</div>

		<!-- Note on land exclusion -->
		<div class="text-2xs text-amber-700 bg-amber-50 p-2 rounded border border-amber-200 mb-3">
			<strong>Note:</strong> Grand future requirement excludes land acquisition pool (₹11,787.37 Cr unpaid balance).
			Land pool tracked separately in Table 4.5. Stock vs flow distinction maintained per architecture.md §8.
		</div>
	</div>

	<!-- Combined timeline chart -->
	<div class="bg-white rounded-lg border border-slate-200 p-4 overflow-x-auto">
		<svg
			viewBox="0 0 900 420"
			class="w-full h-auto"
			role="img"
			aria-label="Combined timeline: historical cumulative transfers, future debt service, and completion phasing"
		>
			<!-- Chart dimensions -->
			<defs>
				<linearGradient id="releaseGrad" x1="0%" y1="0%" x2="0%" y2="100%">
					<stop offset="0%" stop-color="#059669" stop-opacity="0.3" />
					<stop offset="100%" stop-color="#059669" stop-opacity="0.05" />
				</linearGradient>
				<linearGradient id="debtGrad" x1="0%" y1="0%" x2="0%" y2="100%">
					<stop offset="0%" stop-color="#7c3aed" stop-opacity="0.3" />
					<stop offset="100%" stop-color="#7c3aed" stop-opacity="0.05" />
				</linearGradient>
				<linearGradient id="completionGrad" x1="0%" y1="0%" x2="0%" y2="100%">
					<stop offset="0%" stop-color="#059669" stop-opacity="0.3" />
					<stop offset="100%" stop-color="#059669" stop-opacity="0.05" />
				</linearGradient>
			</defs>

			<!-- Chart area -->
			<rect x="70" y="30" width="780" height="320" fill="none" stroke="#e2e8f0" stroke-width="0.5" />

			<!-- Y axis -->
			<line x1="70" y1="30" x2="70" y2="350" stroke="#cbd5e1" stroke-width="1.5" />
			<!-- X axis -->
			<line x1="70" y1="350" x2="850" y2="350" stroke="#cbd5e1" stroke-width="1.5" />

			<!-- Y axis ticks and grid -->
			{#each [0, 2500, 5000, 7500, 10000, 12500, 15000] as tick}
				<g>
					<line
						x1={70} y1={350 - (tick / 15000) * 300}
						x2={850} y2={350 - (tick / 15000) * 300}
						stroke="#e2e8f0"
						stroke-width="0.5"
						stroke-dasharray="2,2"
					/>
					<line
						x1={65} y1={350 - (tick / 15000) * 300}
						x2={70} y2={350 - (tick / 15000) * 300}
						stroke="#cbd5e1"
						stroke-width="1"
					/>
					<text
						x={60}
						y={350 - (tick / 15000) * 300 + 4}
						text-anchor="end"
						font-size="9"
						fill="#64748b"
						font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
					>
						{formatCrore(tick / 100)}
					</text>
				</g>
			{/each}

			<!-- X axis (years) -->
			{#each futureTimeline as item}
				{@const x = 70 + (futureTimeline.indexOf(item) / (futureTimeline.length - 1)) * 780}
				<g>
					<line
						x1={x} y1={350}
						x2={x} y2={355}
						stroke="#cbd5e1"
						stroke-width="1"
					/>
					<text
						x={x}
						y={365}
						text-anchor="middle"
						font-size="9"
						fill="#64748b"
					>
						{item.year}
					</text>
				</g>
			{/each}

			<!-- Historical cumulative releases (area) -->
			{#if cumulativeReleases.length > 0}
				<path
					d={(() => {
						let d = `M 70 ${350 - (cumulativeReleases[0].cumulative / 15000) * 300}`;
						for (let i = 1; i < cumulativeReleases.length; i++) {
							const x = 70 + ((i - 1) / (cumulativeReleases.length - 1)) * 780;
							const y = 350 - (cumulativeReleases[i].cumulative / 15000) * 300;
							d += ` L ${x} ${y}`;
						}
						d += ` L ${70 + (cumulativeReleases.length - 1) * (780 / (cumulativeReleases.length - 1))} 350 L 70 350 Z`;
						return d;
					})()}
					fill="url(#releaseGrad)"
					stroke="#059669"
					stroke-width="2"
				>
					<title>Cumulative State transfers to KIIFB (Table 3.1)</title>
				</path>

				<!-- Historical releases line -->
				<polyline
					points={cumulativeReleases.map((r, i) => {
						const x = 70 + (i / (cumulativeReleases.length - 1)) * 780;
						const y = 350 - (r.cumulative / 15000) * 300;
						return `${x},${350 - (r.cumulative / 15000) * 300}`;
					}).join(' ')}
					fill="none"
					stroke="#059669"
					stroke-width="2.5"
				>
					<title>Cumulative transfers: {formatCrore(cumulativeReleases[cumulativeReleases.length - 1]?.cumulative || 0)} as of 2026-27</title>
				</polyline>
			{/if}

			<!-- Future debt service bars -->
			{#each futureTimeline as item, i}
				<rect
					x={70 + (i / (futureTimeline.length - 1)) * 780 - 15}
					y={350 - (item.debtService / 15000) * 300}
					width={30}
					height={(item.debtService / 15000) * 300}
					fill="url(#debtGrad)"
					stroke="#7c3aed"
					stroke-width="1"
					opacity="0.8"
				>
					<title>{item.year}: Debt service {formatCrore(item.debtService)}</title>
				</rect>
			{/each}

			<!-- Future completion need bars (stacked on top) -->
			{#each futureTimeline as item, i}
				<rect
					x={70 + (i / (futureTimeline.length - 1)) * 780 - 15}
					y={350 - ((item.debtService + item.completionNeed) / 15000) * 300}
					width={30}
					height={(item.completionNeed / 15000) * 300}
					fill="url(#completionGrad)"
					stroke="#059669"
					stroke-width="1"
					opacity="0.9"
				>
					<title>{item.year}: Completion need {formatCrore(item.completionNeed)}</title>
				</rect>
			{/each}

			<!-- Historical release annual bars -->
			{#if cumulativeReleases.length > 0}
				{#each cumulativeReleases as row, i}
					<rect
						x={70 + (i / (cumulativeReleases.length - 1)) * 780 - 10}
						y={350 - (row.annual / 15000) * 300}
						width={20}
						height={(row.annual / 15000) * 300}
						fill="#059669"
						opacity="0.7"
					>
						<title>{row.year}: Annual transfer {formatCrore(row.annual)}</title>
					</rect>
				{/each}
			{/if}

			<!-- Current year marker (2026-27) -->
			<line
				x1={70 + ((cumulativeReleases.length - 1) / (futureTimeline.length - 1)) * 780}
				y1={30}
				x2={70 + ((cumulativeReleases.length - 1) / (futureTimeline.length - 1)) * 780}
				y2={350}
				stroke="#ef4444"
				stroke-width="2"
				stroke-dasharray="4,4"
			>
				<title>Current reporting boundary: 2026-27 (end of historical data)</title>
			</line>
			<text
				x={70 + ((cumulativeReleases.length - 1) / (futureTimeline.length - 1)) * 780}
				y={25}
				text-anchor="middle"
				font-size="9"
				fill="#ef4444"
				font-weight="600"
			>
				2026-27
			</text>

			<!-- Y axis label -->
			<text
				x={20}
				y={190}
				text-anchor="middle"
				font-size="10"
				font-weight="500"
				fill="#475569"
				transform="rotate(-90, 20, 190)"
			>
				Annual ₹ Crore
			</text>

			<!-- X axis label -->
			<text
				x={460}
				y={395}
				text-anchor="middle"
				font-size="10"
				font-weight="500"
				fill="#475569"
			>
				Financial Year
			</text>
		</svg>
	</div>

	<!-- Legend -->
	<div class="flex flex-wrap gap-4 text-2xs mt-3">
		<div class="flex items-center gap-1.5">
			<span class="w-3 h-3 rounded bg-[#059669] opacity-30 border border-[#059669]"></span>
			<span class="text-emerald-700">Historical cumulative transfers (Table 3.1, FLOW)</span>
		</div>
		<div class="flex items-center gap-1.5">
			<span class="w-3 h-3 rounded bg-[#7c3aed] opacity-30 border border-[#7c3aed]"></span>
			<span class="text-purple-700">Future debt service (Table 6.1, STOCK service)</span>
		</div>
		<div class="flex items-center gap-1.5">
			<span class="w-3 h-3 rounded bg-[#059669] opacity-30 border border-[#059669]"></span>
			<span class="text-emerald-700">Future completion need (Table 6.3, FLOW need)</span>
		</div>
		<div class="flex items-center gap-1.5">
			<span class="w-3 h-3" style="background: linear-gradient(to right, #7c3aed, #059669); opacity: 0.3; border: 1px solid #7c3aed;"></span>
			<span class="text-slate-700">Combined annual obligation (debt + completion)</span>
		</div>
		<div class="flex items-center gap-1.5">
			<span style="width: 12px; height: 2px; background: #ef4444; border-top: 2px dashed #ef4444;"></span>
			<span class="text-rose-700">Current reporting boundary (2026-27)</span>
		</div>
	</div>

	<!-- Data table -->
	<div class="bg-white rounded-lg border border-slate-200 p-4 overflow-x-auto">
		<table class="w-full text-left text-xs">
			<thead class="bg-slate-50 border-b border-slate-200 text-2xs text-slate-500 uppercase">
				<tr>
					<th class="py-2 px-3">Financial Year</th>
					<th class="py-2 px-3 text-right">Hist. Transfer (Cr)</th>
					<th class="py-2 px-3 text-right">Cumul. Transfer (Cr)</th>
					<th class="py-2 px-3 text-right">Debt Service (Cr)</th>
					<th class="py-2 px-3 text-right">Completion Need (Cr)</th>
					<th class="py-2 px-3 text-right">Total Annual Obligation (Cr)</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-slate-100 font-mono tabular-nums">
				{#each futureTimeline as item, i}
					<tr class="hover:bg-slate-50">
						<td class="py-2 px-3 font-sans font-medium text-slate-800">{item.year}</td>
						<td class="py-2 px-3 text-right">
							{#if i < cumulativeReleases.length}
								{formatCrore(cumulativeReleases[i].annual)}
							{:else}
								—
							{/if}
						</td>
						<td class="py-2 px-3 text-right">
							{#if i < cumulativeReleases.length}
								{formatCrore(cumulativeReleases[i].cumulative)}
							{:else}
								{formatCrore(cumulativeReleases[cumulativeReleases.length - 1]?.cumulative || 0)}
							{/if}
						</td>
						<td class="py-2 px-3 text-right text-purple-700">{formatCrore(item.debtService)}</td>
						<td class="py-2 px-3 text-right text-emerald-700">{formatCrore(item.completionNeed)}</td>
						<td class="py-2 px-3 text-right font-bold text-rose-700">{formatCrore(item.debtService + item.completionNeed)}</td>
					</tr>
				{/each}
				<tr class="bg-slate-50 font-bold border-t-2 border-slate-300">
					<td class="py-3 px-3 font-sans">Grand Total (Future)</td>
					<td class="py-3 px-3 text-right">{formatCrore(cumulativeReleases[cumulativeReleases.length - 1]?.cumulative || 0)}</td>
					<td class="py-3 px-3 text-right">—</td>
					<td class="py-3 px-3 text-right text-purple-700">{formatCrore(grandTotals.debtService)}</td>
					<td class="py-3 px-3 text-right text-emerald-700">{formatCrore(grandTotals.completion)}</td>
					<td class="py-3 px-3 text-right text-rose-900">{formatCrore(grandTotals.total)}</td>
				</tr>
			</tbody>
		</table>
	</div>

	<!-- Provenance -->
	<div class="text-3xs text-slate-400 font-mono leading-relaxed">
		* Historical releases: Committee Table 3.1 (2016-17 to 2026-27, FLOW). Debt service: Table 6.1 (2026-27 to 2041-42, STOCK service). Completion phasing: Table 6.3 (2026-27 to 2030-31, FLOW need). Grand total: debt service ₹47,532.54 Cr + completion ₹22,883 Cr = ₹70,415.54 Cr (excl. land pool ₹11,787.37 Cr). As-of: 30 June 2026. Stock vs flow distinction preserved per architecture.md §8.
	</div>
</div>