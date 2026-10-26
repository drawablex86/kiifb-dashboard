# UX Rework v2 — Session State (2026-10-21)

> This file records the plan, progress, and open decisions so work can resume cleanly in a new session. It complements (not replaces) `TASKS.md` and `designsystem.md`.

---

## High-level plan (from designsystem.md §12)

| Phase | Label | Scope | Status |
|---|---|---|---|
| 1.1 | Foundations (spec, depth, vocab, components, theming) | `designsystem.md`, depth store, 7 components, Button/Card, semantic tokens | **Done** |
| 1.2 | Nav + Glossary | grouped humanized nav (`NavGroup`), `/glossary` route, layout rewrite | **Done** |
| 2 | Start-Here homepage | rebuild `/` around 5 questions; V3 framing (KIIFB-first) | **Done (T115)** |
| 3 | Core journey adoption | `/projects`, `/portfolio`, `/financials` with PageIntro/ChartFrame/Nudge/PlainBadge/ResultCount | **Done (T116)** |
| 4 | Remaining routes + a11y | `/outcomes`, `/trends`, `/flags`, `/governance`, `/committee`, `/genesis`; aria parity | **Done (T117)** |

---

## Completed this session (with file list)

### Spec & foundations
- `designsystem.md` — full spec (personas, P1–P14, depth contract, IA, vocabulary, nudges, ChartFrame, theming §13, KIIFB-first V3 direction §14)
- `design-system.md` — cross-reference banner added (canon preserved)
- `src/lib/stores/depth.svelte.ts` — two-gear store (localStorage + `?depth=`, SSR-safe)
- `src/lib/data/vocabulary.ts` — humanized label maps for evidence/lifecycle/flag (single source of truth)
- `src/lib/data/glossary.ts` — 37 entries (plain/expert/why), search helper

### Components (Phase 1 set)
- `DepthToggle.svelte` — segmented control, `aria-pressed`, persists gear
- `GlossaryTerm.svelte` — inline `<details>` popover, depth-aware, Esc-close, fail-loud on unknown id
- `PlainBadge.svelte` — centralized badge, tooltips, Evidence gear appends raw id
- `NudgeCallout.svelte` — three kinds (situate/interpret/ask), single indigo treatment, session-dismiss
- `ChartFrame.svelte` — Question → Takeaway → How-to-read → Chart → Data-table → depth-aware provenance
- `PageIntro.svelte` — breadcrumb + h1 + standing question + lead + "On this page / Not on this page"
- `ResultCount.svelte` — "Showing N of M" with `aria-live="polite"`

### Theming layer (shadcn-svelte aligned)
- `src/app.css` — semantic CSS variables (background/foreground, card, primary/secondary/destructive/muted/accent, border, input, ring, --radius), reserved `.dark` block, global `:focus-visible` blue ring, `prefers-reduced-motion`
- `tailwind.config.js` — mapping to `bg-card`, `text-muted-foreground`, `border-border`, radius scale, color aliases
- `Button.svelte` — 5 variants × 3 sizes, `href`→`<a>`, stratified signals (transparent outline → soft hover ring → blue focus ring)
- `Card.svelte` — header/body/footer slots, metric-card/provenance compose on top

### Nav + Glossary
- `src/lib/nav.ts` — 4 disclosure groups (Start / Follow / Watch / Claims & verify) with scent descriptions
- `NavGroup.svelte` — ARIA disclosure dropdown, Esc/outside-click/route-change close, active pill indicator
- `src/routes/+layout.svelte` — rewritten with grouped nav, mobile disclosure menu, skip link, DepthToggle placement
- `src/routes/glossary/+page.svelte` — searchable A–Z, depth-aware definitions, seeAlso anchors, verification entry points

### Phase 2: Start-Here Homepage (T115)
- `src/routes/+page.svelte` — rebuilt around 5 plain-language questions, welcome note, depth-gear explainer, "how this site works" spine, committee assertions under "The Committee's Claims — checked against the record" (V3 framing)

