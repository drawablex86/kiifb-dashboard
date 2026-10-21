#!/usr/bin/env python3
"""Master Data Pipeline Refresh Script for KIIFB Dashboard.

Reproduces all data processing steps from data/raw/ to data/processed/.
Validates SHA-256 checksums of archived source documents and tests outputs.
"""

import argparse
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
            print(f"    [FAIL] Source path does not exist: {rel_path}")
            return False

        if p.is_dir() and "files" in src:
            for subfile in src["files"]:
                sub_p = p / subfile["name"]
                if not sub_p.exists():
                    print(f"    [FAIL] Missing raw file in directory {rel_path}: {subfile['name']}")
                    return False
                actual_hash = compute_sha256(sub_p)
                expected_hash = subfile.get("sha256")
                if actual_hash == expected_hash:
                    print(f"    [OK] {src['source_id']}: {subfile['name']} ({actual_hash[:12]}...)")
                else:
                    print(f"    [FAIL] Hash mismatch for {src['source_id']} file {subfile['name']}: expected {expected_hash[:12]}, got {actual_hash[:12]}")
                    return False
        else:
            actual_hash = compute_sha256(p)
            expected_hash = src.get("sha256")
            if actual_hash == expected_hash:
                print(f"    [OK] {src['source_id']}: {p.name} ({actual_hash[:12]}...)")
            else:
                print(f"    [FAIL] Hash mismatch for {src['source_id']}: expected {expected_hash[:12]}, got {actual_hash[:12]}")
                return False

    print("--> Step 2: Verifying Checksums of Institutional & Federal Scrutiny Datasets...")
    for ds in manifest.get("institutional_and_federal_datasets", []):
        rel_path = ds.get("local_path")
        if not rel_path:
            continue
        p = PROJECT_ROOT / rel_path
        if not p.exists():
            print(f"    [FAIL] Dataset file does not exist: {rel_path}")
            return False
        actual_hash = compute_sha256(p)
        expected_hash = ds.get("sha256")
        if actual_hash == expected_hash:
            print(f"    [OK] {ds['dataset_id']}: {p.name} ({actual_hash[:12]}...)")
        else:
            print(f"    [FAIL] Hash mismatch for {ds['dataset_id']}: expected {expected_hash[:12]}, got {actual_hash[:12]}")
            return False
    return True


def run_script(script_name: str, args: list[str] | None = None):
    script_path = SCRIPTS_DIR / script_name
    print(f"--> Executing: {script_name} {' '.join(args or [])}...")
    res = subprocess.run(
        [sys.executable, str(script_path)] + (args or []),
        capture_output=True, text=True, cwd=str(PROJECT_ROOT))
    if res.returncode != 0:
        print(f"    [ERROR] {script_name} failed:")
        print(res.stderr)
        return False
    for line in res.stdout.strip().splitlines():
        print(f"    {line}")
    print(f"    [OK] {script_name} completed.")
    return True


def run_fetchers(sources: list[str]) -> list[str]:
    """Run live fetchers (T081 --fetch mode). Non-fatal per source failure;
    returns the list of source_ids that were attempted."""
    fetchers = {
        "kiifb": "fetch_kiifb_portal.py",
        "kite": "fetch_kite_sametham.py",
        "kanakku": "fetch_kanakku.py",
    }
    attempted = []
    print("--> Step 1b: LIVE FETCH (Milestone 8 fetch mode)...")
    for sid in sources:
        script = fetchers.get(sid)
        if not script:
            continue
        attempted.append(sid)
        print(f"    [{sid}]: {script}")
        res = subprocess.run([sys.executable, str(SCRIPTS_DIR / script)],
                             capture_output=True, text=True, cwd=str(PROJECT_ROOT))
        print("    " + (res.stdout.strip().replace("\n", "\n    ") or res.stderr.strip()))
        if res.returncode != 0:
            print(f"    [WARN] {script} reported failure — pipeline continues with "
                  f"newest available snapshot/pinned baseline for this source. "
                  f"See data/manifest.json live_crawls for the recorded failure note.")
    return attempted



