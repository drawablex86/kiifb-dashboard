#!/usr/bin/env python3
"""Live fetcher for DS030 — Kerala Kanakku Open Data Suite.

Acquires the Kanakku CSV extracts (projects.csv, funding.csv, liability.csv —
the last covering the PWD Defect Liability Period register) and archives a
complete dated snapshot to:
    data/raw/kanakku/<YYYY-MM-DD>/projects.csv
    data/raw/kanakku/<YYYY-MM-DD>/funding.csv
    data/raw/kanakku/<YYYY-MM-DD>/liability.csv
without touching the pinned baseline files at data/raw/kanakku/*.csv.

The direct CSV endpoints are discovered from the public data page
(https://keralakanakku.com/en/data) by scanning for links ending in '.csv'
whose file names match the three known extracts. If the site moves the files,
the fetch aborts with a failure record and manual retrieval instructions
per datasources.md §2 rather than guessing.

Direct endpoints may be passed explicitly with `--urls <url1,url2,url3>`
(projects,funding,liability order) if discovery ever breaks.

Crawl metadata is appended to data/manifest.json under 'live_crawls'.

Usage:
    python3 scripts/fetch_kanakku.py                 # discover + crawl
    python3 scripts/fetch_kanakku.py --dry-run       # discovery only, no download
    python3 scripts/fetch_kanakku.py --urls A,B,C    # direct endpoints
"""

from __future__ import annotations

import argparse
import html.parser
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
import urllib.parse

sys.path.insert(0, str(Path(__file__).parent))

import fetch_common as fc  # noqa: E402

SOURCE_ID = "DS030"
GROUP, DATASET = "kanakku", ""
DATA_PAGE_URL = fc.KANAKKU_DATA_URL
KNOWN_ARCNAMES = ("projects.csv", "funding.csv", "liability.csv")


class _CsvLinkParser(html.parser.HTMLParser):
    """Collect href values ending in .csv from a data page."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() != "a":
            return
        for (k, v) in attrs:
            if k.lower() == "href" and v:
                self.links.append(v)


def discover_csv_urls(html_bytes: bytes) -> dict[str, str]:
    """Return arcname -> absolute URL for the three known extracts."""
    parser = _CsvLinkParser()
    parser.feed(html_bytes.decode("utf-8", errors="ignore"))
    found: dict[str, str] = {}
    for href in parser.links:
        path = urllib.parse.urlparse(href).path
        base = path.rsplit("/", 1)[-1].lower()
        if base in KNOWN_ARCNAMES:
            absolute = urllib.parse.urljoin(DATA_PAGE_URL, href)
            found.setdefault(base, absolute)
    return found


def fetch_data_page() -> bytes:
    """Download the Kanakku data page into a throwaway temp dir."""
    with tempfile.TemporaryDirectory(prefix="kanakku-page-") as td:
        tmp_path, _status = fc.download_to_temp(
            DATA_PAGE_URL, Path(td), timeout=fc.LINK_DISCOVERY_TIMEOUT
        )
        return tmp_path.read_bytes()


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch DS030 Kanakku CSV extracts.")
    ap.add_argument("--dry-run", action="store_true",
                    help="discover endpoints only; no downloads or manifest save")
    ap.add_argument("--urls", type=str, default="",
                    help="direct CSV URLs in order: projects,funding,liability")
    args = ap.parse_args()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Its own robots/CSP usually allow CSV downloads; discovery failure path
    def record_failure(note: str, reason: str | None = None) -> None:
        manifest = fc.load_manifest()
        dest = str((fc.archive_root(GROUP, DATASET) / now).relative_to(fc.PROJECT_ROOT))
        fc.record_crawl(manifest, SOURCE_ID, DATA_PAGE_URL, "", [], "failure",
                        note=note + " | " + fc.manual_retrieval_note(DATA_PAGE_URL, dest))
        fc.save_manifest(manifest)
        if reason:
            print(f"    reason: {reason}")
        print("    Manual path: download the projects/funding/liability CSVs from "
              f"{DATA_PAGE_URL} into data/raw/kanakku/{now}/ (never overwrite the "
              "data/raw/kanakku/*.csv baselines) and register them in data/manifest.json.")

    resolved: list[dict]
    if args.urls:
        parts = [u.strip() for u in args.urls.split(",") if u.strip()]
        if len(parts) != len(KNOWN_ARCNAMES):
            print("error: --urls expects exactly 3 comma-separated URLs "
                  "(projects,funding,liability)")
            return 2
        resolved = [{"url": u, "arcname": n} for u, n in zip(parts, KNOWN_ARCNAMES)]
        discovery = "manual --urls override"
    else:
        ok, robots_info = fc._robots_cached(DATA_PAGE_URL, {})
        if not ok:
            record_failure(f"robots.txt disallows data page ({robots_info})",
                           "fetch aborted before any download")
            print(f"[{SOURCE_ID}] failure")
            return 1
        try:
            found = discover_csv_urls(fetch_data_page())
        except Exception as e:  # noqa: BLE001 — record & guide manual retrieval
            record_failure(
                f"data-page discovery failed: {type(e).__name__}: {e}",
                f"data page unreachable ({type(e).__name__})",
            )
            print(f"[{SOURCE_ID}] failure")
            return 1
        missing = [n for n in KNOWN_ARCNAMES if n not in found]
        if missing:
            record_failure(
                f"CSV endpoints not discovered on data page (missing: "
                f"{', '.join(missing)}). Site layout may have changed; "
                f"pass explicit --urls or fix discovery.",
                f"content discovery failed (missing {missing})",
            )
            print(f"[{SOURCE_ID}] failure")
            print(f"    Try: open {DATA_PAGE_URL} in a browser; CSV links may have moved.")
            return 1
        resolved = [{"url": found[n], "arcname": n} for n in KNOWN_ARCNAMES]
        discovery = f"discovered {len(resolved)} CSV endpoints from data page"

    if args.dry_run:
        for r in resolved:
            print(f"    {r['arcname']} <- {r['url']}")
        print(f"[{SOURCE_ID}] dry-run ({discovery}); no downloads, no manifest save")
        return 0

    manifest = fc.load_manifest()
    summary = fc.crawl_targets(
        manifest=manifest,
        source_id=SOURCE_ID,
        group=GROUP,
        dataset=DATASET,
        primary_url=DATA_PAGE_URL,
        resolved_files=resolved,
        date_iso=now,
    )
    fc.save_manifest(manifest)
    files = summary.get("files") or []
    for f in files:
        flag = " (unchanged)" if f.get("unchanged") else ""
        print(f"    {f['name']}: sha256 {f['sha256'][:12]}...{flag}")
    print(f"[{SOURCE_ID}] {summary['status']} {summary.get('arc_dir', '')} ({discovery})")
    if summary["status"] == "failure":
        print(f"    reason: {summary.get('reason')}")
        print("    " + fc.manual_retrieval_note(DATA_PAGE_URL, summary.get("arc_dir", "")))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
