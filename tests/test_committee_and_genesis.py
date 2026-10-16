"""
Unit tests for Committee Scrutiny, KIIFB Genesis, and Opposing Pillars & Federalism datasets.
Validates structural schema, member records, documented conflicts of interest,
financial reconciliation, and federalism metrics.
"""

import json
import os
import unittest


class TestCommitteeScrutiny(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.scrutiny_path = os.path.join(cls.base_dir, 'data', 'processed', 'committee_scrutiny.json')
        cls.genesis_path = os.path.join(cls.base_dir, 'data', 'processed', 'kiifb_genesis.json')
        cls.pillars_path = os.path.join(cls.base_dir, 'data', 'processed', 'opposing_pillars_and_federalism.json')
        cls.tables_path = os.path.join(cls.base_dir, 'data', 'processed', 'committee_financial_tables.json')

        with open(cls.scrutiny_path, 'r', encoding='utf-8') as f:
            cls.scrutiny = json.load(f)

        with open(cls.genesis_path, 'r', encoding='utf-8') as f:
            cls.genesis = json.load(f)

        with open(cls.pillars_path, 'r', encoding='utf-8') as f:
            cls.pillars = json.load(f)

        with open(cls.tables_path, 'r', encoding='utf-8') as f:
            cls.tables = json.load(f)

    def test_committee_legal_constitution(self):
        """Verify the legal standing and executive order of the review committee."""
        legal = self.scrutiny.get('legal_constitution', {})
        self.assertEqual(legal.get('constituting_order'), 'G.O.(P) No.80/2026/FIN')
        self.assertEqual(legal.get('order_date'), '2026-07-13')
        self.assertEqual(legal.get('legal_status'), 'Executive Advisory Committee')
        self.assertFalse(legal.get('subpoena_powers'))
        self.assertFalse(legal.get('evidentiary_protection'))
        self.assertIn('Commissions of Inquiry Act, 1952', legal.get('statutory_inquiry_status', ''))
        self.assertIn('jurisdictional_paradox', legal)

    def test_procedural_and_positional_lapses(self):
        """Verify that all four critical procedural lapses are documented."""
        lapses = self.scrutiny.get('procedural_and_positional_lapses', [])
        self.assertGreaterEqual(len(lapses), 4)

        lapse_ids = [l['lapse_id'] for l in lapses]
        self.assertIn('LAPSE-001', lapse_ids)  # ToR framing bias
        self.assertIn('LAPSE-002', lapse_ids)  # Sub judice intrusion
        self.assertIn('LAPSE-003', lapse_ids)  # Panel conflict of interest
        self.assertIn('LAPSE-004', lapse_ids)  # Assembly tabling bypass

    def test_committee_member_dossiers_and_conflicts(self):
        """Verify the dossiers and explicit conflicts of interest for all 5 members."""
        members = self.scrutiny.get('members', [])
        self.assertEqual(len(members), 5)

        member_names = [m['name'] for m in members]
        self.assertIn('Sudha Pillai', member_names)
        self.assertIn('Tarun Bajaj', member_names)
        self.assertIn('Shyam Srinivasan', member_names)
        self.assertIn('Nilesh Vikamsey', member_names)
        self.assertIn('H. Shubhalakshmi Narayanan', member_names)

        # 1. Tarun Bajaj conflict verification (Union MoF & Article 293 deductions)
        bajaj = next(m for m in members if m['name'] == 'Tarun Bajaj')
        self.assertIn('Revenue Secretary', bajaj['career_background'])
        self.assertIn('Department of Economic Affairs', bajaj['career_background'])
        self.assertIn('Article 293(3)', bajaj['documented_conflict'])
        self.assertIn('25,932.55', bajaj['documented_conflict'])

        # 2. Shyam Srinivasan conflict verification (Federal Bank KIFML equity holding)
        srinivasan = next(m for m in members if m['name'] == 'Shyam Srinivasan')
        self.assertIn('Federal Bank', srinivasan['career_background'])
        self.assertIn('Federal Bank', srinivasan['documented_conflict'])
        self.assertIn('KIFML', srinivasan['documented_conflict'])
        self.assertIn('5.61%', srinivasan['documented_conflict'])

        # 3. Nilesh Vikamsey verification (Past ICAI President)
        vikamsey = next(m for m in members if m['name'] == 'Nilesh Vikamsey')
        self.assertIn('ICAI', vikamsey['career_background'])

    def test_advisory_apparatus_chandrasekhar_connection(self):
        """Verify that the advisory role of K.M. Chandrasekhar (2014 author) is documented."""
        advisors = self.scrutiny.get('advisory_apparatus', {}).get('key_advisors', [])
        advisor_names = [a['name'] for a in advisors]
        self.assertIn('K.M. Chandrasekhar', advisor_names)
        self.assertIn('Prof. D. Narayana', advisor_names)
        self.assertIn('Prof. M. Parameswaran', advisor_names)

        kmc = next(a for a in advisors if a['name'] == 'K.M. Chandrasekhar')
        self.assertIn('2014', kmc['background'])
        self.assertIn('SBI Caps', kmc['background'])


class TestKIIFBGenesis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.genesis_path = os.path.join(cls.base_dir, 'data', 'processed', 'kiifb_genesis.json')

        with open(cls.genesis_path, 'r', encoding='utf-8') as f:
            cls.genesis = json.load(f)

    def test_statutory_evolution_phases(self):
        """Verify the 3 phases of statutory evolution."""
        phases = self.genesis.get('statutory_evolution', [])
        self.assertEqual(len(phases), 3)

        phase_ids = [p['phase_id'] for p in phases]
        self.assertEqual(phase_ids, ['EVO-001', 'EVO-002', 'EVO-003'])

        # 1999 Act
        p1 = phases[0]
        self.assertIn('Act 4 of 2000', p1['governing_instrument'])

        # 2014 SBI Caps Note
        p2 = phases[1]
        self.assertIn('2014', p2['period'])
        self.assertIn('SBI Caps', p2['phase_name'])

        # 2016 Act 8 Overhaul
        p3 = phases[2]
        self.assertIn('Kerala Act 8 of 2016', p3['governing_instrument'])
        self.assertIn('Social Infrastructure', p3['intent'])

    def test_key_architects(self):
        """Verify the key people involved in KIIFB's formation."""
        architects = self.genesis.get('key_architects', [])
        names = [a['name'] for a in architects]
        self.assertIn('Dr. T.M. Thomas Isaac', names)
        self.assertIn('Dr. K.M. Abraham', names)
        self.assertIn('Pinarayi Vijayan', names)

        isaac = next(a for a in architects if a['name'] == 'Dr. T.M. Thomas Isaac')
        self.assertIn('Keynesian', isaac['contribution_to_kiifb'])

        abraham = next(a for a in architects if a['name'] == 'Dr. K.M. Abraham')
        self.assertIn('SEBI', abraham['contribution_to_kiifb'])
        self.assertIn('TRC', abraham['contribution_to_kiifb'])

    def test_fiduciary_commission_ftac(self):
        """Verify the statutory Fund Trustee and Advisory Commission (FTAC)."""
        ftac = self.genesis.get('fiduciary_trust_commission', {})
        self.assertIn('Section 6D', ftac.get('statutory_mandate', ''))

        trustees = ftac.get('distinguished_trustees', [])
        trustee_names = [t['name'] for t in trustees]
        self.assertIn('Vinod Rai', trustee_names)
        self.assertIn('Usha Thorat', trustee_names)
        self.assertIn('Radhakrishnan Nair', trustee_names)

        vr = next(t for t in trustees if t['name'] == 'Vinod Rai')
        self.assertIn('Comptroller and Auditor General', vr['background'])

        ut = next(t for t in trustees if t['name'] == 'Usha Thorat')
        self.assertIn('Reserve Bank of India', ut['background'])

    def test_theoretical_premise_and_rationale(self):
        """Verify the theoretical and economic principles underpinning KIIFB."""
        premise = self.genesis.get('theoretical_premise', {})
        self.assertIn('Kerala Model', premise.get('core_economic_challenge', {}).get('name', ''))
        self.assertIn('Committed Expenditure', premise.get('fiscal_trap', {}).get('name', ''))

        principles = premise.get('economic_rationale', {}).get('principles', [])
        p_names = [p['principle_name'] for p in principles]
        self.assertIn('Rejection of Neoliberal Austerity', p_names)
        self.assertIn('The High Capital Multiplier (k > 1.5 - 2.0)', p_names)
        self.assertIn('Inter-Generational Equity in Debt Financing', p_names)
        self.assertIn('Statutory Revenue Hypothecation (Section 7)', p_names)
        self.assertIn('Public Value & ERR vs Commercial FIRR', p_names)


class TestOpposingPillarsAndFederalism(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.pillars_path = os.path.join(cls.base_dir, 'data', 'processed', 'opposing_pillars_and_federalism.json')

        with open(cls.pillars_path, 'r', encoding='utf-8') as f:
            cls.pillars = json.load(f)

    def test_opposing_pillars_matrix(self):
        """Verify the 7 core dimensions contrasting Fiscal Orthodoxy with Keynesian Developmentalism."""
        matrix = self.pillars.get('opposing_pillars_matrix', [])
        self.assertEqual(len(matrix), 7)

        dimensions = [row['dimension'] for row in matrix]
        self.assertIn('Core Economic Ideology', dimensions)
        self.assertIn('Role of the State & Public Finance', dimensions)
        self.assertIn('Philosophy of Public Debt', dimensions)
        self.assertIn('Scope & Classification of Infrastructure', dimensions)
        self.assertIn('Debt Servicing & Repayment Mechanism', dimensions)
        self.assertIn('Governance & Institutional Execution', dimensions)
        self.assertIn('Constitutional Federal Posture', dimensions)

    def test_article_293_deductions_reconciliation(self):
        """Verify that the Article 293(3) deduction arithmetic reconciles exactly to ₹25,932.55 Cr."""
        fed = self.pillars.get('federalism_context', {})
        a293 = fed.get('article_293_weaponisation', {})

        yearly = a293.get('yearly_deductions_in_crores', [])
        self.assertEqual(len(yearly), 5)

        total_sum = sum(y['deduction_amount'] for y in yearly)
        self.assertAlmostEqual(total_sum, 25932.55, places=2)
        self.assertEqual(a293.get('total_deduction_crore'), 25932.55)

    def test_union_double_standard_and_entities(self):
        """Verify documented off-budget borrowings by the Union Government."""
        fed = self.pillars.get('federalism_context', {})
        entities = fed.get('union_double_standard', {}).get('central_off_budget_entities', [])

        entity_names = [e['entity'] for e in entities]
        self.assertTrue(any('NHAI' in name for name in entity_names))
        self.assertTrue(any('Food Corporation of India' in name for name in entity_names))
        self.assertTrue(any('IRFC' in name for name in entity_names))
        self.assertTrue(any('PFC' in name for name in entity_names))

    def test_supreme_court_constitution_bench_details(self):
        """Verify details of State of Kerala v. Union of India referral to 5-Judge Constitution Bench."""
        fed = self.pillars.get('federalism_context', {})
        sc = fed.get('supreme_court_constitution_bench', {})

        self.assertIn('Original Suit No. 1 of 2024', sc.get('case_details', ''))
        self.assertIn('5-Judge Constitution Bench', sc.get('adjudication_milestone', ''))
        self.assertIn('1 April 2024', sc.get('adjudication_milestone', ''))


if __name__ == '__main__':
    unittest.main()
