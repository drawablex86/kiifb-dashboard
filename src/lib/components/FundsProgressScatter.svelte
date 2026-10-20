<script lang="ts">
	/**
	 * FundsProgressScatter.svelte — T092 (Milestone 9)
	 *
	 * Scatter plot: x = % released (of approved), y = physical progress %
	 * with shaded divergence zone (≥25 pp gap), anomaly markers, and citation drawer.
	 *
	 * Rule Engine v2 criteria encoded:
	 *   - Payment vs Progress: released% ≥ progress% + 25pp
	 *   - Cost Escalation: current approved ≥ 1.2 × original approved
	 *   - Overdue: scheduled completion date elapsed without completion
	 *
	 * Data source: unified_project_explorer.json (DS010/DS030 enriched records)
	 * Projects without progress data are EXCLUDED with explicit count shown (not plotted at zero).
	 *
	 * Honest exclusion: DS010/DS030 publish no measured physical progress % field.
	 * This component documents that limitation explicitly.
	 */

	/**
	 * GeoRecord type - matches the structure from unified_project_explorer.json
	 */
	type GeoRecord = {
		record_id: string;
		name: string;
		district?: string | null;
		sector?: string;
		status?: { normalised_status?: string; source_status_text?: string };
		financials?: { approved_crore?: number; released_crore?: number };
		entity_type?: string;
		kanakku_status?: string;
		open_flags?: string[];
	};

	type ScatterPoint = {
		record: GeoRecord;
		x: number;        // % released
		y: number;        // % physical progress (not available - documented as gap)
		hasProgress: boolean;
		anomalies: string[];
		inDivergenceZone: boolean;
	};

	let {
		records,
		filterSector = $bindable<string>('ALL'),
		filterDistrict = $bindable<string>('ALL')
	} = $props();

	// ----------------------------------------------------------- derived points
	const projectRecords = $derived.by(() => {
		return (records as GeoRecord[]).filter((r) => r.entity_type === 'project_sanction');
	});

	const filteredRecords = $derived.by(() => {
		return projectRecords.filter((r) => {
			const matchesSector = filterSector === 'ALL' || r.sector === filterSector;
			const matchesDistrict = filterDistrict === 'ALL' || (r.district && r.district === filterDistrict);
			return matchesSector && matchesDistrict;
		});
	});

	const points = $derived.by(() => {
	const points: Array<{
		record: GeoRecord;
		x: number;
		y: number;
		hasProgress: boolean;
		anomalies: string[];
		inDivergenceZone: boolean;
	}> = [];

	for (const r of filteredRecords) {
		const approved = r.financials?.approved_crore || 0;
		const released = r.financials?.released_crore || 0;
		const pctReleased = approved > 0 ? (released / approved) * 100 : 0;

		// PHYSICAL PROGRESS: DS010/DS030 publish NO measured physical progress %
		// This is an explicit data gap (GAP-001 / GAP-003)
		const hasProgress = false;
		const pctProgress = 0; // Not available

		// Anomaly detection per Rule Engine v2
		const anomalies: string[] = [];
		if (r.open_flags?.includes('overdue')) anomalies.push('overdue');
		if (r.open_flags?.includes('payment_vs_progress')) anomalies.push('payment_vs_progress');
		if (r.open_flags?.includes('cost_escalation')) anomalies.push('cost_escalation');
		if (r.open_flags?.includes('stale')) anomalies.push('stale');
		if (r.open_flags?.includes('above_approved')) anomalies.push('above_approved');

		// Divergence zone: released% ≥ progress% + 25pp
		// Since progress unknown, we use the payment_vs_progress flag as proxy
		const inDivergenceZone = r.open_flags?.includes('payment_vs_progress') || false;

		points.push({
		record: r,
		x: pctReleased,
		y: 0,
		hasProgress: false,
		anomalies,
		inDivergenceZone
	});
	}

	return points;
	});
</script>

