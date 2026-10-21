<script lang="ts">
	import FreshnessBadge from '$lib/components/FreshnessBadge.svelte';

	/**
	 * T094 (Milestone 9) — `/trends` time-series view.
	 *
	 * Everything is derived from `data/snapshots/` + `data/processed/change_log.json`
	 * via +page.server.ts. Every series prints its own as-of dates; timeline
	 * granularity matches available snapshots and is disclosed in the cadence
	 * banner. Coverage limitations from GAP-001 are stated everywhere they bite.
	 */

	type DistrictPoint = { district: string; releasedCrore: number; records: number };

	type SnapshotPoint = {
		run: string;
		asOfLabel: string;
		asOfDate: string;
		approvedCrore: number;
		releasedCrore: number;
		records: number;
		districtedRecords: number;
		coordRecords: number;
		flaggedRecords: number;
		statusHistogram: Record<string, number>;
		perDistrict: DistrictPoint[];
		top3SharePct: number;
	};

	let { data } = $props();
	const points = $derived(data.points as SnapshotPoint[]);
	const topDistricts = $derived(data.topDistricts as string[]);
	const migrations = $derived(
		(data.statusMigrations ?? []) as { id: string; from: string | null; to: string | null }[]
	);
	const flagTrend = $derived(
		(data.flagTrend ?? { added: 0, resolved: 0 }) as { added: number; resolved: number }
	);
	const coverage = $derived(
		(data.coverageDelta ?? {}) as { prev: number | null; curr: number | null; total: number | null }
	);

	const crore = (v: number): string =>
		'₹' + Math.round(v).toLocaleString('en-IN') + ' Cr';

	const pct = (v: number): string => v.toFixed(1) + '%';

	// ---- geometry helpers (SVG chart space, identical across charts) --------
	const W = 640;
	const H = 210;
	const PAD_L = 8;
	const PAD_R = 8;
	const PAD_T = 14;
	const PAD_B = 34;

	function xAt(i: number, n: number): number {
		if (n <= 1) return PAD_L + (W - PAD_L - PAD_R) / 2;
		return PAD_L + (i / (n - 1)) * (W - PAD_L - PAD_R);
	}

	function yAt(v: number, min: number, max: number): number {
		if (max === min) return PAD_T + (H - PAD_T - PAD_B) / 2;
		return PAD_T + (1 - (v - min) / (max - min)) * (H - PAD_T - PAD_B);
	}

	function line(pts: [number, number][]): string {
		return pts.map((c, i) => (i === 0 ? 'M' : 'L') + c[0].toFixed(1) + ',' + c[1].toFixed(1)).join(' ');
	}

	// ---- series -------------------------------------------------------------

	const fundSeries = $derived(
		points.slice().sort((a, b) => (a.run < b.run ? -1 : 1))
	);
	const fundsFlat = $derived(
		points.length >= 2 && new Set(points.map((p) => Math.round(p.releasedCrore))).size === 1
	);
	const maxApproved = $derived(Math.max(...points.map((p) => p.approvedCrore), 1));
	const maxReleased = $derived(Math.max(...points.map((p) => p.releasedCrore), 1));

	const migrationGroups = $derived.by(() => {
		const m = new Map<string, number>();
		for (const mig of migrations) {
			const key = `${mig.from ?? '—'} → ${mig.to ?? '—'}`;
			m.set(key, (m.get(key) ?? 0) + 1);
		}
		return [...m.entries()].sort((a, b) => b[1] - a[1]);
	});

	const maxMigration = $derived(Math.max(1, ...migrationGroups.map((g) => g[1])));

	const districtSeries = $derived.by(() => {
		// rows: one per top district; values per snapshot point (sorted chronologically)
		return topDistricts.map((d) => ({
			district: d,
			values: points.map((p) => p.perDistrict.find((x) => x.district === d)?.releasedCrore ?? 0)
		}));
	});
	const maxDistrictValue = $derived(
		Math.max(1, ...districtSeries.flatMap((row) => row.values))
	);

	// Y-max for the district-coverage chart (denominator = full register size).
	const coverageYMax = $derived(
		coverage.total ?? Math.max(1, ...points.map((p) => p.districtedRecords))
	);

	const barClusterW = 34;
</script>

