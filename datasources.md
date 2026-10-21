# Data Sources and Acquisition Registry — KIIFB Dashboard

## 1. Purpose and usage

This file is the living registry of public sources for the KIIFB Accountability & Public Value Dashboard.

The agent must:
- search for additional relevant public sources when a required field is missing;
- prefer primary official records;
- download and archive sources where permitted and useful;
- verify every downloaded file;
- record source/reporting dates and retrieval metadata;
- update this file whenever a source is added, replaced, found unreliable, or found to have different definitions than expected.

A URL listed here is a starting point, not proof that the page is available, current, complete, machine-readable, or suitable for automated retrieval. Verify each source in the current session.

## 2. Source acquisition rules

For each source, record:
- stable `source_id`;
- source title and publisher;
- original URL and final URL after redirects if available;
- source type and file format;
- publication date;
- reporting/as-of date;
- retrieval timestamp;
- local repository path;
- SHA-256 checksum;
- relevant page/table/sheet/section;
- licence/terms or redistribution limitations;
- reliability and known caveats;
- update cadence, if known.

Suggested repository layout:

```text
data/
  raw/
    committee-report/
    kiifb/
    kite/
    kiidc/
    state-planning-board/
    government-and-legal/
    other-official/
  processed/
  derived/
  manifest.json
  README.md
```

Keep originals immutable. Do not replace a prior snapshot with a newer file; archive each version separately and compare changes. Do not commit very large files or files whose redistribution rights are unclear. In those cases, retain a retrieval script and source instructions instead.

Respect website terms, robots rules, rate limits, access controls, and applicable copyright. Do not bypass CAPTCHAs, authentication, or paywalls. If automated downloads fail, record the failure and a safe manual retrieval path.

## 3. Primary source: Expert Committee Report

### DS001 — KIIFB Expert Committee Report (Official PDF)

- URL: https://www.niyamasabha.org/codes/16kla/session_2/Report%20of%20KIIFB_combined.pdf
- Publisher/host: Kerala Legislative Assembly / Niyamasabha website.
- Type: PDF report.
- Purpose: Primary source for committee findings, financial tables, land-acquisition tables, recommendations, legal arguments, and project/governance assertions.
- Download target: `data/raw/committee-report/<retrieval-date>/kiifb-expert-committee-report.pdf`
- Processing: Extract text and tables with PyMuPDF/pdfplumber from the primary PDF; reconcile with `DS001-LOCAL`. Store a page-indexed text representation and table extracts under `data/processed/committee-report/`.
- Must capture: report date, contents, page numbers, table names, units, reporting dates, footnotes, and methodology.
- Caveat: This is a committee report, not a judicial decision. Verify every key baseline figure against the actual report page/table.
- Initial priority: Critical.

### DS001-LOCAL — KIIFB Expert Committee Report (Local Markdown Extract)

- Local Path: `data/KIIFB Findings Report.md`
- Origin: Pre-existing local markdown transcript of the October 2026 Committee Report (chaired by Sudha Pillai).
- Size/Extent: 2,400 lines; contains full Chapters I-VI and Tables 3.1 to 4.4.
- Purpose: Enables immediate offline extraction of the 5 headline assertions (`T010`) and core financial tables (`T030`) while awaiting PDF download and validation.
- Verification status: Verified present in repository baseline during `T001`. To be registered in `data/manifest.json` during `T002`.

### DS002 — Supreme Court proceedings concerning Kerala borrowing limits

- Starting search: https://www.sci.gov.in/
- Search for: `State of Kerala v Union of India Article 293 1 April 2024`
- Purpose: Establish what the Court actually decided, what was referred or left unresolved, and distinguish interim orders from final merits decisions.
- Download target: `data/raw/government-and-legal/supreme-court/`
- Must capture: case name, case number, order/judgment date, operative directions, paragraph/page locator, official URL.
- Caveat: Do not rely on media headlines where the actual order is available.

## 4. KIIFB sources

### DS010 — KIIFB project-status database

