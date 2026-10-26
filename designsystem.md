# UX & Design System v2 — KIIFB Accountability Dashboard (`designsystem.md`)

> **Status:** Operational spec for the *UX Rework* (two-persona depth model). This file **extends and depends on `design-system.md`** — the palette, badge tints, typography, Indian financial notation, and provenance component patterns in `design-system.md` §2–§4 remain canonical and unchanged. Everything here is additive: how content is *layered, humanized, signified, and explained* for two kinds of readers.

---

## 1. The two readers (personas)

### 1.1 Meera — the curious citizen (Layperson)

- **Who:** 34, reads newspapers about KIIFB debt, runs a small business. No finance, engineering, or statistics background. May miss a day's news but is not naive.
- **What she wants:** "What is KIIFB? How much money is involved? Is my district getting anything? Which parts of the committee's report hold up?"
- **What blocks her today:** insider labels (`Assertions`, `Portfolio Funnel`, `GAP-001`, `payment_vs_progress`), raw codes shown as `committee_finding`, charts with no "how to read this", no sense of scale, no answer to *compared to what*.
- **Risk profile:** she can be *misled by incompleteness* (reading "approved" as "built") or *dismissed by density* (leaves the site). The design must make honest reading the path of least resistance.
- **Design response:** plain-language answer first, definitions exactly at the word that confuses her, thought nudges to situate scale, humanized badges, and an always-visible "what this page cannot tell you."

### 1.2 Dr. Rajan — the data expert (Verifier)

- **Who:** journalist, researcher, auditor, or policy analyst. Transactional: verify, extract, cite.
- **What he wants:** "Where is this figure from? What exactly is the locator (table/page)? What's the as-of date? Can I download the record set? How is this derived number calculated?"
- **What blocks him today:** provenance is present but scattered (small mono footers, hidden behind hovers); no single consistent affordance for "show me the evidence"; jargon humanization could *hide* the exact taxonomy IDs he needs to cross-reference.
- **Risk profile:** he does not want to be *dumbed down to* or forced to hunt. Depth must be one consistent gesture away.
- **Design response:** Evidence view surfaces locator strings, raw taxonomy IDs, formulas, exports. The **same page, same URL**, instant gear change.

### 1.3 One page, two gears

There is no separate "lite site". A single **depth switch** (`Plain English ⇄ Evidence`) re-renders the same content in the right key for each reader. Rules:

1. **Plain is lossy but never false.** Hiding provenance in Plain mode never changes a number's value, never converts a data gap into a zero, and never softens a contested interpretation into a fact.
2. **Evidence changes presentation, not facts.** It restores machine vocabulary (IDs, locators, checksums) and expands derived-metric formulas.
3. **Gear is remembered**, per browser (`localStorage`), overridable by `?depth=` in the URL for shareable links, and defaults to `plain` for first-time visitors.

---

## 2. Principles — Norman & IxDF mapped to rules on this site

These are the "UI Truths" of the rework; component reviewers check screens against this table.

