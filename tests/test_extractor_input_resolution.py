"""Extractor Input-Resolution Tests for KIIFB Dashboard (T081, Milestone 8).

Validates the precedence contract shared by all extractors via
`fetch_common.resolve_input` and `fetch_common.newest_snapshot`:

    CLI argument > environment variable > newest dated live-crawl snapshot >
    pinned baseline path (offline byte-reproducibility).

No network access; all file fixtures live in an isolated temp data tree.
"""

import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import fetch_common as fc  # noqa: E402


class SnapshotResolutionBase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.temp_root = Path(self._tmp.name)
        self._orig_raw = fc.PROJECT_ROOT
        fc.PROJECT_ROOT = self.temp_root

    def tearDown(self) -> None:
        fc.PROJECT_ROOT = self._orig_raw
        self._tmp.cleanup()

    def make_crawl(self, group: str, dataset: str, date: str, arcname: str,
                   content: bytes = b"crawl-content") -> Path:
        d = self.temp_root / "data/raw" / group
        if dataset:
            d = d / dataset
        d = d / date
        d.mkdir(parents=True, exist_ok=True)
        path = d / arcname
        path.write_bytes(content)
        return path


class TestNewestSnapshot(SnapshotResolutionBase):
    def test_none_when_never_crawled(self) -> None:
        self.assertIsNone(fc.newest_snapshot("kiifb", "project-status", "x.html"))

    def test_returns_newest_dated_snapshot(self) -> None:
        self.make_crawl("kanakku", "", "2026-10-16", "projects.csv", b"old")
        self.make_crawl("kanakku", "", "2026-10-20", "projects.csv", b"new")
        got = fc.newest_snapshot("kanakku", "", "projects.csv")
        self.assertEqual(got.parent.name, "2026-10-20")
        self.assertEqual(got.read_bytes(), b"new")

    def test_same_day_recal_crawl_suffix_wins(self) -> None:
        self.make_crawl("kiifb", "project-status", "2026-10-20", "a.html", b"v1")
        self.make_crawl("kiifb", "project-status", "2026-10-20_r2", "a.html", b"v2")
        got = fc.newest_snapshot("kiifb", "project-status", "a.html")
        self.assertEqual(got.parent.name, "2026-10-20_r2")
        self.assertEqual(got.read_bytes(), b"v2")

    def test_missing_arcname_skips_dir(self) -> None:
        self.make_crawl("kite", "kiifb-funded-schools", "2026-10-20", "other.html")
        self.assertIsNone(
            fc.newest_snapshot("kite", "kiifb-funded-schools", "expected.html"))


class TestResolveInputPrecedence(SnapshotResolutionBase):
    GROUP, DATASET = "kiifb", "project-status"
    ARCNAME = "kiifb-prjStatus.html"
    PINNED = "data/raw/kiifb/kiifb-prjStatus.html"

    def setUp(self) -> None:
        super().setUp()
        # Pinned baseline always exists in the tree.
        pinned = self.temp_root / self.PINNED
        pinned.parent.mkdir(parents=True)
        pinned.write_bytes(b"PINNED")
        self._old_env = {k: None for k in ("KIIFB_PROJECTS_HTML",
                                           "KITE_SAMETHAM_HTML",
                                           "KANAKKU_PROJECTS_CSV")}

    def tearDown(self) -> None:
        import os
        for k in list(self._old_env):
            os.environ.pop(k, None)
        super().tearDown()

    def _resolve(self, explicit=None):
        return fc.resolve_input(explicit, "KIIFB_PROJECTS_HTML",
                                self.GROUP, self.DATASET, self.ARCNAME, self.PINNED)

    def test_pinned_baseline_is_last_fallback(self) -> None:
        path, origin = self._resolve()
        self.assertTrue(str(path).endswith(self.PINNED))
        self.assertIn("pinned baseline", origin)

    def test_newest_crawl_beats_pinned(self) -> None:
        self.make_crawl(self.GROUP, self.DATASET, "2026-10-20", self.ARCNAME,
                        b"CRAWL")
        path, origin = self._resolve()
        self.assertIn("2026-10-20", str(path))
        self.assertIn("newest live-crawl snapshot", origin)

    def test_env_var_beats_newest_crawl(self) -> None:
        import os
        self.make_crawl(self.GROUP, self.DATASET, "2026-10-20", self.ARCNAME)
        override = self.temp_root / "manual-download.html"
        override.write_bytes(b"MANUAL")
        os.environ["KIIFB_PROJECTS_HTML"] = str(override)
        path, origin = self._resolve()
        self.assertEqual(path, override.resolve())
        self.assertIn("env KIIFB_PROJECTS_HTML", origin)

    def test_cli_arg_beats_everything(self) -> None:
        import os
        self.make_crawl(self.GROUP, self.DATASET, "2026-10-20", self.ARCNAME)
        override = self.temp_root / "explicit.html"
        override.write_bytes(b"EXPLICIT")
        os.environ["KIIFB_PROJECTS_HTML"] = str(self.temp_root / "manual.html")
        path, origin = self._resolve(str(override.resolve()))
        self.assertEqual(path, override.resolve())
        self.assertIn("cli argument", origin)


class TestExtractorsUseResolution(unittest.TestCase):
    """Static wiring test: each extractor's entry point must consult
    fetch_common.resolve_input with its own pinned baseline (guards against
    regressions reverting to hardcoded paths)."""

    def wiring_cases(self):
        return [
            (PROJECT_ROOT / "scripts/extract_kiifb_projects.py",
             ["resolve_input", "KIIFB_PROJECTS_HTML",
              "data/raw/kiifb/kiifb-prjStatus.html"]),
            (PROJECT_ROOT / "scripts/extract_kite_schools.py",
             ["resolve_input", "KITE_SAMETHAM_HTML",
              "data/raw/kite/kiifb-funded-schools-sametham.html"]),
            (PROJECT_ROOT / "scripts/enrich_projects_with_kanakku.py",
             ["resolve_input", "KANAKKU_PROJECTS_CSV",
              "data/raw/kanakku/projects.csv"]),
            (PROJECT_ROOT / "scripts/refresh_pipeline.py",
             ["--fetch", "newest_crawl_or_pinned"]),
        ]

    def test_extractors_wired_to_resolution(self) -> None:
        for path, needles in self.wiring_cases():
            src = path.read_text(encoding="utf-8")
            for needle in needles:
                self.assertIn(needle, src, f"{path.name} missing {needle!r}")


if __name__ == "__main__":
    unittest.main()
