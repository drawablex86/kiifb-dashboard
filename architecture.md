# Architecture — KIIFB Accountability & Public Value Dashboard

## 1. Purpose

A source-linked research dashboard comparing the KIIFB Expert Committee Report with official evidence about project funding, delivery, public outcomes, financial obligations, and legal/governance issues.

The architecture prioritises:
- traceability from every displayed claim to a source;
- reproducible calculations;
- separation of raw, cleaned, and derived data;
- explicit uncertainty and conflicting records;
- incremental implementation and maintainability.

The system must not assume that all KIIFB projects are successful or that the committee's financial findings alone determine public value.

## 2. Default system design

```text
Public official sources
  ├── Committee report and appendices
  ├── KIIFB project register / GIS / annual reports
  ├── KITE / KIIDC / implementing departments / SPVs
  ├── State Planning Board / budgets / economic reviews
  └── legislation / government orders / audit reports / court orders
          |
          v
Source acquisition scripts (Python)
  ├── Download and checksum originals
  ├── Write source metadata to manifest
  └── Respect source terms, access limits and rate limits
          |
          v
Immutable raw data: data/raw/
          |
          v
Extraction and normalisation (Python)
  ├── PDF text/table extraction
  ├── CSV/XLSX/HTML ingestion
  ├── validation and data-quality checks
  ├── project/entity matching
  └── reproducible calculations
          |
          v
Processed datasets: data/processed/
          |
          +---- Initial prototype: versioned CSV/JSON
          |
          +---- Mature application: PostgreSQL (+ PostGIS if justified)
                         |
                         v
             SvelteKit server loads/endpoints
                         |
                         v
         SvelteKit + TypeScript dashboard
          ├── committee assertion register
          ├── project explorer and map
          ├── debt and liabilities
          ├── land acquisition
          ├── public-value/outcome evidence
          ├── legal/recommendation tracker
          └── methodology and data-quality view
```

## 3. Architecture principle: begin small

The first working version should use:
- SvelteKit 2, Svelte 5 and TypeScript;
- Python scripts for acquisition, extraction and validation;
- versioned JSON/CSV datasets;
- tests for core calculations and parsing;
- a source manifest;
- strict visual and evidence guidelines defined in `design-system.md`.

Introduce PostgreSQL when multiple related tables, project matching, history, and concurrent filtering become cumbersome in flat files. Introduce PostGIS when actual spatial queries or geographic joins justify it. Add FastAPI only when a separate Python API is required by a concrete use case. Avoid premature Redis, queues, microservices, or orchestration.

If the existing repository already uses a different established stack, inspect it first and document any decision to retain or change it.

## 4. Proposed technology choices

| Concern | Default | Rationale |
|---|---|---|
| Web app | SvelteKit 2 / Svelte 5 | UI, routing, server-side data loading |
| Language | TypeScript | Safer frontend contracts |
| Styling | Tailwind CSS or existing repo convention | Consistent responsive UI |
| Charts | Apache ECharts or existing chart library | Flexible comparative charts |
| Maps | MapLibre GL JS | Interactive maps using appropriately licensed tiles/data |
| Data pipeline | Python, pandas | Tabular cleaning, reconciliation, calculations |
| PDF parsing | PyMuPDF, pdfplumber | Text and table extraction; OCR only if needed |
| Validation | Pydantic and/or Pandera | Schema and data-quality checks |
| Initial storage | CSV/JSON + manifest | Fast, transparent prototype |
| Mature storage | PostgreSQL | Relational source/project/evidence model |
| Geospatial database | PostGIS if needed | District, constituency, and spatial queries |
| DB migrations | Alembic if SQLAlchemy is used | Reproducible schema evolution |
| API | SvelteKit server routes initially | Avoid a second service before necessary |
| Python API | FastAPI only if justified | Separate Python service when required |
| Tests | pytest, repo's frontend tests, Playwright | Data and UI reliability |
| Hosting | Node-compatible SvelteKit hosting + persistent DB | Keep app and persistent storage concerns separate |

