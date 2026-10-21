"""Matching Coverage Tests for KIIFB Dashboard (T083, Milestone 8).

Validates the Kanakku enrichment fill-up tiers offline:

1. District coverage of the 1,408-record KIIFB register meets the >= 70%
   acceptance target (baseline was 41.7%).
2. Stability: every district/coordinate/flag assignment that existed at the
   previous commit (git HEAD ~ data/processed/kiifb_projects.json, built from
   the pinned baselines with the pre-T083 matcher) is UNCHANGED in the current
   processed file. Fill-up tiers only fill records with null districts.
3. New-tier semantics: explicit district naming, department-filtered
   containment and token fuzzy units tested against synthetic packages.
4. Audit match log consistency: every fill-up entry references an existing
   project with a matching resolution/confidence; counters reconcile.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import enrich_projects_with_kanakku as en  # noqa: E402


class TestNameDistrictMentionTier(unittest.TestCase):
    def test_exact_mentions(self) -> None:
        self.assertEqual(en.extract_districts_from_name(
            "Betterment of facilities at GHSS Mangalam, Alappuzha District"),
            ["Alappuzha"])
        self.assertEqual(en.extract_districts_from_name(
            "Construction of Flyover at Ulloor in Thiruvananthapuram"),
            ["Thiruvananthapuram"])

    def test_alias_mapping(self) -> None:
        self.assertEqual(
            en.extract_districts_from_name("Water Supply Scheme, Trivandrum"),
            ["Thiruvananthapuram"])
        self.assertEqual(
            en.extract_districts_from_name("Zoo renovation, Trichur"),
            ["Thrissur"])

    def test_case_insensitive_word_boundary(self) -> None:
        self.assertEqual(
            en.extract_districts_from_name(" Setting up of new KANNUR complex"),
            ["Kannur"])

    def test_no_mention_yields_empty(self) -> None:
        self.assertEqual(
            en.extract_district_from_name_meta("Some Road works"), (None, None))
        self.assertEqual(en.extract_districts_from_name("Road works"), [])

    def test_ambiguous_over_two_districts_rejected(self) -> None:
        # Three distinct districts - deliberately ambiguous, must not assign.
        self.assertEqual(en.extract_districts_from_name(
            "Statewide scheme in Kannur, Kottayam and Ernakulam"), [])
        # Two consistent districts are allowed (multi-district umbrella).
        self.assertEqual(en.extract_districts_from_name(
            "Scheme covering Kannur and Kottayam"), ["Kannur", "Kottayam"])

    def test_name_substring_false_positive_guard(self) -> None:
        # 'Kollam' inside 'Kollannur' must NOT match (word-boundary guard).
        self.assertEqual(en.extract_districts_from_name("Kollannur bypass"), [])


class TestPackageTiers(unittest.TestCase):
    def test_containment_same_dept(self) -> None:
        # Package title nests inside the longer project title → containment tier.
        packages = [
            {"code": "P1", "title": "Cultural Complex at Kottayam DLLW block",
             "department": "Cultural Affairs Department", "district": "Kottayam",
             "constituencies": "Kottayam", "open_flags": "", "latitude": "9.6",
             "longitude": "76.5"},
            {"code": "P2", "title": "Cultural Complex at Idukki",
             "department": "Cultural Affairs Department", "district": "Idukki",
             "constituencies": "", "open_flags": "overdue", "latitude": "",
             "longitude": ""},
        ]
        got = en.containment_and_fuzzy_geo(
            "Land Acquisition for Cultural Complex at Kottayam DLLW block phase 1",
            "Cultural Affairs Department", packages)
        self.assertIsNotNone(got)
        district, constituency, coords, flags, codes, resolution, confidence = got
        self.assertEqual(district, "Kottayam")
        self.assertEqual(resolution, "work_containment_same_dept")
        self.assertEqual(codes, ["P1"])
        self.assertEqual(confidence, 0.75)
        self.assertEqual(coords, [(9.6, 76.5)])

    def test_containment_requires_department_agreement(self) -> None:
        packages = [{"code": "P1", "title": "Cultural Complex at Kottayam",
                     "department": "Cultural Affairs Department",
                     "district": "Kottayam", "constituencies": "",
                     "open_flags": "", "latitude": "9.6", "longitude": "76.5"}]
        self.assertIsNone(en.containment_and_fuzzy_geo(
            "Cultural Complex at Kottayam", "Health & Family Welfare", packages))

    def test_containment_requires_district_agreement(self) -> None:
        # Both package titles nest in the project name; districts disagree →
        # containment is rejected and falls through to strict token fuzzy.
        packages = [
            {"code": "P1", "title": "Cultural Complex at Kottayam",
             "department": "Cultural Affairs Department", "district": "Kottayam",
             "constituencies": "", "open_flags": "", "latitude": "9.6", "longitude": "76.5"},
            {"code": "P2", "title": "Cultural Complex at Idukki",
             "department": "Cultural Affairs Department", "district": "Idukki",
             "constituencies": "", "open_flags": "", "latitude": "9.8", "longitude": "77.0"},
        ]
        got = en.containment_and_fuzzy_geo(
            "Cultural Complex at Kottayam wing of Cultural Complex at Idukki",
            "Cultural Affairs Department", packages)
        _, _, _, _, codes, resolution, _ = got
        self.assertEqual(resolution, "token_fuzzy_same_dept_j55")

    def test_token_fuzzy_same_dept_minimum(self) -> None:
        # Short project name shares tokens but a smaller one than the
        # containment threshold requires (neither title nests in the other).
        packages = [{"code": "P1",
                     "title": "Second Bridge at Kankakkadavu, Tirur",
                     "department": "Water Resources Department",
                     "district": "Malappuram", "constituencies": "Perinthalmanna",
                     "open_flags": "", "latitude": "11.0", "longitude": "76.2"}]
        got = en.containment_and_fuzzy_geo(
            "Setting up Second Bridge Kankakkadavu 2",
            "Water Resources Department", packages)
        self.assertIsNotNone(got)
        district, _, _, _, _, resolution, confidence = got
        self.assertEqual(district, "Malappuram")
        self.assertEqual(resolution, "token_fuzzy_same_dept_j55")
        self.assertGreaterEqual(confidence, 0.55)

    def test_token_fuzzy_below_threshold_rejected(self) -> None:
        packages = [{"code": "P1",
                     "title": "Second Bridge at Kankakkadavu over Tirur river",
                     "department": "Water Resources Department",
                     "district": "Malappuram", "constituencies": "Perinthalmanna",
                     "open_flags": "", "latitude": "11.0", "longitude": "76.2"}]
        # One shared token (bridge) → j=0.25 < 0.55 → rejected.
        self.assertIsNone(en.containment_and_fuzzy_geo(
            "Renovation of Bridge approach road 4",
            "Water Resources Department", packages))


class TestCommittedCoverageStability(unittest.TestCase):
    """Runs against the committed/current processed state — offline, read-only."""

    @classmethod
    def setUpClass(cls) -> None:
        with open(PROJECT_ROOT / "data" / "processed" / "kiifb_projects.json",
                  encoding="utf-8") as f:
            cls.current = json.load(f)["projects"]
        head_text = subprocess.run(
            ["git", "show", "HEAD:data/processed/kiifb_projects.json"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)).stdout
        cls.head = json.loads(head_text)["projects"]

    def test_district_coverage_target(self) -> None:
        with_d = sum(1 for p in self.current if p.get("district"))
        pct = with_d / len(self.current)
        self.assertGreaterEqual(with_d, 70 * len(self.current) / 100,
                                f"coverage dropped: {with_d}/{len(self.current)}")
        self.assertGreaterEqual(pct, 0.70)

    def test_prior_match_assignments_unchanged(self) -> None:
        head_by_id = {p["project_id"]: p for p in self.head}
        for p in self.current:
            prev = head_by_id[p["project_id"]]
            if prev.get("district"):
                self.assertEqual(p.get("district"), prev.get("district"),
                                 f"district changed for {p['project_id']}")
                self.assertEqual(p.get("constituency"), prev.get("constituency"),
                                 f"constituency changed for {p['project_id']}")
                self.assertEqual(p.get("open_flags"), prev.get("open_flags"),
                                 f"flags changed for {p['project_id']}")
                if prev.get("coordinates"):
                    self.assertEqual(p.get("coordinates"), prev.get("coordinates"),
                                     f"coords changed for {p['project_id']}")

    def test_new_districts_only_where_previously_null(self) -> None:
        head_by_id = {p["project_id"]: p for p in self.head}
        for p in self.current:
            if not head_by_id[p["project_id"]].get("district") and p.get("district") is not None:
                meta = p.get("district_match")
                self.assertIsNotNone(
                    meta, f"fill-up without audit meta for {p['project_id']}")
                self.assertIn(meta["resolution"], (
                    "name_district_mention", "work_containment_same_dept",
                    "token_fuzzy_same_dept_j55"))
                self.assertGreaterEqual(meta["confidence"], 0.55)

    def test_all_nonnull_districts_are_valid_kerala_districts(self) -> None:
        valid = set(en.KERALA_DISTRICTS)
        for p in self.current:
            d = p.get("district")
            if d:
                self.assertTrue(
                    all(part.strip() in valid for part in d.split(",")) or
                    d in valid, f"invalid district value: {d!r}")


class TestMatchLogConsistency(unittest.TestCase):
    def test_log_reconciles_with_register(self) -> None:
        log = json.load(open(PROJECT_ROOT / "data" / "processed" /
                             "kanakku_match_log.json", encoding="utf-8"))
        projects = {
            p["project_id"]: p for p in json.load(
                open(PROJECT_ROOT / "data" / "processed" / "kiifb_projects.json",
                     encoding="utf-8"))["projects"]}
        self.assertEqual(log["total_entries"], len(log["entries"]))
        counts = {}
        for e in log["entries"]:
            p = projects.get(e["project_id"])
            self.assertIsNotNone(p, f"log references unknown {e['project_id']}")
            self.assertIsNotNone(p.get("district"),
                                 f"log entry without district {e['project_id']}")
            self.assertEqual(e["resolution"], p["district_match"]["resolution"])
            self.assertEqual(int(e["confidence"] * 100),
                             int(p["district_match"]["confidence"] * 100))
            counts[e["resolution"]] = counts.get(e["resolution"], 0) + 1
        self.assertEqual(log["tiers_applied"], counts)


if __name__ == "__main__":
    unittest.main()
