# Data Matching & Counting Unit Rules — KIIFB Project Evidence

## 1. Objective

This document defines the strict, non-destructive matching rules and entity disambiguation principles used to join project records from diverse official public sources:
- **`DS010`**: KIIFB Official Project Status Register (`data/raw/kiifb/kiifb-prjStatus.html`, 1,408 project rows).
- **`DS021`**: KITE Sametham Public School Directory (`data/raw/kite/kiifb-funded-schools-sametham.html`, 969 school institutions).
- **`DS001` / `DS001-LOCAL`**: Expert Committee Report (October 2026, Tables 4.1, 4.4, 4.5, 4A.1).
- **`DS020`**: KITE Official Handover Records (242 verified handed-over institutions).

---

## 2. Counting Unit Hierarchy & Distinction

A foundational analytical error in public infrastructure reporting is equating *schemes*, *institutions*, *buildings*, and *contracts*. The system enforces the following hierarchy:

```
Level 1: Umbrella Scheme / Sanctioned Cluster (KIIFB Portfolio Level)
   │  - Examples: "General Education Phase-3 Cluster", "Centres of Excellence in 140 Constituencies (₹5 Cr Scheme)"
   │  - Unit: Sanctioned Portfolio Entry (158 to 175 projects in General Education)
   ▼
Level 2: Institution / Beneficiary Asset (Delivery Level)
   │  - Examples: "G.H.S.S. Kasaragod (School Code: 11002)", "Medical College Hospital, Konni"
   │  - Unit: Physical School or Health Facility (969 KITE Sametham schools; 242 handed-over institutions)
   ▼
Level 3: Individual Building / Package / Physical Work (Contract Level)
      - Examples: "Academic Block 1", "Auditorium & Lab Complex"
      - Unit: Physical Asset / Handover Certificate
```

### Mandatory Rules:
1. **Never conflate a Scheme with an Institution**:
   - 1 KIIFB cluster project entry in `DS010` (e.g. `Ernakulam-Idukki Phase-3 Cluster`) funds multiple individual school institutions.
   - Reporting that KIIFB has 175 General Education projects does NOT mean only 175 schools were funded. Similarly, 969 funded schools does NOT mean 969 separate KIIFB board sanctions.
2. **Never equate "Project Approved" with "Operational"**:
   - In `DS010`, the official status string is almost universally `Project Approved` (1,400+ rows) or `Project Under Evaluation` (7 rows).
   - This source string is preserved as `source_status_text`.
   - The normalised status is computed deterministically:
     - Zero disbursements (`released == 0`): `approved`.
     - Active disbursements (`0 < released < approved`): `in_progress`.
     - Complete financial release (`released >= approved`): `physically_complete` (awaiting formal operational handover certificate).

---

## 3. Matching Protocol & Conflict Resolution

### 3.1 Direct Identifier Matching (Tier 1 — High Confidence)
- **Rule**: Match by explicit alphanumeric identifier (e.g., KIIFB Application ID `official_app_id` or KITE School Code `hs_code`/`hse_code`).
- **Confidence**: `high`.

### 3.2 Canonical Name & Location Normalisation (Tier 2 — Deterministic)
- **Rule**: Normalise institution names by removing honorifics, legal abbreviations (GHSS, GBHSS, G.H.S.S.), converting to lowercase ASCII, and matching within the exact Assembly Constituency and District.
- **Confidence**: `medium`.

### 3.3 Ambiguous or Cluster Matches (Tier 3 — Explicitly Unresolved)
- **Rule**: If a KIIFB project is an umbrella cluster (e.g., `Wayanad Phase-3 Cluster`), it maps to multiple institutions via an explicit 1-to-N relationship in `project_clusters`, NOT by merging rows.
- **Rule**: No fuzzy threshold merges are performed automatically. Any ambiguous match is flagged with `match_confidence: ambiguous` and preserved for manual review.

---

## 4. Discrepancy & Ambiguity Audit Log

| Discrepancy ID | Entities Involved | Nature of Discrepancy | Resolution in Dashboard |
|---|---|---|---|
| **DISC-001** | KIIFB Portal vs Committee Table 4.1 | Portal shows 1,408 projects (Oct 2026); Committee Table 4.1 reports 1,240 approved projects (June 2026 snapshot). | Disclosed explicitly as reporting date gap (June 2026 vs live October 2026). Both snapshots preserved with respective as-of dates. |
| **DISC-002** | KIIFB General Education Outlay vs KITE Schools | Portal reports 175 General Education project rows; KITE Sametham registers 969 individual schools. | Disclosed as counting unit difference: KIIFB sanctions umbrella district/phase clusters (SPVs: INKEL, KITCO, KITE); Sametham lists beneficiary school campuses. |
| **DISC-003** | Status Divergence | KIIFB portal lists all active works under `Project Approved`; KITE reports 242 schools handed over. | Preserved separately: `source_status_text` shows official portal label; `normalised_status` applies objective financial/delivery rules. |
