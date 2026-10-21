"""API & Export Provenance Tests (T103, Milestone 10).

Static provenance verification for the SvelteKit /api/v1 endpoints:
1. endpoints import ONLY processed public datasets (no raw / private data);
2. exports preserve source_id / source_locator columns;
3. endpoints document licence inheritance (CC BY 4.0 for Kanakku/DS030
   derivatives).
"""

import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_DIR = os.path.join(ROOT, "src", "routes", "api", "v1")

ENDPOINTS = {
    "projects.json": os.path.join(API_DIR, "projects.json", "+server.ts"),
    "change-log.json": os.path.join(API_DIR, "change-log.json", "+server.ts"),
    "projects.csv": os.path.join(API_DIR, "projects.csv", "+server.ts"),
}

PROCESSED_IMPORTS = {
    "unified_project_explorer.json",
    "change_log.json",
}


def _read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


class TestApiEndpoints(unittest.TestCase):
    def test_01_all_endpoints_exist_and_are_read_only(self):
        for name, path in ENDPOINTS.items():
            self.assertTrue(os.path.exists(path), f"{name} endpoint missing")
            src = _read(path)
            self.assertIn("RequestHandler", src)
            self.assertNotRegex(
                src, r"\b(POST|PUT|DELETE|PATCH)\b\s*:",
                f"{name} must expose GET only (read-only)",
            )

    def test_02_endpoints_import_only_processed_datasets(self):
        for name, path in ENDPOINTS.items():
            src = _read(path)
            for import_path in re.findall(r"from\s+'([^']+)';( [^;]*)?", src):
                pass
            imports = re.findall(r"from\s+'([^']+)'", src)
            dataset_imports = [i for i in imports if i.endswith(".json")]
            self.assertTrue(dataset_imports, f"{name} imports no dataset")
            for imp in dataset_imports:
                self.assertTrue(
                    any(ds in imp for ds in PROCESSED_IMPORTS),
                    f"{name} imports unexpected dataset {imp}",
                )
                self.assertNotIn(  # only 'data/processed' paths allowed
                    "/data/raw", imp, f"{name} must not import raw data ({imp})"
                )

    def test_03_csv_preserves_provenance_columns(self):
        src = _read(ENDPOINTS["projects.csv"])
        for column in ("source_id", "source_locator"):
            self.assertIn(f"'{column}'", src)

    def test_04_json_endpoints_preserve_record_provenance(self):
        """projects.json serves the explorer records verbatim (provenance intact)."""
        src = _read(ENDPOINTS["projects.json"])
        self.assertIn("records: explorerData.records", src)
        self.assertIn("summary: explorerData.summary", src)

    def test_05_licence_inheritance_documented(self):
        for name, path in ENDPOINTS.items():
            src = _read(path)
            if name in ("projects.json", "projects.csv"):
                # explorer-derived data: Kanakku (DS030) derivatives inherit CC BY 4.0
                self.assertIsNotNone(
                    re.search(r"CC BY 4\.0", src),
                    f"{name} must document CC BY 4.0 inheritance",
                )
            # every endpoint must declare a licence block at all
            self.assertTrue(
                re.search(r"(?i)licence|license", src),
                f"{name} must declare its licence terms",
            )
        self.assertIn(
            "provenance",
            _read(ENDPOINTS["change-log.json"]).lower(),
            "change-log endpoint must require provenance preservation",
        )

    def test_06_endpoints_expose_no_private_fields(self):
        """Guard against shipping unprocessed/private fields not present in the
        processed dataset schema (e.g. internal match confidence tiers)."""
        import json
        explorer = json.load(open(
            os.path.join(ROOT, "data", "processed", "unified_project_explorer.json"),
            encoding="utf-8"))
        public_keys = set(explorer["records"][0].keys())
        src = _read(ENDPOINTS["projects.csv"])
        csv_header = re.search(r"const header = \[(.*?)\];", src, re.S).group(1)
        fields = re.findall(r"'([a-z_0-9]+)'", csv_header)
        for f in fields:
            accepted = {"approved_inr", "approved_crore", "released_inr", "released_crore",
                        "release_ratio_pct", "source_status_text", "normalised_status",
                        "status_as_of", "open_flags"}
            self.assertTrue(
                f in accepted or f in public_keys,
                f"CSV column '{f}' is not an established public field",
            )


if __name__ == "__main__":
    unittest.main()
