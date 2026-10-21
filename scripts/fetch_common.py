#!/usr/bin/env python3
"""Shared helpers for live-source fetchers (T080, Milestone 8).

Design contract (per `datasources.md` §2 and ADR-001 scope decisions):

- Every crawl is written to a dated, immutable archive directory:
      data/raw/<group>/<dataset>/<YYYY-MM-DD>/[<arcname>...]
  Existing pinned baseline files (verified by `scripts/refresh_pipeline.py`)
  are never overwritten, prior dated crawls are never modified, and if a dated
  directory already holds crawled content, a `_r2`, `_r3` ... suffix directory
  is created instead of writing into it (guarantees immutable snapshots even
  for several crawls on the same day).

- Retrieval metadata (timestamp, URL, SHA-256, size, HTTP status) is appended
  to `data/manifest.json` under a dedicated `live_crawls` key, leaving the
  pinned `sources[]` entries untouched so baseline checksum verification in
  `scripts/refresh_pipeline.py` remains valid.

- Unchanged content is detected by comparing SHA-256 against the most recent
  successful crawl for the same source. If nothing changed, no duplicate
  archive directory is created.

- Failures are recorded (in the manifest) with a safe manual retrieval path,
  per `datasources.md` §2, and never leave partially-written files behind
  (downloads land in a temp file and are atomically renamed into place).
  For multi-file sources, a changed-file crawl is written as a complete
  self-consistent snapshot so "newest crawl dir" is always complete.

- Robots.txt is checked best-effort before any download; a disallowed path
  aborts the fetch with a clear message (recorded in the manifest).

All HTTP uses `urllib.request` only (no third-party runtime dependencies),
with a polite, identifying user agent and bounded timeouts.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = PROJECT_ROOT / "data" / "manifest.json"

USER_AGENT = (
    "KIIFB-Dashboard-CivicTech/1.0 (open-source accountability dashboard; "
    "reproducible-source-archiver; +https://github.com/drawablex86/kiifb-dashboard)"
)
DOWNLOAD_TIMEOUT = 90      # seconds per download
LINK_DISCOVERY_TIMEOUT = 45
MAX_ATTEMPTS = 3
BACKOFF_SECONDS = (5, 15)  # delay before retry 1, retry 2, if needed

KANAKKU_DATA_URL = "https://keralakanakku.com/en/data"


# ---------------------------------------------------------------------------
# Checksum & paths
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    """SHA-256 of a file, streamed (conventions match data/manifest.json)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(131072):
            h.update(chunk)
    return h.hexdigest()


def archive_root(group: str, dataset: str) -> Path:
    """Root archive directory for a source, e.g. data/raw/kiifb/project-status."""
    base = PROJECT_ROOT / "data" / "raw" / group
    if dataset:
        base = base / dataset
    return base


def archive_dir(group: str, dataset: str, date_iso: str) -> Path:
    """Dated (base) directory for a crawl, e.g. data/raw/kiifb/project-status/2026-10-20."""
    return archive_root(group, dataset) / date_iso


def resolve_unique_dir(base_dir: Path) -> Path:
    """Return an immutable dated archive dir under base_dir.

    base_dir must be named '<YYYY-MM-DD>' already. If that directory exists and
    has content (an earlier crawl), returns '<base>_r2', '<base>_r3', ...
    """
    if not base_dir.exists() or not any(base_dir.iterdir()):
        return base_dir
    n = 2
    while True:
        candidate = base_dir.with_name(f"{base_dir.name}_r{n}")
        if not candidate.exists() or not any(candidate.iterdir()):
            return candidate
        n += 1


# ---------------------------------------------------------------------------
# Manifest live-crawls history
# ---------------------------------------------------------------------------

def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_manifest(manifest_path: Path | None = None) -> dict:
    p = manifest_path or DEFAULT_MANIFEST
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: dict, manifest_path: Path | None = None) -> None:
    """Persist the manifest atomically (temp file + rename)."""
    path = manifest_path or DEFAULT_MANIFEST
    manifest["last_updated"] = _utcnow_iso()
    fd, tmp_name = tempfile.mkstemp(
        prefix="manifest-", suffix=".tmp", dir=str(path.parent)
    )
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(manifest, out, indent=2, ensure_ascii=False)
        out.write("\n")
    Path(tmp_name).replace(path)


