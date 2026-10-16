import json
from datetime import datetime, timezone

def generate_unified_dataset():
    # Load KIIFB projects
    with open('data/processed/kiifb_projects.json', 'r', encoding='utf-8') as f:
        kiifb_data = json.load(f)
        kiifb_projects = kiifb_data['projects']

    # Load KITE schools
    with open('data/processed/kite_schools.json', 'r', encoding='utf-8') as f:
        kite_data = json.load(f)
        kite_schools = kite_data['schools']

    # Load 44 Revenue-generating projects & 7 Land acquisition pool from Report tables
    # Build unified project records with proper counting unit tags
    unified_records = []

    # 1. Ingest KIIFB live projects
    for p in kiifb_projects:
        unified_records.append({
            "record_id": p['project_id'],
            "name": p['project_name'],
            "entity_type": "project_sanction",
            "sector": p['sector'],
            "department": p['implementing_department'],
            "spv": p['spv'],
            "district": None, # will be populated or filtered
            "counting_unit": "sanctioned_project_or_cluster",
            "financials": p['financials'],
            "status": p['status'],
            "source_id": p['source_id'],
            "source_locator": p['source_locator'],
            "evidence_label": "official_record"
        })

    # 2. Ingest KITE school delivery institutions
    for s in kite_schools:
        unified_records.append({
            "record_id": s['institution_id'],
            "name": s['school_name'],
            "entity_type": "educational_institution",
            "sector": "General & Higher Education",
            "department": "General Education Department",
            "spv": "KITE",
            "district": s['district'],
            "constituency": s['assembly_constituency'],
            "school_code": s['official_school_code'],
            "counting_unit": "school_institution",
            "financials": None, # specific school-level financial allocations under cluster
            "status": s['status'],
            "source_id": s['source_id'],
            "source_locator": s['source_locator'],
            "evidence_label": "official_record"
        })

    output = {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_records": len(unified_records),
            "kiifb_project_sanctions": len(kiifb_projects),
            "kite_school_institutions": len(kite_schools)
        },
        "records": unified_records
    }

    with open('data/processed/unified_project_explorer.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"Generated unified explorer dataset with {len(unified_records)} total records.")

if __name__ == '__main__':
    generate_unified_dataset()
