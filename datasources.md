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
- Caveat: A status such as “Project Approved” is not evidence of tender, construction, completion, handover, or operation. Preserve the original status label.
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

- Starting URL: https://www.kiifb.org/
- Known annual-report document previously located: https://www.kiifb.org/includes/fileViewer.jsp?dPrfx=RPT&did=440&fmde=res&fname=AnnualReport-KIIFB-2023-24.pdf
- Purpose: Audited financial statements, debt information, project progress, annual outputs, governance and management disclosures.
- Acquisition: Search the official KIIFB site for all available annual reports, financial statements, debt disclosures, and relevant appendices. Verify that links resolve and archive each document.
- Download target: `data/raw/kiifb/annual-reports/<report-year>/`
- Caveat: Annual report project counts may use a different date or definition than the committee report. Preserve report-year context.
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
- Caveat: School directory data may not provide actual expenditure, handover date, or current utilisation.
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

### DS030 — Kerala State Planning Board Economic Review 2025, Volume I

- URL: https://spb.kerala.gov.in/sites/default/files/2026-01/ER%202025%20Volume1%20Eng%20final.pdf
- Type: Official PDF.
- Purpose: Statewide sectoral context, infrastructure expenditure, roads, transport, education, health and economic indicators.
- Download target: `data/raw/state-planning-board/economic-review/2025/`
- Caveat: Budgetary and sectoral categories may not map one-to-one to KIIFB project records.

### DS031 — Kerala Development Report 2026

- URL: https://spb.kerala.gov.in/wp-content/uploads/2026/01/kerala-development-report_2026.pdf
- Alternate previously encountered URL: https://spb.kerala.gov.in/sites/default/files/inline-files/Kerala_Report_2026.pdf
- Purpose: Development outcomes and infrastructure delivery context, including education and sectoral indicators.
- Download target: `data/raw/state-planning-board/development-report/2026/`
- Caveat: Preserve the report's own definitions, date and category boundaries. Do not merge figures with KIIFB annual-report counts without reconciling methodology.

### DS032 — State budget and Finance Department documents

- Starting point: Kerala Finance Department / official State budget portal. Search official sources for budget estimates, revised estimates, actuals, borrowing limits, guarantees, public debt, transfers to KIIFB and relevant fiscal statements.
- Search terms: `Kerala budget KIIFB transfer public debt guarantees`, `Kerala Finance Accounts KIIFB`, `Kerala budget documents 2025-26`.
- Save exact official URLs and report periods here after verification.
- Purpose: Verify State transfers, debt-service support, fiscal context and the treatment of KIIFB liabilities.
- Priority: Critical.

### DS033 — Kerala Economic Review and sector reports

- Starting point: Kerala State Planning Board publications: https://spb.kerala.gov.in/
- Purpose: Roads, coastal infrastructure, education, healthcare, industrial development, water and other sector outputs.
- Acquisition: Find the exact publication, table, page and reporting period. Archive the report and record definitions.
- Caveat: Sector totals can overlap with KIIFB project totals; do not add them without a documented reconciliation.

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
