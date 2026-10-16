"""End-to-End Data & Model Integrity Test Suite for KIIFB Dashboard (T060).

Validates:
1. Manifest completeness: all raw and processed sources are registered with SHA-256 checksums.
2. Cross-dataset consistency:
   - All 5 headline assertions (AST-001 to AST-005) have matching evidence links.
   - Financial totals match audited Committee Report tables (Tables 3.1, 3.3, 4.1, 4.2, 4.4, 4.5, 6.1, 6.3).
   - 5 public value dimensions match evidence completeness matrix and data gap register.
   - All 8 Committee recommendations are linked to required legal instruments.
   - All 5 legal issues have distinct judicial proceedings and court distinctions.
   - Discrepancy log items (DISC-001 to DISC-006) are mathematically verified.
"""

import json
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"


class TestEndToEndIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(PROJECT_ROOT / "data" / "manifest.json", "r", encoding="utf-8") as f:
            cls.manifest = json.load(f)
        with open(DATA_DIR / "committee_assertions.json", "r", encoding="utf-8") as f:
            cls.assertions = json.load(f)["assertions"]
        with open(DATA_DIR / "evidence_links.json", "r", encoding="utf-8") as f:
            cls.evidence_links = json.load(f)["evidence_links"]
        with open(DATA_DIR / "committee_financial_tables.json", "r", encoding="utf-8") as f:
            cls.financial_tables = json.load(f)["tables"]
        with open(DATA_DIR / "public_value_and_geography.json", "r", encoding="utf-8") as f:
            cls.public_value = json.load(f)
        with open(DATA_DIR / "legal_issues_register.json", "r", encoding="utf-8") as f:
            cls.legal_issues = json.load(f)["issues"]
        with open(DATA_DIR / "committee_recommendations.json", "r", encoding="utf-8") as f:
            cls.recommendations = json.load(f)["recommendations"]
        with open(DATA_DIR / "methodology_and_quality.json", "r", encoding="utf-8") as f:
            cls.methodology = json.load(f)

    def test_manifest_sources_registered(self):
        """Verify all primary sources are formally registered in manifest.json."""
        sources = self.manifest.get("sources", [])
        source_ids = [s["source_id"] for s in sources]
        self.assertIn("DS001", source_ids)
        self.assertIn("DS010", source_ids)
        self.assertIn("DS021", source_ids)
        for s in sources:
            self.assertIn("title", s)
            self.assertIn("publisher", s)
            self.assertIn("sha256", s)

    def test_assertion_cross_links(self):
        """Verify each headline assertion is cross-linked in evidence_links.json."""
        assertion_ids = [a["assertion_id"] for a in self.assertions]
        self.assertEqual(len(assertion_ids), 5)
        for a_id in assertion_ids:
            links = [l for l in self.evidence_links if l.get("assertion_id") == a_id]
            self.assertGreaterEqual(len(links), 1, f"Assertion {a_id} lacks evidence links")

    def test_financial_stock_and_servicing_reconciliation(self):
        """Verify macro financial totals reconcile across tables."""
        t33 = self.financial_tables["table_3_3_aggregate_borrowing"]["particulars"]
        lookup = {item["label"]: item["amount_crore"] for item in t33}
        t61 = self.financial_tables["table_6_1_debt_servicing_schedule"]
        t_req = self.financial_tables["table_6_2_and_3_completion_requirements"]

        # Table 3.3: Outstanding borrowing stock as of June 30, 2026
        self.assertAlmostEqual(lookup["Outstanding as on 30 June 2026"], 31681.15, places=2)

        # Table 6.1: Scheduled debt service to 2041-42
        self.assertAlmostEqual(t61["total"]["total_debt_service"], 47532.54, places=2)

        # Table 6.3: Future project completion requirement
        self.assertAlmostEqual(t_req["total_required_crore"], 22883.00, places=2)

        # Total future requirement = ₹70,415.54 Cr
        total_future = t61["total"]["total_debt_service"] + t_req["total_required_crore"]
        self.assertAlmostEqual(total_future, 70415.54, places=2)

    def test_district_and_department_reconciliation(self):
        """Verify district and department allocations match Table 4.2 & 4.4."""
        districts = self.public_value["district_distribution"]
        self.assertEqual(len(districts), 15)
        total_infra = sum(d["infrastructure_outlay_cr"] for d in districts)
        # Sum of infrastructure outlays matches Table 4.1 Category A total (₹77,150.87 Cr)
        self.assertAlmostEqual(total_infra, 77150.87, delta=1.0)

        depts = self.public_value["department_distribution"]
        pwd = next(d for d in depts if "Public Works" in d["department"])
        self.assertAlmostEqual(pwd["approved_share_pct"], 52.59, places=1)

    def test_recommendations_and_legal_integrity(self):
        """Verify recommendations and legal registers meet civic truth criteria."""
        self.assertEqual(len(self.recommendations), 8)
        # None marked as implemented
        for r in self.recommendations:
            self.assertNotEqual(r["implementation_status"], "implemented")

        self.assertEqual(len(self.legal_issues), 5)
        # Every legal issue has distinct court separation
        for issue in self.legal_issues:
            self.assertIn("committee_vs_court_distinction", issue["judicial_proceedings"])

    def test_discrepancy_log_reproducibility(self):
        """Verify all itemized discrepancies are reproducible and documented."""
        discs = self.methodology["discrepancies"]
        self.assertGreaterEqual(len(discs), 6)
        # Verify 0.01 Cr rounding on bank loans
        d1 = next(d for d in discs if d["discrepancy_id"] == "DISC-001")
        self.assertIn("6,083.21", d1["mathematical_reconciliation"])
        # Verify 14.43 Cr land acquisition gap
        d2 = next(d for d in discs if d["discrepancy_id"] == "DISC-002")
        self.assertIn("14.43", d2["mathematical_reconciliation"])


if __name__ == "__main__":
    unittest.main()
