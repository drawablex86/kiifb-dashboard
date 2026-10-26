/**
 * nav.ts — grouped navigation data for the UX rework (designsystem.md §4.1).
 *
 * Humanized noun labels with one-line "scent" descriptions (NavGroup renders
 * them in the disclosure panel). Grouping follows the V3 KIIFB-first IA (§14):
 * L0 Record base → L1 KIIFB story (primary narrative) → L2 Analytical layers.
 * This is the single file to edit for IA changes.
 */

export type NavItem = {
	label: string;
	href: string;
	description: string;
	layer?: 'L0' | 'L1' | 'L2';
	badge?: string;
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
				description: 'How KIIFB was created, what it borrows against, and why',
				layer: 'L1',
				badge: 'KIIFB story'
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
				description: 'Search every sanctioned project: money, status, district, evidence',
				layer: 'L1',
				badge: 'Record base'
			},
			{
				label: 'Where the Money Goes',
				href: '/portfolio',
				description: 'Follow a rupee of approved money through the delivery pipeline',
				layer: 'L1',
				badge: 'Record base'
			},
			{
				label: 'Debt & Repayments',
				href: '/financials',
				description: 'Who KIIFB owes, on what terms, and the schedule to 2041',
				layer: 'L1',
				badge: 'Record base'
			},
			{
				label: 'Districts & Map',
				href: '/outcomes',
				description: "Where the money landed across Kerala — and what can't yet be measured",
				layer: 'L1',
				badge: 'Record base'
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
				description: 'What the numbers looked like at earlier snapshots, and what changed',
				layer: 'L1',
				badge: 'Record base'
			},
			{
				label: 'Alerts & Delays',
				href: '/flags',
				description: 'Projects with overdue, cost-rise, or paid-but-idle indicators',
				layer: 'L1',
				badge: 'Record base'
			}
		]
	},
	{
		id: 'analyses',
		label: 'Analyses',
		items: [
			{
				label: "The Committee's Claims",
				href: '/committee',
				description: 'Oct 2026 Expert Committee findings — checked against the record',
				layer: 'L2',
				badge: 'Analytical layer'
			},
			{
				label: 'Recommendations & Law',
				href: '/governance',
				description: 'What the committee asked for, legal positions, contractor liability',
				layer: 'L2',
				badge: 'Analytical layer'
			}
		]
	},
	{
		id: 'verify',
		label: 'Verify',
		items: [
			{
				label: 'Glossary & Sources',
				href: '/glossary',
				description: 'Every term in plain words; every source with its locator and licence',
				layer: 'L0',
				badge: 'Record base'
			}
		]
	}
];