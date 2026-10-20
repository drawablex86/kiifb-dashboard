# ADR-001 — MapLibre GL with hosted basemap tiles for the Kerala map

- Status: Approved
- Date: 2026-10-20
- Decision owner: Rahul
- Related tasks: T090 (`TASKS.md`)

## Context

The dashboard's architecture (`architecture.md` §2 principle "begin small", §4 technology table) names MapLibre GL JS as the intended map technology. However, the repository's civic evidence standard otherwise requires **100% offline reproducibility**: every consumed artefact must be retrievable and verifiable from the command line without leaving the machine. An interactive MapLibre map normally loads a hosted basemap (raster or vector tiles), which:

1. makes the map view depend on a third-party tile provider at render time;
2. breaks the "offline reproducibility" property for that one view;
3. introduces a tile-licence consideration that must be recorded.

The schematic SVG dot map currently on `/outcomes` avoids all three issues, but is not a geographically accurate representation of Kerala and cannot show the 591 GPS-tagged project points in true position.

## Decision

**Approved by Rahul (2026-10-20):** Build T090 with **MapLibre GL JS and hosted basemap tiles**, accepting the loss of offline reproducibility **for the interactive map feature only**.

- The rest of the dashboard remains fully offline-reproducible; this waiver is scoped strictly to the live tile basemap.
- Data layers (district choropleth values, geo-tagged project points) continue to come exclusively from versioned, checksum-verified processed datasets in `data/processed/` — no project data may be fetched from the tile provider.
- The existing schematic SVG map is retained as an in-app no-network fallback/mobility aid (user choice, reduced-data and unsupported-network environments).
- Tile provider and licence terms must be documented in `datasources.md` and the component's provenance note before release.

## Alternatives considered

1. **Hand-built district-boundary SVG choropleth** (Kerala 14-district boundaries as committed SVG path data). Rejected for T090: authoritative district boundary geometry is hard to source under a licence we can commit, and the effort is large relative to the value; retained as a future option.
2. **Static PNG map export**. Rejected: loses interactivity (click-through to the explorer), which is a core requirement of T090.

## Consequences

- `npm` build of the dashboard is unaffected; tiles are runtime-fetched in the browser only.
- Users fully offline see the schematic fallback automatically.
- The "Open Civic Reproducibility Standard" claim in `README.md` must be footnoted to reference this ADR's scope waiver so the public documentation does not overstate the guarantee.
- A follow-up source entry (e.g. `DS050` — basemap tiles) must be added to `datasources.md` by the executing agent with the chosen provider's terms.
