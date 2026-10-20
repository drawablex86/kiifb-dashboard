<script lang="ts">
	/**
	 * KeralaGeographyMap.svelte — T090 (Milestone 9)
	 *
	 * Real geographic Kerala map with two rendering engines, chosen at runtime:
	 *   1. `maplibre` — MapLibre GL choropleth of the 14 districts by approved
	 *      outlay (Committee Table 4.2) + dot layer for geo-tagged records
	 *      (DS010/DS030 processed datasets), on hosted OSM raster tiles per
	 *      ADR-001 (docs/decisions/ADR-001-maplibre-hosted-tiles.md).
	 *   2. `schematic` — zero-network SVG fallback (the pre-existing schematic
	 *      layout, keyboard & mobility aid) rendered automatically when tiles or
	 *      WebGL are unavailable, and manually selectable at any time.
	 *
	 * Licences (see src/lib/data/BASEMAP_PROVENANCE.md):
	 *   - District geometry: datameet.org/maps, CC BY 2.5 India.
	 *   - Basemap raster tiles: © OpenStreetMap contributors (ODbL).
	 *   - Data layers: versioned, checksum-verified processed datasets only.
	 */
	import * as maplibregl from 'maplibre-gl';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import keralaDistrictsRaw from '../data/kerala_districts.json';
	import { goto } from '$app/navigation';

	type DistrictRow = {
		district: any;
		infrastructure_outlay_cr: number;
		infrastructure_share_pct: number;
		land_acquisition_outlay_cr: number;
		total_approved_cr: number;
		category: string;
		[key: string]: unknown;
	};

	type GeoRecord = {
		record_id: string;
		name: string;
		district?: string | null;
		sector?: string;
		status?: { normalised_status?: string; source_status_text?: string };
		financials?: { approved_crore?: number; released_crore?: number };
		coordinates?: { lat: number; lng: number };
		open_flags?: string[];
	};

	let {
		districts,
		geotagged,
		selected = $bindable<string | null>(null),
		mode = $bindable<'districts' | 'dots' | 'both'>('both')
	} = $props();

	// ---------------------------------------------------------------- palette
	// Same evaluator semantics as the district comparison bars on /outcomes.
	const BUCKETS = [
		{ min: 10.0, color: '#065f46', label: 'High outlay (>10% of state pool)' },
		{ min: 5.0, color: '#0284c7', label: 'Medium outlay (5–10%)' },
		{ min: 3.0, color: '#64748b', label: 'Low outlay (<5%)' },
		{ min: 0.0, color: '#f59e0b', label: 'Underserved (<3%)' }
	];
	const SELECT_COLOR = '#059669';

	// Dashboard dataset spells "Kasargod"; census geometry spells "Kasaragod".
	const NAME_ALIASES: Record<string, string> = { Kasaragod: 'Kasargod' };

	function alias(name: string): string {
		return NAME_ALIASES[name] || name;
	}

	function bucketColor(share: number, isSelected: boolean): string {
		if (isSelected) return SELECT_COLOR;
		for (const b of BUCKETS) if (share >= b.min) return b.color;
		return BUCKETS[BUCKETS.length - 1].color;
	}

	// ------------------------------------------------------- derived payloads
	const districtByName = $derived.by(() => {
		const m = new Map<string, DistrictRow>();
		for (const d of districts as DistrictRow[]) m.set(String((d as any).district), d);
		return m;
	});

	const districtGeo = $derived.by(() => {
		const feats = (keralaDistrictsRaw as any).features.map((f: any) => {
			const name = alias(f.properties.district);
			const row: DistrictRow | undefined = districtByName.get(name);
			return {
				type: 'Feature',
				properties: {
					district: name,
					share: row ? Number(row.infrastructure_share_pct.toFixed(2)) : 0,
					outlay: row ? row.infrastructure_outlay_cr : null,
					category: row ? row.category : 'district_not_in_table_4_2'
				},
				geometry: f.geometry
			};
		});
		return { type: 'FeatureCollection', features: feats };
	});

	const pointsGeo = $derived.by(() => {
		const feats = ((geotagged || []) as GeoRecord[])
			.filter((r) => r.coordinates && Number.isFinite(r.coordinates.lat) && Number.isFinite(r.coordinates.lng))
			.map((r) => ({
				type: 'Feature',
				properties: {
					record_id: r.record_id,
					name: r.name,
					district: r.district || null,
					status: r.status?.normalised_status || 'unknown',
					flags: (r.open_flags || []).join(', '),
					released: r.financials?.released_crore ?? null,
					approved: r.financials?.approved_crore ?? null
				},
				geometry: { type: 'Point', coordinates: [r.coordinates!.lng, r.coordinates!.lat] }
			}));
		return { type: 'FeatureCollection', features: feats };
	});

	// ------------------------------------------------------------- engines
	let engine = $state<'maplibre' | 'schematic'>('maplibre');
	let engineNote = $state('');
	let container: HTMLDivElement | undefined = $state();
	let tileFailures = 0;
	// MapLibre map instances are an external non-reactive resource; the plain
	// module variable avoids reactivity warnings for class instances in $state.
	let map: maplibregl.Map | null = null;

	function paintExpression(): any {
		// Rebuilt whenever the selection changes; consumes the baked feature
		// property "district" so paint stays in sync with the shared selection.
		const expr: any[] = ['match', ['get', 'district']];
		for (const f of districtGeo.features as any[]) {
			expr.push(f.properties.district, bucketColor(f.properties.share, f.properties.district === selected));
		}
		expr.push('#94a3b8'); // slate for geometry rows missing from Table 4.2
		return expr;
	}

	function styleJson() {
		return {
			version: 8,
			sources: {
				osmBasemap: {
					type: 'raster',
					tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
					tileSize: 256,
					attribution: '© OpenStreetMap contributors (ODbL) • Hosted-tile decision: ADR-001'
				},
				keralaDistricts: {
					type: 'geojson',
					data: districtGeo as any
				},
				kiifbPoints: {
					type: 'geojson',
					data: pointsGeo as any
				}
			},
			layers: [
				{ id: 'osm-basemap', type: 'raster', source: 'osmBasemap', paint: { 'raster-opacity': 0.9 } },
				{
					id: 'district-fill',
					type: 'fill',
					source: 'keralaDistricts',
					paint: { 'fill-color': paintExpression(), 'fill-opacity': 0.72 }
				},
				{
					id: 'district-outline',
					type: 'line',
					source: 'keralaDistricts',
					paint: { 'line-color': '#ffffff', 'line-width': 1.4 }
				},
				{
					id: 'kiifb-dots',
					type: 'circle',
					source: 'kiifbPoints',
					paint: {
						'circle-radius': 3.5,
						'circle-color': '#059669',
						'circle-stroke-color': '#064e3b',
						'circle-stroke-width': 0.8,
						'circle-opacity': 0.85
					}
				}
			]
		} as any;
	}

	$effect(() => {
		if (engine !== 'maplibre') return;
		if (!container || map) return;

		try {
			const m = new maplibregl.Map({
				container,
				style: styleJson(),
				center: [76.18, 10.2],
				zoom: 6.65,
				minZoom: 5.5,
				maxZoom: 12,
				attributionControl: { compact: true } as any,
				maxBounds: [
					[74.4, 7.9],
					[77.9, 13.2]
				]
			});

			m.on('load', () => {
				// Anomaly-marked pins are red, everything else emerald.
				m.setPaintProperty('kiifb-dots', 'circle-color', [
					'case',
					['to-boolean', ['get', 'flags']],
					'#ef4444',
					'#059669'
				] as any);
				m.setPaintProperty('kiifb-dots', 'circle-radius', [
					'case',
					['to-boolean', ['get', 'flags']],
					4.5,
					3.5
				] as any);
			});

			m.on('click', 'district-fill', (e) => {
				const f = e.features?.[0];
				if (f?.properties?.district) selected = String(f.properties.district);
			});
			m.on('click', 'kiifb-dots', (e) => {
				const f = e.features?.[0];
				if (f?.properties?.record_id) {
					goto('/projects?q=' + encodeURIComponent(String(f.properties.record_id)));
				}
			});
			m.on('mouseenter', 'district-fill', () => (m.getCanvas().style.cursor = 'pointer'));
			m.on('mouseleave', 'district-fill', () => (m.getCanvas().style.cursor = ''));
			m.on('mouseenter', 'kiifb-dots', () => (m.getCanvas().style.cursor = 'pointer'));
			m.on('mouseleave', 'kiifb-dots', () => (m.getCanvas().style.cursor = ''));

			// Tile / network failure watchdog → automatic no-network fallback.
			m.on('error', (e) => {
				const msg = String((e as any)?.error?.message || (e as any)?.errorStatus || 'unknown map error');
				if (/tile|network|fetch|failed|aborted|CORS|load/i.test(msg)) {
					tileFailures += 1;
					if (tileFailures >= 2 && engine === 'maplibre') {
						engineNote = 'Basemap tiles unreachable — switched to the no-network schematic map (fallback per ADR-001).';
						engine = 'schematic';
						try { m.remove(); } catch { /* already removed */ }
						map = null;
					}
				}
			});

			map = m;
		} catch (err: any) {
			// WebGL/browser initialization failure.
			engineNote = 'Map engine unavailable in this browser — showing the no-network schematic map. (' + (err?.message || 'WebGL init failed') + ')';
			engine = 'schematic';
		}
	});

	$effect(() => {
		// Repaint choropleth whenever the selection changes (map engine only).
		if (engine !== 'maplibre' || !map || mode === 'dots') return;
		const apply = () => {
			try {
				if (map && map.isStyleLoaded()) map.setPaintProperty('district-fill', 'fill-color', paintExpression());
			} catch { /* style replaced during teardown; ignore */ }
		};
		if (map.isStyleLoaded()) apply();
		else map.once('load', apply);
	});

	$effect(() => {
		// Layer visibility follows the mode toggle (map engine only).
		if (engine !== 'maplibre' || !map) return;
		const wantsDots = mode === 'dots' || mode === 'both';
		const wantsFill = mode === 'districts' || mode === 'both';
		const apply = () => {
			try {
				if (!map || !map.isStyleLoaded()) return;
				map.setLayoutProperty('kiifb-dots', 'visibility', wantsDots ? 'visible' : 'none');
				map.setLayoutProperty('district-fill', 'visibility', wantsFill ? 'visible' : 'none');
				map.setLayoutProperty('district-outline', 'visibility', wantsFill ? 'visible' : 'none');
			} catch { /* style replaced during teardown; ignore */ }
		};
		if (map.isStyleLoaded()) apply();
		else map.once('load', apply);
	});

	$effect(() => {
		// Teardown on component destroy.
		return () => {
			map?.remove();
			map = null;
		};
	});

	// Schematic fallback geometry (the pre-existing M4 layout on /outcomes).
	const districtMapNodes = [
		{ name: 'Kasargod', x: 42, y: 35, width: 72, height: 26 },
		{ name: 'Kannur', x: 58, y: 72, width: 78, height: 30 },
		{ name: 'Wayanad', x: 145, y: 88, width: 74, height: 26 },
		{ name: 'Kozhikode', x: 68, y: 115, width: 80, height: 28 },
		{ name: 'Malappuram', x: 80, y: 155, width: 88, height: 30 },
		{ name: 'Palakkad', x: 150, y: 190, width: 82, height: 32 },
		{ name: 'Thrissur', x: 95, y: 228, width: 78, height: 30 },
		{ name: 'Ernakulam', x: 108, y: 270, width: 84, height: 32 },
		{ name: 'Idukki', x: 175, y: 298, width: 74, height: 34 },
		{ name: 'Kottayam', x: 115, y: 338, width: 76, height: 28 },
		{ name: 'Alappuzha', x: 65, y: 365, width: 74, height: 26 },
		{ name: 'Pathanamthitta', x: 135, y: 388, width: 92, height: 28 },
		{ name: 'Kollam', x: 105, y: 430, width: 76, height: 28 },
		{ name: 'Thiruvananthapuram', x: 122, y: 475, width: 110, height: 32 }
	];

	function projectGps(lat: number, lng: number) {
		const minLat = 8.28, maxLat = 12.85, minLng = 74.85, maxLng = 77.45;
		const x = 30 + ((lng - minLng) / (maxLng - minLng)) * 210;
		const y = 30 + ((maxLat - lat) / (maxLat - minLat)) * 470;
		return { x: Math.max(10, Math.min(270, x)), y: Math.max(15, Math.min(525, y)) };
	}

	const reprojectedPoints = $derived.by(() => {
		return ((geotagged || []) as GeoRecord[])
			.filter((r) => r.coordinates && Number.isFinite(r.coordinates.lat))
			.slice(0, 800)
			.map((r) => ({ record: r, pt: projectGps(r.coordinates!.lat, r.coordinates!.lng) }));
	});

	const modeDescription = $derived(
		mode === 'districts'
			? 'District choropleth: 14 Kerala districts shaded by their share of the approved infrastructure outlay pool (Committee Table 4.2).'
			: mode === 'dots'
				? 'Geo-tagged view: pins for all ' + ((geotagged as GeoRecord[])?.length ?? 0) + ' DS030-enriched KIIFB records with GPS coordinates (DS010/DS030 processed data).'
				: 'Combined view: districts shaded by approved outlay share (Table 4.2) with geo-tagged record pins (DS010/DS030).'
	);

	function hasFlags(r: GeoRecord): boolean {
		return Array.isArray(r.open_flags) && r.open_flags.length > 0;
	}
