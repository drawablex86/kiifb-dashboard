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
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_common as fc  # T081: input resolution (cli > env > newest crawl > pinned)

def norm(text):
    if not text:
        return ""
    return re.sub(r'[^a-z0-9]', '', str(text).lower())


def dept_norm(text):
    """Department-key normalisation used by the department-filtered tiers."""
    return re.sub(r'[^a-z0-9]', '', str(text or '').lower())


def clean_tokens(text):
    """Token set for the fuzzy tiers (stopword-light, acronym-expanded)."""
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


# ---------------------------------------------------------------------------
# T083 — additional deterministic enrichment tiers (all auditable, documented
# in docs/matching-rules.md). Existing join tiers are untouched and keep
# precedence; these tiers only fill records where district is still null.
# ---------------------------------------------------------------------------

KERALA_DISTRICTS = [
    "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", "Kottayam",
    "Idukki", "Ernakulam", "Thrissur", "Palakkad", "Malappuram", "Kozhikode",
    "Wayanad", "Kannur", "Kasaragod",
]

# Common official spellings still used in project titles (documented alias map).
DISTRICT_ALIASES = {"Trivandrum": "Thiruvananthapuram", "Trichur": "Thrissur"}


def extract_districts_from_name(name):
    """Tier 'name_district_mention': districts explicitly named in the title.

    Returns [] when nothing (or more than 2 contradictory districts) is
    mentioned. Deliberately returns the district NAME only — no coordinates,
    no flags — so downstream consumers can treat it as geography-kind 'name'.
    """
    if not name:
        return []
    text = str(name)
    found = set()
    for d in KERALA_DISTRICTS:
        if re.search(r'\b%s\b' % re.escape(d), text, re.IGNORECASE):
            found.add(d)
    for alias, target in DISTRICT_ALIASES.items():
        if re.search(r'\b%s\b' % re.escape(alias), text, re.IGNORECASE):
            found.add(target)
    if not found or len(found) > 2:
        return []
    return sorted(found)


def extract_district_from_name_meta(name):
    """Returns (district_value, tier_meta) or (None, None) for the tier."""
    hits = extract_districts_from_name(name)
    if not hits:
        return None, None
    meta = {
        "resolution": "name_district_mention",
        "confidence": 0.95,
        "sources": [],
        "note": "District name appears verbatim in the official project title "
                "(no Kanakku package join; coordinates intentionally absent).",
    }
    return ", ".join(hits), meta


def geo_package_index(packages):
    """Packages carrying geography (district and/or coordinates)."""
    return [p for p in packages if p.get('district') or (p.get('latitude') and p.get('longitude'))]


