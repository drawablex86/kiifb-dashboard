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
- Status: done
- Dependencies: T001
- Objective: create directory layout for raw, processed, and derived research assets, set up `data/README.md`, and register existing local assets in `data/manifest.json`.
- Outputs: directories `data/raw/`, `data/processed/`, `data/derived/`, `data/README.md`, and `data/manifest.json`.
- Acceptance: data layout is created; `data/KIIFB Findings Report.md` is registered in `data/manifest.json` with SHA-256 checksum and metadata.
- Completed: 2026-10-16
- Notes: directories created, `data/README.md` authored, `data/manifest.json` initialized with `DS001-LOCAL` checksum and metadata.

### T003 — Initialize Git version control
- Status: done
- Dependencies: T002
- Objective: initialize Git repository, configure `.gitignore` (ignoring `.DS_Store`, `node_modules`, large binaries), and create initial baseline commit.
- Outputs: `.git/` repository and `.gitignore`.
- Acceptance: repository is cleanly initialized with an initial commit preserving all baseline files.
- Completed: 2026-10-16
- Notes: Git initialized, `.gitignore` created, root commit `2511c0d` created with all baseline documentation and assets. Clean working tree verified.

## Milestone 1 — Five-assertion prototype

### T010 — Extract five major committee assertions from local findings
- Status: done
- Dependencies: T002
- Objective: extract 5 headline committee assertions from `data/KIIFB Findings Report.md` with explicit page/table locators, amounts, reporting dates, evidence labels, and caveats into structured JSON.
- Outputs: `data/processed/committee_assertions.json` and schema validation script.
- Five Target Assertions:
  1. KIIFB borrowing and State borrowing-space deduction (₹25,932.55 Cr, Table 3.11).
  2. Debt service and State transfers (99.4% met by State transfers, Table 3.2).
  3. Borrowing cost premium over State borrowing rates (approx ₹910 Cr, Table 3.12).
  4. Revenue-generating project classification and actual repayments (TransGrid 2.0, Technocity, Petrochemical Park).
  5. Project delivery and public outcome reporting coverage vs omitted dimensions (Table 4.1 & 6.2).
- Acceptance: JSON file strictly conforms to assertion schema in `architecture.md` with zero missing required fields.
- Completed: 2026-10-16
- Notes: Created `data/processed/committee_assertions.json` with all 5 verified headline assertions.

### T011 — Archive official PDF of Committee Report
- Status: done
- Dependencies: T002
- Objective: download official PDF from Niyamasabha (`DS001`), verify integrity, compute SHA-256, and archive under `data/raw/committee-report/`.
- Outputs: `data/raw/committee-report/kiifb-expert-committee-report.pdf` and updated `data/manifest.json`.
- Acceptance: PDF is archived with checksum recorded in manifest.
- Completed: 2026-10-16
- Notes: Archived 80,384,059 byte official PDF from Niyamasabha with SHA-256 `143f9978bf1b6242e6c251ff5389f7a8183d48778b62e5a02ae75c415cd812ca` and registered in `data/manifest.json`.

### T012 — Build counter-evidence & corroboration dataset
- Status: done
- Dependencies: T010
- Objective: compile at least one corroborating or qualifying official record for each of the five assertions (e.g. State budget transfers, CAG audit excerpts, KITE school handover counts) into structured evidence links.
- Outputs: `data/processed/evidence_links.json`.
- Acceptance: every assertion has at least one linked qualifying record with exact citation and evidence label.
- Completed: 2026-10-16
- Notes: Created `data/processed/evidence_links.json` linking 6 corroborating/qualifying records (Supreme Court order, CAG audits, KIIF Act statutory earmarking, KITE 242 school completions).

### T013 — Scaffold SvelteKit 2 + Tailwind application
- Status: done
- Dependencies: T001
- Objective: initialize SvelteKit 2 + Svelte 5 + TypeScript + Tailwind CSS application matching `design-system.md` specifications.
- Outputs: `package.json`, `svelte.config.js`, `tailwind.config.js`, `src/routes/+layout.svelte`.
- Acceptance: development server builds and runs cleanly without errors; design system typography and colors are configured.
- Completed: 2026-10-16
- Notes: Configured SvelteKit 2 + Svelte 5 + TypeScript + Tailwind with civic tech header, footer, and styling system.