def newest_crawl_or_pinned(group: str, dataset: str, arcname: str, pinned_rel: str) -> str:
    """T081: fetch mode extracts from the newest live-crawl snapshot; fallback
    to the pinned baseline when the source has never been crawled."""
    sys.path.insert(0, str(SCRIPTS_DIR))
    import fetch_common as fc
    found = fc.newest_snapshot(group, dataset, arcname)
    if found:
        return str(found)
    return str(PROJECT_ROOT / pinned_rel)


def build_extract_inputs(fetch_mode: bool, sources: list[str]) -> list[tuple[str, list[str]]]:
    """Per-script argv for extraction. Offline mode pins EVERY input to the
    checksum-verified baselines so output stays byte-reproducible; fetch mode
    extracts from newest archived crawls."""
    # (script, [(group, dataset, arcname, pinned_rel), ...], arg_names)
    schedule = [
        ("extract_committee_financial_tables.py", [], []),
        ("extract_kiifb_projects.py",
         [("kiifb", "project-status", "kiifb-prjStatus.html",
           "data/raw/kiifb/kiifb-prjStatus.html")], ["--input"]),
        ("extract_kite_schools.py",
         [("kite", "kiifb-funded-schools", "kiifb-funded-schools-sametham.html",
           "data/raw/kite/kiifb-funded-schools-sametham.html")], ["--input"]),
        ("build_unified_project_dataset.py", [], []),
        ("enrich_projects_with_kanakku.py",
         [("kanakku", "", "projects.csv", "data/raw/kanakku/projects.csv"),
          ("kanakku", "", "funding.csv", "data/raw/kanakku/funding.csv"),
          ("kanakku", "", "liability.csv", "data/raw/kanakku/liability.csv")],
         ["--proj", "--funding", "--liability"]),
    ]
    plan: list[tuple[str, list[str]]] = []
    for script, specs, arg_names in schedule:
        args: list[str] = []
        for (group, dataset, arcname, pinned_rel), arg in zip(specs, arg_names):
            if fetch_mode and (group in sources):
                args += [arg, newest_crawl_or_pinned(group, dataset, arcname, pinned_rel)]
            else:
                # Offline mode (or source not fetched): pin to the checksum-verified
                # baseline so processed output stays byte-reproducible.
                args += [arg, str(PROJECT_ROOT / pinned_rel)]
        plan.append((script, args))
    return plan


def main():
    ap = argparse.ArgumentParser(description="KIIFB data pipeline refresh.")
    ap.add_argument("--fetch", action="store_true",
                    help="fetch mode: run live fetchers first, then extract from "
                         "the newest archived crawls (T081). Offline mode remains "
                         "the default and reproduces processed output from the "
                         "checksum-verified pinned baselines.")
    ap.add_argument("--sources", type=str, default="kiifb,kite,kanakku",
                    help="comma-separated subset of live sources for --fetch mode")
    args = ap.parse_args()

    fetch_mode = args.fetch
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]

    print("=" * 60)
    print(f"KIIFB DASHBOARD — PIPELINE REFRESH ({'FETCH' if fetch_mode else 'OFFLINE'} MODE)")
    print("=" * 60)

    if not verify_raw_sources():
        sys.exit(1)

    if fetch_mode:
        run_fetchers(sources)

    steps = build_extract_inputs(fetch_mode, sources)
    for script, script_args in steps:
        if not run_script(script, script_args):
            print(f"[FATAL] Pipeline stopped at step {script}")
            sys.exit(1)

    # T082: snapshot processed datasets, then diff against the previous
    # run (empty-delta baseline log when no prior snapshot exists).
    if not run_script("diff_snapshots.py"):
        print("[FATAL] Pipeline stopped at diff_snapshots.py")
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