- URL: https://www.kiifb.org/prjStatus.jsp
- Type: Official web project register/dashboard.
- Purpose: Project names, implementing agencies/SPVs, approval amounts, releases, and published project statuses.
- Download strategy: Inspect page structure and linked resources. Prefer downloadable files or documented endpoints if available. If scraping is necessary, follow site terms and rate limits; retain the source page and extraction timestamp.
- Download target: `data/raw/kiifb/project-status/<retrieval-date>/`
- Automated crawl: `python3 scripts/fetch_kiifb_portal.py` (**T080**). Archives a dated immutable snapshot to `data/raw/kiifb/project-status/<YYYY-MM-DD>/kiifb-prjStatus.html`, records SHA-256 and HTTP metadata under `data/manifest.json → live_crawls`, and skips archiving when content is unchanged from the previous crawl. The pinned baseline above is never overwritten.
- Caveat: A status such as “Project Approved” is not evidence of tender, construction, completion, handover, or operation. Preserve the original status label.
- **Live-crawl status (2026-10-20):** crawl succeeded; returned content differs from the 2026-10-16 pinned baseline (same byte size, different SHA-256 — portal has updated since). Snapshot at `data/raw/kiifb/project-status/2026-10-20/`.
- Initial priority: Critical.

### DS011 — KIIFB integrated GIS dashboard

- URL: https://gis.kiifb.org/
- Type: Official GIS/map dashboard.
- Purpose: Project locations, categories, project portfolio snapshots, and spatial exploration.
- Download strategy: Inspect visible records, map layers, metadata, and any official downloadable services. Do not assume that a web map exposes a supported public API. Verify the underlying source and licensing before downloading boundaries or geometries.
- Download target: `data/raw/kiifb/gis/<retrieval-date>/`
- Caveat: Previously observed snapshot was dated 31 December 2025 and reported totals different from the committee's June 2026 snapshot. Preserve both snapshots and explain date/scope differences.
- Initial priority: High.

### DS012 — KIIFB annual reports and financial disclosures

- Starting URL: https://www.kiifb.org/resources.jsp (`RPT` block; documents served via `fileViewer.jsp?dPrfx=RPT&did=<n>&fmde=res&fname=<file>`)
- Purpose: Audited financial statements, debt information, project progress, annual outputs, governance and management disclosures.
- **Acquired (2026-10-21, T084):**
  - `data/raw/kiifb/annual-reports/2025-26/AnnualReport-KIIFB-2025-26.pdf` — FY 2025-26 Annual Report & Audited Accounts, published 2026-09-07 (SHA-256 `73285f74...`).
  - `data/raw/kiifb/annual-reports/2024-25/AnnualReport-KIIFB-2024-25.pdf` — FY 2024-25 edition, published 2025-09-03 (SHA-256 `5dc2f1b4...`).
  - Both checksum-registered under `data/manifest.json → sources[]` (compound `sha256`; per-file hashes authoritative in `files[]`).
- The full archive listing (2016-17 through 2023-24, `did=50..440`, e.g. `AnnualReport-KIIFB-2023-24.pdf` at did=440) remains available at resources.jsp; fetch on demand if a specific fiscal year is needed.
- Caveat: Annual report project counts may use a different date or definition than the committee report. Preserve report-year context. No explicit open licence is stated on the documents — official KIIFB publication, use with attribution and source link.
- Initial priority: Critical.

### DS013 — KIIFB news, newsletters and project-completion releases

- Starting URL: https://www.kiifb.org/
- Purpose: Supporting evidence for completion, inauguration, handover, milestones, and specific project outputs.
- Acquisition: Search official news and newsletter pages by project name and date. Store the original page or PDF where permitted.
- Caveat: Publicity announcements are useful evidence but should be corroborated for disputed claims; distinguish inauguration from sustained operation.
- Initial priority: Medium.

## 5. Education and implementing agencies

### DS020 — KITE infrastructure progress

- URL: https://kite.kerala.gov.in/KITE/index.php/welcome/infra
- Type: Official implementing-agency page/dashboard.
- Purpose: KIIFB-funded education infrastructure, scheme-level progress and reported completion/handover counts.
- Download target: `data/raw/kite/infra/<retrieval-date>/`
- Required investigation: Determine whether the reported count refers to projects, institutions, schemes, buildings, or a combination. Obtain a project/institution-level list where available.
- Caveat: A scheme count must not be equated automatically with the number of new buildings or schools.
- Initial priority: Critical.

### DS021 — KITE KIIFB-funded schools directory

