# Design System — KIIFB Accountability & Public Value Dashboard

> **Note (Oct 2026 UX rework):** This file is **extended (not replaced)** by [`designsystem.md`](./designsystem.md), which adds the two-persona depth system (`Plain English ⇄ Evidence`), humanized vocabulary, ChartFrame/Nudge/Term component specs, and signifier/motion tokens. Token definitions in §2–§4 remain canonical and unchanged.

## 1. Design Principles & UI Truths

The KIIFB Accountability & Public Value Dashboard is a public-interest research tool, not an advocacy platform or a marketing site. The UI design must establish neutrality, rigorous provenance, and clear delineation of evidence states.

### Core Truths:
1. **Traceability Above All**: Every data point, summary card, chart element, and assertion MUST visually expose its provenance (Source ID, locator/page, reporting date, and evidence classification label).
2. **Explicit Evidence States**: A project being "approved" or having "funds released" must never look like or be confused with "physically completed", "handed over", or "operational". Visual status tags must strictly respect evidence hierarchies.
3. **Absence of Evidence != Evidence of Absence**: Missing outcome metrics or unreported social returns must render explicitly as `Unknown / Not Documented`, never as zero or negative performance.
4. **Distinction Between Committee Claims and Verified Reality**: Claims originating directly from the Sudha Pillai Committee Report must be clearly tagged as `committee_finding`, distinguished from `official_record`, `verified_outcome`, or `contested_interpretation`.

---

## 2. Visual Hierarchy & Color Palette

The interface uses a deliberate, sober, editorial/civic-tech palette designed for high legibility, WCAG 2.1 AA/AAA compliance, and clear functional meaning.

### 2.1 Base Colors
- **Canvas / Background**: `#F8FAFC` (Slate 50)
- **Surface / Card Background**: `#FFFFFF` (White)
- **Surface Hover / Subtle Accent**: `#F1F5F9` (Slate 100)
- **Border Default**: `#E2E8F0` (Slate 200)
- **Border Strong**: `#CBD5E1` (Slate 300)
- **Text Primary (Headings & Values)**: `#0F172A` (Slate 900)
- **Text Secondary (Labels & Metadata)**: `#475569` (Slate 600)
- **Text Muted (Footnotes & Captions)**: `#64748B` (Slate 500)

### 2.2 Semantic & Evidence Status Badges
Status indicators use consistent, subdued background tints with high-contrast text to prevent sensory overload while providing immediate categorical distinction:

| Evidence Label | Badge Tint / Border | Text Color | Meaning / Context |
|---|---|---|---|
| `official_record` | `#ECFDF5` / `#A7F3D0` | `#065F46` (Emerald 800) | Primary audited data, statutory records, gazettes |
| `verified_outcome` | `#EFF6FF` / `#BFDBFE` | `#1E40AF` (Blue 800) | Independently verified physical completion / delivery |
| `committee_finding` | `#F5F3FF` / `#DDD6FE` | `#5B21B6` (Purple 800) | Findings/assertions from the 2026 Committee Report |
| `analytical_inference` | `#F0FDF4` / `#BBF7D0` | `#166534` (Green 800) | Derived metric or calculated model (with explicit formula) |
| `contested_interpretation` | `#FFFBEB` / `#FDE68A` | `#92400E` (Amber 800) | Conflicting legal or accounting interpretations |
| `unverified_claim` | `#FFF7ED` / `#FED7AA` | `#9A3412` (Orange 800) | Media reports, uncorroborated press statements |
| `data_gap` / `unknown` | `#F8FAFC` / `#E2E8F0` | `#475569` (Slate 600) | Missing or untracked data points |

### 2.3 Project Lifecycle Status Badges
Status must be visually unmistakable:

- `approved`: Slate / Gray (`#F1F5F9` / `#475569`) - Authorized on paper, no ground work implied.
- `tendered`: Sky / Slate (`#F0F9FF` / `#0369A1`) - Work put to tender.
- `in_progress`: Indigo (`#EEF2FF` / `#4338CA`) - Active construction/execution.
- `physically_complete`: Cyan (`#ECFEFF` / `#0E7490`) - Structure built; not yet handed over.
- `handed_over`: Teal (`#F0FDFA` / `#0F766E`) - Officially transferred to department.
- `operational`: Emerald (`#ECFDF5` / `#047857`) - Serving public / open.
- `delayed`: Amber (`#FFFBEB` / `#B45309`) - Behind schedule or stalled.
- `cancelled`: Red (`#FEF2F2` / `#B91C1C`) - Dropped or revoked.
- `conflicting_evidence`: Rose (`#FFF1F2` / `#BE123C`) - Discrepant status across sources.

---

## 3. Typography & Numerical Formatting

### 3.1 Typeface System
- **UI / Headings / Body**: Modern system sans-serif font stack:
  `font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;`
- **Tabular / Numbers / Financial Figures**: Monospaced font with tabular numerals (`tnum`):
  `font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;`
  `font-variant-numeric: tabular-nums;`
- **Citations / Metadata / Code**: Monospaced font.

### 3.2 Indian Financial Numbering & Notation
All currency figures must adhere strictly to standard Indian financial notation:
- Display in **₹ Crore** (`₹ X,XXX.XX Cr`) or **₹ Lakh** (`₹ XX.XX L`), never in Western Billions/Millions.
- Standard comma separation: Thousands, then two-digit groupings (e.g. `₹31,681.15 Cr`, `₹1,00,341.00 Cr`).
- Always show the unit explicitly alongside or in the column header.
- Distinguish between **Stock** (as-of date, balance) and **Flow** (period, e.g. FY 2021-22 to FY 2024-25).

---

## 4. Component Patterns

### 4.1 Metric Card (KPI / Stat Card)
Every metric card must contain:
1. **Title / Metric Name**: Short, neutral descriptor.
2. **Primary Value**: Formatted with tabular numbers.
3. **Category Indicator**: E.g., `Financial Liability (Stock)` vs `State Budget Transfer (Flow)`.
4. **Source Footer**: Source ID link, page/table locator, reporting as-of date.

### 4.2 Citation Drawer & Tooltip
Hovering or clicking any claim or metric reveals a uniform Citation Popover/Drawer:
- Source Name & Entity (e.g., *Report of the Committee on Comprehensive Review of KIIFB, Oct 2026*).
- Exact Table / Page locator (e.g., *Table 3.3, Page 18*).
- As-of Date (e.g., *30 June 2026*).
- Direct link to PDF / original document extract if available.
- Calculation methodology or caveats (if derived).

### 4.3 Comparison & Discrepancy Tables
When presenting conflicting datasets (e.g., KIIFB GIS Portal vs. Committee Report):
- Present side-by-side with distinct date badges.
- Highlight delta / scope differences explicitly.
- Provide explanatory note regarding reporting date gap (e.g. Dec 2025 vs June 2026).

---

## 5. Accessibility & Responsive Requirements
- Minimum contrast ratio 4.5:1 for normal text, 3:1 for large text and UI components.
- Complete keyboard accessibility for filters, drawers, and project tables.
- Mobile/Tablet adaptive layouts with horizontal scroll affordance for rich data tables.
