<script lang="ts">
	/**
	 * SankeyFlow.svelte — T091 (Milestone 9)
	 *
	 * Hand-built SVG Sankey diagram visualizing portfolio deployment flow
	 * by project lifecycle stage, using Kanakku's 20 lifecycle-stage field.
	 *
	 * Stages (simplified from Kanakku's 20 statuses):
	 *   1. Approved      — Project sanctioned, no ground work yet
	 *   2. Tendered      — Work put to tender / tender process started
	 *   3. Contracted    — Contract awarded / agreement executed
	 *   4. In Progress   — Active construction / execution
	 *   5. Complete      — Physically complete, awaiting handover
	 *   6. Handed Over   — Officially transferred to department
	 *   7. Operational   — Serving public / open
	 *
	 * Data source: unified_project_explorer.json (enriched with DS030 lifecycle stages)
	 * Sliceable by sector or district via parent component.
	 */

	type SankeyNode = {
		id: string;
		name: string;
		value: number;
		projects: number;
		x: number;
		y: number;
		height: number;
	};

	type SankeyLink = {
		source: string;
		target: string;
		value: number;
		projects: number;
		path: string;
	};

	type GeoRecord = {
		record_id: string;
		name: string;
		district?: string | null;
		sector?: string;
		status?: { normalised_status?: string; source_status_text?: string };
		financials?: { approved_crore?: number; released_crore?: number };
		entity_type?: string;
		kanakku_status?: string;
	};

	let {
		records,
		filterSector = $bindable<string>('ALL'),
		filterDistrict = $bindable<string>('ALL')
	} = $props();

	// ----------------------------------------------------------- lifecycle stages
	// Map Kanakku's 20 statuses to 7 Sankey stages
	const STAGE_ORDER = [
		'Approved',
		'Tendered',
		'Contracted',
		'In Progress',
		'Complete',
		'Handed Over',
		'Operational'
	];

	const STAGE_COLORS: Record<string, string> = {
		'Approved': '#94a3b8',       // Slate
		'Tendered': '#38bdf8',       // Sky
		'Contracted': '#60a5fa',     // Blue
		'In Progress': '#a5b4fc',    // Indigo
		'Complete': '#22d3ee',       // Cyan
		'Handed Over': '#5eead4',    // Teal
		'Operational': '#34d399'     // Emerald
	};

	const STATUS_TO_STAGE: Record<string, string> = {
		// Kanakku statuses -> Sankey stage
		'Project Approved': 'Approved',
		'Project Under Evaluation': 'Approved',
		'Project Created': 'Approved',
		'Project Initiated': 'Approved',
		'Design Basis Report Created': 'Approved',
		'Design Basis Report Approved': 'Approved',
		'WBS Approval Created': 'Approved',
		'WBS Base Zero Approved': 'Approved',
		'WBS Base One Approved': 'Approved',
		'Technical Sanction Created': 'Tendered',
		'Technical Sanction Completed': 'Tendered',
		'Tender Created': 'Tendered',
		'Tender Completed': 'Tendered',
		'Contract Process Created': 'Contracted',
		'Contract Process Completed': 'Contracted',
		'Project Execution Document Stage 1 Created': 'Contracted',
		'Project Execution Document Stage 1 Approved': 'Contracted',
		'Project Execution Document Stage 2 Initiated': 'In Progress',
		'Project Execution Document Stage 2 Approved': 'In Progress',
		'Submitted for Confirmation by KIIFB': 'In Progress',
		'Return to SPV': 'In Progress',
		'Payment milestone finalization pending base 0': 'In Progress',
		'Payment milestone finalization pending base 1': 'In Progress',
		// Normalised statuses from KIIFB portal
		'approved': 'Approved',
		'tendered': 'Tendered',
		'in_progress': 'In Progress',
		'physically_complete': 'Complete',
		'handed_over': 'Handed Over',
		'operational': 'Operational',
		'delayed': 'In Progress',
		'cancelled': 'Approved'
	};

	// ------------------------------------------------------------ derived data
	const filteredRecords = $derived.by(() => {
		return (records as GeoRecord[]).filter((r) => {
			if (r.entity_type !== 'project_sanction') return false;
			const matchesSector = filterSector === 'ALL' || r.sector === filterSector;
			const matchesDistrict = filterDistrict === 'ALL' || (r.district && r.district === filterDistrict);
			return matchesSector && matchesDistrict;
		});
	});

	const stageData = $derived.by(() => {
		const stageMap = new Map<string, { value: number; projects: Set<string> }>();

		// Initialize all stages
		for (const stage of STAGE_ORDER) {
			stageMap.set(stage, { value: 0, projects: new Set() });
		}

		for (const r of filteredRecords) {
			let stage: string | null = null;

			// Prefer Kanakku status if available
			if (r.kanakku_status) {
				stage = STATUS_TO_STAGE[r.kanakku_status] || null;
			}

			// Fallback to normalised status
			if (!stage && r.status?.normalised_status) {
				stage = STATUS_TO_STAGE[r.status.normalised_status] || null;
			}

			// Fallback to source status text
			if (!stage && r.status?.source_status_text) {
				stage = STATUS_TO_STAGE[r.status.source_status_text] || null;
			}

			if (stage && stageMap.has(stage)) {
				const approved = r.financials?.approved_crore || 0;
				const released = r.financials?.released_crore || 0;
				// Use approved outlay as the flow value (stock), released as secondary
				stageMap.get(stage)!.value += approved;
				stageMap.get(stage)!.projects.add(r.record_id);
			}
		}

		return STAGE_ORDER.map((name) => {
			const data = stageMap.get(name)!;
			return { name, value: data.value, projects: data.projects.size };
		}).filter((s) => s.projects > 0 || s.value > 0);
	});

	// ----------------------------------------------------------- layout
	const PADDING_TOP = 60;
	const PADDING_BOTTOM = 40;
	const PADDING_LEFT = 160;
	const PADDING_RIGHT = 160;
	const NODE_WIDTH = 32;
	const NODE_GAP = 18;
	const LINK_CURVATURE = 0.5;

	const svgWidth = $derived(800);
	const svgHeight = $derived(480);

	const availableHeight = $derived(svgHeight - PADDING_TOP - PADDING_BOTTOM);
	const totalProjects = $derived(stageData.reduce((sum, s) => sum + s.projects, 0));
	const totalValue = $derived(stageData.reduce((sum, s) => sum + s.value, 0));

	const nodes = $derived.by(() => {
		// Position nodes horizontally across the diagram
		const stageCount = stageData.length;
		const stageSpacing = (svgWidth - PADDING_LEFT - PADDING_RIGHT) / Math.max(1, stageCount - 1);

		return stageData.map((stage, i) => {
			const x = PADDING_LEFT + i * stageSpacing;
			// Vertical centering based on cumulative flow
			// For simplicity, center each node vertically
			const y = svgHeight / 2;
			return {
				id: stage.name.toLowerCase().replace(/\s+/g, '-'),
				...stage,
				x,
				y,
				height: Math.max(30, (stage.projects / Math.max(1, totalProjects)) * availableHeight * 0.8)
			};
		});
	});

	const links = $derived.by(() => {
		const result: SankeyLink[] = [];
		for (let i = 0; i < nodes.length - 1; i++) {
			const source = nodes[i];
			const target = nodes[i + 1];
			// Flow value is the minimum of source and target (conservative)
			const value = Math.min(source.value, target.value);
			const projects = Math.min(source.projects, target.projects);
			if (value > 0 || projects > 0) {
				result.push({
					source: source.name,
					target: target.name,
					value,
					projects,
					path: generateLinkPath(source, target)
				});
			}
		}
		return result;
	});

	function generateLinkPath(source: SankeyNode, target: SankeyNode): string {
		const sourceRight = source.x + NODE_WIDTH;
		const targetLeft = target.x;
		const midX = sourceRight + (targetLeft - sourceRight) * LINK_CURVATURE;

		const sourceY = source.y;
		const targetY = target.y;
		const sourceH = source.height;
		const targetH = target.height;

		// Link flows from center of source node to center of target node
		// with vertical spread based on flow proportion
		const y1 = sourceY;
		const y2 = targetY;

		return `M ${sourceRight} ${y1} C ${midX} ${y1}, ${midX} ${y2}, ${targetLeft} ${y2}`;
	}

	function formatCrore(val: number): string {
		return '₹' + val.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' Cr';
	}

	function formatNumber(val: number): string {
		return val.toLocaleString('en-IN');
	}

	// ------------------------------------------------------------ animation
	let visible = $state(true);

	function toggleVisibility() {
		visible = !visible;
	}
