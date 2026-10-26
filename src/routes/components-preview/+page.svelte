<script lang="ts">
	// REVIEW-ONLY page: exercises every Phase 1 component in the UX v2
	// foundation set (designsystem.md). Not linked from nav. Remove or keep
	// behind review — it renders no real data.
	import DepthToggle from '$lib/components/DepthToggle.svelte';
	import GlossaryTerm from '$lib/components/GlossaryTerm.svelte';
	import PlainBadge from '$lib/components/PlainBadge.svelte';
	import NudgeCallout from '$lib/components/NudgeCallout.svelte';
	import ChartFrame from '$lib/components/ChartFrame.svelte';
	import PageIntro from '$lib/components/PageIntro.svelte';
	import ResultCount from '$lib/components/ResultCount.svelte';
	import Button from '$lib/components/Button.svelte';
	import Card from '$lib/components/Card.svelte';
	import { depth } from '$lib/stores/depth.svelte';

	const ALL_EVIDENCE = [
		'official_record',
		'verified_outcome',
		'committee_finding',
		'analytical_inference',
		'contested_interpretation',
		'unverified_claim',
		'data_gap'
	] as const;

	const ALL_LIFECYCLE = [
		'approved',
		'tendered',
		'in_progress',
		'physically_complete',
		'handed_over',
		'operational',
		'delayed',
		'cancelled',
		'conflicting_evidence'
	] as const;

	const ALL_FLAGS = ['overdue', 'payment_vs_progress', 'cost_escalation', 'stale', 'above_approved'] as const;

	// Toy numbers for the preview chart SVG only — not real data.
	const bars = [
		{ district: 'Ernakulam', pct: 14.2 },
		{ district: 'Thiruvananthapuram', pct: 12.1 },
		{ district: 'Kozhikode', pct: 9.4 },
		{ district: 'Wayanad', pct: 1.8 }
	];
	const stateAvg = 7.1;
</script>

<svelte:head>
	<title>Component Review — UX v2 Foundations</title>
</svelte:head>

