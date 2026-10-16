import re
import json
from datetime import datetime, timezone

def clean_text(html_text):
    text = re.sub(r'<[^>]+>', '', html_text)
    text = text.replace('&nbsp;', ' ').replace('&#39;', "'").replace('&amp;', '&')
    return re.sub(r'\s+', ' ', text).strip()

def parse_kite_schools():
    with open('data/raw/kite/kiifb-funded-schools-sametham.html', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    tbody_match = re.search(r'<tbody[^>]*>(.*?)</tbody>', html, re.DOTALL)
    if not tbody_match:
        raise ValueError("tbody not found in kiifb-funded-schools-sametham.html")

    rows = re.findall(r'<tr>(.*?)</tr>', tbody_match.group(1), re.DOTALL)
    
    schools = []
    idx = 1
    for r in rows:
        cols = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
        if len(cols) >= 5:
            num = clean_text(cols[0])
            code_raw = cols[1]
            
            hs_m = re.search(r'HS:\s*</span>\s*(\d+)', code_raw)
            hse_m = re.search(r'HSE\s*</span>:\s*(\d+)', code_raw)
            vhse_m = re.search(r'VHSE\s*</span>:\s*(\d+)', code_raw)

            name_m = re.search(r'<a href=\"([^\"]+)\">([^<]+)</a>', cols[2])
            school_url = name_m.group(1) if name_m else ''
            school_name = clean_text(name_m.group(2)) if name_m else clean_text(cols[2])

            district = clean_text(cols[3])
            
            # In HTML: col 6 holds assembly name if row has 9 columns
            assembly = ''
            if len(cols) > 6:
                assembly = clean_text(cols[6])
            elif len(cols) > 4:
                assembly = clean_text(cols[4])

            # Determine official institution code
            primary_code = hs_m.group(1) if hs_m else (hse_m.group(1) if hse_m else (vhse_m.group(1) if vhse_m else num))

            schools.append({
                "institution_id": f"KITE-SCH-{idx:04d}",
                "official_school_code": primary_code,
                "hs_code": hs_m.group(1) if hs_m else None,
                "hse_code": hse_m.group(1) if hse_m else None,
                "vhse_code": vhse_m.group(1) if vhse_m else None,
                "school_name": school_name,
                "district": district,
                "assembly_constituency": assembly,
                "sametham_url": school_url,
                "counting_unit": "school_institution",
                "sector": "General & Higher Education",
                "implementing_agency": "KITE (Kerala Infrastructure and Technology for Education)",
                "status": {
                    "source_status_text": "KIIFB Funded School",
                    "normalised_status": "in_progress", # specific handovers will be matched against KITE verified handovers
                    "notes": "Listed on official KITE Sametham KIIFB-funded school directory"
                },
                "source_id": "DS021",
                "source_locator": f"sametham.kite.kerala.gov.in/{primary_code}"
            })
            idx += 1

    output = {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "DS021 (KITE Sametham KIIFB Funded Schools Directory)",
        "total_schools": len(schools),
        "schools": schools
    }

    with open('data/processed/kite_schools.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"Generated data/processed/kite_schools.json with {len(schools)} school institutions.")

if __name__ == '__main__':
    parse_kite_schools()
