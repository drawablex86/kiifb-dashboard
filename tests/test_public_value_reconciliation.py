"""Unit tests for Milestone 4 public value and geography dataset reconciliation.

Validates that:
1. All 5 public value dimensions are formally defined.
2. Unmeasured economic outcomes are tagged explicitly as 'data_gap' / unknown rather than 0.
3. District infrastructure distributions cover all 14 districts + State-wide allocation.
4. District percentage shares sum to ~100% and top 3 districts match Chapter IV findings (~41.6%).
5. Evidence completeness matrix tracks multi-tier operational/outcome gaps.
"""

import json
from pathlib import Path
import unittest

DATA_DIR = Path(__file__).parent.parent / "data" / "processed"


class TestPublicValueReconciliation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        public_val_path = DATA_DIR / "public_value_and_geography.json"
        with open(public_val_path, "r", encoding="utf-8") as f:
            cls.data = json.load(f)

    def test_five_dimensions_present(self):
        """T040: Verify 5 distinct public value dimensions exist."""
        dimensions = self.data.get("dimensions", {})
        expected_keys = [
            "financial_return",
            "economic_return",
            "social_return",
            "distributional_return",
            "financing_suitability",
        ]
        for key in expected_keys:
            self.assertIn(key, dimensions, f"Missing dimension {key}")
            self.assertTrue(len(dimensions[key]["definition"]) > 10)
            self.assertTrue(len(dimensions[key]["committee_finding_summary"]) > 10)

    def test_economic_return_data_gap(self):
        """T040: Verify missing economic return is marked as data_gap, not zero."""
        econ = self.data["dimensions"]["economic_return"]
        self.assertEqual(econ.get("evidence_status"), "data_gap")
        self.assertNotIn("return_cr", econ)
        self.assertNotIn("roi_pct", econ)

    def test_fourteen_districts_plus_statewide(self):
        """T042: Verify all 14 Kerala districts and state-wide pool are present."""
        districts = self.data.get("district_distribution", [])
        self.assertEqual(len(districts), 15)
        names = [d["district"] for d in districts]
        expected_districts = [
            "Thiruvananthapuram", "Kannur", "Ernakulam", "Kozhikode", "Alappuzha",
            "Thrissur", "Kollam", "Malappuram", "Palakkad", "Kottayam",
            "Kasargod", "Wayanad", "Pathanamthitta", "Idukki", "State-wide / Inter-district"
        ]
        for exp in expected_districts:
            self.assertIn(exp, names)

    def test_district_shares_sum(self):
        """T042: Verify district percentage shares sum to ~100%."""
        districts = self.data.get("district_distribution", [])
        total_share = sum(d["infrastructure_share_pct"] for d in districts)
        self.assertAlmostEqual(total_share, 100.0, delta=0.5)

    def test_top_three_concentration(self):
        """T040/T042: Verify Thiruvananthapuram + Kannur + Ernakulam account for ~41.6%."""
        dist_map = {d["district"]: d["infrastructure_share_pct"] for d in self.data["district_distribution"]}
        top_three = dist_map["Thiruvananthapuram"] + dist_map["Kannur"] + dist_map["Ernakulam"]
        self.assertAlmostEqual(top_three, 41.61, delta=0.2)

    def test_evidence_completeness_matrix(self):
        """T041: Verify evidence completeness tiers and data-gap classifications."""
        matrix = self.data.get("evidence_completeness_matrix", {})
        self.assertEqual(matrix.get("total_portfolio_projects"), 1240)
        metrics = matrix.get("metrics_tracked", [])
        self.assertGreaterEqual(len(metrics), 6)
        
        # Operational and Ex-post outcome must be marked as data_gap
        gap_metrics = [m for m in metrics if m["status"] == "data_gap"]
        self.assertGreaterEqual(len(gap_metrics), 2)
        metric_names = [m["metric_name"] for m in gap_metrics]
        self.assertIn("Active Operational Service Status", metric_names)
        self.assertIn("Ex-Post Social & Economic Outcome Metrics", metric_names)

    def test_departmental_distribution(self):
        """T042: Verify departmental distribution totals match Table 4.4."""
        depts = self.data.get("department_distribution", [])
        self.assertGreater(len(depts), 20)
        pwd = next(d for d in depts if "Public Works" in d["department"])
        self.assertAlmostEqual(pwd["approved_share_pct"], 52.59, delta=0.1)
        self.assertEqual(pwd["projects_count"], 535)

    def test_portfolio_data_gaps(self):
        """T041: Verify portfolio data gaps are explicitly itemized."""
        gaps = self.data.get("portfolio_data_gaps", [])
        self.assertGreaterEqual(len(gaps), 4)
        gap_ids = [g["gap_id"] for g in gaps]
        self.assertIn("GAP-001", gap_ids)
        self.assertIn("GAP-002", gap_ids)


if __name__ == "__main__":
    unittest.main()
