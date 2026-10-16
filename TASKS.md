# Task Board — KIIFB Accountability & Public Value Dashboard

Statuses: `backlog` · `ready` · `in_progress` · `blocked` · `done`

## Milestone 0 — Repository audit and bootstrap

### T001 — Inspect repository
- Status: done
- Dependencies: none
- Objective: inspect files, package scripts, Git status, tests, and conventions before editing.
- Outputs: short repository baseline in task notes, `design-system.md` creation.
- Acceptance: existing work and constraints are documented; no files overwritten blindly.
- Completed: 2026-10-16
- Notes:
  - Repository baseline: Starter kit with documentation (`agent.md`, `architecture.md`, `datasources.md`, `TASKS.md`, `README.md`) and a local 2400-line markdown transcription of the October 2026 Committee Report in `data/KIIFB Findings Report.md`.
  - Git status: Workspace is not yet initialized as a git repository (`.git` absent).
  - Stack environment: Node v23.7.0, npm 10.9.2, Python 3.13.2 installed. SvelteKit/Tailwind project scaffolding not yet created.
  - Added `design-system.md` to establish visual standards, palette, and Indian financial notation rules (`₹ Crore`, `₹ Lakh`, tabular numerals).

### T002 — Bootstrap research data layout & manifest
- Status: ready
- Dependencies: T001
- Objective: create directory layout for raw, processed, and derived research assets, set up `data/README.md`, and register existing local assets in `data/manifest.json`.
- Outputs: directories `data/raw/`, `data/processed/`, `data/derived/`, `data/README.md`, and `data/manifest.json`.
- Acceptance: data layout is created; `data/KIIFB Findings Report.md` is registered in `data/manifest.json` with SHA-256 checksum and metadata.
- Verification command: `python3 -c "import json; manifest = json.load(open('data/manifest.json')); print('Manifest entries:', len(manifest['sources']))"`

### T003 — Initialize Git version control
- Status: backlog
- Dependencies: T002
- Objective: initialize Git repository, configure `.gitignore` (ignoring `.DS_Store`, `node_modules`, large binaries), and create initial baseline commit.
- Outputs: `.git/` repository and `.gitignore`.
- Acceptance: repository is cleanly initialized with an initial commit preserving all baseline files.
- Verification command: `git status`

## Milestone 1 — Five-assertion prototype

### T010 — Extract five major committee assertions from local findings
- Status: backlog
- Dependencies: T002
- Objective: extract 5 headline committee assertions from `data/KIIFB Findings Report.md` with explicit page/table locators, amounts, reporting dates, evidence labels, and caveats into structured JSON.
- Outputs: `data/processed/committee_assertions.json` and schema validation script.
- Five Target Assertions:
  1. KIIFB borrowing and State borrowing-space deduction (₹25,932.55 Cr).
  2. Debt service and State transfers (99.4% met by State transfers).
  3. Borrowing cost premium over State borrowing rates (approx ₹910 Cr).
  4. Revenue-generating project classification and actual repayments (TransGrid, Technocity, Petrochemical Park).
  5. Project delivery and public outcome reporting coverage vs omitted dimensions.
- Acceptance: JSON file strictly conforms to assertion schema in `architecture.md` with zero missing required fields.
- Verification command: `python3 -m json.tool data/processed/committee_assertions.json > /dev/null`

### T011 — Archive official PDF of Committee Report
- Status: backlog
- Dependencies: T002
- Objective: download official PDF from Niyamasabha (`DS001`), verify integrity, compute SHA-256, and archive under `data/raw/committee-report/`.
- Outputs: `data/raw/committee-report/kiifb-expert-committee-report.pdf` and updated `data/manifest.json`.
- Acceptance: PDF is archived with checksum recorded in manifest. If automated download fails due to network restrictions, document manual retrieval instructions in `datasources.md`.
- Verification command: `test -f data/raw/committee-report/kiifb-expert-committee-report.pdf || echo 'Manual download required'`

### T012 — Build counter-evidence & corroboration dataset
- Status: backlog
- Dependencies: T010
- Objective: compile at least one corroborating or qualifying official record for each of the five assertions (e.g. State budget transfers, CAG audit excerpts, KITE school handover counts) into structured evidence links.
- Outputs: `data/processed/evidence_links.json`.
- Acceptance: every assertion has at least one linked qualifying record with exact citation and evidence label.

### T013 — Scaffold SvelteKit 2 + Tailwind application
- Status: backlog
- Dependencies: T001
- Objective: initialize SvelteKit 2 + Svelte 5 + TypeScript + Tailwind CSS application matching `design-system.md` specifications.
- Outputs: `package.json`, `svelte.config.js`, `tailwind.config.js`, `src/routes/+layout.svelte`.
- Acceptance: development server builds and runs cleanly without errors; design system typography and colors are configured.
- Verification command: `npm run check` or `npm run build`