<svelte:head>
	<title>Trends & Change History — KIIFB Accountability Dashboard</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header / cadence banner -->
	<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<div class="flex flex-col lg:flex-row lg:items-start justify-between gap-4">
			<div>
				<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200 mb-2">
					<span>T094</span>
					<span>•</span>
					<span>Derived from T082 snapshot archive + change log</span>
				</div>
				<h2 class="text-2xl font-bold tracking-tight text-slate-900">
					Trends & Change History
				</h2>
				<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-3xl">
					Every series below is recomputed exclusively from the immutable snapshot archive
					(<code class="text-[11px] bg-slate-100 px-1 rounded">data/snapshots/</code>) and the
					deterministic change log — no page-level assumptions.
				</p>
			</div>
			<FreshnessBadge sources={['DS010', 'DS030']} note="snapshot runs denoted below" />
		</div>

		<!-- Cadence disclosure (acceptance: granularity matches available snapshots, documented on-page) -->
		<div class="mt-4 rounded border border-slate-200 bg-amber-50/50 p-3 text-xs text-slate-700">
			<strong class="font-semibold">Timeline granularity.</strong>
			The archive currently holds <strong>{points.length}</strong> snapshot point{points.length === 1 ? '' : 's'}
			(cadence: monthly <code class="bg-white px-1 rounded">&lt;YYYY-MM&gt;</code>, intra-month re-runs
			<code class="bg-white px-1 rounded">__&lt;timestamp&gt;</code>):
			{points.map((p) => p.asOfLabel).join('  •  ')}.
			{#if points.length < 3}
				<span class="text-slate-600">
					With fewer than three points, series read as before/after comparisons rather than curves;
					they become monthly curves as future <code class="bg-white px-1 rounded">refresh_pipeline.py</code> runs accumulate.
				</span>
			{/if}
			<span class="block mt-1 text-slate-600">

			</span>
		</div>
	</div>

	<!-- 1. Cumulative released vs approved -->
	<section class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<h3 class="text-lg font-bold text-slate-900">Financial trajectory over snapshots</h3>
		<p class="text-xs text-slate-500 mt-0.5">
			Cumulative totals recomputed from each archived <code>kiifb_projects.json</code>. As-of dates printed at ticks.
		</p>
		{#if fundsFlat && points.length >= 2}
			<p class="mt-2 text-xs text-amber-800 bg-amber-50 border border-amber-200 rounded px-2 py-1.5">
				<strong>Honest disclosure:</strong> released funds are identical across the two current
				snapshot points because both were regenerated in <em>offline mode</em> from the pinned
				2026-10-16 baselines (T083's matching tiers changed geography, never financial values).
				The line becomes a real curve from the first <code>refresh_pipeline.py --fetch</code> snapshot
				once a DS010 financial change is detected.
			</p>
		{/if}
		<div class="mt-3 grid md:grid-cols-2 gap-4">
			<svg viewBox="0 0 {W} {H}" class="w-full" role="img" aria-label="Released funds over snapshots">
				<text x="{PAD_L}" y="10" class="fill-slate-500" font-size="9">CUMULATIVE RELEASED (₹ Cr)</text>
				<polyline
					points={line(points.map((p, i) => [xAt(i, points.length), yAt(p.releasedCrore, 0, maxReleased)]) as [number, number][])}
					fill="none" stroke="#0f766e" stroke-width="2.5"
				/>
				{#each points as p, i (p.run)}
					<circle cx={xAt(i, points.length)} cy={yAt(p.releasedCrore, 0, maxReleased)} r="4" fill="#0f766e" />
					<text x={xAt(i, points.length)} y={yAt(p.releasedCrore, 0, maxReleased) - 8} text-anchor="middle" font-size="9" class="fill-slate-700">{crore(p.releasedCrore)}</text>
					<text x={xAt(i, points.length)} y={H - 8} text-anchor="middle" font-size="8.5" class="fill-slate-500">{p.asOfDate}</text>
				{/each}
			</svg>
			<svg viewBox="0 0 {W} {H}" class="w-full" role="img" aria-label="Approved outlay over snapshots">
				<text x="{PAD_L}" y="10" class="fill-slate-500" font-size="9">CUMULATIVE APPROVED (₹ Cr)</text>
				<polyline
					points={line(points.map((p, i) => [xAt(i, points.length), yAt(p.approvedCrore, 0, maxApproved)]) as [number, number][])}
					fill="none" stroke="#9333ea" stroke-width="2.5"
				/>
				{#each points as p, i (p.run)}
					<circle cx={xAt(i, points.length)} cy={yAt(p.approvedCrore, 0, maxApproved)} r="4" fill="#9333ea" />
					<text x={xAt(i, points.length)} y={yAt(p.approvedCrore, 0, maxApproved) - 8} text-anchor="middle" font-size="9" class="fill-slate-700">{crore(p.approvedCrore)}</text>
					<text x={xAt(i, points.length)} y={H - 8} text-anchor="middle" font-size="8.5" class="fill-slate-500">{p.asOfDate}</text>
				{/each}
			</svg>
		</div>
	</section>

	<!-- 2. Coverage growth — the meaningful series today (GAP-001 tracker) -->
	<section class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<h3 class="text-lg font-bold text-slate-900">Geography coverage growth (GAP-001 tracker)</h3>
		<p class="text-xs text-slate-500 mt-0.5">
			District-attributed and geo-coordinate coverage of the 1,408-record register per snapshot
			— the direct output of the T083 matching tiers, tracked by the change engine.
		</p>
		<div class="mt-3 grid sm:grid-cols-2 gap-4">
			<div class="border border-slate-200 rounded p-4 bg-emerald-50/40">
				<div class="text-2xs text-slate-500 uppercase font-semibold">District attributed</div>
				<div class="text-2xl font-bold text-emerald-800 tabular-nums">
					{coverage.prev} → {coverage.curr}
					<span class="text-sm font-semibold text-slate-500">/ {coverage.total}</span>
				</div>
				<svg viewBox="0 0 {W} {H * 0.6}" class="w-full mt-1" role="img" aria-label="District coverage growth">
					<polyline
						points={line(points.map((p, i) => [xAt(i, points.length), yAt(p.districtedRecords, 0, coverageYMax)]) as [number, number][])}
						fill="none" stroke="#059669" stroke-width="2.5"
					/>
					{#each points as p, i (p.run)}
						<circle cx={xAt(i, points.length)} cy={yAt(p.districtedRecords, 0, coverageYMax)} r="4" fill="#059669" />
						<text x={xAt(i, points.length)} y={yAt(p.districtedRecords, 0, coverageYMax) - 7} text-anchor="middle" font-size="9" class="fill-slate-700">{p.districtedRecords} ({pct((p.districtedRecords / p.records) * 100)})</text>
						<text x={xAt(i, points.length)} y={H * 0.6 - 8} text-anchor="middle" font-size="8.5" class="fill-slate-500">{p.asOfDate}</text>
					{/each}
				</svg>
			</div>
			<div class="border border-slate-200 rounded p-4 bg-sky-50/40">
				<div class="text-2xs text-slate-500 uppercase font-semibold">GPS coordinates</div>
				{#each points as p, i (p.run)}
					<div class="{i > 0 ? 'text-sm text-slate-600' : 'text-2xl font-bold text-sky-800 tabular-nums'}">
						{p.asOfDate}: {p.coordRecords} ({pct((p.coordRecords / p.records) * 100)})
					</div>
				{/each}
				<p class="text-2xs text-slate-500 mt-2">
					Coordinates come only from DS030 GIS package joins; the district-name-mention tier deliberately
					assigns no coordinates (documented in <code>docs/matching-rules.md</code> §3.4).
				</p>
			</div>
		</div>
		<p class="mt-2 text-xs text-rose-700 bg-rose-50 border border-rose-200 rounded px-2 py-1.5">
			<strong>GAP-001 coverage limitation:</strong> district-attributed series only include
			{coverage.curr} / {coverage.total} register records ({pct(((coverage.curr ?? 0) / (coverage.total || 1)) * 100)});
			unattributed records are excluded from concentration maths, not plotted at zero.
		</p>
	</section>

	<!-- 3. Status-migration waterfall -->
	<section class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<h3 class="text-lg font-bold text-slate-900">Normalised status-migration waterfall</h3>
		<p class="text-xs text-slate-500 mt-0.5">
			Transitions observed between the two most recent snapshot runs, from the deterministic change log.
		</p>
		{#if migrationGroups.length === 0 || migrations.length === 0}
			<p class="mt-3 text-xs text-slate-700 bg-slate-50 border border-slate-200 rounded px-2 py-1.5">
				<strong>No status migrations recorded in this interval.</strong>
				Both current snapshots contain identical <code>normalised_status</code> fields per stable
				<code>project_id</code> (the only recorded change event was geography enrichment, T083).
				Waterfall structure is live — migrations appear here automatically once a DS010
				status change is snapshotted.
			</p>
		{:else}
			<div class="mt-3 space-y-2">
				{#each migrationGroups as [key, count] (key)}
					<div class="flex items-center gap-3">
						<span class="w-64 shrink-0 text-xs font-medium text-slate-700">{key}</span>
						<div class="flex-1 bg-slate-100 rounded h-4 overflow-hidden">
							<div class="h-full bg-indigo-500" style="width: {(count / maxMigration) * 100}%"></div>
						</div>
						<span class="text-xs tabular-nums text-slate-700 w-10 text-right">{count}</span>
					</div>
				{/each}
			</div>
		{/if}
		<p class="mt-2 text-2xs text-slate-400">
			As-of: {points.map((p) => p.asOfDate).join(' → ')} • source: data/processed/change_log.json (deterministic, byte-identical re-runs)
		</p>
	</section>

	<!-- 4. Anomaly-flag trend -->
	<section class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<h3 class="text-lg font-bold text-slate-900">Anomaly-flag trend</h3>
		<p class="text-xs text-slate-500 mt-0.5">
			Open flags per snapshot (<code>overdue</code>: schedule elapsed with funds unreleased), plus
			raises/resolutions recorded by the change log.
		</p>
		<div class="mt-3 flex flex-wrap items-end gap-6">
			{#each points as p (p.run)}
				<div class="text-center">
					<div class="text-2xl font-bold text-rose-700 tabular-nums">{p.flaggedRecords}</div>
					<div class="text-2xs text-slate-500">open @ {p.asOfDate}</div>
				</div>
			{/each}
			<div class="text-center pl-6 border-l border-slate-200">
				<div class="text-sm font-semibold text-slate-700 tabular-nums">+{flagTrend.added} raised / −{flagTrend.resolved} resolved</div>
				<div class="text-2xs text-slate-500">recorded by change log between latest runs</div>
			</div>
		</div>
		<p class="mt-2 text-xs text-slate-700 bg-slate-50 border border-slate-200 rounded px-2 py-1.5">
			Flag count is stable across the two current snapshots (66 overdue records both times) because
			flag sources (DS010 schedules) were unchanged between the pinned baseline and the crawl that
			fed snapshot B. Flag movements will print here as snapshots accumulate.
		</p>
	</section>

	<!-- 5. Top-3 district concentration + per-district release curves -->
	<section class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<h3 class="text-lg font-bold text-slate-900">District concentration & release curves</h3>
		<p class="text-xs text-slate-500 mt-0.5">
			Share of district-attributed released funds held by the top-3 districts per snapshot,
			and released-crore bars for the top districts.
		</p>
		<div class="mt-3 flex flex-wrap gap-4">
			{#each points as p (p.run)}
				<div class="border border-slate-200 rounded p-3 bg-slate-50">
					<div class="text-2xs text-slate-500">{p.asOfDate}</div>
					<div class="text-xl font-bold text-slate-900 tabular-nums">{pct(p.top3SharePct)}</div>
					<div class="text-2xs text-slate-600">
						top-3: {p.perDistrict.slice(0, 3).map((d) => d.district).join(', ')}
					</div>
				</div>
			{/each}
		</div>
		<p class="mt-2 text-xs text-amber-800 bg-amber-50 border border-amber-200 rounded px-2 py-1.5">
			<strong>Conflation disclosure:</strong> the concentration jump between the current points is
			driven by <em>coverage expansion</em> (T083 newly attributed ₹35,182 Cr of umbrella sanctions,
			notably the land-acquisition pool skewing Kannur/Palakkad), not by real redistribution.
			Concentration becomes a comparable series only after a snapshot pair with identical district coverage.
		</p>
		<div class="mt-4 overflow-x-auto">
			<table class="w-full text-xs">
				<thead>
					<tr class="text-left text-slate-500 border-b border-slate-200">
						<th class="py-1.5 pr-3">District</th>
						{#each points as p, i (p.run)}
							<th class="py-1.5 px-3 text-right">Released @ {p.asOfDate}</th>
						{/each}
						<th class="py-1.5 pl-3 text-right">Records @latest</th>
					</tr>
				</thead>
				<tbody>
					{#each districtSeries as row (row.district)}
						<tr class="border-b border-slate-100">
							<td class="py-1.5 pr-3 font-medium text-slate-800">{row.district}</td>
							{#each row.values as v, i (points[i].run)}
								<td class="py-1.5 px-3 text-right tabular-nums text-slate-700">
									{crore(v)}
								</td>
							{/each}
							<td class="py-1.5 pl-3 text-right tabular-nums text-slate-500">
								{points[points.length - 1].perDistrict.find((d) => d.district === row.district)?.records ?? 0}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
		<p class="mt-2 text-2xs text-slate-400">
			Multi-district umbrella sanctions are comma-joined by the matcher; released value is split evenly across credited
			districts (unit rule: <code>docs/matching-rules.md</code> — never conflate sanction with completion).
			As-of dates: {points.map((p) => p.asOfLabel).join(' • ')}
		</p>
	</section>

	<!-- About the data engine -->
	<section class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<h3 class="text-lg font-bold text-slate-900">How this page is built</h3>
		<ol class="mt-2 text-xs text-slate-700 space-y-1.5 list-decimal list-inside">
			<li><code>scripts/refresh_pipeline.py</code> extracts processed datasets (offline pinned / --fetch live crawls).</li>
			<li><code>scripts/diff_snapshots.py</code> (T082) snapshots processed state into <code>data/snapshots/&lt;run&gt;/</code>. Runs are never modified — reuse instead of overwrite.</li>
			<li>The change log (<code>data/processed/change_log.json</code>) records deltas computed only via stable IDs (<code>project_id</code>/<code>record_id</code>), documented in <code>docs/matching-rules.md</code> §3.4.</li>
			<li>This route aggregates snapshot archives + change log at prerender time. Gap-001 coverage, granularity and flat-line disclosures are stamped wherever figures could mislead.</li>
		</ol>
	</section>
</div>
