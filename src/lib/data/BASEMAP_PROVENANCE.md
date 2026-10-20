# Basemap data provenance — `kerala_districts.json`

- **File**: `src/lib/data/kerala_districts.json` — GeoJSON `FeatureCollection`, 14 Kerala district polygons (EPSG:4326).
- **Upstream source**: https://github.com/geohacker/kerala (`geojsons/district.geojson`), itself compiled from **datameet.org/maps** (Census-derived district boundaries).
- **Licence**: datameet maps are shared under the **Creative Commons Attribution 2.5 India** licence (attribution: "Data{Meet} Community Created Maps of India"). Reproduced and attributed here in accordance with CC BY 2.5 IN.
- **Derivation applied (this repository, 2026-10-20)**:
  1. Selected only the 14 Kerala district polygons; dropped all non-district properties.
  2. Coordinates quantized to 4 decimal places (≈ 11 m precision).
  3. Per-ring Douglas–Peucker simplification with tolerance ε = 0.0015° (≈ 165 m), duplicates retained the source ring and ring closure preserved.
  4. Renormalised to properties `{ "district": "<Name>" }` to join with Committee Table 4.2 (`data/processed/public_value_and_geography.json`).
- **Known attribute note**: boundary spelling `Kasaragod` matches the 2011 district inventory; the dashboard dataset spells it `Kasargod` (Committee Table 4.2 spelling). The map component aliases one to the other; no geometry is altered.
- **Use in app**: choropleth fill layer inside `src/lib/components/KeralaGeographyMap.svelte` (T090). No KIIFB data is embedded in this geometry file — values are joined at render time from the versioned processed datasets.
- **Boundary disclaimer**: boundaries are census-era community-compiled approximations and are **not** an authoritative delimitation; no sovereignty claim is made or implied. For official limits see the Office of the Surveyor General of India.
