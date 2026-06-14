<!-- distilled from alfa skills/stakeholder-mapping -->
<!-- Influence/interest matrix. RACI matrix. Communication plan. Power/interest grid. Stakeholder registry. [EXPLICIT] -->
# stakeholder-mapping {Analysis} (v1.0)
> **"Analyze with evidence. Every claim tagged. Every finding actionable."**
## Purpose
Produce four linked artifacts: a stakeholder **registry**, a **power/interest grid**, a **RACI matrix**, and a **communication plan** — so delivery decisions name an accountable owner and no influential party is engaged late. [EXPLICIT]
**When to use:** Analysis mode (MAO DNA), before architecture or development. Re-run at every scope change, re-org, or steering escalation — stakeholder maps decay. [INFERENCE]
**Anti-scope:** Not org-chart reproduction, not a contact list, not RACI for every task (reserve RACI for decisions and deliverables, not routine work). [INFERENCE]
## Core Principles
1. **Law of Evidence:** Every finding tagged [CODE], [CONFIG], [DOC], [INFERENCE], or [ASSUMPTION] (R-001). [EXPLICIT]
2. **Law of Completeness:** No analysis deliverable ships without covering all required sections. [EXPLICIT]
3. **Law of Firebase Lens:** All assessments evaluated through Firebase/Google/Hostinger feasibility. [EXPLICIT]
4. **One Accountable per row:** Exactly one `A` per RACI row; multiple `A` = diffused ownership and is a defect, not a style choice. [INFERENCE]
## Core Process
### Phase 1: Gather
1. Collect inputs (documents, code, conversations, existing systems, org chart, prior steering minutes). [EXPLICIT]
2. Identify stakeholders: sponsors, approvers, users, operators, regulators, vendors, blockers. Include the silent-but-powerful (e.g. security, legal, finance). [INFERENCE]
### Phase 2: Analyze
1. Score each stakeholder on **power** (can they fund/halt/redirect?) and **interest** (how much does the outcome affect them?), each High/Low. [EXPLICIT]
2. Place on the grid → derive an engagement posture per quadrant (table below). [EXPLICIT]
3. Assign RACI per key decision/deliverable; tag every finding with an evidence tag. [EXPLICIT]
### Phase 3: Document
1. Produce registry + grid + RACI + comms plan in markdown. [EXPLICIT]
2. Include evidence tag summary (% by tag type). If >30% [ASSUMPTION], add WARNING banner. [EXPLICIT]

## Power / Interest Grid
| Quadrant | Power | Interest | Posture | Cadence |
|----------|-------|----------|---------|---------|
| Manage Closely | High | High | Co-design; secure active buy-in | Weekly 1:1 + steering |
| Keep Satisfied | High | Low | Brief crisply; never surprise | Steering / milestone |
| Keep Informed | Low | High | Consult; harvest detail | Newsletter / demo |
| Monitor | Low | Low | Minimal effort; watch for shifts | On-demand |

A stakeholder's quadrant is a working hypothesis, not a fact — re-score when behavior contradicts placement. [ASSUMPTION] (verify: confirm power/interest with the sponsor each steering cycle).
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Project context | Text/Files | Yes | What to analyze |
| Org chart / roster | Text/Files | No | Seeds stakeholder discovery; absence raises [ASSUMPTION] rate |
| Output | Type | Description |
|--------|------|-------------|
| Registry | Markdown table | Per stakeholder: name, role, power, interest, quadrant, owner |
| Grid + RACI + comms plan | Markdown | Engagement posture, decision ownership, cadence |

**Registry schema** (one row per stakeholder): `name · role · power(H/L) · interest(H/L) · quadrant · stance(champion/neutral/blocker) · relationship owner · evidence tag`. [EXPLICIT]

**RACI legend:** R = does the work, A = single accountable sign-off, C = consulted before, I = informed after. Rule: every row has ≥1 R and exactly 1 A; minimize C (consultation is the hidden schedule cost). [INFERENCE]

## Worked Example
Decision: "Adopt Firebase Auth vs. custom IdP."
| Stakeholder | Power | Interest | Quadrant | RACI |
|-------------|-------|----------|----------|------|
| VP Eng (sponsor) | H | H | Manage Closely | A |
| Security lead | H | L | Keep Satisfied | C |
| Auth squad | L | H | Keep Informed | R |
| Support team | L | L | Monitor | I |
Read: squad builds (R), VP signs off (A), security must be consulted before (C) — skipping that C is the classic late-veto failure. [INFERENCE]

## Validation Gate
- [ ] Every stakeholder placed in exactly one quadrant with a relationship owner
- [ ] Every RACI row has exactly one A and ≥1 R
- [ ] High-power stakeholders each have a named cadence (no High-power left in "Monitor" by omission)
- [ ] All findings have evidence tags; Firebase feasibility assessed
- [ ] No implementation details (phase separation); actionable recommendations included (R-008)
## 5. Self-Correction Triggers
> [!WARNING]
> IF >30% claims are [ASSUMPTION] THEN add prominent WARNING banner.
> IF analysis contains implementation details THEN move to plan (Art. 1.5 phase separation).
> IF any RACI row has 0 or >1 `A` THEN reassign until exactly one. [INFERENCE]
> IF a High-power stakeholder lacks a cadence THEN engagement gap — fix before ship. [INFERENCE]
> IF a known blocker is absent from the registry THEN re-run Gather; silent blockers surface at steering, too late. [INFERENCE]

## Usage

Example invocations:

- "/stakeholder-mapping" — Run the full stakeholder mapping workflow
- "stakeholder mapping on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No org chart available | Map from conversation/docs; tag inferred stakeholders [ASSUMPTION], flag for sponsor confirmation |
| One person holds many roles | Split into role-rows, not person-rows — RACI is by role, conflicts (same person R and A) become visible |
| Two stakeholders, equal power, opposed stance | Do not average — surface as a decision for the sponsor (the A) to resolve |
| Stakeholder declines to engage | Record stance=blocker, escalate via the Keep-Satisfied path; absence of input is itself a finding [INFERENCE] |
