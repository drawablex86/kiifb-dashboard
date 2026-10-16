# Data Refresh, Backup & Reproducibility Guide (T061)

This document provides repeatable commands and procedures to refresh data processing, verify raw source integrity, and perform backup/restore operations.

---

## 1. Quick Data Refresh Command

To refresh the entire data pipeline from raw sources, re-run all extraction scripts, build unified datasets, and run all validation tests:

```bash
python3 scripts/refresh_pipeline.py
```

### Execution Steps in Pipeline:
1. **Source Integrity Check**: Validates SHA-256 checksums of archived source files in `data/raw/` against `data/manifest.json`.
2. **Financial Table Extraction**: Executes [`scripts/extract_committee_financial_tables.py`](file:///Users/rahulrajeev/Downloads/kiifb-dashboard/scripts/extract_committee_financial_tables.py) to generate [`data/processed/committee_financial_tables.json`](file:///Users/rahulrajeev/Downloads/kiifb-dashboard/data/processed/committee_financial_tables.json).
3. **KIIFB Project Extraction**: Executes [`scripts/extract_kiifb_projects.py`](file:///Users/rahulrajeev/Downloads/kiifb-dashboard/scripts/extract_kiifb_projects.py) to parse 1,408 project records into [`data/processed/kiifb_projects.json`](file:///Users/rahulrajeev/Downloads/kiifb-dashboard/data/processed/kiifb_projects.json).
4. **KITE Schools Extraction**: Executes [`scripts/extract_kite_schools.py`](file:///Users/rahulrajeev/Downloads/kiifb-dashboard/scripts/extract_kite_schools.py) to parse 969 school records into [`data/processed/kite_schools.json`](file:///Users/rahulrajeev/Downloads/kiifb-dashboard/data/processed/kite_schools.json).
5. **Unified Dataset Build**: Executes [`scripts/build_unified_project_dataset.py`](file:///Users/rahulrajeev/Downloads/kiifb-dashboard/scripts/build_unified_project_dataset.py) to generate the unified 2,377-record dataset in [`data/processed/unified_project_explorer.json`](file:///Users/rahulrajeev/Downloads/kiifb-dashboard/data/processed/unified_project_explorer.json).
6. **Integrity Test Suite**: Runs all 29 automated reconciliation tests (`python3 -m unittest discover tests`).

---

## 2. Primary Source Manifest & File Paths

| Source ID | File Name & Location | File Type & Size | SHA-256 Checksum |
|---|---|---|---|
| **`DS001`** | `data/raw/committee-report/kiifb-expert-committee-report.pdf` | PDF (80.3 MB) | `143f9978bf1b6242e6c251ff5389f7a8183d48778b62e5a02ae75c415cd812ca` |
| **`DS001-LOCAL`** | `data/KIIFB Findings Report.md` | Markdown (244.8 KB) | `e698d85847aa940cd7ae054ea4e47b0d555957707d23e7ee9eddf8e7ea57f7e5` |
| **`DS010`** | `data/raw/kiifb/kiifb-prjStatus.html` | HTML (756.5 KB) | `c5ad164cce5da54b959acad9a7e6b5ee3eb085025aa72e831b64e1b5ab3e57a6` |
| **`DS021`** | `data/raw/kite/kiifb-funded-schools-sametham.html` | HTML (767.0 KB) | `2841ee59a93c8cceaa0cbc89964166b5b6153a0a0b674869b88498f739f1fb37` |

### Manual Checksum Verification Command

```bash
# Verify checksums on macOS / Linux
shasum -a 256 data/raw/committee-report/kiifb-expert-committee-report.pdf
shasum -a 256 data/raw/kiifb/kiifb-prjStatus.html
shasum -a 256 data/raw/kite/kiifb-funded-schools-sametham.html
```

---

## 3. Backup & Archival Procedure

To create a self-contained archive of raw source documents and processed datasets:

```bash
# Create timestamped tarball archive of raw and processed data
tar -czvf kiifb-data-backup-$(date +%Y%m%d).tar.gz data/raw/ data/processed/ data/manifest.json
```

### Restore Procedure:

```bash
# Restore data archive
tar -xzvf kiifb-data-backup-YYYYMMDD.tar.gz

# Re-verify and rebuild pipeline
python3 scripts/refresh_pipeline.py
```