- URL: https://sametham.kite.kerala.gov.in/KIIFBFundedSchools/spv
- Type: Official education directory / project listing.
- Purpose: School-level matching, school identifiers, location, scheme and project status where available.
- Download strategy: Inspect page and any downloadable records. Respect site restrictions; avoid collecting student-level personal data.
- Download target: `data/raw/kite/kiifb-funded-schools/<retrieval-date>/`
- Automated crawl: `python3 scripts/fetch_kite_sametham.py` (**T080**). Archives a dated immutable snapshot to `data/raw/kite/kiifb-funded-schools/<YYYY-MM-DD>/kiifb-funded-schools-sametham.html`, records SHA-256 and HTTP metadata under `data/manifest.json → live_crawls`, and skips archiving when content is unchanged from the previous crawl. The pinned baseline above is never overwritten.
- Caveat: School directory data may not provide actual expenditure, handover date, or current utilisation.
- **Live-crawl status (2026-10-20):** crawl succeeded; returned content is byte-identical to the 2026-10-16 pinned baseline (SHA-256 `2841ee59...`).
- Initial priority: Critical.

### DS022 — KIIDC KIIFB projects

- URL: https://kiidc.kerala.gov.in/kiifb-projects/
- Type: Official implementing agency project listing.
- Purpose: Water resources and other KIIDC-implemented projects, where included.
- Download target: `data/raw/kiidc/kiifb-projects/<retrieval-date>/`
- Caveat: Verify the scope of the listing and whether project status is current.

### DS023 — KIIDC funded projects

- URL: https://kiidc.kerala.gov.in/kiifb-funded-projects/
- Purpose: Cross-check project names, implementation details, status, and project-specific documents.
- Download target: `data/raw/kiidc/funded-projects/<retrieval-date>/`
- Caveat: Avoid treating a project listing as a final completion certificate.

### DS024 — Relevant departmental and SPV project records

- Starting point: identify each department/SPV from KIIFB project records, then locate its official project page, tender, progress report, completion certificate, or annual report.
- Candidate agencies include Public Works Department, Health and Family Welfare, Water Resources, Power, IT, education agencies, KINFRA, KIIDC, and relevant SPVs.
- Save source-specific entries in this registry as they are discovered.
- Priority: High, project by project.

## 6. State Planning Board and public statistics

### DS034 — Kerala State Planning Board Economic Review 2025, Volume I

- URL: https://spb.kerala.gov.in/sites/default/files/2026-01/ER%202025%20Volume1%20Eng%20final.pdf
- Type: Official PDF.
- Purpose: Statewide sectoral context, infrastructure expenditure, roads, transport, education, health and economic indicators.
- Download target: `data/raw/state-planning-board/economic-review/2025/`
- Caveat: Budgetary and sectoral categories may not map one-to-one to KIIFB project records.
- Note: **Renumbered from `DS030` to `DS034` on 2026-10-20** — `DS030` belongs to the acquired Kerala Kanakku Open Data Suite below (registered in `data/manifest.json`, referenced by all processed datasets). This entry has never been downloaded/acquired, so the renumbering touches this registry only.

### DS031 — Kerala Development Report 2026

- URL: https://spb.kerala.gov.in/wp-content/uploads/2026/01/kerala-development-report_2026.pdf
- Alternate previously encountered URL: https://spb.kerala.gov.in/sites/default/files/inline-files/Kerala_Report_2026.pdf
- Purpose: Development outcomes and infrastructure delivery context, including education and sectoral indicators.
- Download target: `data/raw/state-planning-board/development-report/2026/`
- Caveat: Preserve the report's own definitions, date and category boundaries. Do not merge figures with KIIFB annual-report counts without reconciling methodology.

### DS032 — State budget and Finance Department documents

- Starting point: official Kerala budget portal `budget.kerala.gov.in` (documents under `keralabudgetdoc/<fiscal-year>/` — e.g. `AFS.pdf`, `BudgetinBrief.pdf`, DBE volumes, Summary Document) and the Finance Department index at `finance.kerala.gov.in/bdgtDcs.jsp`.
- **Acquired (2026-10-21, T084):**
  - `data/raw/finance/budget/2025-26/AFS-2025-26.pdf` — Annual Financial Statement 2025-26, laid before the Legislature, Feb 2025 (SHA-256 `121e903b...`).
  - `data/raw/finance/budget/2026-27/AFS-2026-27.pdf` — Annual Financial Statement 2026-27, first budget after the 2026 assembly election (SHA-256 `34c9bcca...`).
  - Checksum-registered under `data/manifest.json → sources[]`.
