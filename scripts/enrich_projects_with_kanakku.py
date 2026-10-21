#!/usr/bin/env python3
"""
Enriches KIIFB projects and unified project explorer with Kerala Kanakku open data.
Source: DS030 (keralakanakku.com) under CC BY 4.0.
"""

import json
import csv
import re
import os
import argparse
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_common as fc  # T081: input resolution (cli > env > newest crawl > pinned)

def norm(text):
    if not text:
        return ""
    return re.sub(r'[^a-z0-9]', '', str(text).lower())

def run_enrichment(proj_path=None, funding_path=None, liability_path=None):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resolved, origin = fc.resolve_input(
        proj_path, "KANAKKU_PROJECTS_CSV", "kanakku", "",
        "projects.csv", "data/raw/kanakku/projects.csv")
    kanakku_proj_file = str(resolved)
    print(f"[input] DS030 (projects.csv) -> {kanakku_proj_file} ({origin})")
    resolved, _origin = fc.resolve_input(
        funding_path, "KANAKKU_FUNDING_CSV", "kanakku", "",
        "funding.csv", "data/raw/kanakku/funding.csv")
    kanakku_funding_file = str(resolved)
    resolved, _origin = fc.resolve_input(
        liability_path, "KANAKKU_LIABILITY_CSV", "kanakku", "",
        "liability.csv", "data/raw/kanakku/liability.csv")
    kanakku_liability_file = str(resolved)

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
    # A single map_group can link to multiple packages under the same sub_project_code
    pkgs_by_code = {}
    for p in kanakku_packages:
        c = p.get('code')
        if c:
            pkgs_by_code.setdefault(c, []).append(p)
        sp = p.get('sub_project_code')
        if sp:
            pkgs_by_code.setdefault(sp, []).append(p)

    proj_to_geo = {}
    for row in kanakku_funding:
        pname = norm(row.get('project'))
        mg = row.get('map_group')
        if pname and mg and mg in pkgs_by_code:
            for pkg in pkgs_by_code[mg]:
                dist = pkg.get('district')
                const = pkg.get('constituencies')
                lat = pkg.get('latitude')
                lng = pkg.get('longitude')
                flags = [f.strip() for f in pkg.get('open_flags', '').split(';') if f.strip()]

                proj_to_geo.setdefault(pname, {
                    "districts": set(),
                    "constituencies": set(),
                    "flags": set(),
                    "coords": []
                })
                if dist:
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
        lat = pkg.get('latitude')
        lng = pkg.get('longitude')
        if tname and (dist or (lat and lng)):
            proj_to_geo.setdefault(tname, {
                "districts": set(),
                "constituencies": set(),
                "flags": set(),
                "coords": []
            })
            if dist:
                proj_to_geo[tname]["districts"].add(dist)
            if pkg.get('constituencies'):
                proj_to_geo[tname]["constituencies"].add(pkg.get('constituencies'))
            flags = [f.strip() for f in pkg.get('open_flags', '').split(';') if f.strip()]
            if flags:
                proj_to_geo[tname]["flags"].update(flags)
            if lat and lng:
                proj_to_geo[tname]["coords"].append((float(lat), float(lng)))

    # High-precision fuzzy fallback matching for projects without coordinates
    def clean_tokens(text):
        if not text:
            return set()
        t = str(text).lower()
        t = re.sub(r'\bgovt\b', 'government', t)
        t = re.sub(r'\bhss\b', 'higher secondary school', t)
        t = re.sub(r'\bhs\b', 'high school', t)
        t = re.sub(r'\biti\b', 'industrial training institute', t)
        t = re.sub(r'\bphc\b', 'primary health centre', t)
        t = re.sub(r'\bchc\b', 'community health centre', t)
        t = re.sub(r'\b(construction|setting|upgradation|improvement|improvements|providing|procurement|establishment|renovation|rehabilitation|development|strengthening|modernization|supply|installation|mitigating|handling|of|to|in|at|and|for|the|phase|stage|under|via)\b', ' ', t)
        return set(re.findall(r'[a-z0-9]{3,}', t))

    geo_packages_with_coords = [p for p in kanakku_packages if p.get('latitude') and p.get('longitude')]
    pkg_tokens_map = {}
    for p in geo_packages_with_coords:
        toks = clean_tokens(p.get('title'))
        if len(toks) >= 2:
            pkg_tokens_map[p['code']] = (p, toks)

    def get_geo_info_for_name(raw_name):
        pname = norm(raw_name)
        if pname in proj_to_geo and (proj_to_geo[pname]["districts"] or proj_to_geo[pname]["coords"]):
            return proj_to_geo[pname]

        # Fuzzy fallback against packages
        toks = clean_tokens(raw_name)
        if len(toks) >= 2:
            best_j = 0
            best_pkg = None
            for code, (pkg, p_toks) in pkg_tokens_map.items():
                j = len(toks & p_toks) / len(toks | p_toks)
                if j > best_j:
                    best_j = j
                    best_pkg = pkg
            if best_j >= 0.70 and best_pkg:
                dist = best_pkg.get("district")
                const = best_pkg.get("constituencies")
                lat = best_pkg.get("latitude")
                lng = best_pkg.get("longitude")
                flags = [f.strip() for f in best_pkg.get("open_flags", "").split(";") if f.strip()]
                return {
                    "districts": {dist} if dist else set(),
                    "constituencies": {const} if const else set(),
                    "flags": set(flags),
                    "coords": [(float(lat), float(lng))] if (lat and lng) else []
                }
        return None

    # Enrich kiifb_projects.json
    print("Enriching kiifb_projects.json...")
    with open(kiifb_proj_file, 'r', encoding='utf-8') as f:
        kiifb_data = json.load(f)

    enriched_count = 0
    for p in kiifb_data.get('projects', []):
        info = get_geo_info_for_name(p.get('project_name'))
        if info and (info["districts"] or info["coords"]):
            p["district"] = ", ".join(sorted(info["districts"])) if info["districts"] else None
            p["constituency"] = ", ".join(sorted(info["constituencies"])) if info["constituencies"] else None
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
            info = get_geo_info_for_name(r.get('name'))
            if info and (info["districts"] or info["coords"]):
                r["district"] = ", ".join(sorted(info["districts"])) if info["districts"] else None
                r["constituency"] = ", ".join(sorted(info["constituencies"])) if info["constituencies"] else None
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
    ap = argparse.ArgumentParser(
        description="Enrich projects with Kanakku DS030 data (CC BY 4.0).")
    ap.add_argument('--proj', default=None,
                    help='projects.csv snapshot path (default: newest live-crawl, else pinned)')
    ap.add_argument('--funding', default=None,
                    help='funding.csv snapshot path (same default rule)')
    ap.add_argument('--liability', default=None,
                    help='liability.csv snapshot path (same default rule)')
    args = ap.parse_args()
    run_enrichment(args.proj, args.funding, args.liability)