### T014 — Build assertion comparison view
- Status: backlog
- Dependencies: T010, T012, T013
- Objective: implement interactive assertion cards in SvelteKit showcasing claim, evidence badge, cited amounts (in `₹ Crore` tabular format), caveats, and citation popover.
- Outputs: `src/routes/assertions/+page.svelte` and associated components.
- Acceptance: all 5 assertions render with compliant badges, tabular currency, and clickable citation drawers.
- Verification command: `npm run build`

## Milestone 2 — Project-level evidence

### T020 — Acquire KIIFB project records
- Status: backlog
- Dependencies: T001
- Outputs: archived source and processed project register, or documented alternative if no bulk download exists.
- Acceptance: source labels, reporting date, identifiers and status values preserved.

### T021 — Acquire KITE education records
- Status: backlog
- Dependencies: T001
- Outputs: archived KITE records and processed institution/project list.
- Acceptance: scheme/project/institution/building counting units are documented.

### T022 — Design project matching rules
- Status: backlog
- Dependencies: T020, T021
- Outputs: documented match rules and ambiguous-match report.
- Acceptance: no silent fuzzy-match merges; uncertain matches remain unresolved.

### T023 — Build project explorer
- Status: backlog
- Dependencies: T020, T021, T022, T013
- Outputs: searchable project page, filters, status and source detail.
- Acceptance: approval is not mislabelled as completion; every status is dated and sourced.

## Milestone 3 — Financial model

### T030 — Extract committee financial tables
- Status: backlog
- Dependencies: T011
- Outputs: versioned tables with source locators and units.
- Acceptance: core figures verified or marked provisional.

### T031 — Add calculation and reconciliation tests
- Status: backlog
- Dependencies: T030
- Outputs: automated tests for totals, units, stock/flow separation and calculation formulas.
- Acceptance: all known differences are reported, not silently adjusted.

### T032 — Build debt and land-liability views
- Status: backlog
- Dependencies: T030, T031
- Outputs: financial charts, land-acquisition table, assumption panels.
- Acceptance: future commitments are not mislabelled as outstanding debt; overlap and scope are documented.

## Milestone 4 — Outcomes and geography

### T040 — Implement public-value dimensions
- Status: backlog
- Dependencies: T023
- Outputs: separate financial, economic, social and distributional evidence fields.
- Acceptance: missing metrics display as unknown, not zero.

### T041 — Add evidence completeness view
- Status: backlog
- Dependencies: T023, T040
- Outputs: indicators for missing completion, handover, operation, usage, cost and outcome data.
- Acceptance: evidence gaps are measurable and clearly defined.

### T042 — Add district/sector visualisations
- Status: backlog
- Dependencies: T020, T040
- Outputs: map and comparative charts.
- Acceptance: geographic denominators, map data provenance and reporting dates are explicit.

## Milestone 5 — Legal and governance

### T050 — Build legal issue register
- Status: backlog
- Dependencies: T011
- Outputs: issue records for Articles 266/293, relevant KIIFB Act sections, Masala bond questions and court proceedings.
- Acceptance: committee interpretation is separated from binding court findings.

### T051 — Build recommendation tracker
- Status: backlog
- Dependencies: T011
- Outputs: committee recommendation status table linked to official actions.
- Acceptance: report recommendations are not represented as implemented without evidence.

### T052 — Build methodology and data-quality pages
- Status: backlog
- Dependencies: T031, T041, T050
- Outputs: source methodology, discrepancy log and caveats.
- Acceptance: source dates, calculations, matching rules and limitations are reproducible.

## Milestone 6 — Release readiness

### T060 — Test and review
- Status: backlog
- Dependencies: T013, T023, T032, T042, T052
- Outputs: test report, accessibility review, data-quality checks.
- Acceptance: critical checks pass or documented blockers remain.

### T061 — Document refresh and backup
- Status: backlog
- Dependencies: T020, T030
- Outputs: repeatable refresh commands and backup/restore instructions.
- Acceptance: another contributor can reproduce data processing from archived sources.

### T062 — Prepare release
- Status: backlog
- Dependencies: T060, T061
- Outputs: source-linked methodology and deployment instructions.
- Acceptance: claims are traceable and limitations are visible.

## Task completion rule

A task is `done` only when acceptance criteria are met, relevant tests have run, sources and metadata are recorded, documentation is updated, and remaining gaps are captured in follow-up tasks.
