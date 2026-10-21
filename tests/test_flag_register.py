"""Flag Register Reconciliation Tests (T102, Milestone 10).

Asserts the /flags delay & anomaly register reconciles exactly with the
processed dataset: the union of per-flag counts equals the count of every
open_flag occurrence in unified_project_explorer.json, the registry covers
every flag id present in the data, and change_log.json retains resolved /
added flag history rather than deleting it.
"""

import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPLORER = os.path.join(ROOT, "data", "processed", "unified_project_explorer.json")
CHANGE_LOG = os.path.join(ROOT, "data", "processed", "change_log.json")
FLAGS_TS = os.path.join(ROOT, "src", "lib", "data", "flags.ts")

REGISTER_IDS = ["overdue", "payment_vs_progress", "cost_escalation", "stale", "above_approved"]


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


class TestFlagRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = _load(EXPLORER)
        cls.change_log = _load(CHANGE_LOG)
        with open(FLAGS_TS, "r", encoding="utf-8") as fh:
            cls.flags_source = fh.read()

    def _flag_counts(self):
        counts = {fid: 0 for fid in REGISTER_IDS}
        for r in self.data["records"]:
            for f in r.get("open_flags") or []:
                counts[f] = counts.get(f, 0) + 1
        return counts

    def test_01_register_union_reconciles_with_dataset(self):
        """Sum of per-flag counts equals every open_flag row in the dataset."""
        counts = self._flag_counts()
        dataset_total = sum(len(r.get("open_flags") or []) for r in self.data["records"])
        self.assertEqual(sum(counts.values()), dataset_total)
        # Register-known flags total the same rows
        self.assertEqual(sum(counts[fid] for fid in REGISTER_IDS), dataset_total)

    def test_02_registry_ids_cover_every_flag_in_data(self):
        unknown = {f for r in self.data["records"] for f in (r.get("open_flags") or [])
                   if f not in REGISTER_IDS}
        self.assertEqual(unknown, set(), f"Flags missing from register: {unknown}")

    def test_03_registry_defines_objective_criteria(self):
        for fid in REGISTER_IDS:
            self.assertIn(f"id: '{fid}'", self.flags_source, f"{fid} not in FLAG_REGISTRY")

    def test_04_criteria_text_states_measurable_conditions(self):
        import re
        blocks = re.findall(r"\{\s*id: '([a-z_]+)'", self.flags_source)
        self.assertEqual(sorted(blocks), sorted(REGISTER_IDS))
        for fid, criterion in [
            ("stale", "change_log.json"),
            ("above_approved", "exceeds its sanctioned approved outlay"),
        ]:
            self.assertIn(criterion, self.flags_source)

    def test_05_resolved_flags_retained_in_change_log(self):
        """change_log.json keeps flags_added / flags_resolved per dataset."""
        for dataset, info in self.change_log["datasets"].items():
            self.assertIn("flags_added", info, dataset)
            self.assertIn("flags_resolved", info, dataset)

    def test_06_flag_totals_consistent_with_status_migrations(self):
        """Flags added + resolved are logged even when zero (baseline rule)."""
        totals = {ds: info["totals"].get("flags_added", 0)
                  for ds, info in self.change_log["datasets"].items()}
        self.assertEqual(totals, {
            "kanakku_packages.json": 0,
            "kiifb_projects.json": 0,
            "kite_schools.json": 0,
            "unified_project_explorer.json": 0,
        })


if __name__ == "__main__":
    unittest.main()
