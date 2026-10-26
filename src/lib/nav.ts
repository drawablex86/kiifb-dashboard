/**
 * nav.ts — grouped navigation data for the UX rework (designsystem.md §4.1).
 *
 * Humanized noun labels with one-line "scent" descriptions (NavGroup renders
 * them in the disclosure panel). Grouping follows the money's real-world
 * lifecycle (P3 mapping). When the V3 KIIFB-first restructure (§14) lands this
 * is the single file to edit.
 */

export type NavItem = {
	label: string;
	href: string;
	description: string;
};

export type NavGroupData = {
	id: string;
	label: string;
	items: NavItem[];
};

export const NAV_GROUPS: NavGroupData[] = [
	{
		id: 'start',
		label: 'Start',
		items: [
			{
				label: 'Start Here',
				href: '/',
				description: 'What this site is, and five questions it can answer'
			},
			{
				label: 'Background: What is KIIFB',
				href: '/genesis',
				description: 'How KIIFB was created, what it borrows against, and why'
			}
		]
	},
	{
		id: 'follow',
		label: 'Follow the money',
		items: [
			{
				label: 'Projects',
				href: '/projects',
				description: 'Search every sanctioned project: money, status, district, evidence'
			},
			{
				label: 'Where the Money Goes',
				href: '/portfolio',
				description: 'Follow a rupee of approved money through the delivery pipeline'
			},
			{
				label: 'Debt & Repayments',
				href: '/financials',
				description: 'Who KIIFB owes, on what terms, and the schedule to 2041'
			},
			{
				label: 'Districts & Map',
				href: '/outcomes',
				description: "Where the money landed across Kerala — and what can't yet be measured"
			}
		]
	},
	{
		id: 'watch',
		label: 'Watch',
		items: [
			{
				label: 'Change Over Time',
				href: '/trends',
				description: 'What the numbers looked like at earlier snapshots, and what changed'
			},
			{
				label: 'Alerts & Delays',
				href: '/flags',
				description: 'Projects with overdue, cost-rise, or paid-but-idle indicators'
			}
		]
	},
	{
		id: 'claims',
		label: 'Claims & verify',
		items: [
			{
				label: "The Committee's Claims",
				href: '/committee',
				description: 'Who wrote the Oct 2026 report, and how its findings hold up'
			},
			{
				label: 'Recommendations & Law',
				href: '/governance',
				description: 'What the committee asked for, legal positions, contractor liability'
			},
			{
				label: 'Glossary & Sources',
				href: '/glossary',
				description: 'Every term in plain words; every source with its locator'
			}
		]
	}
];