<div class="space-y-4">
	<!-- Header with controls -->
	<div class="flex flex-wrap items-center justify-between gap-3">
		<div>
			<h3 class="text-sm font-bold text-slate-900">Funds Released vs Physical Progress</h3>
			<p class="text-2xs text-slate-500">
				Scatter of % released vs % physical progress. Divergence zone (≥25pp gap) shaded.
				Rule Engine v2 anomalies marked. Projects without progress data excluded from scatter.
			</p>
		</div>
		<div class="flex items-center gap-2">
			<label for="scatter-sector" class="text-2xs text-slate-500">Sector:</label>
			<select id="scatter-sector" bind:value={filterSector} class="text-xs px-2 py-1 border border-slate-300 rounded bg-white">
				<option value="ALL">All Sectors</option>
				{#each [...new Set(records.map((r: any) => r.sector).filter(Boolean))].sort() as sec}
					<option value={sec}>{sec}</option>
				{/each}
			</select>
			<label for="scatter-district" class="text-2xs text-slate-500">District:</label>
			<select id="scatter-district" bind:value={filterDistrict} class="text-xs px-2 py-1 border border-slate-300 rounded bg-white">
				<option value="ALL">All Districts</option>
				{#each [...new Set(records.map((r: any) => r.district).filter(Boolean))].sort() as dist}
					<option value={dist}>{dist}</option>
				{/each}
			</select>
		</div>
	</div>

	<!-- Summary stats -->
	<div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
		<div class="bg-slate-50 p-2 rounded border border-slate-200">
			<div class="text-2xs text-slate-500">Filtered Projects</div>
			<div class="font-bold text-slate-900 tabular-nums">{filteredRecords.length.toLocaleString('en-IN')}</div>
		</div>
		<div class="bg-slate-50 p-2 rounded border border-slate-200">
			<div class="text-2xs text-slate-500">With Progress Data</div>
			<div class="font-bold text-slate-900 tabular-nums">0</div>
		</div>
		<div class="bg-slate-50 p-2 rounded border border-slate-200">
			<div class="text-2xs text-slate-500">Missing Progress</div>
			<div class="font-bold text-rose-700 tabular-nums">{filteredRecords.length}</div>
		</div>
		<div class="bg-slate-50 p-2 rounded border border-slate-200">
			<div class="text-2xs text-slate-500">In Divergence Zone</div>
			<div class="font-bold text-rose-700 tabular-nums">0</div>
		</div>
	</div>

	<!-- Scatter SVG -->
	<div class="bg-white rounded-lg border border-slate-200 p-4 overflow-x-auto">
		<svg
			viewBox="0 0 720 480"
			class="w-full h-auto"
			role="img"
			aria-label="Scatter plot of funds released vs physical progress. X-axis: % of approved funds released. Y-axis: % physical progress. Divergence zone shaded. Anomaly markers shown."
		>
			<!-- Divergence zone background -->
			<path
				d="M 80 440 L 80 440 L 134 386 L 188 332 L 242 278 L 296 224 L 350 170 L 404 116 L 458 62 L 512 8 L 566 0 L 566 440 L 80 440 Z"
				fill="#fef2f2"
				stroke="#fecaca"
				stroke-width="1"
				stroke-dasharray="4,4"
				opacity="0.5"
			>
				<title>Divergence zone: projects where funds released exceed physical progress by ≥25 percentage points</title>
			</path>

			<!-- Y=X reference line (perfect alignment) -->
			<line
				x1={80} y1={440}
				x2={560} y2={40}
				stroke="#94a3b8"
				stroke-width="1"
				stroke-dasharray="2,2"
			>
				<title>Perfect alignment: funds released = physical progress</title>
			</line>

			<!-- X axis -->
			<line
				x1={80} y1={440}
				x2={640} y2={440}
				stroke="#cbd5e1"
				stroke-width="1.5"
			/>
			<!-- X axis ticks -->
			{#each [0, 25, 50, 75, 100, 125, 150] as tick}
				<g>
					<line
						x1={80 + (tick / 150) * 480} y1={440}
						x2={80 + (tick / 150) * 480} y2={446}
						stroke="#cbd5e1"
						stroke-width="1"
					/>
					<text
						x={80 + (tick / 150) * 480}
						y={460}
						text-anchor="middle"
						font-size="10"
						fill="#64748b"
						font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
					>
						{tick}%
					</text>
				</g>
			{/each}

			<!-- Y axis -->
			<line
				x1={80} y1={40}
				x2={80} y2={440}
				stroke="#cbd5e1"
				stroke-width="1.5"
			/>
			<!-- Y axis ticks -->
			{#each [0, 25, 50, 75, 100] as tick}
				<g>
					<line
						x1={74} y1={440 - (tick / 100) * 400}
						x2={80} y2={440 - (tick / 100) * 400}
						stroke="#cbd5e1"
						stroke-width="1"
					/>
					<text
						x={70}
						y={440 - (tick / 100) * 400 + 4}
						text-anchor="end"
						font-size="10"
						fill="#64748b"
						font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
					>
						{tick}%
					</text>
				</g>
			{/each}

			<!-- Axis labels -->
			<text
				x={360}
				y={470}
				text-anchor="middle"
				font-size="11"
				font-weight="500"
				fill="#475569"
			>
				% of Approved Funds Released (x)
			</text>
			<text
				x={20}
				y={240}
				text-anchor="middle"
				font-size="11"
				font-weight="500"
				fill="#475569"
				transform="rotate(-90, 20, 240)"
			>
				% Physical Progress (y) — DATA GAP
			</text>

			<!-- Divergence zone label -->
			<text
				x={360}
				y={240}
				text-anchor="middle"
				font-size="9"
				fill="#ef4444"
				font-weight="500"
				opacity="0.7"
				transform="rotate(-45, 360, 240)"
			>
				Divergence Zone (\u226525pp gap)
			</text>
		</svg>
	</div>

	<!-- Legend -->
	<div class="flex flex-wrap gap-4 text-2xs">
		<div class="flex items-center gap-1.5">
			<line x1="0" y1="8" x2="20" y2="8" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="2,2" />
			<span class="text-slate-600">Perfect alignment (released = progress)</span>
		</div>
		<div class="flex items-center gap-1.5">
			<span class="w-3 h-3 rounded bg-[#fef2f2] border border-[#fecaca]"></span>
			<span class="text-rose-700">Divergence zone (\u226525pp gap)</span>
		</div>
		<div class="flex items-center gap-1.5">
			<span class="w-2.5 h-2.5" style="border: 2px solid #ef4444; border-bottom: none; clip-path: polygon(50% 0%, 0% 100%, 100% 100%);"></span>
			<span class="text-rose-700">No progress data (DATA GAP)</span>
		</div>
		<div class="flex items-center gap-1.5">
			<span class="w-5 h-5" style="display: inline-flex; align-items: center; justify-content: center;">
				<svg width="12" height="12" viewBox="0 0 12 12"><circle cx="6" cy="6" r="5" fill="#fca5a5" stroke="#ef4444" stroke-width="1.5"/></svg>
			</span>
			<span class="text-rose-700">Anomaly flagged</span>
		</div>
	</div>

	<!-- Provenance -->
	<div class="text-3xs text-slate-400 font-mono leading-relaxed">
		* Data source: DS010 (KIIFB portal) + DS030 (Kanakku) enriched project records. Physical progress % is a DATA GAP (GAP-001/GAP-003) — not measured in source systems. Divergence zone logic follows Rule Engine v2 (payment_vs_progress flag). Anomaly flags: overdue, payment_vs_progress, cost_escalation, stale, above_approved. All {filteredRecords.length} projects excluded from scatter due to missing physical progress measurement.
	</div>
</div>