- Purpose: Verify State transfers to KIIFB, debt-service support, borrowing limits, guarantees and the treatment of KIIFB liabilities inside the receipts and public-debt statements.
- Caveat: PDF text layers could not be verified with the tooling available (no pdftotext); KIIFB-specific line-item extraction is pending a text-extraction pass. Treat as *registered & archived*, not yet *ingested*. Later fiscal years exist at the same URL pattern.
- Search terms: `Kerala budget KIIFB transfer public debt guarantees`, `Kerala Finance Accounts KIIFB`, `keralabudgetdoc AFS.pdf`.
- Priority: Critical.

### DS044 — KIIFB bond issuance & SEBI disclosures (acquired)

- Starting URL: https://www.kiifb.org/resources.jsp (`CMPL` compliance block, row prefix `FA-6/2027/2021/KIIFB`; documents via `fileViewer.jsp?dPrfx=CMPL&did=<n>&fmde=res&fname=<file>`)
- **Acquired (2026-10-21, T084):**
  - `data/raw/kiifb/bonds/masala-bond-2019/KIIFB-MasalaBond.pdf` — Masala bond document (did=99; a 1-page booklet — **gap:** the full LSE prospectus/offer document was NOT located in this pass and needs manual retrieval; noted in §9).
  - `data/raw/kiifb/sebi-filings/2025-26/KIIFB-Reg27-AnnualComplianceReport-FY2025-26.pdf` — SEBI LODR Regulation 27(2) Annual Compliance Report, FY 2025-26 (did=761).
  - Checksum-registered under `data/manifest.json → sources[]`.
- Purpose: Debt stock, interest obligations, use-of-proceeds (Reg 52(7) statements of utilisation), audit qualifications, and bond-servicing behaviour over time — the deepest public financial evidence after the Annual Reports.
- High-value follow-ups in the same CMPL table: quarterly Reg 52(7) "Statement of utilisation of issue proceeds", "Audited Financial Results (Standalone and Consolidated)", "Statement of Impact of Audit Qualifications".
- Rights: official KIIFB publication (SEBI-listed entity disclosure); no explicit licence — use with attribution and source link.
- Initial priority: High.

### DS046 — KIIFB RTI disclosures and CIC rulings (candidate; not yet acquired)

- Starting point: https://www.kiifb.org/ (RTI disclosures section) and Central Information Commission decision search.
- Purpose: Voluntary RTI disclosures, CIC decisions on KIIFB information requests (project-wise release figures, contractor information not on the portal).
- Acquisition plan: identify the RTI disclosure page/URL and archive disclosures relevant to project finance; date-stamp every retrieval. Record access terms before ingesting.
- Caveat: RTI disclosures are point-in-time responses; verify against portal figures before use.
- Priority: Medium.

### DS047 — Niyamasabha (Kerala Legislative Assembly) questions & papers (candidate; not yet acquired)

- Starting point: https://www.niyamasabha.org/ ( starred/off-listed questions, budget documents, committee papers mentioning KIIFB).
- Purpose: Independent legislative scrutiny — questions on KIIFB releases, stalled projects, guarantees; floor statements with project names and amounts.
- Acquisition plan: search the 15th/16th KLA business lists for "KIIFB" questions; archive question + answer pairs with session/date metadata.
- Caveat: answers given on the floor vary in completeness; treat as supporting evidence, never as the sole source for a financial figure.
- Priority: Medium.

### DS033 — Kerala Economic Review and sector reports

- Starting point: Kerala State Planning Board publications: https://spb.kerala.gov.in/
- Purpose: Roads, coastal infrastructure, education, healthcare, industrial development, water and other sector outputs.
- Acquisition: Find the exact publication, table, page and reporting period. Archive the report and record definitions.
- Caveat: Sector totals can overlap with KIIFB project totals; do not add them without a documented reconciliation.

### DS030 — Kerala Kanakku Open Data Suite (civic open data; acquired)