<div class="space-y-10">
	<header class="bg-slate-900 text-white rounded-lg p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
		<div>
			<h1 class="text-lg font-bold">UX v2 Component Review (dev-only)</h1>
			<p class="text-sm text-slate-300">
				Current gear: <span class="font-mono">{depth.mode}</span>
				<span class="text-slate-500">·</span> Try the switch → shared links carry <code class="font-mono text-xs">?depth=</code>
			</p>
		</div>
		<DepthToggle />
	</header>

	<!-- PageIntro -->
	<div>
		<h2 class="text-sm font-semibold uppercase tracking-wide text-slate-500 mb-3">PageIntro</h2>
		<div class="bg-white rounded-lg border border-slate-200 p-5">
			<PageIntro
				crumbs={[{ label: 'Debt & Repayments', href: '/financials' }]}
				title="Who does KIIFB owe, and when is it repaid?"
				question="Can Kerala's budget carry these repayments?"
				lead="Two sentences standing in for the page's plain-language answer. This is the 'Plain answer' slot of the page spine."
				shows={['Audited liability totals with sources', 'Year-by-year repayment schedule']}
				doesnt={['A verdict on whether the debt is wise', 'Live-updated finance department figures']}
			/>
		</div>
	</div>

	<!-- ChartFrame -->
	<div>
		<h2 class="text-sm font-semibold uppercase tracking-wide text-slate-500 mb-3">ChartFrame (toy SVG)</h2>
		<ChartFrame
			question="Where did approved money land across Kerala?"
			takeaway="Two of fourteen districts hold over a quarter of the state's approved outlay."
			howToRead="Bars show each district's share of total approved money (₹ Cr converted to %). The dashed line marks the Kerala average."
			provenance="Source: DS001, Table 4.2, as of 30 Jun 2026 · derived share calculated site-side"
			ariaNote="Bar chart of approved outlay share by district: Ernakulam 14.2%, Thiruvananthapuram 12.1%, Kozhikode 9.4%, Wayanad 1.8%; state average 7.1%."
		>
			{#snippet controls()}
				<button type="button" class="text-xs px-2.5 py-1.5 rounded border border-slate-300 bg-white hover:bg-slate-50 font-medium">
					Sort: alphabetical ⇄ largest first
				</button>
			{/snippet}
			<svg viewBox="0 0 300 120" role="img" aria-label="Toy preview chart" class="w-full max-w-md">
				<line x1="0" x2="300" y1="100" y2="100" stroke="#E2E8F0" />
				{#each bars as b, i (b.district)}
					<rect x={i * 75 + 10} y={100 - b.pct * 6} width="50" height={b.pct * 6} rx="2" fill="#4338CA" />
					<text x={i * 75 + 35} y="112" text-anchor="middle" font-size="7" fill="#64748B">{b.district}</text>
					<text x={i * 75 + 35} y={96 - b.pct * 6} text-anchor="middle" font-size="7" fill="#0F172A">{b.pct}%</text>
				{/each}
				<line x1="0" x2="300" y1={100 - stateAvg * 6} y2={100 - stateAvg * 6} stroke="#94A3B8" stroke-dasharray="4 3" />
				<text x="300" y={96 - stateAvg * 6} text-anchor="end" font-size="7" fill="#64748B">avg {stateAvg}%</text>
			</svg>
			{#snippet table()}
				<table class="text-xs font-mono">
					<thead><tr class="border-b"><th class="text-left py-1 pr-4">District</th><th class="text-right py-1">Share of outlay</th></tr></thead>
					<tbody>
						{#each bars as b (b.district)}
							<tr class="border-b border-slate-100"><td class="py-1 pr-4">{b.district}</td><td class="py-1 text-right tabular-nums">{b.pct}%</td></tr>
						{/each}
					</tbody>
				</table>
			{/snippet}
		</ChartFrame>
	</div>

	<!-- Nudges -->
	<div>
		<h2 class="text-sm font-semibold uppercase tracking-wide text-slate-500 mb-3">NudgeCallout (all three kinds — dismiss persists per session)</h2>
		<div class="space-y-3">
			<NudgeCallout kind="situate" id="preview-situate" heading="scale first, verdict later">
				A crore is ten million rupees; India writes ₹1,00,341 Cr as "one lakh crore". Before reacting to the size, compare it to a budget you know — see <a class="underline underline-offset-2 text-indigo-900 hover:text-indigo-700" href="/financials">Debt & Repayments</a>.
			</NudgeCallout>
			<NudgeCallout kind="interpret" id="preview-interpret">
				Approved is permission, not delivery. A project counted here may have zero bricks laid — check its position on the delivery ladder before concluding it is done.
			</NudgeCallout>
			<NudgeCallout kind="ask" id="preview-ask">
				This district received the smallest share. Worth asking: is that because its need is lower, or because it was overlooked?
			</NudgeCallout>
		</div>
	</div>

	<!-- PlainBadge -->
	<div>
		<h2 class="text-sm font-semibold uppercase tracking-wide text-slate-500 mb-3">PlainBadge (hover for tooltip; Evidence gear appends raw ids)</h2>
		<div class="bg-white rounded-lg border border-slate-200 p-5 space-y-4">
			<div class="flex flex-wrap gap-2">
				{#each ALL_EVIDENCE as l (l)}<PlainBadge kind="evidence" label={l} />{/each}
			</div>
			<div class="flex flex-wrap gap-2">
				{#each ALL_LIFECYCLE as l (l)}<PlainBadge kind="lifecycle" label={l} />{/each}
			</div>
			<div class="flex flex-wrap gap-2">
				{#each ALL_FLAGS as l (l)}<PlainBadge kind="flag" label={l} />{/each}
			</div>
		</div>
	</div>

	<!-- GlossaryTerm -->
	<div>
		<h2 class="text-sm font-semibold uppercase tracking-wide text-slate-500 mb-3">GlossaryTerm (inline — click the underlined words)</h2>
		<div class="bg-white rounded-lg border border-slate-200 p-5 text-sm text-slate-700 leading-relaxed max-w-3xl">
			<p>
				Sentences standing in for real page copy: the committee argues that
				<GlossaryTerm id="article_293" /> commitments cut Kerala's <GlossaryTerm id="borrowing_space" />,
				while the repayments on both <GlossaryTerm id="masala_bond" /> and the internal <GlossaryTerm id="debt_service" display="debt service" />
				load are carried by <GlossaryTerm id="revenue_hypothecation" display="hypothe­cated revenue" />.
				The claim count counts <GlossaryTerm id="crore" /> correctly — a classic failure in other coverage.
			</p>
			<p class="mt-3 text-xs text-slate-500">
				Depth-aware: in Plain gear the popover leads with the everyday meaning; in Evidence gear the technical definition comes first. Unknown ids fail loud at build time.
			</p>
		</div>
	</div>

	<!-- ResultCount -->
	<div>
		<h2 class="text-sm font-semibold uppercase tracking-wide text-slate-500 mb-3">ResultCount (+ footer pattern slot)</h2>
		<ResultCount shown={42} total={2377} noun="projects">
			<button type="button" class="font-medium text-blue-700 hover:text-blue-900 hover:underline underline-offset-2">Clear filters</button>
		</ResultCount>
	</div>

	<!-- Theming primitives (shadcn-svelte direction, designsystem.md §13) -->
	<div>
		<h2 class="text-sm font-semibold uppercase tracking-wide text-slate-500 mb-3">Theming primitives — Button variants × sizes, Card</h2>
		<div class="space-y-4">
			<div class="flex flex-wrap items-center gap-3">
				<Button variant="primary">Primary action</Button>
				<Button variant="secondary">Secondary</Button>
				<Button variant="outline">Outline</Button>
				<Button variant="ghost">Ghost</Button>
				<Button variant="destructive">Destructive</Button>
				<Button variant="primary" disabled>Disabled</Button>
			</div>
			<div class="flex flex-wrap items-center gap-3">
				<Button size="sm">Small</Button>
				<Button size="md">Medium</Button>
				<Button size="lg">Large</Button>
				<span class="text-xs text-muted-foreground">Check: hover = soft grey ring + tint change; Tab (keyboard) = bold blue focus ring; two different signals, no layout shift</span>
			</div>
			<Card>
				{#snippet header()}
					<h3 class="text-base font-semibold text-foreground">Metric card composed on Card primitive</h3>
					<p class="text-xs text-muted-foreground">Header slot owns type; footer slot owns provenance — presentation stays quiet (hairlines, not box soup)</p>
				{/snippet}
				<p class="font-mono text-3xl font-bold tabular-nums">₹31,681.15 <span class="text-sm font-medium text-muted-foreground">Cr</span></p>
				<p class="text-sm text-slate-600 mt-1">Outstanding debt <span class="text-xs text-slate-400">(stock, as of 30 Jun 2026)</span></p>
				{#snippet footer()}
					<div class="border-t border-border pt-3 -mx-5 px-5 flex items-center justify-between text-[11px]">
						<span class="font-mono text-muted-foreground">Source: DS001, Table 3.3</span>
						<Button variant="ghost" size="sm" href="/financials">Verify →</Button>
					</div>
				{/snippet}
			</Card>
			<p class="text-xs text-muted-foreground">Token check: these use semantic utilities (bg-card, border-border, text-muted-foreground) — switch to <code class="font-mono">.dark</code> in devtools on &lt;html&gt; once wired, to preview the reserved scheme.</p>
		</div>
	</div>

	<!-- Depth behaviours -->
	<div>
		<h2 class="text-sm font-semibold uppercase tracking-wide text-slate-500 mb-3">Depth behaviours to check while toggling</h2>
		<ul class="text-xs text-slate-600 list-disc pl-5 space-y-1">
			<li>Plain: provenance collapses behind "Where's this from?" — Evidence: expanded mono footer.</li>
			<li>Plain: badges only humanized — Evidence: raw snake_case id appears beside each.</li>
			<li>Gear persists across reloads; <code class="font-mono">?depth=evidence</code> in the URL wins over storage.</li>
			<li>Nudges: dismissing hides for the browser session only.</li>
			<li>Keyboard-only pass: every summary/button reachable; Esc closes the glossary popover; focus rings visible globally.</li>
		</ul>
	</div>
</div>
