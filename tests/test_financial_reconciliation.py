import json
import unittest

class TestFinancialReconciliation(unittest.TestCase):
    """
    Automated test suite verifying the arithmetic, internal consistency,
    stock/flow separation, and documented source discrepancies of KIIFB Committee tables.
    """
    @classmethod
    def setUpClass(cls):
        with open('data/processed/committee_financial_tables.json', 'r', encoding='utf-8') as f:
            cls.tables = json.load(f)['tables']

    def test_aggregate_borrowings_reconciliation(self):
        """
        Table 3.3:
        Sanctioned = Availed + Undrawn (48,559.69 Cr)
        Outstanding = Availed - Repaid (31,681.15 Cr)
        """
        t3 = self.tables['table_3_3_aggregate_borrowing']['particulars']
        lookup = {item['label']: item['amount_crore'] for item in t3}

        sanctioned = lookup['Total sanctioned for borrowing']
        availed = lookup['Total availed']
        undrawn = lookup['Sanctioned but undrawn']
        repaid = lookup['Repaid']
        outstanding = lookup['Outstanding as on 30 June 2026']

        self.assertEqual(round(availed + undrawn, 2), round(sanctioned, 2))
        self.assertEqual(round(sanctioned, 2), 48559.69)
        self.assertEqual(round(availed - repaid, 2), round(outstanding, 2))
        self.assertEqual(round(outstanding, 2), 31681.15)

    def test_bank_loans_sum_and_rounding_difference(self):
        """
        Table 3.4:
        Sum of raised = 9,200.00 Cr.
        Sum of individual bank outstanding = 6,083.21 Cr.
        Reported total = 6,083.22 Cr.
        Documented rounding delta = 0.01 Cr (1 Lakh).
        """
        t4 = self.tables['table_3_4_bank_loans']
        raised_sum = sum(row['amount_raised'] for row in t4['rows'])
        outstanding_sum = sum(row['outstanding'] for row in t4['rows'])

        self.assertEqual(round(raised_sum, 2), 9200.00)
        self.assertEqual(round(outstanding_sum, 2), 6083.21)
        self.assertEqual(round(t4['total']['outstanding'], 2), 6083.22)
        # Verify that discrepancy is precisely 0.01 Cr
        self.assertAlmostEqual(outstanding_sum, t4['total']['outstanding'], places=1)

    def test_institution_loans_sum(self):
        """
        Table 3.5: Sum of institutional loans matches reported totals.
        """
        t5 = self.tables['table_3_5_institution_loans']
        sanctioned_sum = sum(row['sanctioned'] for row in t5['rows'])
        availed_sum = sum(row['availed'] for row in t5['rows'])
        outstanding_sum = sum(row['outstanding'] for row in t5['rows'])

        self.assertEqual(round(sanctioned_sum, 2), 25886.97)
        self.assertEqual(round(availed_sum, 2), 19620.74)
        self.assertEqual(round(outstanding_sum, 2), 15380.55)

    def test_bse_bonds_sum(self):
        """
        Table 3.7: Sum of BSE-listed domestic bonds equals 8,649.97 Cr.
        """
        t7 = self.tables['table_3_7_bse_bonds']
        bonds_sum = sum(row['amount'] for row in t7['rows'])
        self.assertEqual(round(bonds_sum, 2), 8649.97)

    def test_space_deduction_sum(self):
        """
        Table 3.11: Sum of borrowing space deductions equals 25,932.55 Cr.
        """
        t11 = self.tables['table_3_11_space_deduction']
        deduction_sum = sum(row['amount_deducted'] for row in t11['rows'])
        self.assertEqual(round(deduction_sum, 2), 25932.55)

    def test_land_acquisition_pool_and_source_discrepancy(self):
        """
        Table 4.5:
        Outlay (23,189.74 Cr) = Paid (11,402.37 Cr) + Balance (11,787.37 Cr).
        Source Table Internal Discrepancy:
        Sum of individual project repaid amounts = 1,401.07 Cr.
        Reported table footer for Repaid = 1,386.64 Cr.
        Difference = 14.43 Cr.
        """
        t45 = self.tables['table_4_5_land_acquisition']
        outlay_sum = sum(row['outlay'] for row in t45['rows'])
        paid_sum = sum(row['amount_paid'] for row in t45['rows'])
        balance_sum = sum(row['balance'] for row in t45['rows'])
        repaid_sum = sum(row['repaid'] for row in t45['rows'])

        self.assertEqual(round(outlay_sum, 2), 23189.74)
        self.assertEqual(round(paid_sum, 2), 11402.37)
        self.assertEqual(round(balance_sum, 2), 11787.37)
        self.assertEqual(round(paid_sum + balance_sum, 2), round(outlay_sum, 2))

        # Explicitly verify the documented 14.43 Cr source discrepancy
        self.assertEqual(round(repaid_sum, 2), 1401.07)
        self.assertEqual(round(t45['total']['repaid'], 2), 1386.64)
        self.assertEqual(round(repaid_sum - t45['total']['repaid'], 2), 14.43)

    def test_debt_servicing_schedule_math(self):
        """
        Table 6.1:
        Total = Principal + Interest for each year (2026-27 to 2041-42).
        Grand Totals:
        Principal = 31,857.20 Cr
        Interest = 15,675.34 Cr
        Total Debt Service = 47,532.54 Cr
        """
        t61 = self.tables['table_6_1_debt_servicing_schedule']
        for row in t61['rows']:
            self.assertEqual(round(row['principal'] + row['interest'], 2), round(row['total'], 2),
                             f"Mismatch in year {row['year']}")

        principal_total = sum(row['principal'] for row in t61['rows'])
        interest_total = sum(row['interest'] for row in t61['rows'])
        debt_service_total = sum(row['total'] for row in t61['rows'])

        self.assertEqual(round(principal_total, 2), 31857.20)
        self.assertEqual(round(interest_total, 2), 15675.34)
        self.assertEqual(round(debt_service_total, 2), 47532.54)

    def test_future_total_fiscal_requirement(self):
        """
        Table 6.2/6.3:
        Scheduled Debt Service (47,532.54 Cr) + Project Completion (22,883.00 Cr)
        = 70,415.54 Cr.
        """
        t_req = self.tables['table_6_2_and_3_completion_requirements']
        phased_sum = sum(row['amount_required'] for row in t_req['phasing'])
        categories_sum = sum(cat['amount_crore'] for cat in t_req['categories'])

        self.assertEqual(round(phased_sum, 2), 22883.00)
        self.assertEqual(round(categories_sum, 2), 22883.00)

        debt_servicing = t_req['grand_future_fiscal_requirement']['debt_servicing_crore']
        completion = t_req['grand_future_fiscal_requirement']['project_completion_crore']
        total_req = t_req['grand_future_fiscal_requirement']['total_fiscal_requirement_crore']

        self.assertEqual(round(debt_servicing + completion, 2), 70415.54)
        self.assertEqual(round(total_req, 2), 70415.54)

if __name__ == '__main__':
    unittest.main()
