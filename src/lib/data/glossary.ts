/**
 * glossary.ts — definitions powering GlossaryTerm popovers and the /glossary page.
 *
 * Contract (designsystem.md §5.4): every human-facing jargon term gets:
 *   plain  — ≤ ~40 words, no jargon, no acronyms left unexplained
 *   expert — technical definition, citing locator/framework where possible
 *   why    — one sentence on why it matters *on this site*
 *
 * Definitions are definitional/neutral: they describe what a term means and
 * how this dashboard treats it. They do not add editorial claims of their own.
 */

export type GlossaryEntry = {
	/** Stable slug used by GlossaryTerm id props and /glossary anchors. */
	id: string;
	/** Canonical / expert term as displayed. */
	term: string;
	/** One-sentence plain definition (Plain mode shows this first). */
	plain: string;
	/** Technical definition (Evidence mode shows this first). */
	expert: string;
	/** Why it matters on this dashboard. */
	why: string;
	seeAlso?: string[];
};

export const GLOSSARY: GlossaryEntry[] = [
	// ── Units & dates ─────────────────────────────────────────────────────────
	{
		id: 'crore',
		term: 'Crore (₹ Cr)',
		plain: 'A unit used across India. One crore is ten million rupees (1,00,00,000). This site writes large amounts as "₹1,00,341 Cr".',
		expert: 'Indian numbering unit: 1 crore = 10⁷ rupees = 100 lakh = 10 million. Conventionally grouped 1,00,00,000 under the en-IN locale.',
		why: 'Every money figure on this site is in crore — misreading the unit by a factor of 100 dB changes every conclusion.',
		seeAlso: ['lakh', 'indian_notation']
	},
	{
		id: 'lakh',
		term: 'Lakh (₹ L)',
		plain: 'A unit equal to one hundred thousand rupees. 100 lakh = 1 crore. Used for smaller amounts like school-level costs.',
		expert: 'Indian numbering unit: 1 lakh = 10⁵ rupees. 100 lakh = 1 crore.',
		why: 'Land and household-scale figures are often quoted in lakh; mixing it up with crore is a classic reading error.',
		seeAlso: ['crore']
	},
	{
		id: 'indian_notation',
		term: 'Indian number notation',
		plain: 'India groups digits as ones-tens-hundreds, then thousands, then lakhs and crores — e.g. ₹1,00,341.00 Cr, not ₹100,341.',
		expert: 'en-IN digit grouping (10^3, 10^5, 10^7 nodes). Mandated site-wide by design-system.md §3.2 with tabular numerals.',
		why: 'The grouping looks unusual to global readers; never "fix" it to Western commas.',
		seeAlso: ['crore', 'lakh']
	},
	{
		id: 'as_of_date',
		term: 'As-of date',
		plain: 'The date a number is true *for*. Money figures describe a balance at a moment, so every stock figure carries one.',
		expert: 'Reference date for stock quantities. Two records with different as-of dates cannot be netted or compared without reconciliation.',
		why: 'Most apparent "disagreements" between KIIFB records and the committee report are actually different as-of dates.',
		seeAlso: ['stock_vs_flow']
	},
	{
		id: 'stock_vs_flow',
		term: 'Stock vs flow',
		plain: 'A stock is what you hold at a moment (total debt on 30 June 2026). A flow is what passes through over a period (borrowing during 2024-25).',
		expert: 'Quantity anchored to an instant (balance) vs a cumulative or periodic quantity over an interval (rate, series). Mixing them produces category errors.',
		why: 'The site labels both everywhere because summing debt stock (stock) with yearly repayments (flow) is the commonest misreading of KIIFB numbers.',
		seeAlso: ['as_of_date', 'approved_outlay', 'released_disbursed']
	},

	// ── Money: approval & release ────────────────────────────────────────────
	{
		id: 'approved_outlay',
		term: 'Approved outlay',
		plain: 'Money KIIFB has permission to spend on a project. Permission is not the same as money spent — most projects have released far less.',
		expert: "Total sanction value committed by KIIFB's board for a project or package; a budgetary authorisation (stock at sanction date), not disbursement.",
		why: 'Headlines often quote approved outlay (₹1,00,341 Cr is the figure). Centre-line it against released money to see how much of the story is paper.',
		seeAlso: ['released_disbursed', 'technical_sanction']
	},
	{
		id: 'released_disbursed',
		term: 'Released / disbursed',
		plain: 'Money actually paid out so far — usually much less than the amount approved.',
		expert: 'Cumulative amount released from KIIFB to implementing agencies, per Table 3.1 of the Oct 2026 committee report.',
		why: 'Released ≠ spent. Money can sit with an agency after release; some gaps reported here measure exactly that.',
		seeAlso: ['approved_outlay', 'absorption_rate']
	},
	{
		id: 'technical_sanction',
		term: 'Technical sanction',
		plain: 'An engineer-approved, itemised estimate for a work. Government in principle (administrative sanction) comes first; detailed costing comes second.',
		expert: 'Detailed measurable sanction by a competent technical authority (GFR/R Works Manual procedure), typically per estimates; a precondition for tendering.',
		why: 'Kanakku delivery stages below "in progress" usually require technical sanction; its absence is why many approved projects show little movement.',
		seeAlso: ['approved_outlay', 'tender']
	},
	{
		id: 'umbrella_sanction',
		term: 'Umbrella sanction',
		plain: 'One large approval covering many smaller sub-projects. Reported figures can differ depending on how the umbrella is counted.',
		expert: 'A single sanction instrument aggregating multiple works/packages; sub-sanctions may exist downstream, causing double-count or under-count in project-level statistics.',
		why: 'The project explorer normalises counting units precisely to avoid comparing 1 umbrella with 404 sub-projects.',
		seeAlso: ['counting_unit', 'normalised_status']
	},
	{
		id: 'counting_unit',
		term: 'Counting unit',
		plain: 'What "one project" means in a count — a road work, a school, or a ₹100 Cr umbrella bundle. Different sources count differently.',
		expert: 'Unit of analysis ambiguity across datasets (sanction, package, work, component). Reconciliation requires explicit unit normalisation rules.',
		why: 'Most "how many projects?" disagreements between the committee report and delivery databases are counting-unit clashes.',
		seeAlso: ['umbrella_sanction']
	},
	{
		id: 'absorption_rate',
		term: 'Absorption rate',
		plain: 'How fast an agency turns money received into completed work — the share of funds that has been "absorbed" into physical delivery.',
		expert: 'Expenditure/utilisation as a fraction of funds released to an agency, over the stated period. A low rate signals idle funds or slow execution.',
		why: 'A department-level absorption bar on this site measures how much of each department\'s transfer has been deployed.',
		seeAlso: ['released_disbursed']
	},

	// ── Debt ──────────────────────────────────────────────────────────────────
	{
		id: 'article_293',
		term: 'Article 293(3)',
		plain: 'A part of India\u2019s Constitution: a state must ask the central government\u2019s Reserve Bank before borrowing from abroad or against its own lawmaking power — KIIFB borrowing is discussed in this light.',
		expert: 'Constitutional provision reserving foreign/certain interstate borrowing to the Union\u2019s consent via the RBI. The 2026 report treats Article 293(3) commitments as deductions from borrowing space (₹25,932.55 Cr).',
		why: 'Whether KIIFB loans count as state borrowing under this clause is the jointly-fought constitutional question on this site.',
		seeAlso: ['borrowing_space', 'evidence_label']
	},
	{
		id: 'borrowing_space',
		term: 'Borrowing space',
		plain: 'How much more a state could legally borrow: the annual ceiling set by central rules, minus promises already counted against the state.',
		expert: 'Residual headroom under RBI-indicative state borrowing targets after deductions (guarantees, off-budget borrowings, Article 293(3) commitments).',
		why: 'The committee argues KIIFB debt consumes ₹25,932.55 Cr of Kerala\u2019s space; the state disputes that framing.',
		seeAlso: ['article_293']
	},
	{
		id: 'masala_bond',
		term: 'Masala bond',
		plain: 'Loans raised abroad but repayable in rupees, not dollars — so exchange-rate risk stays with the investor. KIIFB raised such bonds overseas.',
		expert: 'INR-denominated offshore bonds (IFSC/SBI London issues by KIIFB). Coupon and spread are the priced terms; currency risk remains with the subscriber.',
		why: 'Terms of KIIFB\u2019s masala bonds (coupon, redemption) define part of the debt-service schedule shown here.',
		seeAlso: ['coupon_rate', 'debt_service', 'article_293']
	},
	{
		id: 'debt_service',
		term: 'Debt service',
		plain: 'The money due each year to repay loans: interest charges plus the portions of loan being paid back.',
		expert: 'Principal + interest payable per period. Table 6.1 of the committee report schedules ₹47,532.54 Cr of debt service across FY 2026-27 to 2041-42.',
		why: 'Debt service is a flow (each year) that must be met from the budget — the trajectory chart plots it against what transfer history suggests.',
		seeAlso: ['stock_vs_flow', 'amortisation', 'coupon_rate']
	},
	{
		id: 'amortisation',
		term: 'Amortisation schedule',
		plain: 'The year-by-year repayment timetable for a loan: how much of each instalment is interest versus principal.',
		expert: 'Bond/loan repayment table splitting service per period into interest and principal components (bullet, step-down, or annuity structures for KIIFB instruments).',
		why: 'The steep rise in repayment obligations after FY 2028 in the schedule comes from amortisation step-ups, not new borrowing.',
		seeAlso: ['debt_service', 'coupon_rate']
	},
	{
		id: 'coupon_rate',
		term: 'Coupon rate',
		plain: 'The fixed yearly interest rate a bond pays, written as a percentage of its face value.',
		expert: 'Contractual periodic interest rate on the instrument\u2019s face value; for bonds, payable irrespective of cash flow.',
		why: 'A bond\u2019s coupon fixes how much interest Kerala owes each year — a core input to the repayment schedule here.',
		seeAlso: ['debt_service', 'masala_bond', 'spread_bps']
	},
	{
		id: 'spread_bps',
		term: 'Spread (basis points)',
		plain: 'The extra interest over a safe benchmark rate expressed in hundredths of a percent: 1 basis point = 0.01%.',
		expert: 'Yield premium over reference curve (e.g. g-sec) demanded by investors as a risk price; 100 bps = 1 percentage point.',
		why: 'The spread on KIIFB bonds is market evidence of risk perception — part of the financial defence-and-rebuttal split on the debt pages.',
		seeAlso: ['masala_bond', 'coupon_rate']
	},
	{
		id: 'revenue_hypothecation',
		term: 'Revenue hypothecation',
		plain: 'Setting aside specific taxes in advance to repay a loan — the committed money is no longer available for other needs.',
		expert: 'Creation of a charge on designated revenue streams (e.g. Motor Vehicles Tax via Section 7 of the KIIFB Act) as debt-service securitisation.',
		why: 'This is KIIFB\u2019s repayment engine and also its critics\u2019 target: hypothecated fuel and vehicle taxes tighten the rest of the budget.',
		seeAlso: ['mvt', 'petroleum_cess', 'debt_service']
	},
	{
		id: 'mvt',
		term: 'Motor Vehicles Tax (MVT)',
		plain: 'The tax Kerala charges on registration and running of vehicles. Since the KIIFB Act, part of it is earmarked to repay KIIFB debt.',
		expert: 'State motor vehicles tax revenue assigned under Section 7 of the KIIFB Act 2016 into the KIIFB Fund as a dedicated servicing stream.',
		why: 'MVT hypothecation is why one rupee of vehicle tax is spent twice — a key trade-off plotted in the debt trajectory.',
		seeAlso: ['revenue_hypothecation', 'petroleum_cess']
	},
	{
		id: 'petroleum_cess',
		term: 'Petroleum cess',
		plain: 'An extra levy on fuel. A share of it is dedicated to repaying KIIFB loans rather than going to the general budget.',
		expert: 'State petroleum cess share hypothecated to KIIFB debt service alongside MVT under the hypothecation regime of the KIIFB Act.',
		why: 'Together with MVT, it forms the "own-source" repayment stream — the steady inflow shown against debt service.',
		seeAlso: ['revenue_hypothecation', 'mvt']
	},
	{
		id: 'budget_transfer',
		term: 'Budget transfer',
		plain: 'Yearly money the state budget has handed to KIIFB — the recurring inflow that covers interest after taxes fell short.',
		expert: 'Annual statutory transfer from the consolidated fund to KIIFB under the Act; 99.4% servicing coverage ratio per Tables 3.1/3.2 (committee).',
		why: 'The trajectory overlay contrasts these transfers with the scheduled repayments they must meet.',
		seeAlso: ['debt_service', 'revenue_hypothecation']
	},
	{
		id: 'strpp',
		term: 'STRPP',
		plain: 'A legal financing structure that channels a future income stream (like road tolls) to repay construction money today.',
		expert: 'Structured Transfer of Project Proceeds — securitisation-style structure routing designated receivables (e.g. BOT annuity/toll) to the lender.',
		why: 'Some KIIFB-financed corridors are structured via STRPPs; their income streams appear as dedicated repayment rows.',
		seeAlso: ['revenue_hypothecation']
	},

	// ── Delivery pipeline ─────────────────────────────────────────────────────
	{
		id: 'tender',
		term: 'Tender',
		plain: 'A public invitation for contractors to bid and quote prices for a work. It\u2019s the bridge between permission and construction.',
		expert: 'Formal procurement event initiating contract award; follows technical sanction; precedes work order (contract).',
		why: 'The delivery ladder runs Approved → Tendered → Contracted — a project stuck before "tendered" exists only on paper.',
		seeAlso: ['technical_sanction']
	},
	{
		id: 'dlp',
		term: 'DLP (Defect Liability Period)',
		plain: 'The guarantee period after handover — usually one to few years — during which the contractor must fix defects at its own cost.',
		expert: 'Post-completion period (CPWD/RPWD norms) in which the contractor remains liable for defects; final payments/retentions release after it.',
		why: "'Physically complete' is not done-done: unfixed DLP tails show why handovers alone overstate readiness.",
		seeAlso: ['dlp']
	},
	{
		id: 'kanakku',
		term: 'Kanakku',
		plain: 'A public Kerala PWD website listing thousands of work packages with their stage status. This site cross-checks KIIFB\u2019s claims against it.',
		expert: 'State PWD public works ledger (kanakku.kerala.gov.in) enumerating packages, stages and financials; used here as DS030 delivery ground truth with checksummed snapshots.',
		why: 'Kanakku is the delivery half of every contradiction or corroboration shown between report claims and status.',
		seeAlso: ['normalised_status', 'kite_sametham']
	},
	{
		id: 'kite_sametham',
		term: 'KITE Sametham',
		plain: 'A Kerala education-technology agency\u2019s programme upgrading thousands of government schools\u2019 infrastructure, funded through KIIFB.',
		expert: 'KITE (Kerala Infrastructure and Technology for Education) higher-education/ghss infrastructure programme; 969 records in the unified explorer.',
		why: 'Nearly half the project records here are KITE schools — so any average about projects is strongly shaped by school works.',
		seeAlso: ['counting_unit']
	},
	{
		id: 'pmas',
		term: 'KIIFB PMAS',
		plain: 'KIIFB\u2019s own project database on its website — one of three delivery sources this site merges and reconciles.',
		expert: 'Project Monitoring & Assessment System scrape (kiifb.kite.kerala.gov.in PMAS) — source of contractor/date/status fields in the merged explorer.',
		why: 'Where PMAS and Kanakku disagree, the record is marked "Sources disagree" rather than silently chosen.',
		seeAlso: ['kanakku', 'conflicting_evidence']
	},
	{
		id: 'normalised_status',
		term: 'Normalised status',
		plain: 'Each source describes stages differently, so this site maps them onto one shared ladder (approved → tendered → … → operational).',
		expert: 'Cross-dataset status canonicalisation via explicit per-source mapping rules (matched_rule in the match log), preserving the source_status_text for audit.',
		why: 'Status comparisons only mean something after normalisation — this site shows the rule it applied so you can contest it.',
		seeAlso: ['kanakku', 'pmas']
	},
	{
		id: 'err_firr',
		term: 'ERR / FIRR',
		plain: 'Two ways to judge whether a project is "worth it": against society\u2019s broader benefit (economic) or against the money invested (financial).',
		expert: 'Economic and Financial Internal Rate of Return — discount rates making net present value zero under economic shadow prices vs cash flows.',
		why: 'The committee questioned the optimistic rates used to justify some KIIFB projects; where appraisal rates are reported, they are shown for scrutiny.',
		seeAlso: ['capital_multiplier']
	},
	{
		id: 'capital_multiplier',
		term: 'Capital multiplier',
		plain: 'The argued boost to Kerala\u2019s economy from every rupee of infrastructure spending — supporters claim each borrowed rupee raises output (and tax revenue) by more than a rupee.',
		expert: 'Keynesian multiplier argument asserting k > 1.5–2.0 for capital outlays, funding debt service from incremental GSDP-linked receipts.',
		why: 'The debt-vs-growth argument in the report and the state\u2019s response both hang on how big this k is.',
		seeAlso: ['err_firr']
	},

	// ── Data quality / verification ───────────────────────────────────────────
	{
		id: 'evidence_label',
		term: 'Evidence taxonomy',
		plain: 'Every fact here carries a small tag saying where it comes from: official record, independently verified, committee finding, calculated estimate, disputed, unverified, or a gap.',
		expert: 'Seven-state provenance taxonomy (design-system.md §2.2) enforcing epistemic hierarchy across all surfaces.',
		why: 'The badge you see is the audit trail: never trust a number without checking which state it carries.',
		seeAlso: ['conflicting_evidence', 'gap_register']
	},
	{
		id: 'gap_register',
		term: 'Data gap register (GAP-001…004)',
		plain: 'A list of pieces of information the public was promised but nobody publishes — e.g. how much physical progress money produced. Gaps are listed, not guessed.',
		expert: 'Curated register of material unavailability: GAP-001 delivery-status coverage, GAP-002 physical progress, GAP-003 completion cost, GAP-004 social outcomes.',
		why: 'Absence is data here. Every chart that "looks empty" is rendered because a register entry says the underlying number does not exist.',
		seeAlso: ['gap_register']
	},
	{
		id: 'checksum',
		term: 'Checksum',
		plain: 'A digital fingerprint of a downloaded file. If the file changes by even one character, the fingerprint changes — proof the source wasn\u2019t silently altered.',
		expert: 'SHA-256 digest recorded per source snapshot in data/manifest.json, enabling bit-independent verification of archived evidence.',
		why: 'Checkouts let an expert rebuild every figure exactly as shown, months later, even if websites change.',
		seeAlso: ['snapshot']
	},
	{
		id: 'snapshot',
		term: 'Snapshot',
		plain: 'Frozen copies of the raw sources taken at a date (e.g. Oct 2026). Comparing snapshots shows what changed over time.',
		expert: 'Immutable archived crawl datasets under data/snapshots/ keyed by retrieval date; /trends derives all time-series from snapshot diffs, not memory.',
		why: 'Numbers only get meaning against a versioned baseline; snapshots are that baseline.',
		seeAlso: ['checksum', 'as_of_date']
	},
	{
		id: 'jaccard',
		term: 'Fuzzy name matching',
		plain: 'When the same project appears in different lists with slightly different names, the site matches them by textual similarity — and records the match so you can double-check it.',
		expert: 'Record linkage via token-Jaccard similarity thresholds with logged tiers (exact/s/high/med) in kanakku_match_log.json for auditability.',
		why: 'Merging KIIFB and PWD records involves judgement calls; the log makes every one contestable.',
		seeAlso: ['kanakku', 'pmas']
	},
	{
		id: 'conflicting_evidence',
		term: 'Sources disagree',
		plain: 'Two records give different answers for the same project. This site shows both instead of quietly picking one.',
		expert: 'Divergent assertions across ground-truth datasets (e.g. status text, financials, dates) surviving normalisation; flagged as record-level evidence state.',
		why: 'It is exactly these disagreements that make verification necessary — and possible.',
		seeAlso: ['normalised_status']
	}
];

const INDEX = new Map<string, GlossaryEntry>(GLOSSARY.map((e) => [e.id, e]));

/** Lookup by stable id. Throws in dev to fail loud on typos (build-time guard). */
export function getEntry(id: string): GlossaryEntry {
	const entry = INDEX.get(id);
	if (!entry) {
		throw new Error(`[glossary] unknown term id: "${id}"`);
	}
	return entry;
}

/** For /glossary search: filter on term + plain + expert. */
export function searchGlossary(query: string): GlossaryEntry[] {
	const q = query.trim().toLowerCase();
	if (!q) return GLOSSARY;
	return GLOSSARY.filter(
		(e) => e.term.toLowerCase().includes(q) || e.plain.toLowerCase().includes(q) || e.expert.toLowerCase().includes(q)
	);
}