| # | Principle (Norman / IxDF) | Binding rule for this dashboard |
|---|---|---|
| P1 | **Signifiers** | Every interactive element visibly announces itself: clickable cards carry an explicit `View evidence →` affordance; glossary terms are dotted-underlined with an `ⓘ` marker; toggles look like segmented switches; nav shows the current location as a filled pill. "Click to inspect" hints in tiny gray text are **forbidden** as the only signifier. |
| P2 | **Affordances** | Real `<button>`, `<a>`, `<details>` elements everywhere. `role="button" tabindex="0"` divs are tolerated only in legacy SVG charts and must be queued for replacement. Hover/active/focus states always change the visual in ≥2 ways (e.g. shadow + border). |
| P3 | **Mapping** | Navigation order mirrors the real-world lifecycle of the money: Background → Projects → Where money goes → Debt → Districts → Time → Alerts → Claims → Verify. Filters sit directly above the lists they filter. Map controls map spatially (north = up = Kerala's north). |
| P4 | **Feedback** | Every action responds immediately and visibly: filter changes update a live "Showing N of M" count; drawers animate and dim the backdrop; copy/share actions confirm ("Copied") for ≥2s; charts' data-table toggles announce state. Never leave an action without an effect the reader can see. |
| P5 | **Conceptual model** | One page spine everywhere: **Question → Plain answer → Evidence → Verify → Before-you-conclude → Next question.** One vocabulary everywhere (§5). If a reader learns one page, they've learned the site. |
| P6 | **Constraints** | Filters that cannot apply are disabled *with a stated reason*. Missing data renders as an explicit GAP, never zero (inherited from `design-system.md` core truth 3). In Plain mode, machine identifiers are hidden — a constraint in the reader's favour. |
| P7 | **Gulf of execution** | Every page opens by answering "what can I do here?" (page intro + primary action). |
| P8 | **Gulf of evaluation** | Every page (and every chart via ChartFrame) closes by answering "what did I just learn, and what does it *not* mean?" (takeaways + "Before you conclude…" footer). |
| P9 | **Progressive disclosure** | Defaults are simple; complexity is one visible click away (`<details>`, "Show full 7-stage flow", "View as data table"). Anything buried must have a visible, labelled door. |
| P10 | **Recognition over recall** | No code is ever memorized to use the site: `payment_vs_progress` renders as "Money paid, work not done", with its raw id shown only in Evidence mode. |
| P11 | **Information scent** | Nav labels and chart question-titles describe the *content's answer*, not the tool. Every nav item and chart heading lets the reader predict what they'll get before committing. |
| P12 | **Consistency & standards** | Badge tints keep their fixed semantics from `design-system.md` §2.2–2.3. One tint = one meaning site-wide; nudges use a single reserved treatment (§7) so they never masquerade as badges. |
| P13 | **Hick's law** | First-visit choice is small: the home page offers 5 questions, not 10 pages. Nav is grouped (§4). |
| P14 | **Fitts's law / AC[16:8]** | Primary targets ≥44px tall on touch; row actions ≥40px; drawers close via backdrop click, Esc, and an ✕ button within thumb reach. |

---

## 3. The depth (two-gear) system — contract

### 3.1 Mode definition

| | `plain` (default) | `evidence` |
|---|---|---|
| Labels | Humanized ("Committee finding") | Humanized **+ raw id** in mono (`committee_finding`) — experts keep the shortcut |
| Provenance footers | Collapsed behind a labelled `Where's this from?` disclosure | Always expanded, includes source id, table/page locator, as-of date |
| Glossary popovers | Show `plain` definition first | Show `expert` definition first (plain still below it) |
| Charts | Simplified-first rendering inside ChartFrame; "How to read this" visible | Full-complexity rendering allowed as default; table toggle still available |
| Metadata rows (checksums, record ids, normalisation rules) | Hidden behind disclosures | Visible |
| Nudges | Fully expanded callouts | Reduced to one-line footnotes (content unchanged) |
| Exports/CSV links | Behind "Download & verify" disclosure | Visible inline |

### 3.2 Implementation contract

- Module: `src/lib/stores/depth.svelte.ts` (Svelte 5 runes module), exports `depth` (reactive), `setDepth(mode)`, `initDepth()`.
- Persistence: `localStorage['kiifb-depth']`; URL param `?depth=evidence|plain` wins over storage; `setDepth` writes both (URL via `history.replaceState`, so shared links carry the gear).
- Hydration: `initDepth()` runs in the browser only; server render assumes `plain` (prerendered pages stay valid for both gears).
- The switch (`DepthToggle.svelte`) renders as a segmented control with `aria-pressed` on the active segment and a `role="group"` label: "Information depth".

### 3.3 Reviewer test

For any screen, both gear states must pass: *"Nothing in Plain mode is false; nothing in Evidence mode is missing."*

---

## 4. Information architecture

### 4.1 Route map (old → new)

| Group | New nav label | Route | Old label | One-line scent (hover description) |
|---|---|---|---|---|
| Start | Start Here | `/` | *(new)* | What this site is, and five questions it can answer |
| Start | Background: What is KIIFB | `/genesis` | KIIFB Genesis | How KIIFB was created, what it borrows against, and the theory behind it |
| Follow | Projects | `/projects` | Project Explorer | Search every sanctioned project: money, status, district, evidence |
| Follow | Where the Money Goes | `/portfolio` | Portfolio Funnel | Follow ₹100 of approved money through the delivery pipeline |
| Follow | Debt & Repayments | `/financials` | Financials | Who KIIFB owes, on what terms, and the repayment schedule to 2041 |
| Follow | Districts & Map | `/outcomes` | Outcomes & Map | Where the money landed across Kerala — and what we still can't measure |
| Watch | Change Over Time | `/trends` | Trends | What the numbers looked like at earlier snapshots, and what changed |
| Watch | Alerts & Delays | `/flags` | Flag Register | Projects with overdue, cost-rise, or paid-but-idle indicators |
| Claims | The Committee's Claims | `/committee` | Committee Scrutiny | Who wrote the Oct 2026 report, and how its findings hold up |
| Claims | Recommendations & Law | `/governance` | Governance | What the committee asked for, legal positions, and contractor liability |
| Verify | Glossary & Sources | `/glossary` | *(new)* | Every term in plain words; every source with its locator and licence |

- The five **key assertions** (`committee_assertions.json`) live as a card section on `/` under "The Committee's Claims — checked against the record", and remain linked from `/committee`.
- Grouped nav (desktop: dropdown per group; mobile: accordion) with the labels above. Active route: filled pill + `aria-current="page"`.
- Every nav link includes its scent line as a hover/focus description (and as a visible one-liner in the open dropdown).

### 4.2 Standard page template (the spine)

1. **Breadcrumb** — `Home / {Page}` (sr-labelled nav; also the way back).
2. **Question title (h1)** — the page's plain-language question, e.g. *"Who does KIIFB owe, and when is it repaid?"*.
3. **Plain answer** — 1–3 sentences answering that question, with evidence badge(s).
4. **Page intro panel** — "On this page / Not on this page (yet)" (`PageIntro`), incl. the honest-gap list.
5. **Evidence body** — sections/charts/tables, each under its own ChartFrame question.
6. **Nudges** — Situation/Interpret/Ask callouts at point of use (§6).
7. **"Before you conclude…" footer** — 2–3 bullets: valid takeaways, over-read risks, links to verify.
8. **Next questions** — 2–3 forward links (the site maps itself).

### 4.3 Tabs

In-page tabs get URL state (`?tab=`) so a tab is shareable/reload-safe, keyboard arrow-key navigation, and each tab's button reads in plain words (`Who we owe`, not `Debt Structure`).

---

## 5. Vocabulary system

Humanization lives in **`src/lib/data/vocabulary.ts`** as the single source of truth (`PlainBadge` consumes it). Raw strings remain in the data JSON; the UI never displays a raw snake_case id in Plain mode.

### 5.1 Evidence labels → humanized

| Raw | Humanized | Tooltip gist (authoritative wording lives in `vocabulary.ts`) |
|---|---|---|
| `official_record` | Official record | Published in an official/statutory document we hold |
| `verified_outcome` | Independently verified | Checked against more than one record |
| `committee_finding` | Committee finding | Claim from the Oct 2026 report — treated as a claim |
| `analytical_inference` | Calculated estimate | Derived by this dashboard; formula disclosed |
| `contested_interpretation` | Disputed interpretation | More than one reasonable reading exists |
| `unverified_claim` | Unverified claim | Media/official statement, not corroborated by held documents |
| `data_gap` | Data gap | Nobody publishes this — shown as a gap, never zero |

### 5.2 Lifecycle labels → humanized

`approved`→Approved · `tendered`→Tendered · `in_progress`→In progress · `physically_complete`→Physically complete · `handed_over`→Handed over · `operational`→Operational (in use) · `delayed`→Delayed · `cancelled`→Cancelled · `conflicting_evidence`→Sources disagree. Each tooltip carries the one-line meaning from the badges map.

### 5.3 Flag triggers → humanized

| Raw | Humanized |
|---|---|
| `overdue` | Overdue |
| `payment_vs_progress` | Money paid, work not done |
| `cost_escalation` | Cost rose above approval |
| `stale` | Record not refreshed recently |
| `above_approved` | Spending above approved cost |

### 5.4 Glossary contract (`src/lib/data/glossary.ts`)

```ts
type GlossaryEntry = {
  id: string;        // stable slug, e.g. 'article_293'
  term: string;      // canonical/expert term
  plain: string;     // ≤ 40 words, no jargon
  expert: string;    // technical definition, cites locator/framework where possible
  why: string;       // why it matters *on this site*, one sentence
  seeAlso?: string[];// related glossary ids
};
```

- Rendered inline by `GlossaryTerm` (popover) and browsable at `/glossary` (search + A–Z).
- Register any jargon that survives into page copy here; if a term can't get a plain definition, the term is the problem — rewrite the copy.
- Units (`Cr`, `Lakh`), dates policy (`as-of`), and stock/flow discipline remain as in `design-system.md` §3.2 and are themselves glossary entries.

---

## 6. Thinking nudges

Nudges sit **at the point of use** — under the number or chart they qualify — and are dismissible per browser session. They are notes (`role="note"`), never buttons that change data.

### 6.1 Taxonomy

| Kind | Kind label | Question it answers | Copy pattern |
|---|---|---|---|
| `situate` | **Situate** | "How big is this, really? Compared to what?" | Anchor to a familiar baseline: budgets, school buildings, national figures. Never invent a comparison not derivable from held data. |
| `interpret` | **Interpret carefully** | "What could this be misread as?" | State the tempting wrong reading, then the disciplined one: "Approved is permission, not delivery — see the delivery ladder." |
| `ask` | **Worth asking** | "What's the next question this data raises?" | End with a question + a link. Forward motion, not verdicts. |

### 6.2 Rules

- One nudge per chart/section; ≤2 sentences each; no ranking of "importance".
- Shared visual treatment (soft indigo, left rule, icon by kind) — deliberately **not** badge-tinted, so nudges can't be confused with evidence states.
- Page-level footer nudge block is titled **"Before you conclude…"** and always has ≥1 `interpret` bullet.
- Nudge copy is *authored*, stored alongside page data (later: per-chart fields in the data JSONs), never generated from numbers.

---

## 7. Visualization rework — ChartFrame rules

Every visualization is wrapped by `ChartFrame.svelte` with this narrative order:

1. **Question title** — the chart is the answer's body; the title asks the question ("Has approved money actually reached districts?").
2. **Key takeaway** — one sentence with the number in it ("41.6% of outlay went to 3 of 14 districts").
3. **"How to read this"** — one-liner for the visual encoding ("Thicker ribbon = more money").
4. **Chart** — the existing component, unchanged data logic.
5. **View as data table** — `<details>` toggle; the table is the a11ytractive text alternative and the expert's extraction path.
6. **Provenance footer** — `Where's this from?` in Plain mode; expanded source/locator/as-of in Evidence mode.

### Simplify-first patterns

- **Sankey** → default 3-step summary (Approved → In progress → Operational); full 7-stage flow behind "Show full lifecycle".
- **Trajectory overlay** (future to 2041) → default shows history + next FY; full schedule behind a disclosure.
- **Scatter (funds vs progress)** → leads with the gap ("We can't plot progress honestly yet — it isn't published"), then charts the funds axis. *The missing chart is itself the chart* — generalize this honesty pattern.
- **Bars** → add a state-average reference line and label it ("Kerala average 7.1%") so every bar is self-situating.

### Chart accessibility

- Charts keep `role="img"` + title; ChartFrame adds the takeaway as visible text (sighted + SR) and the table toggle as the data alternative. Interactive SVG nodes stay keyboard operable.

---

## 8. Component specs (Phase 1 set)

All components: TypeScript props, Svelte 5 runes, Tailwind utility styling only, zero new dependencies.

| Component | File | Purpose / obligations |
|---|---|---|
| `DepthToggle` | `src/lib/components/DepthToggle.svelte` | Segmented `Plain English ⇄ Evidence` control; `initDepth()` on mount; `aria-pressed`; persists via `setDepth`. |
| `Depth store` | `src/lib/stores/depth.svelte.ts` | Reactive `depth.mode`; `localStorage['kiifb-depth']`; URL `?depth=` read on init, written on `setDepth`; SSR-safe (browser guards). |
| `GlossaryTerm` | `src/lib/components/GlossaryTerm.svelte` | Inline dotted-term `<details>` popover (no JS-portal needed): term kind, plain/expert definition ordered by depth, "why here", link to `/glossary#id`. Esc closes. Unknown id falls back to visible raw text (build-time guard). |
| `PlainBadge` | `src/lib/components/PlainBadge.svelte` | Renders evidence/lifecycle/flag label humanized; `title` = authoritative description; Evidence mode appends raw id in mono. Centralizes the tint map. |
| `NudgeCallout` | `src/lib/components/NudgeCallout.svelte` | Kind-labeled indigo note (`situate`/`interpret`/`ask`), optional dismiss (sessionStorage), `role="note"`. |
| `ChartFrame` | `src/lib/components/ChartFrame.svelte` | Wraps a visualization with question/takeaway/how-to-read/table toggle/provenance per §7; depth-aware footer; `aria-label` from question. |
| `PageIntro` | `src/lib/components/PageIntro.svelte` | Breadcrumb + h1 + standing question + lead + "On this page / Not on this page (yet)" panel. |
| `ResultCount` | `src/lib/components/ResultCount.svelte` | "Showing N of M records" with `aria-live="polite"` `role="status"`, tabular numerals; used above every filterable list. |

---

## 9. Visual language: signifiers, focus, motion

### 9.1 Signifier inventory (the only sanctioned clickable look)

| Thing | Signifier |
|---|---|
| Glossary term | Slate-700 text, dotted underline, trailing `ⓘ`, `cursor-help` |
| Invisible-click card | Card hover: border-strong + shadow-md **and** an explicit `View evidence →` link-label |
| Popover/disclosure content | `▲/▼` chevron on the summary row |
| Depth switch | Segmented pills; active = white surface + shadow |
| Current page | Nav pill filled slate-900/white + `aria-current="page"` |
| Share/copy | Brief inline "Copied ✓" replacing the label |

### 9.2 Focus & feedback tokens

- **Global focus ring** (added to `app.css`): `:focus-visible { outline: 2px solid #2563EB; outline-offset: 2px; }` — never remove outlines without a replacement.
- Motion: 150ms for hovers/toggles, 200ms for drawers/filters (ease-out). No animation exceeds 250ms; all respect `prefers-reduced-motion` (transitions die, state changes remain instant).
- Feedback colors stay inside the existing palette. The one reserved new treatment: **nudge indigo** (`bg-indigo-50/70`, `border-l-4 border-indigo-300`, text slate-700, kind label `text-indigo-800`). Nothing else may use it, so it stays unambiguous.

### 9.3 Copy rules (voice)

- Sentence case everything human; monospace+tabular only for figures/IDs.
- No hedging filler ("simply", "just", "obviously"); no blame words ("failed to"); verbs over nouns ("Money paid, work not done" not "payment/progress divergence").
- Empty states: name the cause, then the next action — "No projects matched those filters. Clear the district filter or search another sector." (never "Nothing found").
- Numbers: only in `₹ Cr`/`L` en-IN notation (retained rule), always unit-labelled, stock labelled with as-of dates, flows labelled with their period.

---

## 10. Accessibility contract

- WCAG 2.1 AA minimums inherited from `design-system.md` §5; additions below.
- Keyboard: drawers (Esc + backdrop + ✕), tabs (arrow keys), map districts (button list — already present), popovers (Esc closes; focus stays in flow).
- Live regions: `ResultCount` (`polite`), drawer open announcements (`role="dialog"` naming persists), freshness (`role="status"` — existing).
- Pages currently missing `aria-*` (`/governance`, `/genesis`, `/flags`) are brought to parity in Phase 3; the pattern to follow is the one already used on `/` and `/projects`.
- `aria-current="page"` on nav; `aria-pressed` on armed toggles; sr-only "Data provenance" labels on Evidence footers.

---

## 11. Implementation map & phase QA

**Phase 1 (this drop):** `designsystem.md`, `depth` store, `DepthToggle`, `GlossaryTerm`, `PlainBadge`, `NudgeCallout`, `ChartFrame`, `PageIntro`, `ResultCount`, `glossary.ts`, `vocabulary.ts`, app.css focus/motion tokens, `design-system.md` cross-reference banner.

**Later phases (wiring):** grouped nav + rename (layout), Start-Here home, per-page adoption order `/projects` → `/portfolio` → `/financials` → `/outcomes` → `/trends` → `/flags` → `/governance` → `/committee` → `/genesis`, `/glossary` page, welcome card, a11y gap pass.

**Per-component QA checklist**
1. Works identically in both gears; Plain hides only, never lies.
2. Keyboard-only walkthrough passes (reach, operate, escape).
3. Has ≥1 signifier from §9.1; hover and focus states both visible.
4. Empty/zero/gap states render the GAP language, never `0`.
5. Indian notation & stock/flow labelling intact.
6. Dismissals persist for the session only; gear persists across visits.
7. `npm run check` and `npm run build` clean.

---

## 12. Decision log

| Date | Decision | Rationale |
|---|---|---|
| 2026-10-21 | Two-gear depth on one site (chosen over separate persona paths) | Single content source; no fork; expert retains % one-click access. |
| 2026-10-21 | Humanized noun nav labels | Question-style labels were tested on the wireframe and read as tabs of a form; noun labels retain scent while staying scannable; hover descriptions add the missing scent. |
| 2026-10-21 | Single nudge visual treatment (indigo) | Reserves tint semantics for evidence/lifecycle badges; prevents nudge-vs-evidence confusion (P12). |
| 2026-10-21 | `<details>` for popovers/tables | Zero-JS accessible disclosure; survives prerender; consistent with P9. |
| 2026-10-21 | Raw ids visible in Evidence mode | Humanization must not cost experts their cross-reference shortcuts (P10 trade-off documented). |
| 2026-10-21 | shadcn-svelte-aligned token + primitive layer (§13) | Semantic CSS-variable theming (bg-card, border-border…) replaces raw-hex styling for new code; primitives (Button/Card) standardize presentation while composition stays open. |
| 2026-10-21 | V3 direction recorded: KIIFB-first, analyses-as-layers (§14) | The committee report is treated as one analytical layer over KIIFB, not the site's backbone. Affects IA/content framing from Phase 2 onward; does not alter the depth model or Phase 1 component set. |

---

## 13. Theming & presentation — shadcn-svelte-aligned layer

> Direction reference: shadcn(-svelte). Adopted for its *token architecture and
> presentation discipline* — not its black-box components. This repo's evidence
> semantics and provenance rules (design-system.md) take precedence wherever
> they conflict with shadcn defaults.

### 13.1 Token architecture

- **Single source of truth:** CSS variables in `src/app.css` (`:root`); Tailwind exposes them as semantic utilities (`bg-card`, `text-primary-foreground`, `border-border`, `text-muted-foreground`…) via `tailwind.config.js`.
- **Meaning over hue:** components style with *roles* (surface, line, action, state), never hexes. `slate-*` full palette remains available for legacy surfaces and data-vis fills (see §13.2).
- **Reserved color rule sharpened:** saturated color belongs to evidence/lifecycle/flag badges only; `--accent` (subtle hover surface) is *not* a semantic color and must never be used to "highlight" data; the nudge indigo remains a component-internal treatment (§6.2), not a token.
- **Radius scale:** all radii derive from `--radius` (`rounded-sm/md/lg` = −4px/−2px/full). No other radii on new code; `rounded-full` remains only for pills.
- **Elevation discipline:** `shadow-sm` for resting cards, `shadow-md`-class for popovers/dropdowns, nothing floating above `md`. Depth must not compete with evidence states.
- **Dark mode:** token block reserved in `app.css` (`.dark`, documented values) but not exposed to users until contrast is validated against badge tints (queued decision).

### 13.2 Visual presentation rules (sourced from shadcn discipline)

| Trait | Rule on this site |
|---|---|
| Quiet base | Neutral greys carry structure; the page reads calm before it reads colourful |
| Hairline separation | `border-border` (#E2E8F0) between content zones; background tint (`bg-slate-50/60`) for provenance/footer rows, not boxes-for-everything |
| Whitespace generosity | Section rhythm ≥ 1.5rem; Card padding `p-5`; dense mono tables are the exception, visually fenced |
| Typography restraint | One source of emphasis per card: either the *value* (tabular mono) or the *question* (sans semibold), never both at full weight |
| Icons | 16px, 1.5–2px stroke, currentColor, never decorative-alone — always beside a text label (P1) |
| Data-vis fills | Charts may keep `slate-*`/fixed semantic hues, but axis/label/legend text uses `text-muted-foreground`, grid lines `border-border` |

### 13.3 Primitive layer

Current set (all open-composition, slot-based — the shadcn "own the code" posture):

- **`Button.svelte`** — variants `primary / secondary / outline / ghost / destructive`; sizes `sm / md / lg`; renders `<a>` when `href` given. Disabled state dims *and* blocks pointer events (perceivable constraint, P6).
- **`Card.svelte`** — `header` / `children` / `footer` snippets on one `bg-card border-border shadow-sm` surface. Metric-card and provenance-footer patterns compose ON this, not instead of it.
- Later (as pages adopt the spine): `Tabs` (url-state, arrow keys), `Dialog`/`Sheet` (drawers), `Table` primitives — candidates for adoption in Phase 3, following the same token/variant discipline.

**Migration rule:** new and reworked pages use semantic tokens; existing `slate-*`-hardcoded surfaces migrate opportunistically as they're reworked page-by-page (never in a mass find-replace).

### 13.4 Regression guards

- `npm run check` + `npm run build` must stay clean after token/config changes (radius overrides visibly change existing rounded-sm/md surfaces — review diff in browser before merging).
- Any new token needs: a `:root` value, a documented reserved `.dark` counterpart, a Tailwind mapping, and a line in §13.1s table of roles — all four, or it doesn't land.

---

## 14. V3 direction (recorded, not yet executed): KIIFB-first, analyses as layers

**Problem with the current architecture:** the information structure orbits the *October 2026 Expert Committee Report* — assertions, scrutiny, recommendations are first-class destinations, while KIIFB itself (what it is, how it borrows, what it builds) is arrived at sideways. The committee is one *study of* KIIFB, not the subject. Other studies exist and will exist; the site should not need a re-architecture each time one arrives.

**Target model — three strata:**

1. **L0 Record base (canonical):** sources → datasets → reconciliation. The subject matter: money in, borrowing, delivery, geography, time. Largely exists today (projects, financials, outcomes, trends) minus committee framing.
2. **L1 KIIFB story (primary narrative):** Genesis/how-it-works pages reorganized as the site's spine and default reading path. The home becomes "understand KIIFB", not "read the report".
3. **L2 Analytical layers (opinionated overlays):** one layer per published study — the Oct 2026 Committee (first, fully built: assertions AST-001…005, scrutiny REC/LEG registers), plus future entries (e.g. RBI reports, RBI/academic studies, state rebuttals, journalistic investigations). Each layer reuses the existing component set — assertion cards, evidence badges, citation drawer, scrutiny tabs — pointed at a different authored analysis. Layers declare their own: author, date, claim count, contested-count summary, and a heat-map of what they say vs. what the record shows.

**Design consequences when executed (future phases):**

- Nav groups become record-base verbs for L1, and an explicit **"Analyses"** group for L2 entries; committee pages drop their top-level specialness in favour of a layer identity (badge: "Analytical layer · Oct 2026 Expert Committee").
- Homepage spine: What is KIIFB → Follow the money → Delivery/debt → "How others have judged it" (layers index).
- The depth toggle, vocabulary system, nudges, and ChartFrame are all layer-agnostic → carry over unchanged; each L2 layer can bring its own authored nudge copy.
- Data shape to support layers: each layer ships a manifest (studies' claim ids, locators, verdict summaries) analogous to `committee_assertions.json` — the pattern generalizes rather than hard-codes.

**Status:** Direction only. No IA/content changes land until Phase 2's Start-Here homepage is designed against this model; the committee keeps its current routes until then. This section is the reference for that work.

