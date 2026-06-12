<!-- distilled from alfa skills/contract-review -->
<!-- > -->
# Contract Review
> "Method over hacks."

## TL;DR
Systematic review of a contract: extract terms, flag risk clauses, surface negotiation levers, and define renewal/exit strategy — each finding carries a provenance tag and a recommended action. [DOC]

## Scope & Anti-Scope
- IN: clause-by-clause analysis, risk ranking, redline-ready negotiation points, renewal/termination timeline. [DOC]
- OUT: legal advice or sign-off — output is decision support, not a substitute for licensed counsel. [SUPUESTO]
- OUT: drafting net-new contracts (use a drafting skill); jurisdiction-specific enforceability opinions. [DOC]

## Procedure
### Step 1: Discover
- Identify parties, effective date, term, governing law, and the contract's commercial intent. [DOC]
- Flag any missing or unsigned exhibits/schedules before analysis — they often carry the real obligations. [INFERENCIA]

### Step 2: Analyze — clause checklist
Walk these high-leverage clauses; for each, capture the term as written and the risk it creates:
- **Liability & indemnity** — caps, carve-outs, uncapped categories (IP, confidentiality, data breach). Uncapped + broad indemnity = top risk. [INFERENCIA]
- **Termination** — for-convenience vs for-cause, notice period, cure window, survival clauses. [DOC]
- **Auto-renewal** — renewal term, opt-out notice deadline, price-escalation on renewal. [DOC]
- **Payment** — amounts, schedule, late fees, currency, change-of-price triggers. [DOC]
- **IP & license** — ownership of deliverables, license scope, residuals, feedback grants. [DOC]
- **Confidentiality / data** — definition breadth, term, return/destruction, sub-processor and breach-notice duties. [DOC]
- **Limitation of remedies, warranty/disclaimer, assignment, dispute resolution (venue, arbitration), force majeure.** [DOC]

### Step 3: Execute — produce findings
- One row per finding: clause · risk level (High/Med/Low) · plain-language impact · recommended redline · provenance tag. [DOC]
- Rank by exposure (likelihood × business impact), not by clause order. [INFERENCIA]

### Step 4: Validate
- Confirm every High finding has a concrete fallback position the counterparty might accept. [INFERENCIA]

## Worked Example (one finding)
> Clause 8.2 caps liability at fees paid, but Clause 8.4 carves out "any breach of confidentiality" as uncapped. Impact: a single data-handling slip becomes unlimited exposure. Redline: cap confidentiality breaches at a multiple of annual fees (e.g. 2–3x), excluding only willful misconduct. Risk: High. [INFERENCIA]

## Usage
Example invocations:
- "/contract-review" — Run the full contract review workflow
- "contract review on this MSA" — Apply to the attached/current document

## Assumptions & Limits
- Assumes the full executed contract plus all referenced exhibits/schedules are available. [SUPUESTO]
- English-language output unless otherwise specified. [SUPUESTO]
- Does not replace counsel's judgment for final sign-off or jurisdiction-specific enforceability. [DOC]
- Single governing-law assumption; multi-jurisdiction contracts need per-jurisdiction review. [SUPUESTO]

## Quality Criteria
- [ ] Every clause in the Step-2 checklist is addressed or explicitly marked N/A. [DOC]
- [ ] Each finding has risk level, impact, recommended action, and a provenance tag. [DOC]
- [ ] High findings each carry a negotiable fallback position. [DOC]
- [ ] No invented terms — anything not in the text is tagged `[SUPUESTO]` with a verification step. [DOC]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Missing exhibit/schedule | Stop; list what's missing and request before risk-ranking — obligations may live there. [INFERENCIA] |
| Unsigned or draft version | Flag as draft; mark findings provisional pending the executed copy. [SUPUESTO] |
| Conflicting clauses (e.g. cap vs carve-out) | Surface the conflict explicitly; analyze worst-case interpretation. [INFERENCIA] |
| Governing law unstated | Flag as critical gap; do not assume a jurisdiction. [DOC] |
| Auto-renewal opt-out already lapsed | Escalate immediately — deadline-driven, may bind the next term. [INFERENCIA] |
| Out-of-scope (e.g. drafting) | Redirect to the appropriate skill or escalate to counsel. [DOC] |
