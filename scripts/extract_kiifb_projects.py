import re
import json
import hashlib
import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fetch_common as fc  # T081: input resolution (cli > env > newest crawl > pinned)

def clean_text(html_text):
    text = re.sub(r'<[^>]+>', '', html_text)
    text = text.replace('&nbsp;', ' ').replace('&#39;', "'").replace('&amp;', '&')
    return re.sub(r'\s+', ' ', text).strip()

def normalize_status(source_status, approved_inr, released_inr):
    """
    Applies strict normalisation rules from architecture.md and design-system.md.
    Never equates approved with complete or operational.
    """
    approved = float(approved_inr) if approved_inr else 0.0
    released = float(released_inr) if released_inr else 0.0

    if source_status == "Project Under Evaluation":
        return "approved", "Source status is Under Evaluation; registered proposal awaiting final execution."
    
    if released == 0.0:
        return "approved", "Approved on paper; zero financial disbursements recorded in official portal."
    elif released > 0 and released < approved:
        return "in_progress", "Active disbursement recorded (financial release is non-zero but below approved outlay)."
    elif released >= approved and approved > 0:
        # Note: Even if 100% funds released, without a formal handover/completion certificate, 
        # design-system dictates it cannot be assumed 'operational' or 'handed_over'.
        return "physically_complete", "Full financial outlay released according to official records; physical execution/handover certificate pending verification."
    else:
        return "approved", "Default approval baseline."

def parse_kiifb_portal(input_path: str | None = None):
    resolved, origin = fc.resolve_input(
        input_path, "KIIFB_PROJECTS_HTML", "kiifb", "project-status",
        "kiifb-prjStatus.html", "data/raw/kiifb/kiifb-prjStatus.html")
    print(f"[input] DS010 -> {resolved} ({origin})")
    with open(resolved, encoding='utf-8', errors='ignore') as f:
        html = f.read()

    table_match = re.search(r'<table id=\"tblProjects\"[^>]*>(.*?)</table>', html, re.DOTALL)
    if not table_match:
        raise ValueError("tblProjects table not found in kiifb-prjStatus.html")

    table = table_match.group(1)
    # Match all <tr> rows
    rows = re.findall(r'<tr(?:\s+onclick=\"selectProject\(\'([^\']+)\'\)\"[^>]*)?>(.*?)</tr>', table, re.DOTALL)
    
    projects = []
    project_idx = 1
    for pid, row_html in rows:
        tds = [clean_text(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)]
        if len(tds) >= 6:
            dept = tds[0]
            name = tds[1]
            spv = tds[2]
            app_inr_str = tds[3].replace(',', '')
            rel_inr_str = tds[4].replace(',', '')
            src_status = tds[5]
            
            try:
                approved_inr = float(app_inr_str)
            except ValueError:
                approved_inr = 0.0
                
            try:
                released_inr = float(rel_inr_str)
            except ValueError:
                released_inr = 0.0

            approved_cr = round(approved_inr / 10000000.0, 2)
            released_cr = round(released_inr / 10000000.0, 2)

            norm_status, rule = normalize_status(src_status, approved_inr, released_inr)

            # Determine sector based on department
            sector = "Infrastructure & Public Works"
            if "Education" in dept:
                sector = "General & Higher Education"
            elif "Health" in dept:
                sector = "Health & Family Welfare"
            elif "Water" in dept:
                sector = "Water Resources"
            elif "Power" in dept:
                sector = "Power & Energy"
            elif "Information Technology" in dept or "IT" in dept:
                sector = "IT & Digital Infrastructure"
            elif "Transport" in dept:
                sector = "Transport & Mobility"
            elif "SC" in dept or "ST" in dept or "Scheduled" in dept:
                sector = "Social Justice / SC & ST"
            elif "Forest" in dept:
                sector = "Forest & Wildlife"
            elif "Industr" in dept:
                sector = "Industrial Infrastructure"

            # Stable internal project ID
            proj_id = f"KIIFB-PRJ-{project_idx:04d}"
            project_idx += 1

            projects.append({
                "project_id": proj_id,
                "official_app_id": pid if pid else None,
                "project_name": name,
                "normalised_name": name.title() if name.isupper() else name,
                "sector": sector,
                "implementing_department": dept,
                "spv": spv,
                "financials": {
                    "approved_inr": approved_inr,
                    "approved_crore": approved_cr,
                    "released_inr": released_inr,
                    "released_crore": released_cr,
                    "release_ratio_pct": round((released_inr / approved_inr * 100.0), 1) if approved_inr > 0 else 0.0,
                    "currency": "INR",
                    "unit": "Crore"
                },
                "status": {
                    "source_status_text": src_status,
                    "normalised_status": norm_status,
                    "normalisation_rule": rule,
                    "as_of_date": "2026-10"
                },
                "source_id": "DS010",
                "source_locator": f"KIIFB prjStatus.jsp (appId: {pid})" if pid else "KIIFB prjStatus.jsp"
            })

    output_data = {
        "version": "1.0.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "DS010 (KIIFB Official Project Status Database)",
        "total_records": len(projects),
        "projects": projects
    }

    with open('data/processed/kiifb_projects.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)

    print(f"Generated data/processed/kiifb_projects.json with {len(projects)} records.")

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Extract DS010 KIIFB project register.")
    ap.add_argument('--input', default=None,
                    help='path to a kiifb-prjStatus.html crawl snapshot '
                         '(default: newest live-crawl snapshot, else pinned baseline)')
    args = ap.parse_args()
    parse_kiifb_portal(args.input)