### T014 — Build assertion comparison view
- Status: done
- Dependencies: T010, T012, T013
- Objective: implement interactive assertion cards in SvelteKit showcasing claim, evidence badge, cited amounts (in `₹ Crore` tabular format), caveats, and citation popover.
- Outputs: `src/routes/assertions/+page.svelte` (mounted at root `/`) and server data loader.
- Acceptance: all 5 assertions render with compliant badges, tabular currency, and clickable citation drawers. Passes `npm run check` and `npm run build` with zero errors.
- Completed: 2026-10-16
- Notes: Built interactive assertion cards with slide-over evidence drawers and full citation provenance. Zero errors in svelte-check and vite build.

## Milestone 2 — Project-level evidence

### T020 — Acquire KIIFB project records
- Status: done
- Dependencies: T001
- Outputs: archived source `data/raw/kiifb/kiifb-prjStatus.html` and processed project register `data/processed/kiifb_projects.json` (1,408 project rows).
- Acceptance: source labels, reporting date, identifiers and status values preserved.
- Completed: 2026-10-16
- Notes: Downloaded live official KIIFB database (`DS010`), computed SHA-256 (`c5ad164c...`), registered in manifest, and extracted 1,408 projects across 35 departments.

### T021 — Acquire KITE education records
- Status: done
- Dependencies: T001
- Outputs: archived KITE records `data/raw/kite/kiifb-funded-schools-sametham.html` and processed institution list `data/processed/kite_schools.json` (969 school institutions).
- Acceptance: scheme/project/institution/building counting units are documented.
- Completed: 2026-10-16
- Notes: Acquired official KITE Sametham portal (`DS021`), computed SHA-256 (`2841ee59...`), registered in manifest, and extracted 969 school campuses with codes and constituencies.

### T022 — Design project matching rules & disambiguation
- Status: done
- Dependencies: T020, T021
- Outputs: documented match rules in `docs/matching-rules.md` and discrepancy audit log (`DISC-001` to `DISC-003`).
- Acceptance: no silent fuzzy-match merges; counting unit hierarchy (Schemes vs Institutions vs Buildings) strictly enforced; uncertain matches remain unresolved.
- Completed: 2026-10-16
- Notes: Documented multi-tier matching rules, counting unit disambiguation, and discrepancy log in `docs/matching-rules.md`.

### T023 — Build project explorer
- Status: done
- Dependencies: T020, T021, T022, T013
- Outputs: searchable project explorer at `src/routes/projects/+page.svelte`, unified dataset `data/processed/unified_project_explorer.json` (2,377 records), sector/status filters, pagination, and inspection drawer.
- Acceptance: approval is not mislabelled as completion; every status is dated and sourced; passes `npm run check` and `npm run build` with zero errors.
- Completed: 2026-10-16
- Notes: Implemented interactive Project Explorer in Svelte 5 with responsive filters, tabular Indian currency notation, and inspection modals. Zero warnings or errors.

## Milestone 3 — Financial model

### T030 — Extract committee financial tables
- Status: done
- Dependencies: T011
- Outputs: `data/processed/committee_financial_tables.json` containing 10 core verified tables (Tables 3.1, 3.2, 3.3, 3.4, 3.5, 3.7, 3.11, 4.5, 6.1, 6.2/6.3) with chapter/page locators and source definitions.
- Acceptance: core figures verified against cited report tables; currency units explicitly maintained as INR ₹ Crore.
- Completed: 2026-10-16
- Notes: Created `scripts/extract_committee_financial_tables.py` and extracted full financial baseline dataset covering aggregate borrowings, bank loans, institutional loans, BSE bonds, space deductions, land acquisitions, amortisation schedule, and completion liabilities.

