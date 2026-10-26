<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { FLAG_REGISTRY, getFlagMeta } from '$lib/data/flags';
	import PageIntro from '$lib/components/PageIntro.svelte';
	import NudgeCallout from '$lib/components/NudgeCallout.svelte';
	import PlainBadge from '$lib/components/PlainBadge.svelte';
	import ResultCount from '$lib/components/ResultCount.svelte';
	import GlossaryTerm from '$lib/components/GlossaryTerm.svelte';

	/**
	 * /flags — T102 (Milestone 10)
	 *
	 * Delay & anomaly register: a single filterable register of all open
	 * anomaly flags (overdue, payment_vs_progress, cost_escalation,
	 * stale, above_approved) with flag trend history from
	 * `change_log.json`, and per-flag provenance. Resolved flags retain
	 * their history — the register never deletes.
	 */
	let { data } = $props();

	// Filter state is URL-shared (?flag=&q=) and restores exactly.
	let flagParam = $derived(page.url.searchParams.get('flag') ?? 'ALL');
	let qParam = $derived(page.url.searchParams.get('q') ?? '');
	let showResolvedHistory = $derived(page.url.searchParams.get('history') === '1');

	function setParams(params: Record<string, string | null>) {
		const next = new URLSearchParams(page.url.searchParams);
		for (const [k, v] of Object.entries(params)) {
			if (v === null || v === '') next.delete(k);
			else next.set(k, v);
		}
		goto(`/flags?${next.toString()}`, { replaceState: true, keepFocus: true, noScroll: false });
	}

	type FlagRow = {
		flag: string;
		recordId: string;
		name: string;
		sector: string;
		district: string;
		status: string;
		sourceId: string;
		sourceLocator: string;
		asOf: string;
	};

	// Flatten every open flag on every record into register rows.
	let allFlagRows = $derived.by<FlagRow[]>(() => {
		const rows: FlagRow[] = [];
		for (const r of data.records as any[]) {
			for (const f of r.open_flags ?? []) {
				rows.push({
					flag: f,
					recordId: r.record_id,
					name: r.name,
					sector: r.sector ?? '—',
					district: r.district ?? '—',
					status: r.status?.normalised_status ?? '—',
					sourceId: r.source_id ?? '—',
					sourceLocator: r.source_locator ?? '—',
					asOf: r.status?.as_of_date ?? '2026-10'
				});
			}
		}
		return rows;
	});

	// Per-flag counts reconciled with the dataset (asserted in tests/test_flag_register.py)
	let perFlagCounts = $derived.by(() => {
		const counts = new Map<string, number>();
		for (const f of FLAG_REGISTRY) counts.set(f.id, 0);
		for (const row of allFlagRows) counts.set(row.flag, (counts.get(row.flag) ?? 0) + 1);
		return counts;
	});

	let filteredRows = $derived.by(() => {
		let rows = allFlagRows;
		if (flagParam !== 'ALL') rows = rows.filter((r) => r.flag === flagParam);
		const q = qParam.toLowerCase();
		if (q) {
			rows = rows.filter(
				(r) =>
					r.name.toLowerCase().includes(q) ||
					r.recordId.toLowerCase().includes(q) ||
					r.district.toLowerCase().includes(q) ||
					r.sector.toLowerCase().includes(q)
			);
		}
		if (flagParam === 'ALL' && !q) {
			rows = rows.slice(0, 150);
		}
		return rows;
	});

	let totalsMatch = $derived(
		FLAG_REGISTRY.reduce((sum, f) => sum + (perFlagCounts.get(f.id) ?? 0), 0) === allFlagRows.length
	);

	// Change-log trend history (resolved flags retained — never deleted)
	let historyEntries = $derived.by(() => {
		const entries: { dataset: string; added: string[]; resolved: string[] }[] = [];
		const datasets = data.changeLog.datasets as Record<string, any>;
		for (const [dataset, info] of Object.entries(datasets)) {
			const diff = (info as any).flags_added ? info : null;
			if (!diff) continue;
			const added: string[] = diff.flags_added ?? [];
			const resolved: string[] = diff.flags_resolved ?? [];
			if (added.length || resolved.length) {
				entries.push({ dataset, added, resolved });
			}
		}
		return entries;
	});

	function severityBadge(sev: string) {
		return sev === 'high'
			? 'bg-red-50 text-red-700 border-red-200'
			: sev === 'medium'
				? 'bg-amber-50 text-amber-700 border-amber-200'
				: 'bg-slate-50 text-slate-700 border-slate-200';
	}
</script>

<svelte:head>
	<title>Delay & Anomaly Register — KIIFB Accountability Dashboard</title>
</svelte:head>