## 5. Data layers

### Layer 0 — Original source material

Location: `data/raw/`

Store original PDFs, spreadsheets, CSVs, and permitted downloaded data without editing them. Each item must have a manifest entry with source URL, dates, checksum, local path, and rights/access notes.

### Layer 1 — Extracted and cleaned records

Location: `data/processed/`

Examples:
- `committee_assertions.json`
- `committee_financial_tables.csv`
- `kiifb_projects.csv`
- `kite_education_projects.csv`
- `land_acquisition.csv`
- `source_register.csv`

Preserve source labels and original values alongside normalised values. Never silently overwrite conflicting source data.

### Layer 2 — Derived metrics

Location: `data/derived/` or generated through SQL views.

Examples:
- release-to-approval ratios;
- debt service by year;
- interest/principal split;
- project-status completeness;
- district/sector allocations;
- outcome-evidence completeness;
- scenario calculations.

Every derived field must have a documented formula, unit, reporting period, and test where feasible.

### Layer 3 — Application views

SvelteKit reads prepared files during the prototype or queries PostgreSQL in the mature version. Data access should be server-side for private database credentials. Public source links and evidence metadata may be exposed to the client.

## 6. Core entities and relationships

### `sources`
A source is a document, dataset, official page, government order, court order, or corroborating article.

Fields:
- `source_id`
- `title`
- `publisher`
- `source_type`
- `original_url`
- `final_url`
- `publication_date`
- `reporting_date`
- `retrieved_at`
- `local_path`
- `sha256`
- `content_type`
- `licence_or_terms`
- `reliability_notes`

### `projects`
Fields:
- `project_id` (stable internal ID)
- `official_project_ids` (may be a related table)
- `original_name`
- `normalised_name`
- `sector`
- `subsector`
- `district`
- `local_body`
- `constituency` (nullable)
- `implementing_department`
- `spv`
- `description`

Keep official identifiers and source-specific names. A normalised name must not replace the original.

### `project_financials`
Fields:
- `financial_record_id`
- `project_id`
- `measure_type` (approved, revised_approved, released, received, expenditure, final_cost, repayment, liability)
- `amount`
- `currency`
- `unit`
- `period_start`
- `period_end`
- `as_of_date`
- `source_id`
- `source_locator`
- `definition`
- `confidence`
- `notes`

### `project_milestones`
Fields:
- `milestone_id`
- `project_id`
- `milestone_type`
- `event_date`
- `source_id`
- `source_locator`
- `source_status_text`
- `normalised_status`
- `normalisation_rule`
- `confidence`
- `notes`

### `project_outcomes`
Fields:
- `outcome_id`
- `project_id`
- `outcome_type` (financial, economic, social, distributional)
- `metric_name`
- `value`
- `unit`
- `population_or_scope`
- `measurement_date`
- `methodology`
- `source_id`
- `source_locator`
- `limitations`

### `assertions`
Fields:
- `assertion_id`
- `report_claim`
- `claim_type`
- `report_page`
- `report_table_or_section`
- `evidence_label`
- `assessment`
- `interpretation`
- `caveats`
- `status`

### `evidence_links`
Link assertions, projects, financial records, outcomes, and sources. Include whether the evidence supports, qualifies, challenges, or contextualises a claim, plus a precise locator.

### `land_acquisitions`
Store project-linked approved, paid, unpaid, repaid/reimbursed amounts, land area, acquisition stage, as-of date, source and caveats. Define “repaid” exactly as the source does.

### `debt_records`
Store instrument, principal, rate, fees, maturity, currency, hedging where documented, reporting period, source, and assumptions used for comparisons.

### `recommendations`
Store committee recommendation, rationale, responsible authority, prerequisites, implementation status, source, and evidence of action.

### `data_quality_issues`
Store missing data, conflicts, duplicates, suspicious unit mismatches, stale snapshots, unsupported statuses, and resolution status.