### T031 — Add calculation and reconciliation tests
- Status: done
- Dependencies: T030
- Outputs: `tests/test_financial_reconciliation.py` containing automated mathematical unit tests for all extracted financial tables.
- Acceptance: tests pass; stock vs flow figures separated; internal arithmetic verified; all known differences (such as 0.01 Cr rounding on bank loans and 14.43 Cr column total discrepancy on land repayment in Table 4.5) are documented and asserted.
- Verification command: `python3 -m unittest tests/test_financial_reconciliation.py`
- Completed: 2026-10-16
- Notes: 8 automated unit tests pass in 0.001s. All reconciliations verified.

### T032 — Build debt and land-liability views
- Status: done
- Dependencies: T030, T031
- Outputs: interactive financial liabilities view at `src/routes/financials/+page.svelte`, navigation tab enabled in `+layout.svelte`, and server loader at `src/routes/financials/+page.server.ts`.
- Acceptance: debt structure (banks, institutions, bonds), land acquisition pool, 16-year amortisation schedule to 2041-42, and budget transfers are presented with tabular Indian currency notation (`₹ Crore`); future commitments are not conflated with current debt; passes `npm run check` and `npm run build` with zero errors.
- Completed: 2026-10-16
- Notes: Built tabbed financial baseline view covering Tables 3.1, 3.2, 3.3, 3.4, 3.5, 3.7, 3.11, 4.5, and 6.1/6.2/6.3. Zero build warnings.

## Milestone 4 — Outcomes and geography

### T040 — Implement public-value dimensions
- Status: done
- Dependencies: T023
- Outputs: separate financial, economic, social and distributional evidence fields (`data/processed/public_value_and_geography.json`).
- Acceptance: missing metrics display as unknown/data_gap, not zero. Verified by `tests/test_public_value_reconciliation.py`.
- Evidence: Defined 5 distinct dimensions: financial return (only 3 of 44 revenue projects repaid ₹3,351.90 Cr; 99.4% budget funded), economic return (unmodelled, marked data_gap), social return (242 schools, 118 health projects), distributional return (top 3 districts get 41.6% outlay, Kannur gets 74.7% land pool, SC/ST gets 0.18%), and financing suitability (commercial market borrowings used for social assets). Tested via unit tests.

### T041 — Add evidence completeness view
- Status: done
- Dependencies: T023, T040
- Outputs: indicators for missing completion, handover, operation, usage, cost and outcome data. Itemized data gap register (`GAP-001` to `GAP-004`) and 6-tier completeness ladder (`data/processed/public_value_and_geography.json`, `src/routes/outcomes/+page.svelte`).
- Acceptance: evidence gaps are measurable and clearly defined. Missing metrics display as data_gap/unknown, not zero. Verified in unit tests and UI.
- Evidence: Built Evidence Completeness Ladder tracking all 6 portfolio levels (100% financial vs 8% ex-post outcomes) and itemized Data Gap Register documenting geographic omissions (1,408 projects with district null in KIIFB portal), missing ex-post cost-benefit models, missing handover tracking (80.5%), and unprovided vintage aging. Verified by `tests/test_public_value_reconciliation.py`.

### T042 — Add district/sector visualisations
- Status: done
- Dependencies: T020, T040
- Outputs: map and comparative charts (`src/routes/outcomes/+page.svelte`, `data/processed/public_value_and_geography.json`).
- Acceptance: geographic denominators, map data provenance and reporting dates are explicit.
- Evidence: Built interactive Kerala 14-district SVG spatial map, district comparative proportional bar visualizer (identifying Top 3 districts concentration at 41.6% and Kannur industrial LA pool at 74.7%), and Table 4.4 departmental distribution table (26 departments, PWD 52.6% vs SC/ST 0.24%). All denominators, sources (Committee Chapter IV, Tables 4.1-4.5), and reporting dates (June 30, 2026) are explicitly stated. Verified via unit tests (`test_public_value_reconciliation.py`), `npm run check`, and `npm run build`.

## Milestone 5 — Legal and governance