def containment_and_fuzzy_geo(pname, project_department, packages):
    """Tiers 'work_containment_same_dept' and 'token_fuzzy_same_dept_j55'.

    Strictly department-filtered; containment requires one distinct district
    across all hits (<=3); fuzzy requires a unique best token-overlap match
    above 0.55 Jaccard. Returns (district, constituency, coords, flags,
    pkg_codes, resolution, confidence) or None.
    """
    if not pname:
        return None
    pdo = dept_norm(project_department)
    nm = norm(pname)

    # -- containment tier ------------------------------------------------
    if len(nm) >= 12:
        hits = [
            p for p in packages
            if (nm in norm(p.get('title')) or norm(p.get('title')) in nm)
            and dept_norm(p.get('department')) == pdo
        ]
        districts = {p.get('district') for p in hits if p.get('district')}
        if hits and len(hits) <= 3 and len(districts) == 1:
            coords = [(float(p['latitude']), float(p['longitude']))
                      for p in hits if p.get('latitude') and p.get('longitude')]
            consts = {p.get('constituencies') for p in hits if p.get('constituencies')}
            flags = {f.strip() for p in hits
                     for f in (p.get('open_flags') or '').split(';') if f.strip()}
            return (districts.pop(),
                    ", ".join(sorted(c for c in consts if c)) or None,
                    coords, sorted(flags), [p.get('code') for p in hits],
                    "work_containment_same_dept", 0.75)

    # -- token fuzzy tier ------------------------------------------------
    toks = clean_tokens(pname)
    if len(toks) >= 2:
        best, best_j = None, 0.0
        for p in packages:
            pdo_p = dept_norm(p.get('department'))
            if pdo_p != pdo:
                continue
            ptoks = clean_tokens(p.get('title'))
            if not ptoks:
                continue
            j = len(toks & ptoks) / len(toks | ptoks)
            if j > best_j:
                best, best_j = p, j
        if best is not None and best_j >= 0.55:
            lat = best.get('latitude')
            lng = best.get('longitude')
            coords = [(float(lat), float(lng))] if lat and lng else []
            flags = [f.strip() for f in (best.get('open_flags') or '').split(';')
                     if f.strip()]
            return (best.get('district'),
                    best.get('constituencies') or None,
                    coords, sorted(flags), [best.get('code')],
                    "token_fuzzy_same_dept_j55", round(best_j, 2))
    return None


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

    # T083: strict, auditable fill-up tiers (see extract_district_from_name_meta
    # and containment_and_fuzzy_geo; documented in docs/matching-rules.md).
    # They only fill records whose district is still null — existing matches
    # are never re-resolved.
    geo_pkgs = geo_package_index(kanakku_packages)
    match_log_entries = []
    tier_counts = {}
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
            # Tier 1: explicit district mention in the official title.
            district, meta = extract_district_from_name_meta(p.get('project_name'))
            if not district:
                # Tier 2/3: dept-filtered containment / token fuzzy (bundle).
                solved = containment_and_fuzzy_geo(
                    p.get('project_name'), p.get('implementing_department'), geo_pkgs)
                if solved:
                    district, constituency, coords, flags, pkg_codes, resolution, confidence = solved
                    meta = {
                        "resolution": resolution,
                        "confidence": confidence,
                        "sources": [c for c in pkg_codes if c],
                        "note": "Matched against DS030 GIS packages within the same "
                                "department; coordinates only where all evidence "
                                "agrees.",
                    }
                    if district:
                        p["district"] = district
                    if constituency:
                        p["constituency"] = constituency
                    if coords:
                        p["coordinates"] = {
                            "lat": round(sum(c[0] for c in coords) / len(coords), 5),
                            "lng": round(sum(c[1] for c in coords) / len(coords), 5)}
                    p["open_flags"] = sorted(flags)
                    p["district_match"] = meta
                    match_log_entries.append({
                        "project_id": p.get('project_id'),
                        "project_name": p.get('project_name'),
                        "resolution": resolution,
                        "confidence": confidence,
                        "districts": district.split(", ") if district else [],
                        "pkg_codes": meta["sources"],
                    })
                    tier_counts[resolution] = tier_counts.get(resolution, 0) + 1
                    enriched_count += 1
                    continue
                p.setdefault("district", None)
                p.setdefault("constituency", None)
                p.setdefault("open_flags", [])
            else:
                p["district"] = district
                p["district_match"] = meta
                match_log_entries.append({
                    "project_id": p.get('project_id'),
                    "project_name": p.get('project_name'),
                    "resolution": meta["resolution"],
                    "confidence": meta["confidence"],
                    "districts": district.split(", "),
                    "pkg_codes": [],
                })
                tier_counts[meta["resolution"]] = tier_counts.get(meta["resolution"], 0) + 1
                enriched_count += 1

    with open(kiifb_proj_file, 'w', encoding='utf-8') as f:
        json.dump(kiifb_data, f, indent=2)
    print(f"Enriched {enriched_count} / {len(kiifb_data['projects'])} projects in kiifb_projects.json")

    # Audit match log for the T083 fill-up tiers (locale-independent order).
    with open(os.path.join(base_dir, 'data/processed/kanakku_match_log.json'),
              'w', encoding='utf-8') as f:
        json.dump({
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "source": "DS030 (keralakanakku.com) enrichment audit log",
            "licence": "CC BY 4.0",
            "tiers_applied": tier_counts,
            "total_entries": len(match_log_entries),
            "entries": sorted(match_log_entries, key=lambda e: e["project_id"] or ""),
        }, f, indent=2, sort_keys=True)
    print(f"Audit log: {len(match_log_entries)} fill-up-tier matches "
          f"({tier_counts})")

    # Enrich unified_project_explorer.json
    print("Enriching unified_project_explorer.json...")
    with open(unified_proj_file, 'r', encoding='utf-8') as f:
        unified_data = json.load(f)

    u_enriched = 0
    u_fill_tier = 0
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
                # T083 fill-up tiers (same precedence as kiifb_projects).
                district, meta = extract_district_from_name_meta(r.get('name'))
                if not district:
                    solved = containment_and_fuzzy_geo(
                        r.get('name'), r.get('department'), geo_pkgs)
                    if solved:
                        district, constituency, coords, flags, pkg_codes, resolution, confidence = solved
                        r["district"] = district
                        r["constituency"] = constituency
                        if coords:
                            r["coordinates"] = {
                                "lat": round(sum(c[0] for c in coords) / len(coords), 5),
                                "lng": round(sum(c[1] for c in coords) / len(coords), 5)}
                        r["open_flags"] = sorted(flags)
                        r["district_match"] = {
                            "resolution": resolution,
                            "confidence": confidence,
                            "sources": [c for c in pkg_codes if c],
                            "note": "Matched against DS030 GIS packages within the "
                                    "same department.",
                        }
                        u_enriched += 1
                        u_fill_tier += 1
                        continue
                    r.setdefault("district", None)
                    r.setdefault("constituency", None)
                    r.setdefault("open_flags", [])
                else:
                    r["district"] = district
                    r["district_match"] = meta
                    u_enriched += 1
                    u_fill_tier += 1
        else:
            r.setdefault("open_flags", [])

    # Update summary in unified_data
    unified_data['summary']['enriched_with_kanakku_count'] = u_enriched
    unified_data['summary']['enriched_with_fillup_tiers'] = u_fill_tier
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
