#!/usr/bin/env python3
"""
Enriches KIIFB projects and unified project explorer with Kerala Kanakku open data.
Source: DS030 (keralakanakku.com) under CC BY 4.0.
"""

import json
import csv
import re
import os

def norm(text):
    if not text:
        return ""
    return re.sub(r'[^a-z0-9]', '', str(text).lower())

def run_enrichment():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kanakku_proj_file = os.path.join(base_dir, 'data/raw/kanakku/projects.csv')
    kanakku_funding_file = os.path.join(base_dir, 'data/raw/kanakku/funding.csv')
    kanakku_liability_file = os.path.join(base_dir, 'data/raw/kanakku/liability.csv')

    kiifb_proj_file = os.path.join(base_dir, 'data/processed/kiifb_projects.json')
    unified_proj_file = os.path.join(base_dir, 'data/processed/unified_project_explorer.json')
    output_liability_json = os.path.join(base_dir, 'data/processed/contractor_liability.json')
    output_kanakku_packages_json = os.path.join(base_dir, 'data/processed/kanakku_packages.json')

    print("Loading Kanakku data files...")
    with open(kanakku_proj_file, 'r', encoding='utf-8') as f:
        kanakku_packages = list(csv.DictReader(f))

    with open(kanakku_funding_file, 'r', encoding='utf-8') as f:
        kanakku_funding = list(csv.DictReader(f))

    with open(kanakku_liability_file, 'r', encoding='utf-8') as f:
        kanakku_liability = list(csv.DictReader(f))

    # Save liability file as processed JSON for the frontend
    liability_clean = []
    for row in kanakku_liability:
        liability_clean.append({
            "district": row.get("office_district", ""),
            "wing": row.get("wing", ""),
            "work": row.get("work", ""),
            "contractor": row.get("contractor", ""),
            "agreed_amount_inr": float(row.get("agreed_amount") or 0),
            "liability_starts": row.get("liability_starts", ""),
            "liability_ends": row.get("liability_ends", ""),
            "division": row.get("division", ""),
            "subdivision": row.get("subdivision", "")
        })

    with open(output_liability_json, 'w', encoding='utf-8') as f:
        json.dump({
            "version": "1.0.0",
            "source": "DS030 (PWD Defect Liability via Kerala Kanakku)",
            "licence": "CC BY 4.0",
            "total_records": len(liability_clean),
            "records": liability_clean
        }, f, indent=2)
    print(f"Saved {len(liability_clean)} contractor liability records to {output_liability_json}")

    # Build index of packages by code and sub_project_code
    pkg_by_code = {}
    for p in kanakku_packages:
        pkg_by_code[p['code']] = p
        if p.get('sub_project_code'):
            pkg_by_code.setdefault(p['sub_project_code'], p)

    # Export lean packages dataset with GPS coordinates for map dot-density
    geo_packages = []
    for p in kanakku_packages:
        lat = float(p['latitude']) if p.get('latitude') else None
        lng = float(p['longitude']) if p.get('longitude') else None
        if lat and lng:
            geo_packages.append({
                "code": p.get("code"),
                "title": p.get("title"),
                "department": p.get("department"),
                "district": p.get("district") or "District not stated",
                "constituency": p.get("constituencies"),
                "expenditure_inr": float(p.get("expenditure") or 0),
                "status": p.get("status"),
                "open_flags": [f.strip() for f in p.get("open_flags", "").split(";") if f.strip()],
                "lat": round(lat, 5),
                "lng": round(lng, 5)
            })

    with open(output_kanakku_packages_json, 'w', encoding='utf-8') as f:
        json.dump({
            "version": "1.0.0",
            "source": "DS030 (gis.kiifb.org via Kerala Kanakku)",
            "licence": "CC BY 4.0",
            "total_records": len(geo_packages),
            "packages": geo_packages
        }, f, indent=2)
    print(f"Saved {len(geo_packages)} geo-tagged packages to {output_kanakku_packages_json}")

    # Index funding rows to connect project title to packages
    proj_to_geo = {}
    for row in kanakku_funding:
        pname = norm(row.get('project'))
        mg = row.get('map_group')
        if pname and mg and mg in pkg_by_code:
            pkg = pkg_by_code[mg]
            dist = pkg.get('district')
            const = pkg.get('constituencies')
            lat = pkg.get('latitude')
            lng = pkg.get('longitude')
            flags = [f.strip() for f in pkg.get('open_flags', '').split(';') if f.strip()]
            
            if dist:
                proj_to_geo.setdefault(pname, {
                    "districts": set(),
                    "constituencies": set(),
                    "flags": set(),
                    "coords": []
                })
                proj_to_geo[pname]["districts"].add(dist)
                if const:
                    proj_to_geo[pname]["constituencies"].add(const)
                if flags:
                    proj_to_geo[pname]["flags"].update(flags)
                if lat and lng:
                    proj_to_geo[pname]["coords"].append((float(lat), float(lng)))

    # Fallback title match directly from packages
    for pkg in kanakku_packages:
        tname = norm(pkg.get('title'))
        dist = pkg.get('district')
        if tname and dist:
            proj_to_geo.setdefault(tname, {
                "districts": set(),
                "constituencies": set(),
                "flags": set(),
                "coords": []
            })
            proj_to_geo[tname]["districts"].add(dist)
            if pkg.get('constituencies'):
                proj_to_geo[tname]["constituencies"].add(pkg.get('constituencies'))
            flags = [f.strip() for f in pkg.get('open_flags', '').split(';') if f.strip()]
            if flags:
                proj_to_geo[tname]["flags"].update(flags)
            if pkg.get('latitude') and pkg.get('longitude'):
                proj_to_geo[tname]["coords"].append((float(pkg['latitude']), float(pkg['longitude'])))

    # Enrich kiifb_projects.json
    print("Enriching kiifb_projects.json...")
    with open(kiifb_proj_file, 'r', encoding='utf-8') as f:
        kiifb_data = json.load(f)

    enriched_count = 0
    for p in kiifb_data.get('projects', []):
        pname = norm(p.get('project_name'))
        if pname in proj_to_geo:
            info = proj_to_geo[pname]
            p["district"] = ", ".join(sorted(info["districts"]))
            p["constituency"] = ", ".join(sorted(info["constituencies"]))
            p["open_flags"] = sorted(list(info["flags"]))
            if info["coords"]:
                avg_lat = sum(c[0] for c in info["coords"]) / len(info["coords"])
                avg_lng = sum(c[1] for c in info["coords"]) / len(info["coords"])
                p["coordinates"] = {"lat": round(avg_lat, 5), "lng": round(avg_lng, 5)}
            enriched_count += 1
        else:
            p.setdefault("district", None)
            p.setdefault("constituency", None)
            p.setdefault("open_flags", [])

    with open(kiifb_proj_file, 'w', encoding='utf-8') as f:
        json.dump(kiifb_data, f, indent=2)
    print(f"Enriched {enriched_count} / {len(kiifb_data['projects'])} projects in kiifb_projects.json")

    # Enrich unified_project_explorer.json
    print("Enriching unified_project_explorer.json...")
    with open(unified_proj_file, 'r', encoding='utf-8') as f:
        unified_data = json.load(f)

    u_enriched = 0
    for r in unified_data.get('records', []):
        if r.get('entity_type') == 'project_sanction':
            pname = norm(r.get('name'))
            if pname in proj_to_geo:
                info = proj_to_geo[pname]
                r["district"] = ", ".join(sorted(info["districts"]))
                r["constituency"] = ", ".join(sorted(info["constituencies"]))
                r["open_flags"] = sorted(list(info["flags"]))
                if info["coords"]:
                    avg_lat = sum(c[0] for c in info["coords"]) / len(info["coords"])
                    avg_lng = sum(c[1] for c in info["coords"]) / len(info["coords"])
                    r["coordinates"] = {"lat": round(avg_lat, 5), "lng": round(avg_lng, 5)}
                u_enriched += 1
            else:
                r.setdefault("district", None)
                r.setdefault("constituency", None)
                r.setdefault("open_flags", [])
        else:
            r.setdefault("open_flags", [])

    # Update summary in unified_data
    unified_data['summary']['enriched_with_kanakku_count'] = u_enriched
    unified_data['summary']['kanakku_source'] = "DS030 (keralakanakku.com)"

    with open(unified_proj_file, 'w', encoding='utf-8') as f:
        json.dump(unified_data, f, indent=2)
    print(f"Enriched {u_enriched} project sanction records in unified_project_explorer.json")

if __name__ == '__main__':
    run_enrichment()
