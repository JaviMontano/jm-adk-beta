<!-- distilled from alfa skills/cost-estimation -->
<!-- FTE-month estimation (NEVER prices). Effort inductors. Scope drivers. Confidence ranges (optimistic/expected/pessimistic). [EXPLICIT] -->
# cost-estimation {Analysis} (v1.1)
> **"Analyze with evidence. Every claim tagged. Every finding actionable."**
## Purpose
FTE-month estimation (NEVER prices). Effort inductors. Scope drivers. Confidence ranges (optimistic/expected/pessimistic). [EXPLICIT]
**When to use:** During analysis mode (MAO DNA). Before architecture or development begins.
**Anti-scope (do NOT do here):** monetary figures/rates/currency; implementation design (→ architecture); staffing names; vendor selection; final go/no-go (that's a decision owner's call). [EXPLICIT]
## Core Principles
1. **Law of Evidence:** Every finding tagged [CODE], [CONFIG], [DOC], [INFERENCE], or [ASSUMPTION] (R-001). [EXPLICIT]
2. **Law of Completeness:** No analysis deliverable ships without covering all required sections. [EXPLICIT]
3. **Law of Firebase Lens:** All assessments evaluated through Firebase/Google/Hostinger feasibility. [EXPLICIT]
4. **Law of No Prices:** Output is FTE-months only — never derive cost. Rates are not inputs and not outputs. [EXPLICIT]
## Estimation Method
Estimate in **FTE-months** = (effort inductors × scope multipliers) per workstream, then aggregate.
**Effort inductors** (size signals, evidence-tagged): entities/data models, integrations/external APIs, screens/flows, non-functional reqs (security, perf, compliance), migration/data volume, environments. [EXPLICIT]
**Scope multipliers** (×factor on base): novelty/unknowns, team ramp-up, regulatory burden, legacy coupling, test depth. State each factor and its justification. [INFERENCE]
**Confidence range** per workstream and total:
| Band | Basis | Use |
|------|-------|-----|
| Optimistic | Few unknowns realize; inductors at low bound | Best case only |
| Expected | Most likely; the headline number | Planning baseline |
| Pessimistic | Unknowns + multipliers compound | Buffer/risk reserve |
Report all three; never a single point. Spread (pess − opt) is itself a signal — wide spread ⇒ more discovery needed before commitment. [EXPLICIT]
## Core Process
### Phase 1: Gather
1. Collect inputs (documents, code, conversations, existing systems). [EXPLICIT]
2. Parse for requirements, constraints, and context; list each as an inductor or multiplier. [EXPLICIT]
### Phase 2: Analyze
1. Quantify inductors per workstream; tag each with evidence. [EXPLICIT]
2. Apply and justify each scope multiplier. [EXPLICIT]
3. Compute optimistic/expected/pessimistic FTE-months; aggregate to total. [EXPLICIT]
### Phase 3: Document
1. Produce the analysis deliverable in markdown with the estimate table. [EXPLICIT]
2. Include evidence tag summary (% by tag type). [EXPLICIT]
3. If >30% [ASSUMPTION], add WARNING banner. [EXPLICIT]
## Worked Example (illustrative, [ASSUMPTION] inputs)
| Workstream | Inductors | Mult. | Opt | Exp | Pess |
|-----------|-----------|-------|-----|-----|------|
| Auth + onboarding | 1 IdP integ, 4 screens | ×1.2 novelty | 1.5 | 2.0 | 3.5 |
| Core CRUD | 6 entities, 10 screens | ×1.0 | 3.0 | 4.0 | 6.0 |
| Data migration | 1 legacy DB, ~5 tables | ×1.5 unknowns | 1.0 | 2.0 | 4.5 |
| **Total** | — | — | **5.5** | **8.0** | **14.0** |
Read as: "~8 FTE-months expected; commit no tighter than the 8–14 band until migration scope is confirmed." [INFERENCE]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Project context | Text/Files | Yes | What to analyze |
| Workstream breakdown | Text | No | If absent, derive from inductors |
| Output | Type | Description |
|--------|------|-------------|
| Analysis deliverable | Markdown | Evidence-tagged FTE-month estimate with confidence bands |
## Validation Gate
- [ ] All findings have evidence tags
- [ ] Firebase feasibility assessed
- [ ] Deliverable follows R-008 output standards
- [ ] No implementation details (phase separation)
- [ ] Output is FTE-months only — zero monetary figures
- [ ] Optimistic/expected/pessimistic stated for every workstream and total
- [ ] Each scope multiplier carries a justification
- [ ] Actionable recommendations included
## 5. Self-Correction Triggers
> [!WARNING]
> IF >30% claims are [ASSUMPTION] THEN add prominent WARNING banner.
> IF analysis contains implementation details THEN move to plan (Art. 1.5 phase separation).
> IF any monetary figure appears THEN strip it and re-express as FTE-months (Law of No Prices).
> IF only a single number is given THEN reject — confidence range is mandatory.

## Usage

Example invocations:

- "/cost-estimation" — Run the full cost estimation workflow
- "cost estimation on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- FTE-month assumes a standard productive month; calendar duration depends on parallelism/team size and is out of scope here [ASSUMPTION]
- Estimate is a snapshot; re-run when scope or inductors change materially [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| User asks for a price/budget | Decline; deliver FTE-months + disclaimer (Law of No Prices) |
| Unknowns dominate (wide opt↔pess spread) | Recommend discovery spike before committing a number |
| No workstream breakdown given | Derive workstreams from inductors; mark [INFERENCE] |
