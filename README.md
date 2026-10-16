# KIIFB Accountability & Public Value Dashboard

An open-source, reproducible civic tech platform providing source-linked analysis of the **2026 Expert Committee Report on KIIFB** contrasted with primary official project delivery databases, audited financial liabilities, and spatial equity across Kerala's 14 districts.

---

## 1. Project Overview

The **Kerala Infrastructure Investment Fund Board (KIIFB)** was reconstituted in 2016 as a corporate statutory financing vehicle to mobilise extra-budgetary resources for public infrastructure. In October 2026, an Expert Review Committee chaired by Dr. K.M. Abraham submitted a comprehensive review of KIIFB's functioning, raising critical questions regarding debt sustainability, off-budget borrowing space deductions under Article 293, and spatial fund distribution.

This dashboard provides citizens, journalists, legislators, and researchers with:
- **Strict Evidence Provenance**: Every assertion and financial figure is traced directly to primary page numbers, table rows, and official gazetted records.
- **Multidimensional Public Value**: Distinguishes narrow commercial cash receipts from macro-economic efficiency, social human capital returns (schools and hospitals), and geographic equity.
- **Audited Financial Baseline**: Reconciles the ₹31,681.15 Cr outstanding debt stock, ₹25,932.55 Cr Article 293(3) borrowing deductions, and ₹47,532.54 Cr 16-year debt service schedule.
- **2,377-Record Project Explorer**: Merges 1,408 KIIFB project sanctions with 969 KITE Sametham public school institutions, tracking physical progress and documenting data gaps.
- **Separation of Powers**: Strictly separates administrative advisory opinions from pending and binding court rulings (such as the Supreme Court of India's Constitution Bench on Article 293).

---

## 2. Key Audited Figures & Reconciled Baseline

| Metric | Official Figure | Primary Source & Reporting Date | Status & Reconciled Note |
|---|---|---|---|
| **Total Approved Capital** | **₹100,341.00 Cr** | Committee Table 4.1 (As on June 30, 2026) | 1,233 infrastructure projects (₹77,151 Cr) + 7 land acquisition projects (₹23,190 Cr). |
| **Total Cumulative Released** | **₹42,327.00 Cr** | Committee Table 4.1 (As on June 30, 2026) | 42.2% overall portfolio absorption (₹30,924 Cr infra + ₹11,403 Cr land pool). |
| **Outstanding Borrowing Stock** | **₹31,681.15 Cr** | Committee Table 3.3 (As on June 30, 2026) | Sanctioned: ₹48,559.69 Cr; Availed: ₹42,193.45 Cr; Repaid: ₹10,512.30 Cr. |
| **Commercial Bank Loans** | **₹6,083.22 Cr** | Committee Table 3.4 (As on June 30, 2026) | 10 banks; sum of rows = ₹6,083.21 Cr (+0.01 Cr Federal Bank rounding documented). |
| **Financial Institutions Debt** | **₹15,380.55 Cr** | Committee Table 3.5 (As on June 30, 2026) | 6 institutions (NABARD, KFW, SBI Cap, HUDCO, NIIF, PFC). |
| **Listed Domestic Bonds** | **₹8,649.97 Cr** | Committee Table 3.7 (As on June 30, 2026) | 8 BSE-listed series (including ₹1,499.70 Cr Green Bonds). |
| **Borrowing Space Deducted** | **₹25,932.55 Cr** | Committee Table 3.11 (2022-23 to 2026-27) | GoI Ministry of Finance deductions under Article 293(3) guidelines. |
| **Scheduled Debt Service to 2041** | **₹47,532.54 Cr** | Committee Table 6.1 (16-Year Amortisation) | Principal: ₹31,857.20 Cr; Interest: ₹15,675.34 Cr across 16 financial years. |
| **Future Project Completion Need** | **₹22,883.00 Cr** | Committee Table 6.3 (2026-27 to 2030-31) | Budgetary capital expenditure required over 5 years to complete prioritised works. |
| **Total Future Fiscal Need** | **₹70,415.54 Cr** | Table 6.1 + Table 6.3 Consolidated | Debt Service (₹47,532.54 Cr) + Project Completion (₹22,883.00 Cr). |
| **Documented Social Assets** | **242 Schools / 118 Hospitals** | KITE Sametham & Committee Chapter IV | 242 schools handed over (969 in directory); ₹3,186 Cr released for healthcare. |
| **Spatial Concentration** | **41.6% in Top 3 Districts** | Committee Table 4.2 | Thiruvananthapuram (₹10,820 Cr), Kannur (₹10,767 Cr), Ernakulam (₹10,514 Cr). |
| **Industrial Land Skewness** | **74.7% in Kannur** | Committee Table 4.3 | Kannur accounts for ₹12,257.50 Cr of ₹16,420.73 Cr total industrial land acquisition. |
| **SC/ST Development Allocation** | **0.24% of Infra Outlay** | Committee Table 4.4 | ₹182 Cr approved (0.24%) vs statutory 12.64% SCSP/TSP benchmark (₹9,752 Cr). |

---

## 3. Dashboard Navigation & Architecture

The dashboard is built with **SvelteKit 2**, **Svelte 5 Runes**, and **Tailwind CSS**, organised into five core interactive views:

```
src/routes/
├── +page.svelte              # 1. Headline Assertions & Citation Drawer
├── projects/+page.svelte     # 2. Unified Project Explorer (2,377 Records)
├── financials/+page.svelte   # 3. Financial Liabilities & Amortisation Model
├── outcomes/+page.svelte     # 4. Public Value, Evidence Ladder & Kerala SVG Map
└── governance/+page.svelte   # 5. Legal Register, Recommendations & Methodology
```

### 1. Headline Assertions & Citation Drawer (`/`)
- Surfaces the 5 central assertions of the debate (`AST-001` through `AST-005`): Borrowing deductions, Debt service burden, Future funding gap, Social delivery reality, and Revenue project premise.
- Interactive slide-over citation drawer displaying exact report locators, source PDFs, and verifications.

### 2. Unified Project Explorer (`/projects`)
- Interactive database of **2,377 records**: 1,408 KIIFB project sanctions cross-referenced with 969 KITE public school institutions.
- Multi-facet filters by administrative department, sector, counting unit, and normalised status.
- Discloses the critical public portal data gap: 100% of projects on KIIFB's live website omit district tags.

### 3. Financial Liabilities & Baseline Model (`/financials`)
- **Debt Stock & Sources**: Interactive breakdown of Table 3.3, commercial banks, financial institutions, and listed bonds.
- **Land Acquisition Pool**: Table 4.5 tracking ₹23,189.74 Cr approved outlays, ₹11,787.37 Cr unpaid balance, and ₹1,386.64 Cr repayments.
- **16-Year Debt Service Schedule**: Interactive amortisation model (2026-27 to 2041-42) charting annual principal vs interest.
- **State Budget Transfers**: Table 3.1 & 3.2 tracking historical statutory MVT and fuel cess transfers.

### 4. Outcomes, Evidence Completeness & Geography (`/outcomes`)
- **5 Public Value Dimensions**: Financial Return (only 3 of 44 projects repaid ₹3,351.90 Cr), Economic Return (`data_gap`), Social Return (242 schools handed over), Distributional Return (spatial skewness), and Financing Suitability (commercial debt for social goods).
- **6-Tier Evidence Completeness Ladder**: Financial coverage (100%) vs Physical milestones (42.5%) vs Handover certificates (19.5%) vs Ex-post outcome studies (8.0%).
- **Itemized Data Gap Register**: Details `GAP-001` through `GAP-004`.
- **Kerala 14-District SVG Map & Bar Charts**: Accessible, keyboard-navigable spatial map color-coded by outlay tiers, paired with Table 4.4 departmental distribution across all 26 sectors.

### 5. Governance, Legal Register & Methodology (`/governance`)
- **Legal & Constitutional Register (`LEG-001` to `LEG-005`)**: Details Article 293(3), Article 266, Entry 37 of List I (Masala bonds), Section 8 prior sanctions, and SCSP/TSP statutory deficits.
- **Judicial Separation**: Documents *State of Kerala v. Union of India* (Original Suit No. 1 of 2024 pending before a 5-judge Constitution Bench) and full redemption of Masala bonds on 27 March 2024.
- **Recommendation Tracker (`REC-001` to `REC-008`)**: Tracks all 8 restructuring recommendations; none are falsely represented as implemented without gazetted evidence.
- **Discrepancy Log & Reproducibility**: Documents `DISC-001` to `DISC-006` and command-line reproduction instructions.

---

## 4. Open Civic Reproducibility Standard

Every calculation, dataset transformation, and UI component in this repository is 100% reproducible from command line.

### Quickstart

```bash
# 1. Clone the repository and install dependencies
git clone https://github.com/drawablex86/kiifb-dashboard.git
cd kiifb-dashboard
npm install

# 2. Run the full automated verification test suite (29 tests)
python3 -m unittest discover tests

# 3. Re-run the data refresh pipeline from raw files
python3 scripts/refresh_pipeline.py

# 4. Check SvelteKit and TypeScript diagnostics
npm run check

# 5. Start the local development server
npm run dev

# 6. Build the production application bundle
npm run build
```

---

## 5. Primary Source Registry

All raw files are preserved in `data/raw/` with verifiable cryptographic hashes recorded in `data/manifest.json`:

| Source ID | Name & Custodian | Reporting Date | SHA-256 Checksum |
|---|---|---|---|
| **`DS001`** | **Expert Committee Review Report** (Kerala Legislative Assembly) | June 30, 2026 | `143f9978bf1b6242e6c251ff5389f7a8183d48778b62e5a02ae75c415cd812ca` |
| **`DS001-LOCAL`** | **Report Full Text Transcription** (Markdown extraction) | June 30, 2026 | `e698d85847aa940cd7ae054ea4e47b0d555957707d23e7ee9eddf8e7ea57f7e5` |
| **`DS010`** | **KIIFB Live Project Register** (KIIFB IT Division) | October 2026 | `c5ad164cce5da54b959acad9a7e6b5ee3eb085025aa72e831b64e1b5ab3e57a6` |
| **`DS021`** | **KITE Sametham Schools Directory** (General Education Dept) | August 2026 | `2841ee59a93c8cceaa0cbc89964166b5b6153a0a0b674869b88498f739f1fb37` |

---

## 6. Project Documentation Sitemap

- [`TASKS.md`](TASKS.md) — Comprehensive task tracking board across all milestones (M0 through M6).
- [`agent.md`](agent.md) — Operating rules, evidence standards, and civic truth constraints.
- [`architecture.md`](architecture.md) — Data model, counting units hierarchy, and technical architecture.
- [`datasources.md`](datasources.md) — Source registry, acquisition instructions, and metadata schema.
- [`design-system.md`](design-system.md) — UI design tokens, typography, Indian financial notation, and accessibility rules.
- [`docs/matching-rules.md`](docs/matching-rules.md) — Matching rules between umbrella sanctions and institutional schools.
- [`docs/test-and-review-report.md`](docs/test-and-review-report.md) — Full test execution, accessibility review, and bundle audit.
- [`docs/refresh-and-backup.md`](docs/refresh-and-backup.md) — Repeatable pipeline commands and backup/restore steps.

---

## 7. License & Ethical Disclaimer

This dashboard is a public-interest civic technology tool released under the MIT License. All data is sourced from publicly available official documents of the Kerala Legislative Assembly, the Government of Kerala, and the Comptroller and Auditor General of India. It maintains strict non-partisan analytical neutrality, separating political narratives from audited numbers.
