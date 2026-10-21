"""Fetcher Infrastructure Tests for KIIFB Dashboard (T080, Milestone 8).

Validates the live-crawl archive contract without any network access:

1. Checksum & archive-path helpers (SHA-256, dated immutable directories,
   `_rN` suffix collision handling).
2. Manifest live-crawls history: appending records preserves the pinned
   `sources[]` checksums that `scripts/refresh_pipeline.py` verifies.
3. Unchanged-content detection: identical SHA-256 vs previous crawl results in
   status 'unchanged' with NO new archive directory (no duplicate snapshots).
4. Changed-content detection writes a COMPLETE self-consistent snapshot and
   marks unchanged files accordingly.
5. Re-crawl immutability: a second crawl on the same day for changed content
   never overwrites the earlier directory (uses `_r2`).
6. Failure semantics: partial failure leaves no partially-overwritten state and
   records a safe manual retrieval note; unreachable paths recorded, tree clean.
7. Dry-run records and prints intended paths without downloading or saving.
8. end-to-end: manifest schema stays compatible (subset of schema keys used by
   the pipeline: sources, institutional_and_federal_datasets, live_crawls).

Offline contract: no test touches the network. `crawl_targets` is exercised by
pre-creating an archive dir with expected content and monkeypatching
`fetch_common.download_to_temp` to copy from fixtures.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import fetch_common as fc  # noqa: E402


def write_bytes(p: Path, content: bytes) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)
    return p


class FetchCommonBase(unittest.TestCase):
    """Each test runs against an isolated temp project data tree."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.temp_root = Path(self._tmp.name)
        # Redirect PROJECT_ROOT-relative archive paths into the temp tree by
        # monkeypatching the module constant used by archive_root().
        self._orig_raw = fc.PROJECT_ROOT
        fc.PROJECT_ROOT = self.temp_root
        self.manifest_path = self.temp_root / "data" / "manifest.json"
        self.manifest_path.parent.mkdir(parents=True)
        self.manifest = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "sources": [{
                "source_id": "DS010",
                "local_path": "data/raw/kiifb/kiifb-prjStatus.html",
                "sha256": fc.sha256_of(
                    write_bytes(self.temp_root / "data/raw/kiifb/kiifb-prjStatus.html",
                                b"PINNED BASELINE CONTENT")
                ),
            }],
            "institutional_and_federal_datasets": [],
        }

    def tearDown(self) -> None:
        fc.PROJECT_ROOT = self._orig_raw
        self._tmp.cleanup()