<PageIntro
	title="Alerts & Delays"
	question="Which projects are delayed, over budget, or show payment-vs-progress divergence?"
	lead="Single filterable register of all open anomaly flags raised by Kanakku Rule Engine v2 (DS030) and the T092 divergence logic, with flag trend history from the T082 change log. Every flag points to the objective criterion that triggered it. Filter state is URL-shared."
	shows={[
		'Register of all open flags: overdue, payment_vs_progress, cost_escalation, stale, above_approved',
		'Objective trigger criterion printed per flag (never hidden)',
		'Flag trend history from change log — resolved flags retained, never deleted',
		'Per-flag counts reconciled with dataset totals (asserted in tests)',
		'URL-shared filter state (`?flag=&q=&history=1`)'
	]}
	doesnt={[
		'Project-level search & 7 filters (see Projects)',
		'Portfolio funnel drill-down (see Where the Money Goes)',
		'Debt amortisation schedule (see Debt & Repayments)',
		'District map (see Districts & Map)',
		'Change-over-time trends (see Change Over Time)'
	]}
/>

<NudgeCallout kind="situate" id="flags-start" heading="Register scale">
	{allFlagRows.length.toLocaleString('en-IN')} open flag rows across {FLAG_REGISTRY.length} flag types, reconciled with per-flag dataset counts (asserted in <code class="font-mono">tests/test_flag_register.py</code>). Each flag row carries its objective trigger criterion, source ID, locator, and as-of date.
</NudgeCallout>

