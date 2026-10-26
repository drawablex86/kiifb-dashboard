/**
 * depth.svelte.ts — the two-gear depth mode store (UX rework v2, designsystem.md §3).
 *
 * `plain` (default): humanized labels, collapsed provenance, simplified charts.
 * `evidence`: raw taxonomy ids, expanded provenance/locators.
 *
 * Persistence: localStorage['kiifb-depth']; URL parameter `?depth=` wins on
 * navigation and is written back via history.replaceState so shared links carry
 * the gear. SSR/prerender renders assume `plain` — every browser guard is
 * defensive so prerendered HTML stays valid for both gears.
 */

export type DepthMode = 'plain' | 'evidence';

const STORAGE_KEY = 'kiifb-depth';
const URL_PARAM = 'depth';

export const depth: { mode: DepthMode; hydrated: boolean } = $state({
	mode: 'plain',
	hydrated: false
});

function parseMode(value: string | null): DepthMode | null {
	return value === 'evidence' || value === 'plain' ? value : null;
}

/** Read initial gear from `?depth=` param (wins) or localStorage. Browser-only. */
export function initDepth(): void {
	if (typeof window === 'undefined') return;
	const fromUrl = parseMode(new URLSearchParams(window.location.search).get(URL_PARAM));
	if (fromUrl) {
		depth.mode = fromUrl;
	} else {
		try {
			const stored = parseMode(window.localStorage.getItem(STORAGE_KEY));
			if (stored) depth.mode = stored;
		} catch {
			/* storage unavailable (private mode) — keep plain */
		}
	}
	depth.hydrated = true;
}

/** Switch gear and persist to storage + URL (replaceState: no history spam). */
export function setDepth(mode: DepthMode): void {
	depth.mode = mode;
	if (typeof window === 'undefined') return;
	try {
		window.localStorage.setItem(STORAGE_KEY, mode);
	} catch {
		/* ignore */
	}
	const url = new URL(window.location.href);
	url.searchParams.set(URL_PARAM, mode);
	window.history.replaceState(window.history.state, '', url);
}

export function isPlain(): boolean {
	return depth.mode === 'plain';
}
