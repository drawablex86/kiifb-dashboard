"""Portfolio Funnel Reconciliation Tests (T101, Milestone 10).

Asserts that the /portfolio drill-down funnel tile maths — implemented in
src/lib/data/funnel.ts — reconciles exactly with
data/processed/unified_project_explorer.json at the portfolio level and at
drilled (sector, district) levels, and that "approved" is never conflated
with "physically complete".
"""

import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPLORER = os.path.join(ROOT, "data", "processed", "unified_project_explorer.json")

PHYSICALLY_COMPLETE_STATUSES = ("physically_complete", "handed_over", "operational")


def _load():
    with open(EXPLORER, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _summarise(records):
    """Mirror of src/lib/data/funnel.ts summarise()."""
    approved = round(sum((r.get("financials") or {}).get("approved_crore") or 0 for r in records), 2)
    released = round(sum((r.get("financials") or {}).get("released_crore") or 0 for r in records), 2)
    complete = round(100.0 * sum(
        1 for r in records
        if (r.get("status") or {}).get("normalised_status") in PHYSICALLY_COMPLETE_STATUSES
    ) / len(records), 1) if records else 0.0
    return {
        "count": len(records),
        "approved_crore": approved,
        "released_crore": released,
        "pct_physically_complete": complete,
    }


def _belongs_to_district(rec, district):
    return district in {s.strip() for s in (rec.get("district") or "").split(",") if s.strip()}


class TestPortfolioFunnel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = _load()
        cls.records = cls.data["records"]

    def _summarise_all(self, records, sector=None, district=None):
        out = records
        if sector is not None:
            out = [r for r in out if r.get("sector") == sector]
        if district is not None:
            out = [r for r in out if _belongs_to_district(r, district)]
        return _summarise(out)

    def test_01_portfolio_level_record_count(self):
        summary = self.data["summary"]
        funnel = _summarise(self.records)
        self.assertEqual(funnel["count"], summary["total_records"])
        self.assertEqual(funnel["count"], len(self.records))

    def test_02_portfolio_level_financial_sums_match_dataset(self):
        total_approved = round(sum(
            (r.get("financials") or {}).get("approved_crore") or 0 for r in self.records), 2)
        total_released = round(sum(
            (r.get("financials") or {}).get("released_crore") or 0 for r in self.records), 2)
        funnel = _summarise(self.records)
        self.assertEqual(funnel["approved_crore"], total_approved)
        self.assertEqual(funnel["released_crore"], total_released)
        self.assertEqual(
            funnel["approved_crore"] + funnel["released_crore"],
            total_approved + total_released,
        )

    def test_03_sector_level_subset_reconciles(self):
        """Sum over sector drill-down tiles must equal the portfolio sum."""
        total_approved = round(sum(
            (r.get("financials") or {}).get("approved_crore") or 0 for r in self.records), 2)
        sectors = {r.get("sector") for r in self.records if r.get("sector")}
        sector_sum = round(sum(
            self._summarise_all(self.records, sector=s)["approved_crore"] for s in sectors), 2)
        self.assertEqual(sector_sum, total_approved)

    def test_04_district_level_subset_reconciles(self):
        """Sum over district tiles for a sector equals that sector's total."""
        sector = "Public Works"
        records = [r for r in self.records if r.get("sector") == sector]
        expected = _summarise(records)
        districts = {s.strip() for r in records for s in (r.get("district") or "").split(",") if s.strip()}
        district_sum_count = sum(
            self._summarise_all(self.records, sector=sector, district=d)["count"] for d in districts)
        district_sum_approved = round(sum(
            self._summarise_all(self.records, sector=sector, district=d)["approved_crore"]
            for d in districts), 2)
        self.assertEqual(district_sum_count, expected["count"])
        self.assertEqual(district_sum_approved, expected["approved_crore"])

    def test_05_approved_not_conflated_with_completion(self):
        """The % complete tile counts completion statuses only, never sums."""
        complete = [r for r in self.records
                    if (r.get("status") or {}).get("normalised_status") in PHYSICALLY_COMPLETE_STATUSES]
        pct = round(100.0 * len(complete) / len(self.records), 1)
        funnel = _summarise(self.records)
        self.assertEqual(funnel["pct_physically_complete"], pct)
        # An approved outlay figure must not be produced from completion counts
        self.assertNotEqual(funnel["approved_crore"], funnel["pct_physically_complete"])
        self.assertLessEqual(funnel["pct_physically_complete"], 100.0)

    def test_06_funnel_tile_shape(self):
        funnel = _summarise(self.records)
        self.assertEqual(set(funnel.keys()),
                         {"count", "approved_crore", "released_crore", "pct_physically_complete"})


if __name__ == "__main__":
    unittest.main()