</script>

<div class="space-y-4">
	<!-- Header with controls -->
	<div class="flex flex-wrap items-center justify-between gap-3">
		<div>
			<h3 class="text-sm font-bold text-slate-900">Portfolio Deployment Flow (Sankey)</h3>
			<p class="text-2xs text-slate-500">
				Flow of approved capital through Kanakku lifecycle stages. Sliceable by sector/district.
			</p>
		</div>
		<div class="flex items-center gap-2">
			<label for="sankey-sector" class="text-2xs text-slate-500">Sector:</label>
			<select id="sankey-sector" bind:value={filterSector} class="text-xs px-2 py-1 border border-slate-300 rounded bg-white">
				<option value="ALL">All Sectors</option>
				{#each Array.from(new Set(records.map((r: any) => r.sector).filter(Boolean))).sort() as sec}
					<option value={sec}>{sec}</option>
				{/each}
			</select>
			<label for="sankey-district" class="text-2xs text-slate-500">District:</label>
			<select id="sankey-district" bind:value={filterDistrict} class="text-xs px-2 py-1 border border-slate-300 rounded bg-white">
				<option value="ALL">All Districts</option>
				{#each Array.from(new Set(records.map((r: any) => r.district).filter(Boolean))).sort() as dist}
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
			<div class="text-2xs text-slate-500">Approved Capital</div>
			<div class="font-bold text-slate-900 tabular-nums">{formatCrore(filteredRecords.reduce((sum, r) => sum + (r.financials?.approved_crore || 0), 0))}</div>
		</div>
		<div class="bg-slate-50 p-2 rounded border border-slate-200">
			<div class="text-2xs text-slate-500">Released Capital</div>
			<div class="font-bold text-slate-900 tabular-nums">{formatCrore(filteredRecords.reduce((sum, r) => sum + (r.financials?.released_crore || 0), 0))}</div>
		</div>
		<div class="bg-slate-50 p-2 rounded border border-slate-200">
			<div class="text-2xs text-slate-500">Stages with Flow</div>
			<div class="font-bold text-slate-900 tabular-nums">{nodes.length}</div>
		</div>
	</div>

	{#if visible}
		<!-- Sankey SVG -->
		<div class="bg-white rounded-lg border border-slate-200 p-4 overflow-x-auto">
			<svg
				viewBox="0 0 {svgWidth} {svgHeight}"
				class="w-full h-auto"
				role="img"
				aria-label="Sankey diagram showing portfolio deployment flow through lifecycle stages"
			>
				<!-- Links (draw first so they appear behind nodes) -->
				{#each links as link}
					<path
						d={link.path}
						stroke="currentColor"
						stroke-width={Math.max(2, (link.value / Math.max(1, totalValue)) * 60)}
						fill="none"
						stroke-linecap="round"
						opacity="0.6"
						style="color: {STAGE_COLORS[link.source]}"
					>
						<title>
							{link.source} → {link.target}
							Flow: {formatCrore(link.value)}
							Projects: {link.projects}
						</title>
					</path>
				{/each}

				<!-- Nodes -->
				{#each nodes as node}
					<g class="cursor-pointer" tabindex="0" role="button"
						aria-label="{node.name} stage: {formatCrore(node.value)} approved across {node.projects} projects"
						onclick={() => console.log(node.name, node.value, node.projects)}
						onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); console.log(node.name, node.value, node.projects); } }}>
						<!-- Node body -->
						<rect
							x={node.x}
							y={node.y - node.height / 2}
							width={NODE_WIDTH}
							height={node.height}
							rx={4}
							fill={STAGE_COLORS[node.name]}
							opacity="0.9"
							stroke="#ffffff"
							stroke-width="1.5"
						/>
						<!-- Node label (name) -->
						<text
							x={node.x + NODE_WIDTH / 2}
							y={node.y - node.height / 2 - 8}
							text-anchor="middle"
							font-size="11"
							font-weight="600"
							fill="#0f172a"
						>
							{node.name}
						</text>
						<!-- Node value (₹ Cr) -->
						<text
							x={node.x + NODE_WIDTH / 2}
							y={node.y + node.height / 2 + 16}
							text-anchor="middle"
							font-size="10"
							font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
							style="font-variant-numeric: tabular-nums;"
							fill="#475569"
						>
							{formatCrore(node.value)}
						</text>
						<!-- Project count -->
						<text
							x={node.x + NODE_WIDTH / 2}
							y={node.y + node.height / 2 + 28}
							text-anchor="middle"
							font-size="9"
							fill="#64748b"
						>
							{node.projects} projects
						</text>
					</g>
				{/each}
			</svg>
		</div>

		<!-- Legend -->
		<div class="flex flex-wrap gap-3 text-2xs">
			{#each STAGE_ORDER as stage}
				{#if nodes.some(n => n.name === stage)}
					<div class="flex items-center gap-1.5" style="color: {STAGE_COLORS[stage]}">
						<span class="w-2.5 h-2.5 rounded" style="background-color: {STAGE_COLORS[stage]}"></span>
						<span>{stage}</span>
					</div>
				{/if}
			{/each}
		</div>
	{:else}
		<div class="text-center text-slate-500 py-8">Diagram hidden — click to show</div>
	{/if}

	<!-- Provenance -->
	<div class="text-3xs text-slate-400 font-mono leading-relaxed">
		* Data source: DS010 (KIIFB portal) + DS030 (Kanakku) enriched lifecycle stages. Kanakku's 20 statuses mapped to 7 deployment stages per T091 mapping table. Approved capital (stock) used as flow value; released capital shown in summary. Stage mapping documented in component source.
	</div>
</div>