- URL: https://keralakanakku.com/en/data (data page; CSV endpoints discovered at `https://keralakanakku.com/api/v1/projects.csv`, `.../funding.csv`, `.../liability.csv`)
- Publisher/host: Kerala Kanakku (Kanakku Civic Tech Project), independent civic tech project.
- Type: CSV open-data extracts; joins KIIFB's internal GIS portal (`gis.kiifb.org`), KIIFB `prjStatus.jsp`, and the Kerala PWD Defect Liability Period register.
- Purpose: Verified districts, assembly constituencies, GPS coordinates for KIIFB sub-projects/contract packages (bridging `GAP-001`), funding joins, and PWD contractor liability (2,475 works).
- Licence: Creative Commons Attribution 4.0 International (CC BY 4.0); code AGPL-3.0. Derivatives must carry attribution.
- Pinned baselines (2026-10-16): `data/raw/kanakku/projects.csv`, `data/raw/kanakku/funding.csv`, `data/raw/kanakku/liability.csv` (checksums in `data/manifest.json`).
- Automated crawl: `python3 scripts/fetch_kanakku.py` (**T080**). Discovers the three CSV endpoints from the public data page, then archives a complete dated snapshot to `data/raw/kanakku/<YYYY-MM-DD>/`, recording SHA-256 and HTTP metadata under `data/manifest.json → live_crawls`. Skips archiving when content is unchanged from the previous crawl. If discovery ever breaks, pass explicit endpoints: `--urls <projects.csv>,<funding.csv>,<liability.csv>`.
- Caveat: Coordinates and constituencies are Kanakku's daily compilation of KIIFB's internal GIS portal, not a KIIFB-published register field (GAP-001 context). Land-acquisition scope derives from the same pool (industrial land skew, 74.7% Kannur).
- **Live-crawl status (2026-10-20):** crawl succeeded. `projects.csv` and `liability.csv` are byte-identical to the pinned baseline; `funding.csv` differs (new SHA-256 `7acbab95...`, same 4,546 rows) — an in-place value update since 2026-10-16.
- Initial priority: High.

> **Manifest `live_crawls` section (added in T080):** every automated crawl appends an immutable record — `{source_id, retrieved_at, url, arc_dir, files: [{name, sha256, url, http_status, unchanged?, file_size_bytes?}], status: success | unchanged | failure | dry-run, note}` — to `data/manifest.json`, leaving the pinned `sources[]` entries untouched so baseline checksum verification keeps working unchanged.

## 7. Legal and audit sources

### DS040 — KIIFB Act and amendments

- Starting point: Kerala Law Department and official Kerala legislation sources.
- Search for: `Kerala Infrastructure Investment Fund Act 1999 amended Sections 8 9 official`.
- Purpose: Exact statutory text and amendments relevant to committee assertions.
- Store under: `data/raw/government-and-legal/legislation/kiifb-act/`
- Caveat: Record version/effective date and amendment history. Do not cite an outdated consolidation as current law.

### DS041 — Constitution of India

- Starting point: official Government of India legislation/constitution portal.
- Purpose: Articles 266 and 293 and any relevant constitutional text.
- Store under: `data/raw/government-and-legal/constitution/`
- Caveat: Constitutional text is necessary but does not by itself resolve contested interpretation.

### DS042 — CAG and Accountant General reports

- Starting point: https://cag.gov.in/
- Search for Kerala State Finance Audit Reports, Finance Accounts, performance audits, KIIFB-related audits and implementing-agency audits.
- Purpose: Independent audit evidence, financial controls, project implementation and fiscal risk.
- Store under: `data/raw/government-and-legal/cag/`
- Caveat: Distinguish audit observations, replies, draft findings, final findings, and later corrective action.

### DS043 — Government Orders and official committee/reorganisation decisions

- Starting point: official Kerala government order and department portals.
- Purpose: Verify whether committee recommendations have been accepted, implemented, modified or rejected.
- Store under: `data/raw/government-and-legal/government-orders/`
- Caveat: A recommendation in a report is not an implemented policy. Require a dated official action record.

## 8. Public project outcome data to seek

For each project, search for the strongest available evidence of:
- completion certificate;
- formal handover;
- current operational status;
- physical progress;
- actual expenditure/final cost;
- tender/contract details;
- beneficiary count and usage;
- sector-specific outcome metrics;
- maintenance and operating cost;
- land acquisition status and use.

Examples:
- Education: school code, project name, completed facilities, handover date, enrolment and usage metrics when public.
- Health: facility, service availability, equipment commissioning, patient use and staffing where published.
- Roads: route and length, completion/opening, connectivity, travel-time or safety data where measured.
- Power: commissioned capacity, operational date, reliability outcomes where published.
- Water: households/areas served, operational status, supply reliability and capacity.
- Digital connectivity: connections actually active, service availability and use, not only network infrastructure installed.
- Industrial parks: land developed, units operational, employment and investment only when official records support it.

