<!-- distilled from alfa skills/sector-intelligence -->
<!-- > -->
# Sector Intelligence

> "In every industry, there is a set of unwritten rules that determine who wins." — Clayton Christensen

## TL;DR

Provides deep industry-specific context — regulatory requirements, sector terminology, common business processes, and technology adoption patterns — for verticals like healthcare, fintech, retail, education, and government. Use when entering a new vertical or when domain-knowledge gaps block progress. [DOC]

## Scope & Anti-Scope

- IN: vertical domain context that shapes technology decisions — regulation, glossary, value chains, adoption maturity, sector integration rails. [DOC]
- OUT: per-competitor teardown (use `competitive-intelligence`); audit-grade compliance attestation (use `compliance-assessment`); legal advice or binding regulatory interpretation. [DOC]
- LIMIT: outputs are decision-support, not certification. Regulatory claims are point-in-time and jurisdiction-bound; they expire. [SUPUESTO] — verify by re-checking the regulator's primary source before any go/no-go.

## Assumptions

- A specific vertical AND jurisdiction are named before analysis starts; "global" is not a jurisdiction. [SUPUESTO] — if absent, stop and ask.
- A client domain expert is reachable for validation in Step 4. [SUPUESTO] — if not, mark findings `[ASSUMPTION]` and lower confidence.

## Procedure

### Step 1: Discover
- Identify the target vertical AND sub-segment (e.g. "fintech → cross-border B2B payments", not "fintech"). [DOC]
- Gather client context: company size, market position, digital maturity. [CONFIG]
- Research current regulatory environment and pending changes, scoped to jurisdiction. [DOC]
- Identify industry associations, standards bodies, certification requirements. [DOC]

### Step 2: Analyze
- Map sector business processes and value chains. [DOC]
- Identify regulations that constrain technology decisions (data residency, audit trails, consent). [DOC]
- Assess adoption maturity: cloud readiness, digital-channel penetration, legacy lock-in. [INFERENCE]
- Analyze sector risks: seasonal demand, regulatory flux, supply-chain concentration. [INFERENCE]
- Research competitor stacks and transformation patterns (handoff to `competitive-intelligence` for depth). [DOC]

### Step 3: Execute
- Produce an industry context brief with a terminology glossary. [DOC]
- Document a regulatory matrix: requirement, source, jurisdiction, deadline, tech impact. [DOC]
- Create a technology landscape map naming real vendors/solutions. [DOC]
- Write recommendations referencing sector best practices, each tagged. [DOC]
- Identify integration requirements (payment rails, health records, government APIs). [DOC]

### Step 4: Validate
- Verify regulatory info is current and jurisdiction-specific against the primary regulator source. [DOC]
- Confirm terminology matches industry usage, not generic tech terms. [DOC]
- Cross-reference analyst reports and trade publications. [DOC]
- Validate with a client domain expert; record date validated. [SUPUESTO]

## Decisions & Trade-offs

- Breadth vs depth: default to one named sub-segment over a whole vertical — generic sector briefs are the top failure mode (see Anti-Patterns). [INFERENCE] Trade-off: narrower coverage, far higher actionability.
- Recency vs effort: regulatory claims demand primary-source re-check even when an analyst report already states them; analysts lag rule changes. [INFERENCE] Trade-off: slower, but avoids compliance risk.

## Worked Example (fintech, EU cross-border payments)

Sub-segment: B2B cross-border payments, EU. Regulatory matrix row → "PSD2 SCA | EU primary source | applies to payer auth | tech impact: 3-D Secure + exemption engine". [DOC] Glossary disambiguates "settlement" (interbank) from "clearing". [DOC] Integration: SEPA Instant rails, not generic "bank API". [DOC] Recommendation: tag adoption-maturity claim `[INFERENCE]` unless the client confirms current rails. [INFERENCE]

## Edge Cases

- Multi-jurisdiction client: produce one matrix per jurisdiction; never merge conflicting rules into one row. [DOC]
- Emerging sub-sector with no standards body yet: mark the landscape `[ASSUMPTION]` and flag volatility. [SUPUESTO]
- Regulation in active transition (draft → enacted): cite both states with effective dates; do not present draft as binding. [DOC]

## Failure Modes

- Generic brief: sector named, sub-segment skipped → recommendations are interchangeable filler. Mitigate via the breadth-vs-depth decision. [INFERENCE]
- Stale regulation: reused from a prior engagement without date check → compliance risk. Mitigate via Step 4 primary-source re-check. [SUPUESTO]
- Tag inflation: every line tagged `[ASSUMPTION]` to dodge research → defeats provenance. One tag per claim, weakest applicable. [DOC]
- Family mixing: never combine Alfa `[..]` tags with Jarvis `{..}` tags in one document. [DOC]

## Quality / Acceptance Criteria

- [ ] A named sub-segment AND jurisdiction are stated. [DOC]
- [ ] Terminology is accurate with a glossary provided. [DOC]
- [ ] Regulatory requirements are current, jurisdiction-specific, and primary-sourced. [DOC]
- [ ] Technology landscape maps real vendors, not categories. [DOC]
- [ ] Recommendations reference sector best practices. [DOC]
- [ ] Every non-obvious claim carries exactly one Alfa-set evidence tag. [DOC]
- [ ] Each `[ASSUMPTION]` is paired with a concrete verification step. [DOC]

## Anti-Patterns

- Applying generic solutions without sector-specific adaptation. [DOC]
- Outdated regulatory information creating compliance risk. [DOC]
- Ignoring sector data-residency and sovereignty requirements. [DOC]

## Related Skills

- `competitive-intelligence` — technology landscape within the sector
- `compliance-assessment` — sector-specific regulatory compliance
- `domain-driven-design` — sector terminology informs ubiquitous language
