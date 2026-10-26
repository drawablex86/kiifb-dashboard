# UX Rework v2 — Session State (2026-10-21)

> This file records the plan, progress, and open decisions so work can resume cleanly in a new session. It complements (not replaces) `TASKS.md` and `designsystem.md`.

---

## High-level plan (from designsystem.md §12)

| Phase | Label | Scope | Status |
|---|---|---|---|
| 1.1 | Foundations (spec, depth, vocab, components, theming) | `designsystem.md`, depth store, 7 components, Button/Card, semantic tokens | **Done** |
| 1.2 | Nav + Glossary | grouped humanized nav (`NavGroup`), `/glossary` route, layout rewrite | **Done (prerender blocking — see below)** |
| 2 | Start-Here homepage | rebuild `/` around 5 questions; V3 framing (KIIFB-first) | Ready |
| 3 | Core journey adoption | `/projects`, `/portfolio`, `/financials` with PageIntro/ChartFrame/Nudge/PlainBadge/ResultCount | Backlog |
| 4 | Remaining routes + a11y | `/outcomes`, `/trends`, `/flags`, `/governance`, `/committee`, `/genesis`; aria parity | Backlog |

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

### Repo tracking
- `TASKS.md` — Milestone 12 appended (T110–T117 with statuses)
- `src/routes/components-preview/+page.svelte` — dev-only review gallery (all components + theming demo)

---

## Current blocker — prerender failures

**Symptoms (build output):**
```
[500] GET /flags
Error: Cannot access url.searchParams on a page with prerendering enabled
[500] GET /portfolio
Error: Cannot access url.searchParams on a page with prerendering enabled
The following pages contain links to /glossary#contested_interpretation, but no element with id="contested_interpretation" exists on /glossary
```

### Root causes identified
1. **Missing anchor id** — `src/lib/data/glossary.ts:127` (`article_293` entry has `seeAlso: ['borrowing_space', 'contested_interpretation']`). `contested_interpretation` is a vocabulary key, not a glossary id. Fix: change to `'evidence_label'` (the correct glossary entry for the evidence taxonomy).
2. **Pre-existing pages break on searchParams** — `/flags/+page.svelte` and `/portfolio/+page.svelte` use `page.url.searchParams.get()` in `$derived` initializers. This **was passing before** — my layout changes did not touch these pages, but the build failure suggests either (a) the earlier build's success was masked by pipe/tail, or (b) a subtle prerender timing change. Regardless: reading `searchParams` during prerender is invalid per SvelteKit; the fix is to make these pages dynamic (`prerender = false` in their `+page.ts` / `+page.server.ts`) or guard reads with `browser` check. The original codebase apparently had this working; needs investigation.

### Immediate fixes (when resuming)
```bash
# 1. Fix the missing anchor
# Edit src/lib/data/glossary.ts line ~127:
# seeAlso: ['borrowing_space', 'evidence_label']

# 2. Address searchParams in /flags and /portfolio:
# Option A (quick): add `export const prerender = false;` to their +page.ts (they already use URL state)
# Option B (correct): read params in a +page.server.ts load() and pass to component as data
```

---

## Next session — resume order

1. Apply the two fixes above → `npm run check` + `npm run build` must pass clean.
2. Verify `/components-preview` and `/glossary` render in browser (dev server already running on :5174).
3. Begin **T115 — Start Here homepage** (`/` redesign per designsystem.md §4.1 + §14 V3 framing):
   - Five plain-language questions as the site map
   - Welcome/dismissible note, depth-gear explainer, "how this site works" spine
   - Committee assertions relocated under "The Committee's Claims — checked against the record"
   - Use `PageIntro`, `NudgeCallout`, `ChartFrame` (for any embedded viz)
4. Then **T116 — Core journey** (`/projects`, `/portfolio`, `/financials`):
   - Wrap existing Sankey/Scatter/Funnel in `ChartFrame`
   - Add `PlainBadge` for all status/evidence/flag labels
   - Add `ResultCount` above every filterable list
   - Add point-of-use `NudgeCallout` (authored copy, per designsystem.md §6)

---

## Open decisions (recorded, not resolved)

| # | Question | Recorded in | Direction if none given |
|---|---|---|---|
| D1 | Blue focus ring on mouse click too? | §9.2 notes | No — keep keyboard-only; click is its own feedback |
| D2 | Dark mode exposure timeline? | §13.1 | Validate badge contrast against dark tokens first; behind flag |
| D3 | Committee layer naming in V3? | §14 | "Analytical layer · Oct 2026 Expert Committee" badge on all its pages |
| D4 | `/flags` + `/portfolio` searchParams strategy? | this file | Make dynamic (`prerender=false`) — matches their URL-filter purpose |

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
| Fix | `src/lib/data/glossary.ts:127`, `src/routes/flags/+page.ts` (new), `src/routes/portfolio/+page.ts` (new) |
| T115 | `src/routes/+page.svelte` (rewrite), possibly `src/routes/+page.server.ts` (if data needed) |
| T116 | `src/routes/projects/+page.svelte`, `src/routes/portfolio/+page.svelte`, `src/routes/financials/+page.svelte` |

---

*End of session state — commit or stash as desired. `designsystem.md` is the authoritative spec; `TASKS.md` has the task board with checkboxes.*