Do not collect personal or sensitive individual-level records. Prefer aggregate, anonymised public metrics.

## 9. Source discrepancy register

The agent must maintain a discrepancy table in `datasources.md` or a linked `data-quality.md` with:
- issue ID;
- source A and source B;
- values and definitions;
- reporting dates;
- suspected reason for difference;
- investigation performed;
- resolution or unresolved status.

Known discrepancy to investigate:
- The KIIFB GIS snapshot previously observed as of 31 December 2025 reported 1,205 infrastructure projects, ₹76,486.57 crore in infrastructure, 7 land-acquisition pool projects worth ₹20,000 crore, total ₹96,486.57 crore and ₹38,293 crore disbursed.
- The committee report's 30 June 2026 snapshot reports 1,233 infrastructure projects worth ₹77,151 crore, 7 land-acquisition projects worth ₹23,190 crore, total ₹100,341 crore and ₹42,327 crore released.
- These snapshots differ by date and possibly scope/definitions. Do not silently reconcile or assume error.

Other potential discrepancies:
- KITE scheme counts versus building/school counts in annual reports.
- Project-approved status versus completion/handover claims.
- Statewide sector totals versus KIIFB-only totals.
- Approved cost versus revised cost and actual expenditure.
- Land-acquisition amount paid versus amount reimbursed/repaid.

Registered through T084 (2026-10-21) — baseline-integrity notes:
- **DISC-T084a — DS032 budget AFS vs committee figures.** The acquired Annual Financial Statements (2025-26, 2026-27) are *registered & archived* only: their text layers have not been extracted/ingested (no PDF text tool in the acquisition environment). Ingestion must NOT re-baseline any existing processed dataset (`committee_financial_tables.json` remains anchored to DS001); when AFS line items are extracted, they arrive as new reconciliation inputs and any figure conflicts land in this register.
- **DISC-T084b — Masala bond prospectus gap.** KIIFB-MasalaBond.pdf (did=99) is a 1-page booklet, not the LSE offer document. The full prospectus/full national security structure filing must be retrieved manually from London Stock Exchange filings before any bond-size or use-of-proceeds claim is derived from it.
- **DISC-T084c — annual-report vs portal date regimes.** DS012 annual reports state FY-based delivery/financial figures whose as-of dates differ from the prjStatus.jsp live register and the committee's June 2026 snapshot. Cross-referencing requires preserve-as-of-date discipline; no re-baselining of DS010 processed data.

## 10. Search and download workflow

For each new data requirement:

1. Define the missing field or claim precisely.
2. Search the official source first.
3. Confirm that the source addresses the right project, time period and metric.
4. Download the original where permitted.
5. Verify file type, size, page count/row count, and checksum.
6. Add it to the manifest.
7. Extract into a new processed file without altering the original.
8. Record column definitions, units, date, and source locator.
9. Validate totals, duplicates, missing values, and category scope.
10. Add the source to this file and link it from the relevant task.
11. If the source changes the architecture or data model, update `architecture.md` and create an ADR if material.
12. Record unresolved issues instead of guessing.

## 11. Search-query suggestions

Use queries targeted at specific official domains and project names. Examples:
- `site:kiifb.org "project name" completion`
- `site:kiifb.org filetype:pdf annual report KIIFB`
- `site:kite.kerala.gov.in KIIFB completed handed over school`
- `site:spb.kerala.gov.in "project name"`
- `site:cag.gov.in Kerala KIIFB audit`
- `site:kerala.gov.in KIIFB government order`
- `site:sci.gov.in State of Kerala Union of India Article 293`
- `site:kiidc.kerala.gov.in "project name"`

Search results are discovery aids. Open and inspect the underlying source before citing a claim.

## 12. Update policy

Whenever a new source is discovered:
- add a `DS###` entry;
- record exact purpose and source caveats;
- record the local path and manifest ID after successful download;
- update relevant tasks and data dictionaries;
- add known discrepancies or reliability notes;
- update `architecture.md` if the source requires a new ingestion method, entity, or relationship.

Do not remove a source merely because a newer one appears. Mark it superseded and preserve it if it supports a historical snapshot or explains a discrepancy.
