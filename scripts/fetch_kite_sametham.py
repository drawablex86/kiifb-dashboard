#!/usr/bin/env python3
"""Live fetcher for DS021 — KITE Sametham KIIFB-funded schools directory.

Fetches https://sametham.kite.kerala.gov.in/KIIFBFundedSchools/spv and archives
it to
    data/raw/kite/kiifb-funded-schools/<YYYY-MM-DD>/kiifb-funded-schools-sametham.html
without touching the pinned baseline at
data/raw/kite/kiifb-funded-schools-sametham.html.

Crawl metadata is appended to data/manifest.json under 'live_crawls'.

Usage:
    python3 scripts/fetch_kite_sametham.py            # normal crawl
    python3 scripts/fetch_kite_sametham.py --dry-run  # resolve & robots-check only
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import fetch_common as fc  # noqa: E402

SOURCE_ID = "DS021"
URL = "https://sametham.kite.kerala.gov.in/KIIFBFundedSchools/spv"
GROUP, DATASET = "kite", "kiifb-funded-schools"
ARCNAME = "kiifb-funded-schools-sametham.html"


def main() -> int:
    manifest = fc.load_manifest()
    summary = fc.crawl_targets(
        manifest=manifest,
        source_id=SOURCE_ID,
        group=GROUP,
        dataset=DATASET,
        primary_url=URL,
        resolved_files=[{"url": URL, "arcname": ARCNAME}],
        date_iso=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        dry_run="--dry-run" in sys.argv,
    )
    if summary["status"] != "dry-run":
        fc.save_manifest(manifest)
    print(f"[{SOURCE_ID}] {summary['status']} {summary.get('arc_dir', '')}")
    if summary["status"] == "failure":
        print(f"    reason: {summary.get('reason')}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
