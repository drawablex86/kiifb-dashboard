#!/usr/bin/env python3
"""Master Data Pipeline Refresh Script for KIIFB Dashboard.

Reproduces all data processing steps from data/raw/ to data/processed/.
Validates SHA-256 checksums of archived source documents and tests outputs.
"""

import hashlib
import json
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def verify_raw_sources():
    print("--> Step 1: Verifying SHA-256 Checksums of Raw Sources...")
    manifest_path = PROJECT_ROOT / "data" / "manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    for src in manifest.get("sources", []):
        rel_path = src.get("local_path")
        if not rel_path:
            continue
        p = PROJECT_ROOT / rel_path
        if not p.exists():
            print(f"    [WARN] File not found: {rel_path}")
            continue
        actual_hash = compute_sha256(p)
        expected_hash = src.get("sha256")
        if actual_hash == expected_hash:
            print(f"    [OK] {src['source_id']}: {p.name} ({actual_hash[:12]}...)")
        else:
            print(f"    [FAIL] Hash mismatch for {src['source_id']}: expected {expected_hash[:12]}, got {actual_hash[:12]}")
            return False
    return True


def run_script(script_name: str):
    script_path = SCRIPTS_DIR / script_name
    print(f"--> Executing: {script_name}...")
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, cwd=str(PROJECT_ROOT))
    if res.returncode != 0:
        print(f"    [ERROR] {script_name} failed:")
        print(res.stderr)
        return False
    print(f"    [OK] {script_name} completed.")
    return True


def main():
    print("=" * 60)
    print("KIIFB DASHBOARD — COMPLETE DATA PIPELINE REFRESH")
    print("=" * 60)

    if not verify_raw_sources():
        sys.exit(1)

    steps = [
        "extract_committee_financial_tables.py",
        "extract_kiifb_projects.py",
        "extract_kite_schools.py",
        "build_unified_project_dataset.py",
    ]

    for step in steps:
        if not run_script(step):
            print(f"[FATAL] Pipeline stopped at step {step}")
            sys.exit(1)

    print("--> Step 5: Running Full Verification Test Suite...")
    test_res = subprocess.run([sys.executable, "-m", "unittest", "discover", "tests"], capture_output=True, text=True, cwd=str(PROJECT_ROOT))
    if test_res.returncode != 0:
        print("    [FAIL] Unit tests failed:")
        print(test_res.stderr)
        sys.exit(1)
    print(f"    [OK] {test_res.stderr.strip()}")

    print("=" * 60)
    print("DATA PIPELINE REFRESH COMPLETED SUCCESSFULLY (100% REPRODUCIBLE)")
    print("=" * 60)


if __name__ == "__main__":
    main()