## 7. Evidence labels and status normalisation

Allowed evidence labels and their visual representations are authoritatively specified in [`design-system.md`](design-system.md#22-semantic--evidence-status-badges):
- `committee_finding`
- `official_record`
- `verified_outcome`
- `independent_corroboration`
- `analytical_inference`
- `contested_interpretation`
- `data_gap`
- `unverified_claim`

Normalised project lifecycle statuses and visual badges are defined in [`design-system.md`](design-system.md#23-project-lifecycle-status-badges):
- `approved`
- `tendered`
- `in_progress`
- `physically_complete`
- `handed_over`
- `operational`
- `delayed`
- `cancelled`
- `unknown`
- `conflicting_evidence`

Always retain the original source's status string and date alongside the normalised status. A normalised status is an analytical interpretation based on documented rules, not an assertion that the source itself used that label.

## 8. Financial calculation policy

- Store original values and units; normalise only in derived fields.
- Keep crore/lakh/rupee units explicit and test conversions.
- Do not sum overlapping categories without establishing they are disjoint.
- Distinguish stock figures (debt outstanding at a date) from flow figures (annual transfers or expenditure).
- Distinguish future commitments from current outstanding debt.
- Distinguish direct interest, fees, currency/hedging costs, and opportunity costs.
- Reproduce source calculations first, then present independent alternative calculations separately.
- Every scenario must list assumptions and should not be described as a forecast without supporting methodology.
- Use automated tests to verify known totals and equations, including principal + interest = scheduled debt service when the source defines it that way.

## 9. Public value model

Use separate dimensions:
1. Financial cash return.
2. Economic return.
3. Social return.
4. Distributional return.
5. Financing suitability and fiscal sustainability.

Do not collapse these into a single composite score unless the methodology is explicitly designed, justified, and documented. A missing outcome metric means “not measured/unknown”, not zero. Public assets may generate value without direct cash revenue, but that does not remove the need to assess cost, delivery, use, and financing.

## 10. Acquisition and refresh workflow

1. Check whether a source already exists in the manifest.
2. Check whether a newer source version exists where feasible.
3. Download the source without overwriting the old version.
4. Compute checksum and record retrieval metadata.
5. Run extraction into a new processed version.
6. Validate schema, units, dates, row counts, duplicates and totals.
7. Compare with the previous snapshot and report changes.
8. Update project matches and evidence links only under documented matching rules.
9. Run tests and generate a data-quality report.
10. Update `datasources.md`, `TASKS.md`, and this file if the source or design introduces a new assumption.

## 11. Security and deployment

- Never commit secrets or API keys.
- Keep DB credentials server-side.
- Treat downloaded content as untrusted input.
- Do not execute macros or embedded scripts from source documents.
- Validate file types and size before parsing.
- Keep a backup of the database and the source manifest.
- Deploy only to an environment with persistent database storage.
- Document environment variables in `.env.example` with placeholder values.
- Do not assume local filesystem writes persist on stateless/serverless deployments.

## 12. Architecture decisions and changes

Store material decisions as `docs/decisions/ADR-NNN-title.md`, covering:
- context;
- decision;
- alternatives considered;
- consequences and trade-offs;
- migration/rollback plan;
- date and status.

Update this file when actual implementation diverges from the design. Do not preserve an outdated architecture simply because it was in the initial plan.

## 13. Open questions to resolve through tasks

- Which official project dataset is most complete and reliably downloadable?
- Does KIIFB expose machine-readable project data or require page extraction?
- What are the terms and update cadence of GIS boundary datasets and map tiles?
- Which project identifiers reliably join KIIFB records to KITE, KIIDC and departmental records?
- Which source defines completion, handover and operational status?
- Which outcome metrics are available at institution/project level?
- Which files may be redistributed in the repository?
- At what stage does PostgreSQL become more valuable than versioned flat files?
- Is a separate Python API actually needed?

Do not answer these by assumption; create tasks and record verified findings in `datasources.md` and `TASKS.md`.