<div class="space-y-6">
	<!-- Header -->
	<div class="bg-white rounded-lg border border-slate-200 p-6 shadow-sm">
		<div class="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200 mb-2">
			<span>Milestone 10 Register</span>
			<span>•</span>
			<span>T102</span>
		</div>
		<h2 class="text-2xl font-bold tracking-tight text-slate-900">Delay & Anomaly Register</h2>
		<p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-2xl">
			Single filterable register of all open anomaly flags raised by Kanakku Rule Engine v2 (DS030)
			and the T092 divergence logic, with flag trend history from the T082 change log. Every flag
			points to the objective criterion that triggered it. Filter state is URL-shared
			(<code class="font-mono text-2xs">?flag=&q=&history=1</code>).
		</p>
		<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mt-4">
			<div class="bg-slate-50 border border-slate-200 rounded p-3">
				<div class="text-2xs text-slate-500 uppercase font-semibold">Open flag rows</div>
				<div class="text-lg font-bold text-slate-900 tabular-nums">{allFlagRows.length.toLocaleString('en-IN')}</div>
			</div>
			{#each FLAG_REGISTRY as meta}
				<div class="bg-slate-50 border border-slate-200 rounded p-3">
					<div class="text-2xs text-slate-500 uppercase font-semibold">{meta.label}</div>
					<div class="text-lg font-bold tabular-nums {perFlagCounts.get(meta.id) === 0 ? 'text-slate-300' : 'text-amber-800'}">
						{perFlagCounts.get(meta.id) ?? 0}
					</div>
				</div>
			{/each}
		</div>
		<div class="mt-3 text-2xs text-slate-500 flex items-center gap-2">
			<span class="px-1.5 py-0.5 rounded font-semibold {totalsMatch ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-red-50 text-red-800 border border-red-200'}">
				{totalsMatch ? '✓ Reconciliation OK' : '✗ Reconciliation failure'}
			</span>
			<span class="font-mono">union of register rows = Σ per-flag counts = {allFlagRows.length.toLocaleString('en-IN')}</span>
		</div>
	</div>

	<!-- Filters -->
	<div class="bg-white rounded-lg border border-slate-200 p-4 shadow-sm">
		<ResultCount shown={filteredRows.length} total={allFlagRows.length} noun="flag rows" />
		<div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-3">
			<div>
				<label for="flag-filter" class="block text-2xs font-semibold uppercase text-slate-500 mb-1">Flag</label>
				<select
					id="flag-filter"
					value={flagParam}
					onchange={(e) => setParams({ flag: (e.currentTarget as HTMLSelectElement).value === 'ALL' ? null : (e.currentTarget as HTMLSelectElement).value })}
					class="w-full text-xs px-3 py-2 border border-slate-300 rounded bg-white"
				>
					<option value="ALL">ALL OPEN FLAGS</option>
					{#each FLAG_REGISTRY as meta}
						<option value={meta.id}>{meta.label}</option>
					{/each}
				</select>
			</div>
			<div>
				<label for="flag-q" class="block text-2xs font-semibold uppercase text-slate-500 mb-1">Search</label>
				<input
					id="flag-q"
					type="text"
					value={qParam}
					oninput={(e) => setParams({ q: (e.currentTarget as HTMLInputElement).value })}
					placeholder="Record, project, district, sector…"
					class="w-full text-xs px-3 py-2 border border-slate-300 rounded"
				/>
			</div>
			<div class="flex items-end">
				<label class="flex items-center gap-2 text-xs text-slate-700">
					<input
						type="checkbox"
						checked={showResolvedHistory}
						onchange={(e) => setParams({ history: (e.currentTarget as HTMLInputElement).checked ? '1' : null })}
					/>
					Show resolved-flag history (retained, never deleted)
				</label>
			</div>
		</div>
	</div>

	<!-- Flag trend history from change_log.json -->
	{#if showResolvedHistory}
		<div class="bg-white rounded-lg border border-slate-200 p-5 shadow-sm">
			<h3 class="text-sm font-bold text-slate-900 mb-1">Flag Trend History (T082 change log)</h3>
			<p class="text-2xs text-slate-500 mb-3">
				Flags added and resolved between the last two processed snapshots. Resolved flags retain
				their history here permanently — deletion is not permitted.
			</p>
			{#if historyEntries.length === 0}
				<NudgeCallout kind="interpret" id="flags-history-empty" heading="No flag changes in this interval">
					No flags were added or resolved between snapshot <span class="font-mono">{data.changeLog.computed_from.prev}</span>
					and <span class="font-mono">{data.changeLog.computed_from.curr}</span> — the current counts above are the
					open baseline. Resolutions will appear here as flagged records are repaired upstream.
				</NudgeCallout>
			{:else}
				<table class="w-full text-xs border-t border-slate-100">
					<caption class="sr-only">Flag additions and resolutions per dataset</caption>
					<thead class="bg-slate-50 text-2xs uppercase text-slate-500 border-b border-slate-200">
						<tr>
							<th class="px-3 py-2 text-left">Dataset</th>
							<th class="px-3 py-2 text-left">Flags added</th>
							<th class="px-3 py-2 text-left">Flags resolved (history retained)</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-slate-100">
						{#each historyEntries as h}
							<tr>
								<td class="px-3 py-2 font-mono text-2xs">{h.dataset}</td>
								<td class="px-3 py-2">{h.added.length ? h.added.join(', ') : '—'}</td>
								<td class="px-3 py-2">{h.resolved.length ? h.resolved.join(', ') : '—'}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			{/if}
			<p class="mt-3 text-3xs text-slate-400 font-mono">computed_from: {JSON.stringify(data.changeLog.computed_from)}</p>
		</div>
	{/if}

	<!-- Register table -->
	<div class="bg-white rounded-lg border border-slate-200 overflow-hidden shadow-sm">
		<div class="overflow-x-auto">
			<table class="w-full text-left text-xs text-slate-700">
				<thead class="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase text-2xs font-semibold tracking-wider">
					<tr>
						<th class="px-4 py-3">Flag</th>
						<th class="px-4 py-3">Objective trigger criterion</th>
						<th class="px-4 py-3">Record</th>
						<th class="px-4 py-3">Sector / District</th>
						<th class="px-4 py-3">Provenance</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-slate-100">
					{#each filteredRows as row}
						{@const meta = getFlagMeta(row.flag)}
						<tr class="hover:bg-slate-50/80 transition align-top">
							<td class="px-4 py-3">
								<PlainBadge label={row.flag} kind="flag" />
								<div class="mt-1">
									<PlainBadge label={meta?.severity ?? 'info'} kind="flag" />
								</div>
							</td>
							<td class="px-4 py-3 max-w-md text-2xs text-slate-600 leading-relaxed">
								{meta?.criterion ?? 'Objective criterion documented in the flag registry.'}
								<div class="font-mono text-3xs text-slate-400 mt-1">{meta?.primarySource ?? row.sourceId}</div>
							</td>
							<td class="px-4 py-3">
								<div class="font-semibold text-slate-900">{row.name}</div>
								<div class="font-mono text-3xs text-slate-400">{row.recordId} · status: {row.status}</div>
							</td>
							<td class="px-4 py-3 text-2xs text-slate-600">
								<div>{row.sector}</div>
								<div class="text-slate-400">{row.district}</div>
							</td>
							<td class="px-4 py-3 font-mono text-3xs text-slate-500">
								source_id: {row.sourceId}<br />
								source_locator: {row.sourceLocator}<br />
								as-of: {row.asOf}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
		{#if flagParam === 'ALL' && !qParam && allFlagRows.length > 150}
			<div class="bg-slate-50 px-4 py-3 border-t border-slate-200 text-2xs text-slate-500">
				Showing the first 150 of {allFlagRows.length.toLocaleString('en-IN')} register rows —
				filter by flag or search to narrow the register.
			</div>
		{/if}
		{#if filteredRows.length === 0}
			<div class="py-8 text-center text-slate-400 text-xs">No matching register rows.</div>
		{/if}
	</div>

	<!-- Provenance banner -->
	<div class="bg-slate-100 border border-slate-200 rounded-lg p-4 text-xs text-slate-600 mt-6">
		<span class="font-bold text-slate-900">Provenance:</span> Flags from DS030 Rule Engine v2 (lifecycle_status + payment_vs_progress logic) and T092 divergence zone. Change log from <code class="font-mono">scripts/diff_snapshots.py</code> (T082) computed on stable <code class="font-mono">project_id</code>/<code class="font-mono">record_id</code>. Flag registry in <code class="font-mono">src/lib/data/flags.ts</code>. Data as-of: <code class="font-mono">{data.manifest?.last_updated ?? '2026-10-21'}</code>.
	</div>
</div>