### T050 — Build legal issue register
- Status: done
- Dependencies: T011
- Outputs: issue records for Articles 266/293, relevant KIIFB Act sections, Masala bond questions and court proceedings (`data/processed/legal_issues_register.json`).
- Acceptance: committee interpretation is separated from binding court findings.
- Evidence: Built legal issues register covering Articles 266/293, KIIFB Act Section 8, Masala bonds/Entry 37, and SCSP/TSP statutory allocations. Explicitly distinguished Committee/CAG advisory opinions from pending/binding judicial proceedings (Supreme Court Original Suit No. 1 of 2024 referred to Constitution Bench; High Court of Kerala interim orders). Verified via unit tests (`tests/test_legal_and_governance.py`).

### T051 — Build recommendation tracker
- Status: done
- Dependencies: T011
- Outputs: committee recommendation status table linked to official actions (`data/processed/committee_recommendations.json`, `src/routes/governance/+page.svelte`).
- Acceptance: report recommendations are not represented as implemented without evidence.
- Evidence: Tracked all 8 restructuring recommendations (`REC-001` through `REC-008`) from Chapter VI. Each mapped to target authority, required legal instrument (Legislative Assembly Amendment, Executive GO, CAG Requisition), and official action status (0 of 8 fully implemented; 1 partially budgeted). Acceptance criterion satisfied and verified via unit tests (`test_legal_and_governance.py`) and UI.

### T052 — Build methodology and data-quality pages
- Status: done
- Dependencies: T031, T041, T050
- Outputs: source methodology, discrepancy log and caveats (`data/processed/methodology_and_quality.json`, `src/routes/governance/+page.svelte`).
- Acceptance: source dates, calculations, matching rules and limitations are reproducible.
- Evidence: Documented primary sources (`DS001`, `DS010`, `DS021`) with SHA-256 hashes and capture dates; established counting units hierarchy (sanctioned clusters vs institutional schools); published 6 itemized audit discrepancies (`DISC-001` through `DISC-006` including bank rounding, land repayment divergence, portal district omission, and SCSP/TSP deficit); and provided command-line reproducibility steps. Verified via unit tests (`test_legal_and_governance.py`), `npm run check`, and `npm run build`.

## Milestone 6 — Release readiness

### T060 — Test and review
- Status: done
- Dependencies: T013, T023, T032, T042, T052
- Outputs: test report, accessibility review, data-quality checks (`tests/test_end_to_end_integrity.py`, `docs/test-and-review-report.md`).
- Acceptance: critical checks pass or documented blockers remain.
- Evidence: Built end-to-end integration test suite. All 29 unit tests pass in 0.003s across 4 test modules. Svelte-check reports 0 errors and 0 warnings. Accessibility review verifies WCAG 2.1 AA keyboard and ARIA compliance on interactive maps and tables. Documented in `docs/test-and-review-report.md`.

### T061 — Document refresh and backup
- Status: done
- Dependencies: T020, T030
- Outputs: repeatable refresh commands and backup/restore instructions (`scripts/refresh_pipeline.py`, `docs/refresh-and-backup.md`).
- Acceptance: another contributor can reproduce data processing from archived sources.
- Evidence: Built automated master refresh script `scripts/refresh_pipeline.py` which verifies SHA-256 hashes of primary sources, re-runs financial table extraction, project register parsing, school directory processing, and unified dataset compilation, and executes all 29 tests. Documented backup/restore steps in `docs/refresh-and-backup.md`.

### T062 — Prepare release
- Status: done
- Dependencies: T060, T061
- Outputs: source-linked methodology, release documentation, authoritative project overview (`README.md`, `docs/test-and-review-report.md`, `docs/refresh-and-backup.md`).
- Acceptance: claims are traceable and limitations are visible.
- Evidence: Fully overhauled `README.md` with complete audited figures, dashboard module guide, quickstart commands, reproducible test scripts, and data manifest links. All claims are traceable to official tables, and data limitations/discrepancies are prominently documented. Milestone 6 complete.

## Milestone 7 — Institutional Dialectic, Scrutiny & Federal Context