def get_last_crawl(manifest: dict, source_id: str) -> dict | None:
    """Most recent successful or unchanged crawl entry for a source, or None."""
    for entry in reversed(manifest.get("live_crawls", [])):
        if entry.get("source_id") == source_id and entry.get("status") in (
            "success", "unchanged"
        ):
            return entry
    return None


def last_crawl_hashes(manifest: dict, source_id: str) -> dict[str, str]:
    """Map arcname -> sha256 from the most recent successful crawl."""
    entry = get_last_crawl(manifest, source_id)
    if not entry:
        return {}
    return {f["name"]: f["sha256"] for f in entry.get("files", [])}


def record_crawl(
    manifest: dict,
    source_id: str,
    url: str | None,
    arc_dir: str,
    files: list[dict],
    status: str,
    note: str = "",
) -> None:
    """Append a crawl/failure record under manifest['live_crawls']."""
    manifest.setdefault("live_crawls", [])
    manifest["live_crawls"].append(
        {
            "source_id": source_id,
            "retrieved_at": _utcnow_iso(),
            "url": url,
            "arc_dir": arc_dir,
            "files": files,
            "status": status,  # success | unchanged | failure | dry-run
            "note": note,
        }
    )
    # Bound manifest growth: keep at most the latest 200 crawl records.
    if len(manifest["live_crawls"]) > 200:
        manifest["live_crawls"] = manifest["live_crawls"][-200:]


# ---------------------------------------------------------------------------
# Robots.txt (best-effort; documented either way)
# ---------------------------------------------------------------------------

def robots_allowed(url: str, timeout: int = 20) -> tuple[bool, str]:
    """(allowed, info). Fails open only when robots.txt is unreachable/absent."""
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        req = urllib.request.Request(robots_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
        rp.parse(body.splitlines())
        return (
            rp.can_fetch("*", url),
            f"robots.txt fetched and honoured ({robots_url})",
        )
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return True, "robots.txt absent (HTTP 404); proceeding politely"
        return True, f"robots.txt returned HTTP {e.code}; proceeding politely"
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return True, f"robots.txt unreachable ({type(e).__name__}); proceeding politely"


def _robots_cached(url: str, cache: dict[str, tuple[bool, str]]) -> tuple[bool, str]:
    host = urllib.parse.urlparse(url).netloc
    if host not in cache:
        cache[host] = robots_allowed(url)
    return cache[host]


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def download_to_temp(
    url: str, tmp_dir: Path, timeout: int = DOWNLOAD_TIMEOUT
) -> tuple[Path, int]:
    """Download to an unguessable temp file.

    Returns (temp_path, http_status). The caller must move or delete the file.
    """
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"}
    )
    fd, tmp_name = tempfile.mkstemp(prefix="dl-", suffix=".part", dir=str(tmp_dir))
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    with resp, os.fdopen(fd, "wb") as out:
        status = getattr(resp, "status", 200)
        shutil.copyfileobj(resp, out, length=131072)
    return Path(tmp_name), status


def manual_retrieval_note(url: str, dest_dir_rel: str) -> str:
    """Standard safe manual fallback wording for failures (datasources.md §2)."""
    return (
        f"Automated retrieval failed. Manual retrieval path: open {url} in a "
        f"browser, save the file(s), place them in {dest_dir_rel}/ and register "
        f"them in data/manifest.json (see datasources.md §2 and §10)."
    )


# ---------------------------------------------------------------------------
# Crawl orchestration
# ---------------------------------------------------------------------------