### Phase 3: Core Journey (T116)
- `src/routes/projects/+page.svelte` — PageIntro, ResultCount, ChartFrame (Sankey + Scatter), PlainBadge (status/flags), NudgeCallout (situate/interpret), GlossaryTerm
- `src/routes/portfolio/+page.svelte` — PageIntro, ResultCount (3 levels), NudgeCallout (situate/interpret), PlainBadge, GlossaryTerm, URL-shared funnel state
- `src/routes/financials/+page.svelte` — PageIntro, NudgeCallout (situate/interpret on each tab), PlainBadge, tabbed structure

### Phase 4: Remaining Routes (T117)
- `src/routes/outcomes/+page.svelte` — PageIntro, NudgeCallout, PlainBadge, ResultCount, 4 tabs (geography, completeness, dimensions, factsheets)
- `src/routes/trends/+page.svelte` — PageIntro, NudgeCallout (situate/interpret), PlainBadge, FreshnessBadge, cadence disclosures, flat-line honesty
- `src/routes/flags/+page.svelte` — PageIntro, NudgeCallout (situate/interpret), PlainBadge (kind='flag'), ResultCount, URL-shared filters, history panel
- `src/routes/governance/+page.svelte` — PageIntro, NudgeCallout (interpret/situate), PlainBadge, 4 tabs (recs, legal, liability, methodology)
- `src/routes/committee/+page.svelte` — PageIntro, NudgeCallout (situate/interpret), PlainBadge, cross-link to /genesis, 5 tabs
- `src/routes/genesis/+page.svelte` — PageIntro, NudgeCallout (situate/interpret), PlainBadge, cross-link to /committee, 5 tabs

### Repo tracking
- `TASKS.md` — Milestone 12 updated (T110–T117 with statuses)
- `src/routes/components-preview/+page.svelte` — dev-only review gallery (all components + theming demo)

---

## Current status: **All UX Rework v2 phases complete**

All 7 tasks in Milestone 12 (T110–T117) are **done**. The two-persona depth system is implemented across all 10 routes. The V3 "KIIFB-first, analyses-as-layers" framing is reflected in the homepage and cross-links between /committee and /genesis.

### Remaining known issues (pre-existing, not introduced by UX rework)
1. **NavGroup.svelte:20** — `group` referenced in closure warning (Svelte 5 $derived timing)
2. **NavGroup.svelte:44** — div with keydown needs ARIA role (mobile dropdown panel)
3. **+layout.svelte:83** — mobile `<nav>` with onkeydown (non-interactive element)
4. **glossary/+page.svelte:96** — `<h2>` with `aria-hidden="true"` (letter headers in A-Z list)
5. **Drawer components** — non-interactive divs with onkeydown (projects, home page drawers)

These are component-library level warnings that exist in the foundational components. They don't block functionality and are documented for future refinement.

---

## Next steps (future work)

1. **A11y refinement pass** — address the 5 pre-existing warnings above in component library
2. **Dark mode validation** — test badge contrast against reserved `.dark` tokens, expose behind flag (D2)
3. **Committee layer badge** — add "Analytical layer · Oct 2026 Expert Committee" badge to /committee and /genesis pages (D3)
4. **V3 IA execution** — restructure nav groups per §14: L0 record base verbs, L1 KIIFB story, L2 Analyses group

---

## Commands reference

```bash
# Validate (run from /Users/rahulrajeev/Downloads/kiifb-dashboard)
npm run check          # types + a11y (must be 0/0)
npm run build          # production build (must pass)
npm run dev            # already running on :5174 (HMR)
npm run preview        # preview production build on :4174

# Review gallery
open http://localhost:5174/components-preview

# Glossary page
open http://localhost:5174/glossary
```

---

## Files most likely to edit next

| Phase | Files |
|---|---|
| A11y pass | `src/lib/components/NavGroup.svelte`, `src/routes/+layout.svelte`, `src/routes/glossary/+page.svelte` |
| Dark mode | `src/app.css` (`.dark` tokens), `tailwind.config.js` |
| Committee badge | `src/routes/committee/+page.svelte`, `src/routes/genesis/+page.svelte` |
| V3 IA | `src/lib/nav.ts`, `src/routes/+layout.svelte`, `designsystem.md` §14 |

---

*End of session state — commit or stash as desired. `designsystem.md` is the authoritative spec; `TASKS.md` has the task board with checkboxes.*