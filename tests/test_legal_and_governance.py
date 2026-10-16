"""Unit tests for Milestone 5 legal issues register, committee recommendations, and methodology data.

Validates that:
1. Legal issues clearly distinguish administrative/advisory interpretation from binding court rulings.
2. Court citations (Supreme Court Original Suit 1 of 2024, High Court of Kerala) are explicit.
3. Recommendation tracker items are not represented as implemented without evidence.
4. Methodology metadata and discrepancy records are complete and reproducible.
"""

import json
from pathlib import Path
import unittest

DATA_DIR = Path(__file__).parent.parent / "data" / "processed"


class TestLegalAndGovernance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        legal_path = DATA_DIR / "legal_issues_register.json"
        with open(legal_path, "r", encoding="utf-8") as f:
            cls.legal_data = json.load(f)
        recs_path = DATA_DIR / "committee_recommendations.json"
        with open(recs_path, "r", encoding="utf-8") as f:
            cls.recs_data = json.load(f)

    def test_legal_issues_present(self):
        """T050: Verify legal issues exist with required fields."""
        issues = self.legal_data.get("issues", [])
        self.assertGreaterEqual(len(issues), 4)
        issue_ids = [i["issue_id"] for i in issues]
        self.assertIn("LEG-001", issue_ids)
        self.assertIn("LEG-002", issue_ids)
        self.assertIn("LEG-003", issue_ids)
        self.assertIn("LEG-004", issue_ids)

    def test_committee_vs_court_distinction(self):
        """T050: Verify committee interpretation is separated from binding court findings."""
        for issue in self.legal_data.get("issues", []):
            self.assertIn("committee_interpretation", issue)
            self.assertIn("judicial_proceedings", issue)
            jp = issue["judicial_proceedings"]
            self.assertIn("binding_status", jp)
            self.assertIn("committee_vs_court_distinction", jp)
            self.assertTrue(len(jp["committee_vs_court_distinction"]) > 20)

    def test_supreme_court_citation_on_article_293(self):
        """T050: Verify Supreme Court Article 131 suit is recorded for Article 293."""
        issue_293 = next(i for i in self.legal_data["issues"] if i["issue_id"] == "LEG-001")
        jp = issue_293["judicial_proceedings"]
        self.assertEqual(jp["forum"], "Supreme Court of India")
        self.assertIn("Original Suit No. 1 of 2024", jp["case_citation"])
        self.assertIn("Constitution Bench", jp["binding_status"])

    def test_masala_bonds_redemption_and_high_court(self):
        """T050: Verify Masala bond redemption and Kerala High Court proceedings."""
        masala_issue = next(i for i in self.legal_data["issues"] if i["issue_id"] == "LEG-003")
        jp = masala_issue["judicial_proceedings"]
        self.assertEqual(jp["forum"], "High Court of Kerala")
        self.assertIn("27 March 2024", jp["binding_status"])

    def test_recommendations_count_and_fields(self):
        """T051: Verify all 8 recommendations are tracked with required fields."""
        recs = self.recs_data.get("recommendations", [])
        self.assertEqual(len(recs), 8)
        rec_ids = [r["rec_id"] for r in recs]
        for i in range(1, 9):
            self.assertIn(f"REC-00{i}", rec_ids)

    def test_recommendations_not_falsely_implemented(self):
        """T051: Acceptance - recommendations are not represented as implemented without evidence."""
        recs = self.recs_data.get("recommendations", [])
        for rec in recs:
            # None should be marked as "implemented" or "completed" without evidence
            self.assertNotEqual(rec["implementation_status"], "implemented")
            self.assertNotEqual(rec["implementation_status"], "completed")
            self.assertTrue(len(rec["required_instrument"]) > 10)
            self.assertTrue(len(rec["official_evidence"]) > 15)

    def test_methodology_and_discrepancies(self):
        """T052: Acceptance - source dates, calculations, matching rules and limitations are reproducible."""
        meth_path = DATA_DIR / "methodology_and_quality.json"
        with open(meth_path, "r", encoding="utf-8") as f:
            meth_data = json.load(f)

        # Sources
        sources = meth_data.get("sources", [])
        self.assertGreaterEqual(len(sources), 3)
        source_ids = [s["source_id"] for s in sources]
        self.assertIn("DS001", source_ids)
        self.assertIn("DS010", source_ids)
        self.assertIn("DS021", source_ids)

        # Discrepancies
        discrepancies = meth_data.get("discrepancies", [])
        self.assertGreaterEqual(len(discrepancies), 5)
        disc_ids = [d["discrepancy_id"] for d in discrepancies]
        self.assertIn("DISC-001", disc_ids) # 0.01 Cr bank rounding
        self.assertIn("DISC-002", disc_ids) # 14.43 Cr land acquisition gap
        self.assertIn("DISC-003", disc_ids) # 1408 missing portal districts
        self.assertIn("DISC-004", disc_ids) # SC/ST statutory allocation deficit

        # Limitations
        limitations = meth_data.get("limitations", [])
        self.assertGreaterEqual(len(limitations), 4)


if __name__ == "__main__":
    unittest.main()
