import re
import json
from datetime import datetime, timezone

def extract_financial_tables():
    with open('data/KIIFB Findings Report.md', 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Table 3.1 Contribution from GoK
    # 2016-17 to 2026-27 (up to June 30, 2026)
    table_3_1 = {
        "table_id": "Table 3.1",
        "title": "Contribution from the Government of Keralam",
        "locator": "Chapter III, Page 16",
        "unit": "Crore",
        "currency": "INR",
        "rows": [
            {"year": "2016-17", "mvt_share": 366.19, "petroleum_cess": 113.62, "total": 479.81},
            {"year": "2017-18", "mvt_share": 757.24, "petroleum_cess": 242.75, "total": 999.99},
            {"year": "2018-19", "mvt_share": 907.39, "petroleum_cess": 269.41, "total": 1176.80},
            {"year": "2019-20", "mvt_share": 1137.99, "petroleum_cess": 269.11, "total": 1407.10},
            {"year": "2020-21", "mvt_share": 1587.35, "petroleum_cess": 453.64, "total": 2040.99},
            {"year": "2021-22", "mvt_share": 1904.30, "petroleum_cess": 485.84, "total": 2390.14},
            {"year": "2022-23", "mvt_share": 1969.69, "petroleum_cess": 500.00, "total": 2469.69},
            {"year": "2023-24", "mvt_share": 2698.81, "petroleum_cess": 531.45, "total": 3230.26},
            {"year": "2024-25", "mvt_share": 3131.06, "petroleum_cess": 564.12, "total": 3695.18},
            {"year": "2025-26", "mvt_share": 5262.19, "petroleum_cess": 892.49, "total": 6154.68},
            {"year": "2026-27", "mvt_share": 600.00, "petroleum_cess": 120.00, "total": 720.00}
        ],
        "total": {"mvt_share": 20322.21, "petroleum_cess": 4442.43, "total_transferred": 24764.64},
        "notes": "Figures for 2026-27 are up to June 30, 2026. Source: Department of Finance, GoK."
    }

    # 2. Table 3.2 State transfers vs debt service
    table_3_2 = {
        "table_id": "Table 3.2",
        "title": "State transfers compared with KIIFB’s debt service",
        "locator": "Chapter III, Page 17",
        "unit": "Crore",
        "currency": "INR",
        "rows": [
            {"year": "2021-22", "principal_repaid": 307.42, "interest_paid": 739.66, "total_debt_service": 1047.08, "transfers_from_gok": 2390.14},
            {"year": "2022-23", "principal_repaid": 432.74, "interest_paid": 1254.56, "total_debt_service": 1687.30, "transfers_from_gok": 2469.69},
            {"year": "2023-24", "principal_repaid": 3505.02, "interest_paid": 1639.64, "total_debt_service": 5144.66, "transfers_from_gok": 3314.27},
            {"year": "2024-25", "principal_repaid": 2241.67, "interest_paid": 1823.47, "total_debt_service": 4065.14, "transfers_from_gok": 3695.18}
        ],
        "total": {
            "principal_repaid": 6486.85,
            "interest_paid": 5457.33,
            "total_debt_service": 11944.18,
            "transfers_from_gok": 11869.28,
            "servicing_ratio_pct": 99.37
        },
        "notes": "GoK transfers in 2023-24 include Rs 84.01 Cr from KINFRA to KIIFB. Source: CAG Report on State Finances for 2024-25."
    }

    # 3. Table 3.3 Aggregate borrowing position as on 30 June 2026
    table_3_3 = {
        "table_id": "Table 3.3",
        "title": "Aggregate borrowing position as on 30th June 2026",
        "locator": "Chapter III, Page 18",
        "unit": "Crore",
        "currency": "INR",
        "particulars": [
            {"label": "Total sanctioned for borrowing", "amount_crore": 48559.69},
            {"label": "Total availed", "amount_crore": 42193.45},
            {"label": "Sanctioned but undrawn", "amount_crore": 6366.24},
            {"label": "Repaid", "amount_crore": 10512.30},
            {"label": "Outstanding as on 30 June 2026", "amount_crore": 31681.15}
        ],
        "notes": "Source: Details furnished by KIIFB."
    }

    # 4. Table 3.4 Loans from commercial banks as on 30 June 2026
    table_3_4 = {
        "table_id": "Table 3.4",
        "title": "Loans taken from banks (as on June 30, 2026)",
        "locator": "Chapter III, Page 19",
        "unit": "Crore",
        "currency": "INR",
        "rows": [
            {"bank_name": "State Bank of India", "amount_raised": 1000.00, "outstanding": 343.57},
            {"bank_name": "Union Bank of India", "amount_raised": 750.00, "outstanding": 303.12},
            {"bank_name": "Indian Bank", "amount_raised": 1000.00, "outstanding": 575.80},
            {"bank_name": "Canara Bank", "amount_raised": 950.00, "outstanding": 730.00},
            {"bank_name": "Bank of Maharashtra", "amount_raised": 1000.00, "outstanding": 724.99},
            {"bank_name": "Bank of Baroda", "amount_raised": 2000.00, "outstanding": 1289.06},
            {"bank_name": "Bank of India", "amount_raised": 700.00, "outstanding": 525.00},
            {"bank_name": "ICICI Bank", "amount_raised": 200.00, "outstanding": 50.00},
            {"bank_name": "Kotak Mahindra Bank", "amount_raised": 100.00, "outstanding": 41.67},
            {"bank_name": "Indian Overseas Bank", "amount_raised": 1500.00, "outstanding": 1500.00}
        ],
        "total": {"amount_raised": 9200.00, "outstanding": 6083.22},
        "notes": "Source: Details furnished by KIIFB."
    }

    # 5. Table 3.5 Borrowing from financial institutions as on 30 June 2026
    table_3_5 = {
        "table_id": "Table 3.5",
        "title": "Borrowing from financial institutions (as on June 30, 2026)",
        "locator": "Chapter III, Page 19",
        "unit": "Crore",
        "currency": "INR",
        "rows": [
            {"institution": "NABARD", "sanctioned": 9694.70, "availed": 7123.70, "outstanding": 6545.32},
            {"institution": "REC Ltd", "sanctioned": 5389.23, "availed": 4746.32, "outstanding": 2704.02},
            {"institution": "Kerala Financial Corporation", "sanctioned": 2000.00, "availed": 2000.00, "outstanding": 903.37},
            {"institution": "Power Finance Corporation", "sanctioned": 991.33, "availed": 870.72, "outstanding": 870.72},
            {"institution": "HUDCO", "sanctioned": 4836.00, "availed": 3880.00, "outstanding": 3357.12},
            {"institution": "Sagarmala Finance Corporation", "sanctioned": 2975.71, "availed": 1000.00, "outstanding": 1000.00}
        ],
        "total": {"sanctioned": 25886.97, "availed": 19620.74, "outstanding": 15380.55},
        "notes": "Source: Details furnished by KIIFB."
    }

    # 6. Table 3.7 BSE-listed bonds issued
    table_3_7 = {
        "table_id": "Table 3.7",
        "title": "BSE-listed bonds issued",
        "locator": "Chapter III, Page 21",
        "unit": "Crore",
        "currency": "INR",
        "rows": [
            {"series": "Green Bonds", "coupon_rate": "8.49%", "amount": 300.02, "year_of_issue": "2023-24"},
            {"series": "Series 1", "coupon_rate": "8.95%", "amount": 1499.96, "year_of_issue": "2023-24"},
            {"series": "Series 2", "coupon_rate": "9.10%", "amount": 849.94, "year_of_issue": "2024-25"},
            {"series": "Series 3", "coupon_rate": "9.49%", "amount": 1000.02, "year_of_issue": "2024-25"},
            {"series": "Series 4", "coupon_rate": "9.42%", "amount": 1500.03, "year_of_issue": "2024-25"},
            {"series": "Series 5", "coupon_rate": "9.49%", "amount": 499.94, "year_of_issue": "2025-26"},
            {"series": "Series 6", "coupon_rate": "9.67%", "amount": 1500.03, "year_of_issue": "2025-26"},
            {"series": "Series 7", "coupon_rate": "9.30%", "amount": 1500.03, "year_of_issue": "2025-26"}
        ],
        "total": {"amount": 8649.97},
        "notes": "Source: Details furnished by KIIFB."
    }

    # 7. Table 3.11 Deduction from State borrowing space
    table_3_11 = {
        "table_id": "Table 3.11",
        "title": "Deduction from the State’s borrowing space on account of KIIFB’s borrowing",
        "locator": "Chapter III, Page 32",
        "unit": "Crore",
        "currency": "INR",
        "rows": [
            {"year": "2022-23", "amount_deducted": 1940.70},
            {"year": "2023-24", "amount_deducted": 5835.16},
            {"year": "2024-25", "amount_deducted": 2911.05},
            {"year": "2025-26", "amount_deducted": 7155.72},
            {"year": "2026-27", "amount_deducted": 8089.92}
        ],
        "total": {"amount_deducted": 25932.55},
        "notes": "Source: Department of Finance, Government of Keralam."
    }

    # 8. Table 4.5 Land acquisition pool
    table_4_5 = {
        "table_id": "Table 4.5",
        "title": "List of Land Acquisition Projects",
        "locator": "Chapter IV, Page 59",
        "unit": "Crore",
        "currency": "INR",
        "as_of_date": "2026-09-15",
        "rows": [
            {"project_name": "Bio 360 Life Science Park - Phase II Land Acquisition-Trivandrum", "spv": "KSIDC", "outlay": 301.17, "amount_paid": 301.17, "balance": 0.00, "repaid": 84.02},
            {"project_name": "Setting up of Petrochemical & Pharma Park", "spv": "KINFRA", "outlay": 977.46, "amount_paid": 977.46, "balance": 0.00, "repaid": 554.65},
            {"project_name": "Development of Global CITY as part of KBIC-Land Acquisition", "spv": "KINFRA", "outlay": 840.00, "amount_paid": 840.00, "balance": 0.00, "repaid": 0.00},
            {"project_name": "Development of Industrial Park by takeover of land From M/S Hindustan Newsprint Ltd", "spv": "KINFRA", "outlay": 200.60, "amount_paid": 145.60, "balance": 55.00, "repaid": 0.00},
            {"project_name": "Kochi-Bengaluru Industrial Corridor Project-Land Acquisition", "spv": "KINFRA", "outlay": 1374.00, "amount_paid": 1068.28, "balance": 305.72, "repaid": 337.04},
            {"project_name": "Development of Industrial infrastructure - Land Acquisition (Kannur/Palakkad)", "spv": "KINFRA", "outlay": 12727.50, "amount_paid": 2489.12, "balance": 10238.38, "repaid": 425.36},
            {"project_name": "National Highway Land Acquisition", "spv": "PWD", "outlay": 6769.01, "amount_paid": 5580.74, "balance": 1188.27, "repaid": 0.00}
        ],
        "total": {"outlay": 23189.74, "amount_paid": 11402.37, "balance": 11787.37, "repaid": 1386.64},
        "notes": "Source: Compiled by KIIFB as on 15 September 2026."
    }

    # 9. Table 6.1 Debt Servicing Schedule up to 2041-42
    table_6_1 = {
        "table_id": "Table 6.1",
        "title": "KIIFB’s Debt Servicing Schedule upto 2041-42",
        "locator": "Chapter VI, Pages 91-92",
        "unit": "Crore",
        "currency": "INR",
        "rows": [
            {"year": "2026-27", "principal": 3009.82, "interest": 2816.68, "total": 5826.50},
            {"year": "2027-28", "principal": 3502.91, "interest": 2548.57, "total": 6051.48},
            {"year": "2028-29", "principal": 4161.92, "interest": 2224.47, "total": 6386.39},
            {"year": "2029-30", "principal": 3651.88, "interest": 1843.89, "total": 5495.77},
            {"year": "2030-31", "principal": 3159.13, "interest": 1526.98, "total": 4686.11},
            {"year": "2031-32", "principal": 2820.81, "interest": 1245.46, "total": 4066.27},
            {"year": "2032-33", "principal": 2702.55, "interest": 993.90, "total": 3696.45},
            {"year": "2033-34", "principal": 2505.72, "interest": 753.65, "total": 3259.37},
            {"year": "2034-35", "principal": 1964.30, "interest": 543.23, "total": 2507.53},
            {"year": "2035-36", "principal": 1383.02, "interest": 385.99, "total": 1769.01},
            {"year": "2036-37", "principal": 908.96, "interest": 280.85, "total": 1189.81},
            {"year": "2037-38", "principal": 825.62, "interest": 205.13, "total": 1030.75},
            {"year": "2038-39", "principal": 644.38, "interest": 136.90, "total": 781.28},
            {"year": "2039-40", "principal": 434.28, "interest": 85.18, "total": 519.46},
            {"year": "2040-41", "principal": 167.39, "interest": 49.56, "total": 216.95},
            {"year": "2041-42", "principal": 14.51, "interest": 34.90, "total": 49.41}
        ],
        "total": {"principal": 31857.20, "interest": 15675.34, "total_debt_service": 47532.54},
        "notes": "Repayment runs to 2041-42. Excludes Pravasi Dividend Scheme liability (Rs 314.13 Cr outstanding). Source: Furnished by KIIFB."
    }

    # 10. Table 6.2 & 6.3 Future Project Completion Requirements
    table_6_2_and_3 = {
        "table_id": "Table 6.2 & 6.3",
        "title": "Funds Required to Complete Started & Prioritised Works",
        "locator": "Chapter VI, Page 92",
        "unit": "Crore",
        "currency": "INR",
        "categories": [
            {"category": "Amount required for completing started projects", "amount_crore": 14737.0},
            {"category": "Balance payments required for completed projects", "amount_crore": 1400.0},
            {"category": "Works tendered but agreement not executed (priority only)", "amount_crore": 4151.0},
            {"category": "Works ready for tendering (priority only)", "amount_crore": 2595.0}
        ],
        "total_required_crore": 22883.0,
        "phasing": [
            {"year": "2026-27", "amount_required": 2588.0},
            {"year": "2027-28", "amount_required": 5000.0},
            {"year": "2028-29", "amount_required": 5200.0},
            {"year": "2029-30", "amount_required": 5400.0},
            {"year": "2030-31", "amount_required": 4695.0}
        ],
        "grand_future_fiscal_requirement": {
            "debt_servicing_crore": 47532.54,
            "project_completion_crore": 22883.0,
            "total_fiscal_requirement_crore": 70415.54,
            "excludes_land_acquisition": True,
            "unpaid_land_balance_crore": 11787.37
        },
        "notes": "Source: Furnished by KIIFB. Excludes land acquisition pool."
    }

    financial_tables = {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "DS001 / DS001-LOCAL (Report of the Committee on Comprehensive Review of KIIFB, Oct 2026)",
        "tables": {
            "table_3_1_transfers": table_3_1,
            "table_3_2_servicing_ratio": table_3_2,
            "table_3_3_aggregate_borrowing": table_3_3,
            "table_3_4_bank_loans": table_3_4,
            "table_3_5_institution_loans": table_3_5,
            "table_3_7_bse_bonds": table_3_7,
            "table_3_11_space_deduction": table_3_11,
            "table_4_5_land_acquisition": table_4_5,
            "table_6_1_debt_servicing_schedule": table_6_1,
            "table_6_2_and_3_completion_requirements": table_6_2_and_3
        }
    }

    with open('data/processed/committee_financial_tables.json', 'w', encoding='utf-8') as f:
        json.dump(financial_tables, f, indent=2)

    print("Successfully generated data/processed/committee_financial_tables.json with 10 core tables.")

if __name__ == '__main__':
    extract_financial_tables()
