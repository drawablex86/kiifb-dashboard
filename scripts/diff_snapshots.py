#!/usr/bin/env python3
"""Snapshot archive & change-log engine (T082, Milestone 8).

Two operations:

1. SNAPSHOT — copy the current `data/processed/` datasets into an immutable
   dated run directory `data/snapshots/<YYYY-MM>[__<runid>]/`. Existing run
   directories are never modified; when content is identical to an existing
   run the directory is reused instead of duplicated.

2. DIFF — compare a previous snapshot run against the current snapshot run and
   emit a deterministic, machine-readable change log
   (`data/processed/change_log.json`) covering, per dataset:

   - added / removed / name-changed records (stable-ID join only)
   - normalised status migrations (with source-status before/after)
   - financial deltas (approved/released/expenditure, with signed deltas)
   - anomaly flags: newly raised vs newly resolved
   - district & coordinate coverage statistics (GAP-001 tracking)

   Determinism contract: for identical (prev, curr) inputs the change log is
   byte-identical across runs (keys sorted, no timestamps, all lists sorted).

Change computation only joins records on stable IDs (`project_id`,
`institution_id`, `code`, `record_id`), per `docs/matching-rules.md`; no
fuzzy merging happens here.

Usage:
    python3 scripts/diff_snapshots.py                    # snapshot + diff (pipeline default)
    python3 scripts/diff_snapshots.py --no-diff          # snapshot only
    python3 scripts/diff_snapshots.py --prev A --curr B --out C.json  # arbitrary diff
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
SNAPSHOTS_DIR = PROJECT_ROOT / "data" / "snapshots"
CHANGE_LOG_PATH = PROCESSED_DIR / "change_log.json"

# Dataset configuration: (filename, records_container, stable_key, spec)
# spec keys control where typed fields live; unavailable slots are None.
DATASETS: list[dict] = [
    {
        "filename": "kiifb_projects.json",
        "container": "projects",
        "stable_key": "project_id",
        "name_field": "project_name",
        "district": "district",
        "status_nested": ["status", "normalised_status"],
        "source_status_nested": ["status", "source_status_text"],
        "approved_nested": ["financials", "approved_inr"],
        "released_nested": ["financials", "released_inr"],
        "flags": "open_flags",
        "coordinates": "coordinates",
    },
    {
        "filename": "unified_project_explorer.json",
        "container": "records",
        "stable_key": "record_id",
        "name_field": "name",
        "district": "district",
        "status_nested": ["status", "normalised_status"],
        "source_status_nested": ["status", "source_status_text"],
        "approved_nested": ["financials", "approved_inr"],
        "released_nested": ["financials", "released_inr"],
        "flags": "open_flags",
        "coordinates": "coordinates",
    },
    {
        "filename": "kite_schools.json",
        "container": "schools",
        "stable_key": "institution_id",
        "name_field": "school_name",
        "district": "district",
        "status_nested": ["status", "normalised_status"],
        "source_status_nested": None,
        "approved_nested": None,
        "released_nested": None,
        "flags": None,
        "coordinates": None,
    },
    {
        "filename": "kanakku_packages.json",
        "container": "packages",
        "stable_key": "code",
        "name_field": "title",
        "district": "district",
        "status_nested": None,
        "source_status_nested": None,
        "approved_nested": None,
        "released_nested": ["expenditure_inr"],  # treated as spend proxy
        "flags": "open_flags",
        "coordinates": None,
    },
]


def _get_nested(record: dict, path) -> object | None:
    if not path:
        return None
    cur: object = record
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def sha_of_file(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(131072):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Snapshot
# ---------------------------------------------------------------------------

def dir_hashes(run_dir: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not run_dir.is_dir():
        return out
    for p in sorted(run_dir.iterdir()):
        if p.is_file():
            out[p.name] = sha_of_file(p)
    return out


def content_hashes(processed_dir: Path, filenames: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for name in filenames:
        p = processed_dir / name
        if p.is_file():
            out[name] = sha_of_file(p)
    return out


def canonical_bytes(path: Path) -> bytes:
    """Canonical form of a processed JSON dataset: volatile metadata
    ('generated_at') is dropped and keys are sorted, so snapshots and reuse
    checks are keyed on real content only, not on run timestamps."""
    if path.suffix.lower() != ".json":
        return path.read_bytes()
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    payload.pop("generated_at", None)
    return (json.dumps(payload, indent=2, sort_keys=True,
                       ensure_ascii=False) + "\n").encode("utf-8")


def snapshot_processed(
    processed_dir: Path = PROCESSED_DIR,
    snapshots_dir: Path = SNAPSHOTS_DIR,
    runid: str | None = None,
) -> Path:
    """Snapshot processed datasets into an immutable run directory.

    - Files are written in canonical form (see canonical_bytes): snapshots and
      reuse logic are insensitive to 'generated_at' metadata, so re-running
      the pipeline on unchanged data REUSES the same run directory instead of
      creating timestamp noise.
    - Run dir name: '<YYYY-MM>' or '<YYYY-MM>__<runid>' when the plain month
      directory already holds different content.
    - If a run directory already contains byte-identical content for all
      datasets present, it is reused (idempotent, no duplicate snapshots).
    - Root dir is created if missing. Never deletes existing runs.
    Returns the run directory path.
    """
    filenames = [d["filename"] for d in DATASETS]
    current: dict[str, str] = {}
    canonical: dict[str, bytes] = {}
    import hashlib
    for name in filenames:
        p = processed_dir / name
        if p.is_file():
            blob = canonical_bytes(p)
            canonical[name] = blob
            current[name] = hashlib.sha256(blob).hexdigest()

    now = datetime.now(timezone.utc)
    month = now.strftime("%Y-%m")
    runid = runid or now.strftime("%Y%m%dT%H%M%SZ")

    # Reuse an existing run whose every file matches current content.
    if snapshots_dir.is_dir():
        for run in sorted(snapshots_dir.iterdir()):
            if run.is_dir() and dir_hashes(run) == current:
                return run

    base = snapshots_dir / month
    target = base
    if base.exists() and dir_hashes(base):
        target = snapshots_dir / f"{month}__{runid}"
    target.mkdir(parents=True, exist_ok=False)
    for name, sha in sorted(current.items()):
        dest = target / name
        dest.write_bytes(canonical[name])
        assert sha_of_file(dest) == sha  # copy-integrity guarantee
    return target


def newest_run_before_current(run: Path, snapshots_dir: Path = SNAPSHOTS_DIR) -> Path | None:
    """Newest snapshot run (excluding `run`) by lexical order of dir names."""
    if not snapshots_dir.is_dir():
        return None
    runs = sorted(d for d in snapshots_dir.iterdir() if d.is_dir() and d != run)
    return runs[-1] if runs else None


# ---------------------------------------------------------------------------
# Diff
# ---------------------------------------------------------------------------

def load_records(run_dir: Path, spec: dict) -> dict[str, dict]:
    import json
    path = run_dir / spec["filename"]
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    rows = payload.get(spec["container"], [])
    return {row.get(spec["stable_key"]): row for row in rows
            if row.get(spec["stable_key"]) is not None}


def _sorted_unique(values) -> list[str]:
    return sorted({str(v) for v in values})


def diff_one_dataset(prev: dict[str, dict], curr: dict[str, dict], spec: dict) -> dict:
    added, removed, renamed = [], [], []
    status_migrations, financial_deltas, flags_added, flags_resolved = [], [], [], []

    prev_keys = set(prev)
    curr_keys = set(curr)

    for key in sorted(curr_keys - prev_keys):
        entry = {"id": key, "name": _name(curr, key, curr, spec)}
        added.append(entry)
        # Flags of newly added records are newly raised for trend purposes.
        flag_field = spec["flags"]
        if flag_field and isinstance(curr[key].get(flag_field), list):
            for flag in curr[key][flag_field]:
                flags_added.append({"id": key, "flag": flag})
    for key in sorted(prev_keys - curr_keys):
        entry = {"id": key, "name": _name(prev, key, prev, spec)}
        removed.append(entry)
        flag_field = spec["flags"]
        if flag_field and isinstance(prev[key].get(flag_field), list):
            for flag in prev[key][flag_field]:
                flags_resolved.append({"id": key, "flag": flag})
    for key in sorted(prev_keys & curr_keys):
        p, c = prev[key], curr[key]
        p_name, c_name = _name_value(p, spec), _name_value(c, spec)
        if p_name != c_name:
            renamed.append({"id": key, "name_before": p_name, "name_after": c_name})

        p_status, c_status = _status(p, spec), _status(c, spec)
        if p_status != c_status:
            status_migrations.append({
                "id": key, "name": c_name or p_name,
                "from": p_status, "to": c_status,
                "source_status_before": _source_status(p, spec),
                "source_status_after": _source_status(c, spec),
            })

        if spec["approved_nested"] or spec["released_nested"]:
            for field, nested, label in (
                ("approved", spec["approved_nested"], "approved_inr"),
                ("released", spec["released_nested"], None),
            ):
                if not nested:
                    continue
                pv, cv = _get_nested(p, nested), _get_nested(c, nested)
                if pv is None and cv is None:
                    continue
                pv = float(pv) if pv is not None else 0.0
                cv = float(cv) if cv is not None else 0.0
                if pv != cv:
                    financial_deltas.append({
                        "id": key, "name": c_name or p_name,
                        "field": (nested[-1] if isinstance(nested, list) else nested),
                        "before": pv, "after": cv, "delta": round(cv - pv, 2),
                    })

        flag_field = spec["flags"]
        if flag_field and isinstance(p.get(flag_field), list) and isinstance(c.get(flag_field), list):
            for flag in curr[key][flag_field]:
                if flag not in p[flag_field]:
                    flags_added.append({"id": key, "flag": flag})
            for flag in p[flag_field]:
                if flag not in c[flag_field]:
                    flags_resolved.append({"id": key, "flag": flag})

    coverage = {
        "district_prev": sum(1 for r in prev.values() if r.get(spec["district"])),
        "district_curr": sum(1 for r in curr.values() if r.get(spec["district"])),
        "coordinates_prev": sum(1 for r in prev.values() if _coords(r, spec)),
        "coordinates_curr": sum(1 for r in curr.values() if _coords(r, spec)),
        "total_prev": len(prev), "total_curr": len(curr),
    }

    summary = {
        "added": added, "removed": removed, "renamed": renamed,
        "status_migrations": status_migrations,
        "financial_deltas": financial_deltas,
        "flags_added": flags_added, "flags_resolved": flags_resolved,
        "coverage": coverage,
        "totals": {
            "added": len(added), "removed": len(removed), "renamed": len(renamed),
            "status_migrations": len(status_migrations),
            "financial_deltas": len(financial_deltas),
            "flags_added": len(flags_added), "flags_resolved": len(flags_resolved),
        },
        "financial_totals_delta_inr": {
            "approved": _sum_nested(prev, curr, spec, "approved_nested"),
            "released": _sum_nested(prev, curr, spec, "released_nested"),
        },
    }
    return summary


def _sum_nested(prev: dict, curr: dict, spec: dict, nested_attr: str) -> float:
    field = spec.get(nested_attr)
    if not field:
        return 0.0
    pv = sum(float(_get_nested(r, field) or 0.0) for r in prev.values())
    cv = sum(float(_get_nested(r, field) or 0.0) for r in curr.values())
    return round(cv - pv, 2)


def _name(records: dict, key, src: dict[str, dict], spec: dict):
    row = records.get(key) or {}
    return _name_value(row, spec)


def _name_value(row: dict, spec: dict):
    v = row.get(spec["name_field"])
    return v if v is not None else None


def _status(row: dict, spec: dict):
    return _get_nested(row, spec["status_nested"])


def _source_status(row: dict, spec: dict):
    return _get_nested(row, spec["source_status_nested"]) if spec["source_status_nested"] else None


def _coords(row: dict, spec: dict):
    if not spec.get("coordinates"):
        return None
    return row.get(spec["coordinates"])


def json_load(path: Path):
    import json
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_change_log(
    prev_dir: Path,
    curr_dir: Path,
    out_path: Path = CHANGE_LOG_PATH,
    processed_dir: Path = PROCESSED_DIR,
) -> dict:
    """Deterministic stringify-able change log dict; also writes to out_path."""
    try:
        rel_root = str(processed_dir.resolve().relative_to(PROJECT_ROOT))
    except ValueError:
        rel_root = str(processed_dir.resolve())
    change_log: dict = {
        "computed_from": {
            "dataset_root": rel_root,
            "prev": str(prev_dir.name),
            "curr": str(curr_dir.name),
        },
        "schema_version": "1.0.0",
        "datasets": {},
        "portfolio_totals_delta_inr": {},
    }
    empty = prev_dir == curr_dir
    for spec in DATASETS:
        fname = spec["filename"]
        if not (curr_dir / fname).is_file():
            continue
        prev_recs = load_records(prev_dir, spec)
        curr_recs = load_records(curr_dir, spec)
        summary = diff_one_dataset(prev_recs, curr_recs, spec)
        summary["baseline_run"] = empty
        change_log["datasets"][fname] = summary
    change_log["portfolio_totals_delta_inr"] = {
        fname: {
            "approved": ds["financial_totals_delta_inr"]["approved"],
            "released": ds["financial_totals_delta_inr"]["released"],
        } for fname, ds in change_log["datasets"].items()
    }
    header_note = (
        "Baseline snapshot: no prior run existed to compare against."
        if empty else
        f"Change log computed between snapshot {prev_dir.name} and {curr_dir.name}."
    )
    change_log["note"] = header_note

    import json
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(change_log, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    return change_log


def summarize_counts(change_log: dict) -> str:
    lines = []
    for fname, ds in change_log["datasets"].items():
        t = ds["totals"]
        lines.append(
            f"{fname}: +{t['added']} -{t['removed']} ~{t['renamed']} renamed, "
            f"{t['status_migrations']} status migrations, "
            f"{t['financial_deltas']} financial deltas, "
            f"flags +{t['flags_added']}/-{t['flags_resolved']}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Snapshot archive & diff engine (T082).")
    ap.add_argument("--no-diff", action="store_true", help="snapshot only")
    ap.add_argument("--prev", type=str, default=None,
                    help="override prev snapshot run directory (relative or absolute)")
    ap.add_argument("--curr", type=str, default=None,
                    help="override curr snapshot run directory")
    ap.add_argument("--out", type=str, default=str(CHANGE_LOG_PATH),
                    help="change log output path")
    args = ap.parse_args(argv)

    if args.prev and args.curr:
        prev, curr = Path(args.prev), Path(args.curr)
        log = build_change_log(prev, curr, Path(args.out))
        print(summarize_counts(log) or "(no changes)")
        return 0

    curr = snapshot_processed()
    if args.no_diff:
        print(f"[snapshot] {curr}")
        return 0
    prev = newest_run_before_current(curr) or curr
    log = build_change_log(prev, curr)
    print(f"[snapshot] {curr}")
    print(f"[diff] {prev.name} -> {curr.name}"
          + (" (baseline run)" if prev == curr else ""))
    print(summarize_counts(log) or "(no changes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