def crawl_targets(
    manifest: dict,
    source_id: str,
    group: str,
    dataset: str,
    primary_url: str,
    resolved_files: list[dict],
    date_iso: str,
    dry_run: bool = False,
    robots_cache: dict | None = None,
) -> dict:
    """Fetch one source (any number of files) into a dated immutable archive.

    manifest:      mutated with the crawl record (caller persists it).
    resolved_files: list of {"url": ..., "arcname": ...} — URLs already known.
    date_iso:      'YYYY-MM-DD' for the archive directory.
    Returns a summary dict: {status, arc_dir, files?, reason?, robots?}.
    Status is one of: success | unchanged | failure | dry-run.
    """
    robots_cache = robots_cache if robots_cache is not None else {}

    ok, robots_info = _robots_cached(primary_url, robots_cache)
    if not ok:
        record_crawl(
            manifest, source_id, primary_url, "", [], "failure",
            note=f"robots.txt disallows this path ({robots_info}); fetch aborted, "
                 f"nothing downloaded. manual_retrieval_note applies.",
        )
        return {"status": "failure", "reason": "robots disallow", "robots": robots_info}

    if dry_run:
        summary = {"status": "dry-run", "robots": robots_info,
                   "would_fetch": [f["arcname"] for f in resolved_files]}
        record_crawl(manifest, source_id, primary_url, "", [], "dry-run",
                     note="Dry run: no files fetched or archived.")
        return summary

    base = archive_root(group, dataset)
    base.mkdir(parents=True, exist_ok=True)
    dest_dir = resolve_unique_dir(base / date_iso)
    dest_dir.mkdir(parents=True, exist_ok=False)
    dest_dir_rel = str(dest_dir.relative_to(PROJECT_ROOT))

    prev_hashes = last_crawl_hashes(manifest, source_id)

    downloaded: list[tuple[dict, Path, int]] = []
    failures: list[str] = []

    for spec in resolved_files:
        f_url, arcname = spec["url"], spec["arcname"]
        ok, info = _robots_cached(f_url, robots_cache)
        if not ok:
            failures.append(f"{arcname}: robots disallow ({info})")
            continue

        tmp_path = status = None
        last_err = None
        for attempt in range(MAX_ATTEMPTS):
            try:
                tmp_path, status = download_to_temp(f_url, dest_dir)
                last_err = None
                break
            except urllib.error.HTTPError as e:
                # Non-retryable client errors (404/403 etc.): stop immediately.
                last_err = f"HTTP {e.code} from {f_url}"
                if e.code < 500:
                    break
            except Exception as e:  # noqa: BLE001 — failures are recorded, never fatal
                last_err = f"{type(e).__name__} from {f_url}: {e}"
            if attempt < len(BACKOFF_SECONDS):
                time.sleep(BACKOFF_SECONDS[attempt])
        if last_err is None:
            downloaded.append((spec, tmp_path, status))  # type: ignore[arg-type]
        else:
            failures.append(f"{arcname}: {last_err}")
            if tmp_path is not None:
                Path(tmp_path).unlink(missing_ok=True)
    failures = list(dict.fromkeys(failures))  # de-dupe repeated messages

    if failures:
        # Never leave a partial/duplicate-looking crawl behind.
        for (_spec, tmp_path, _status) in downloaded:
            tmp_path.unlink(missing_ok=True)
        try:
            dest_dir.rmdir()  # only succeeds when empty
        except OSError:
            pass
        record_crawl(
            manifest, source_id, primary_url, "", [], "failure",
            note="; ".join(failures) + " | " + manual_retrieval_note(primary_url, dest_dir_rel),
        )
        return {"status": "failure", "reason": "; ".join(failures),
                "arc_dir": ""}

    # Hash everything first, then decide the write policy.
    records: list[dict] = []
    any_changed = not prev_hashes  # no known baseline yet => snapshot needed
    for spec, tmp_path, status in downloaded:
        digest = sha256_of(tmp_path)
        prev = prev_hashes.get(spec["arcname"])
        if prev is not None and prev != digest:
            any_changed = True
        records.append(
            {
                "name": spec["arcname"],
                "sha256": digest,
                "url": spec["url"],
                "http_status": status,
            }
        )

    if not any_changed:
        # Content identical to previous crawl: no new snapshot directory.
        for (_spec, tmp_path, _status) in downloaded:
            tmp_path.unlink(missing_ok=True)
        try:
            dest_dir.rmdir()
        except OSError:
            pass
        for r in records:
            r["unchanged"] = True
        record_crawl(manifest, source_id, primary_url, "", records, "unchanged",
                     note="Content identical to previous crawl; no new snapshot written.")
        return {"status": "unchanged", "arc_dir": "", "files": records}

    # Write a complete, self-consistent dated snapshot: every file of the
    # source goes into this dir, so readers of "the newest crawl dir" always
    # see the whole source.
    for r, (spec, tmp_path, _status) in zip(records, downloaded):
        target = dest_dir / spec["arcname"]
        size = tmp_path.stat().st_size
        shutil.move(str(tmp_path), str(target))
        os.chmod(target, 0o644)  # mkstemp creates 0600; archive files should be readable
        r["unchanged"] = prev_hashes.get(spec["arcname"]) == r["sha256"]
        r["file_size_bytes"] = size

    record_crawl(manifest, source_id, primary_url, dest_dir_rel, records,
                 "success", note="")
    return {"status": "success", "arc_dir": dest_dir_rel, "files": records}