### T070 — Author structured datasets for Committee scrutiny, KIIFB genesis & federalism
- Status: done
- Dependencies: T050, T011
- Outputs: `data/processed/committee_scrutiny.json`, `data/processed/kiifb_genesis.json`, and `data/processed/opposing_pillars_and_federalism.json`.
- Acceptance: G.O.(P) No.80/2026/FIN legality, procedural lapses (ToR bias, sub judice overreach, appointment conflicts, assembly bypass), full member dossiers (Sudha Pillai, Tarun Bajaj, Shyam Srinivasan, Nilesh Vikamsey, H. Shubhalakshmi Narayanan), KIIFB statutory evolution (Act 4 of 2000 to Act 8 of 2016), key people (Isaac, Abraham, Vijayan, Vinod Rai FTAC), Keynesian theoretical premise, and the 7-dimension opposing pillars matrix are fully documented with strict provenance. Registered in `data/manifest.json`.
- Completed: 2026-10-16
- Notes: Created 3 comprehensive datasets with cryptographic hashes registered in manifest.

### T071 — Build automated test suite for institutional and federal scrutiny
- Status: done
- Dependencies: T070
- Outputs: `tests/test_committee_and_genesis.py` (12 new automated unit tests, 41 tests total).
- Acceptance: Verifies executive advisory status of committee, all 4 procedural lapses, member dossiers, specific conflicts (Tarun Bajaj MoF Article 293 deduction; Shyam Srinivasan Federal Bank 5.61% KIFML equity holding in Table 5.6), KIIFB 3-phase statutory evolution, key architects, FTAC trustees, 7-dimension opposing pillars matrix, Article 293(3) ₹25,932.55 Cr deduction sum, Union off-budget double standards (NHAI ₹3.4 lakh Cr, FCI ₹3.8 lakh Cr), and Supreme Court Constitution Bench referral details.
- Completed: 2026-10-16
- Notes: 41 tests pass cleanly in 0.005s.

### T072 — Build Committee Scrutiny & Origins interactive view (`/committee`)
- Status: done
- Dependencies: T070, T071, T013
- Outputs: `src/routes/committee/+page.svelte` and server data loader `src/routes/committee/+page.server.ts`.
- Acceptance: Features 5 interactive tabs (Constitution & Legality, Procedural Lapses, Member Dossiers & Conflicts, Report Origins & Timing, Opposing Pillars & Federal Squeeze), prominent cross-link to `/genesis`, and responsive design. Passes `npm run check` and `npm run build` with zero errors.
- Completed: 2026-10-16
- Notes: Implemented interactive Svelte 5 component with conflict badges, procedural lapse cards, and federalism matrix.

### T073 — Build KIIFB Genesis & Theoretical Premise interactive view (`/genesis`)
- Status: done
- Dependencies: T070, T071, T013
- Outputs: `src/routes/genesis/+page.svelte` and server data loader `src/routes/genesis/+page.server.ts`.
- Acceptance: Features 5 interactive tabs (Statutory Evolution 1999–2016, Key People & FTAC, Theoretical Premise & Multiplier, Revenue Hypothecation Section 7, Opposing Pillars & Federal Squeeze), prominent cross-link to `/committee`, and responsive design. Passes `npm run check` and `npm run build` with zero errors.
- Completed: 2026-10-16
- Notes: Implemented interactive Svelte 5 component with timeline cards, leadership profiles, Keynesian capital principles, and Section 7 transfer breakdown.

### T074 — Integrate navigation, master refresh pipeline and documentation
- Status: done
- Dependencies: T072, T073
- Outputs: Updated `src/routes/+layout.svelte`, `scripts/refresh_pipeline.py`, `data/manifest.json`, `TASKS.md`, and `README.md`.
- Acceptance: Header navigation includes `/committee` and `/genesis` links; master refresh pipeline validates all raw and institutional datasets and passes all 41 unit tests; production build succeeds.
- Completed: 2026-10-16
- Notes: Master pipeline and production build verified cleanly with zero errors.

## Task completion rule

A task is `done` only when acceptance criteria are met, relevant tests have run, sources and metadata are recorded, documentation is updated, and remaining gaps are captured in follow-up tasks.