</script>

<div class="space-y-3">
	<!-- Engine + layer controls -->
	<div class="flex flex-wrap items-center justify-between gap-2">
		<div id="map-mode-group" role="group" aria-label="Map layer selection"
			class="inline-flex rounded-md shadow-xs border border-slate-300 p-0.5 bg-slate-100 text-3xs font-semibold">
			<button type="button" onclick={() => (mode = 'districts')} aria-pressed={mode === 'districts'}
				class="px-2 py-0.5 rounded transition {mode === 'districts' ? 'bg-white text-slate-900 shadow-xs ring-1 ring-slate-900/10' : 'text-slate-600 hover:text-slate-900'}">
				Districts (Table 4.2)
			</button>
			<button type="button" onclick={() => (mode = 'dots')} aria-pressed={mode === 'dots'}
				class="px-2 py-0.5 rounded transition {mode === 'dots' ? 'bg-white text-slate-900 shadow-xs ring-1 ring-slate-900/10' : 'text-slate-600 hover:text-slate-900'}">
				Geo-tagged Records
			</button>
			<button type="button" onclick={() => (mode = 'both')} aria-pressed={mode === 'both'}
				class="px-2 py-0.5 rounded transition {mode === 'both' ? 'bg-white text-slate-900 shadow-xs ring-1 ring-slate-900/10' : 'text-slate-600 hover:text-slate-900'}">
				Both
			</button>
		</div>
		<button type="button" onclick={() => {
			tileFailures = 0;
			engineNote = '';
			engine = engine === 'maplibre' ? 'schematic' : 'maplibre';
		}} class="px-2 py-0.5 rounded border border-slate-300 text-3xs font-semibold bg-white text-slate-700 hover:bg-slate-50 transition">
			{engine === 'maplibre' ? 'Use schematic (no-tile) map' : 'Use geographic map (tiles)'}
		</button>
	</div>

	<p class="text-xs text-slate-500" role="note">
		{modeDescription}
		{#if selected}
			Selected: <button type="button" class="font-semibold text-emerald-700 hover:underline" onclick={() => (selected = null)}>clear “{selected}”</button>.
		{/if}
	</p>

	{#if engine === 'maplibre'}
		<div bind:this={container} class="h-[480px] rounded-lg border border-slate-200 overflow-hidden relative bg-slate-100" aria-hidden="true">
		</div>
		<!-- Canvas maps are pointer-driven; district list below + comparison bars on the page carry keyboard and screen-reader selection -->

		<div class="flex flex-wrap gap-1.5" role="group" aria-label="Select a district (keyboard and screen-reader navigation)">
			{#each districts as d}
				<button type="button" aria-pressed={selected === String((d as any).district)}
					onclick={() => (selected = String((d as any).district))}
					class="px-2 py-0.5 rounded border text-3xs transition {selected === String((d as any).district)
						? 'bg-emerald-600 text-white border-emerald-700 font-semibold'
						: 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'}">
					{(d as any).district}
				</button>
			{/each}
		</div>

		<!-- sr-only narrative for non-visual contexts -->
		<div class="sr-only" role="note">
			<h4 class="sr-only">Geographic map data summary</h4>
			<p>
				Top districts by approved infrastructure outlay share (Committee Table 4.2): Thiruvananthapuram, Kannur, and Ernakulam — approx 41.6% of the state pool combined. Bottom four: Idukki, Pathanamthitta, Wayanad, Kasargod (each under 3%). {((geotagged as GeoRecord[])?.length ?? 0)} enriched records carry GPS coordinates from DS010/DS030.
			</p>
		</div>
	{:else}
		<!-- Schematic no-network fallback (also the keyboard/mobility-friendly engine) -->
		<div class="relative bg-slate-50 border border-slate-200/80 rounded-lg p-3 flex justify-center">
			<svg viewBox="0 0 280 540" class="w-full max-w-[270px] h-auto drop-shadow-sm select-none" role="img"
				aria-label="Schematic map of 14 Kerala districts shaded by share of approved infrastructure outlay; use the district buttons to select.">
				<path d="M 50,30 Q 30,120 60,200 T 90,320 T 60,400 T 130,510" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3" />
				{#each districtMapNodes as node}
					{@const distData = districtByName.get(node.name)}
					{@const isSelected = selected === node.name}
					<g role="button" tabindex={0}
						aria-label={'Select district ' + node.name + (distData ? ' — ' + (distData.infrastructure_share_pct as number).toFixed(2) + '% of infrastructure outlay' : ' — no Table 4.2 data')}
						class="cursor-pointer focus:outline-none focus:ring-2 focus:ring-emerald-500"
						onclick={() => (selected = node.name)}
						onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selected = node.name; } }}>
						<rect x={node.x} y={node.y} width={node.width} height={node.height} rx="5" ry="5"
							fill={distData ? bucketColor(distData.infrastructure_share_pct as number, isSelected) : '#94a3b8'}
							opacity={mode === 'dots' ? '0.25' : '1.0'}
							stroke={isSelected ? '#0f172a' : '#ffffff'}
							stroke-width={isSelected ? '2.5' : '1.5'} />
						<text x={node.x + node.width / 2} y={node.y + node.height / 2 + 3.5} text-anchor="middle" font-size="9"
							font-weight={isSelected ? 'bold' : '600'} fill={mode === 'dots' ? '#475569' : '#ffffff'} pointer-events="none">
							{node.name}
						</text>
					</g>
				{/each}
				{#if mode === 'dots' || mode === 'both'}
					{#each reprojectedPoints as { record, pt }}
						<circle cx={pt.x} cy={pt.y} r={hasFlags(record as GeoRecord) ? 2.5 : 1.5}
							fill={hasFlags(record as GeoRecord) ? '#ef4444' : '#059669'} opacity="0.75">
							<title>{(record as GeoRecord).name}{(record as GeoRecord).district ? ' (' + (record as GeoRecord).district + ')' : ''}{hasFlags(record as GeoRecord) ? ' — open flags: ' + (record as GeoRecord).open_flags!.join(', ') : ''}</title>
						</circle>
					{/each}
				{/if}
			</svg>
		</div>
	{/if}

	<!-- Shared legend -->
	<div class="grid grid-cols-2 gap-1.5 text-3xs text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-200"
		role="list" aria-label="Map color legend">
		{#each BUCKETS as b}
			<div class="flex items-center gap-1.5" role="listitem">
				<span class="w-3 h-3 rounded" style="background-color: {b.color}"></span>
				<span>{b.label}</span>
			</div>
		{/each}
		<div class="flex items-center gap-1.5" role="listitem">
			<span class="w-3 h-3 rounded-full bg-emerald-600"></span>
			<span>Geo-tagged record (no open flags)</span>
		</div>
		<div class="flex items-center gap-1.5" role="listitem">
			<span class="w-3 h-3 rounded-full bg-red-500"></span>
			<span>Record with open anomaly flags</span>
		</div>
	</div>

	{#if engineNote}
		<div class="bg-amber-50 text-amber-900 border border-amber-200 rounded p-2 text-2xs flex gap-2" role="status">
			<span class="font-bold">Fallback:</span> {engineNote}
		</div>
	{/if}

	<!-- Provenance footer (design-system.md §1 and §4.2) -->
	<div class="text-3xs text-slate-400 font-mono leading-relaxed">
		* Data layers: Committee Table 4.2 (June 30, 2026) for district outlay; DS010/DS030 processed datasets for geo-tagged records. Click a pin to open it in the project explorer.<br>
		* Basemap tiles © OpenStreetMap contributors (ODbL) — hosted-tile waiver per <strong>ADR-001</strong> (docs/decisions/ADR-001-maplibre-hosted-tiles.md).<br>
		* District geometry derived from datameet.org/maps (CC BY 2.5 IN), simplified — see src/lib/data/BASEMAP_PROVENANCE.md. Not an authoritative boundary delimitation.
	</div>
</div>