class TestChecksumAndPaths(FetchCommonBase):
    def test_sha256_matches_known_vector(self) -> None:
        # sha256(b"abc") == ba7816bf...
        p = write_bytes(self.temp_root / "x.txt", b"abc")
        self.assertEqual(fc.sha256_of(p),
                         "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_archive_dirs_are_dated_and_distinct(self) -> None:
        d1 = fc.archive_dir("kiifb", "project-status", "2026-10-20")
        d2 = fc.archive_dir("kiifb", "project-status", "2026-10-21")
        self.assertEqual(d1, self.temp_root / "data/raw/kiifb/project-status/2026-10-20")
        self.assertNotEqual(d1, d2)

    def test_resolve_unique_dir_avoids_overwrite(self) -> None:
        base = self.temp_root / "data/raw/kanakku/2026-10-20"
        write_bytes(base / "projects.csv", b"old crawl")
        resolved = fc.resolve_unique_dir(base)
        self.assertEqual(resolved.name, "2026-10-20_r2")
        resolved.mkdir(parents=True, exist_ok=True)
        write_bytes(resolved / "projects.csv", b"second crawl same day")
        self.assertEqual(fc.resolve_unique_dir(base).name, "2026-10-20_r3")
        # Empty existing dir may be reused.
        (self.temp_root / "data/raw/kanakku/2026-10-21").mkdir(parents=True)
        self.assertEqual(
            fc.resolve_unique_dir(self.temp_root / "data/raw/kanakku/2026-10-21").name,
            "2026-10-21")


class TestManifestHistory(FetchCommonBase):
    def test_record_crawl_preserves_pinned_sources(self) -> None:
        pinned_before = json.dumps(self.manifest["sources"], sort_keys=True)
        fc.record_crawl(self.manifest, "DS010", "https://example.org/x",
                        "data/raw/kiifb/project-status/2026-10-20",
                        [{"name": "x.html", "sha256": "abc"}], "success")
        self.assertEqual(json.dumps(self.manifest["sources"], sort_keys=True),
                         pinned_before)
        self.assertEqual(len(self.manifest["live_crawls"]), 1)
        self.assertEqual(self.manifest["live_crawls"][0]["source_id"], "DS010")

    def test_save_manifest_round_trip_is_atomic_and_lossless(self) -> None:
        fc.record_crawl(self.manifest, "DS021", "https://example.org/y", "",
                        [], "failure", note="robot guard")
        fc.save_manifest(self.manifest, self.manifest_path)
        loaded = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(loaded["live_crawls"][0]["status"], "failure")
        self.assertEqual(loaded["sources"][0]["source_id"], "DS010")
        # Atomic save: no temp/manifest leftovers in the data dir itself.
        leftovers = [p.name for p in self.manifest_path.parent.iterdir()
                     if p.name.startswith("manifest-") or p.suffix == ".tmp"]
        self.assertEqual(leftovers, [])

    def test_crawl_history_is_bounded(self) -> None:
        for i in range(250):
            fc.record_crawl(self.manifest, "DS010", "u", "d", [], "success")
        self.assertEqual(len(self.manifest["live_crawls"]), 200)

    def test_get_last_crawl_skips_failures(self) -> None:
        fc.record_crawl(self.manifest, "DS010", "u", "old-dir", [], "failure")
        fc.record_crawl(self.manifest, "DS010", "u", "good-dir",
                        [{"name": "a", "sha256": "h1"}], "success")
        self.assertEqual(fc.get_last_crawl(self.manifest, "DS010")["arc_dir"], "good-dir")
        self.assertEqual(fc.last_crawl_hashes(self.manifest, "DS010"), {"a": "h1"})


class _PatchDownloader:
    """Context: replaces fc.download_to_temp with a fixture-based stub.

    Fixtures map URL -> bytes, or URL -> None to simulate a failed download
    (RuntimeError, as a network layer would raise).
    """

    def __init__(self, fixtures: dict[str, bytes | None]):
        self.fixtures = fixtures
        self._orig = None

    def __enter__(self) -> "_PatchDownloader":
        self._orig = fc.download_to_temp
        fixtures = self.fixtures

        def fake_download(url, tmp_dir, timeout=fc.DOWNLOAD_TIMEOUT):
            if url not in fixtures:
                raise RuntimeError(f"no fixture for {url}")
            import tempfile
            if fixtures[url] is None:
                raise RuntimeError("simulated network failure")
            fd, name = tempfile.mkstemp(prefix="test-dl-", dir=str(tmp_dir))
            with open(name, "wb") as f:
                f.write(fixtures[url])
            return Path(name), 200

        fc.download_to_temp = fake_download
        return self

    def __exit__(self, *a) -> None:
        fc.download_to_temp = self._orig


class TestCrawlTargets(FetchCommonBase):
    URL = "https://example.org/prjStatus.jsp"
    ARCNAME = "kiifb-prjStatus.html"
    DEST_REL = "data/raw/kiifb/project-status/2026-10-20"

    def _crawl(self, content: bytes | None = b"PAGE CONTENT v1") -> dict:
        resolved = [{"url": self.URL, "arcname": self.ARCNAME}]
        with _PatchDownloader({self.URL: content or b""}):
            return fc.crawl_targets(
                manifest=self.manifest, source_id="DS010", group="kiifb",
                dataset="project-status", primary_url=self.URL,
                resolved_files=resolved, date_iso="2026-10-20",
                robots_cache={"example.org": (True, "stub robots")})

    def test_first_crawl_archives_and_records(self) -> None:
        summary = self._crawl()
        self.assertEqual(summary["status"], "success")
        dest = self.temp_root / self.DEST_REL / self.ARCNAME
        self.assertTrue(dest.exists())
        digest = fc.sha256_of(dest)
        rec = self.manifest["live_crawls"][-1]
        self.assertEqual(rec["status"], "success")
        self.assertEqual(rec["files"][0]["sha256"], digest)
        # Pinned baseline untouched.
        pinned = self.temp_root / "data/raw/kiifb/kiifb-prjStatus.html"
        self.assertEqual(pinned.read_bytes(), b"PINNED BASELINE CONTENT")

    def test_identical_content_records_unchanged_without_new_archive(self) -> None:
        self._crawl()
        dirs = list((self.temp_root / "data/raw/kiifb/project-status").iterdir())
        summary = self._crawl()  # same bytes → unchanged
        self.assertEqual(summary["status"], "unchanged")
        self.assertEqual(summary["arc_dir"], "")  # no archived dir this time
        dirs_after = list((self.temp_root / "data/raw/kiifb/project-status").iterdir())
        self.assertEqual(dirs_after, dirs)  # no duplicate archive created
        self.assertTrue(all(f.get("unchanged")
                            for f in self.manifest["live_crawls"][-1]["files"]))

    def test_changed_content_writes_new_snapshot(self) -> None:
        self._crawl(b"PAGE CONTENT v1")
        summary = self._crawl(b"PAGE CONTENT v2 CHANGED")
        self.assertEqual(summary["status"], "success")
        latest = self.manifest["live_crawls"][-1]
        self.assertEqual(latest["files"][0]["unchanged"], False)
        dirs = sorted(d.name for d in
                      (self.temp_root / "data/raw/kiifb/project-status").iterdir())
        # Both immutable snapshots survive: the v1 dir and the v2 `_r2` dir.
        self.assertEqual(dirs, ["2026-10-20", "2026-10-20_r2"])
        self.assertEqual(latest["arc_dir"], self.DEST_REL + "_r2")

    def test_same_day_recrawl_never_overwrites(self) -> None:
        self._crawl(b"VERSION-A")
        first_dir = self.temp_root / self.DEST_REL
        bytes_first = (first_dir / self.ARCNAME).read_bytes()
        summary = self._crawl(b"VERSION-B")  # later same-day crawl, changed
        self.assertEqual(summary["status"], "success")
        second_dir = self.temp_root / (self.DEST_REL + "_r2")
        self.assertEqual((second_dir / self.ARCNAME).read_bytes(), b"VERSION-B")
        self.assertEqual((first_dir / self.ARCNAME).read_bytes(), bytes_first)

    def test_multi_file_partial_failure_leaves_tree_clean(self) -> None:
        urls = {"https://example.org/projects.csv": b"P",
                "https://example.org/broken.csv": None}
        resolved = [{"url": "https://example.org/projects.csv", "arcname": "projects.csv"},
                    {"url": "https://example.org/broken.csv", "arcname": "broken.csv"}]
        with _PatchDownloader(urls):
            summary = fc.crawl_targets(
                manifest=self.manifest, source_id="DS030", group="kanakku",
                dataset="", primary_url="https://example.org/data",
                resolved_files=resolved, date_iso="2026-10-20",
                robots_cache={"example.org": (True, "stub robots")})
        self.assertEqual(summary["status"], "failure")
        note = self.manifest["live_crawls"][-1]["note"]
        self.assertIn("broken.csv", note)
        self.assertIn("Manual retrieval path", note)
        # No partial snapshot directory left behind.
        base = self.temp_root / "data/raw/kanakku"
        self.assertEqual([p.name for p in base.iterdir()], [])

    def test_complete_snapshot_includes_unchanged_siblings(self) -> None:
        urls = {"https://example.org/projects.csv": b"PROJECTS v1",
                "https://example.org/funding.csv": b"FUNDING v1"}
        resolved = [{"url": u, "arcname": n} for u, n in
                    [("https://example.org/projects.csv", "projects.csv"),
                     ("https://example.org/funding.csv", "funding.csv")]]
        with _PatchDownloader(urls):
            fc.crawl_targets(self.manifest, "DS030", "kanakku", "",
                             "https://example.org/data", resolved, "2026-10-19",
                             robots_cache={"example.org": (True, "stub")})
            # Day 2: funding changed, projects identical → snapshot must be
            # complete (both files present in the new dir).
            urls["https://example.org/funding.csv"] = b"FUNDING v2"
            summary = fc.crawl_targets(self.manifest, "DS030", "kanakku", "",
                                       "https://example.org/data", resolved,
                                       "2026-10-20",
                                       robots_cache={"example.org": (True, "stub")})
        self.assertEqual(summary["status"], "success")
        new_dir = self.temp_root / "data/raw/kanakku/2026-10-20"
        self.assertTrue((new_dir / "projects.csv").exists())
        self.assertTrue((new_dir / "funding.csv").exists())
        self.assertEqual((new_dir / "projects.csv").read_bytes(), b"PROJECTS v1")
        flags = {f["name"]: f["unchanged"] for f in self.manifest["live_crawls"][-1]["files"]}
        self.assertTrue(flags["projects.csv"])
        self.assertFalse(flags["funding.csv"])

    def test_dry_run_records_and_downloads_nothing(self) -> None:
        with _PatchDownloader({}) as _pd:
            summary = fc.crawl_targets(
                self.manifest, "DS010", "kiifb", "project-status", self.URL,
                [{"url": self.URL, "arcname": self.ARCNAME}], "2026-10-20",
                dry_run=True, robots_cache={"example.org": (True, "stub robots")})
        self.assertEqual(summary["status"], "dry-run")
        self.assertEqual(self.manifest["live_crawls"][-1]["status"], "dry-run")
        self.assertFalse((self.temp_root / "data/raw/kiifb/project-status").exists())


class TestManifestSchemaCompatibility(FetchCommonBase):
    def test_live_crawls_files_have_required_fields(self) -> None:
        fc.record_crawl(self.manifest, "DS010", "u", "d",
                        [{"name": "a", "sha256": "h", "file_size_bytes": 3}], "success")
        entry = self.manifest["live_crawls"][-1]
        for key in ("source_id", "retrieved_at", "arc_dir", "files", "status"):
            self.assertIn(key, entry)
        self.assertIn("sha256", entry["files"][0])


if __name__ == "__main__":
    unittest.main()
