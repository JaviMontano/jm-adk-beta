<!-- distilled from alfa skills/competitive-intelligence -->
<!-- Market analysis. Competitor feature matrix. Technical stack comparison. SWOT. Differentiation opportunities. [EXPLICIT] -->
# competitive-intelligence {Analysis} (v1.1)
> **"Analyze with evidence. Every claim tagged. Every finding actionable."**
## Purpose
Market analysis. Competitor feature matrix. Technical stack comparison. SWOT. Differentiation opportunities. [EXPLICIT]
**When to use:** During analysis mode (MAO DNA). Before architecture or development begins. [EXPLICIT]
**Anti-scope (do NOT do here):** pricing tables, implementation/architecture choices, go-to-market plans, vendor selection. Those belong to plan/pricing-strategy skills (Art. 1.5 phase separation). [EXPLICIT]
## Core Principles
1. **Law of Evidence:** Every finding tagged [CODE], [CONFIG], [DOC], [INFERENCE], or [ASSUMPTION] (R-001). A competitor claim with no public source is [INFERENCE] at best, never [DOC]. [EXPLICIT]
2. **Law of Completeness:** No deliverable ships without all required sections (matrix, stack, SWOT, differentiation). [EXPLICIT]
3. **Law of Firebase Lens:** All assessments evaluated through Firebase/Google/Hostinger feasibility. [EXPLICIT]
## Core Process
### Phase 1: Gather
1. Collect inputs (documents, code, conversations, existing systems). [EXPLICIT]
2. Parse for requirements, constraints, and context. [EXPLICIT]
3. Name the competitor set + selection reason; record source URL/date per competitor (staleness > 12mo → tag [ASSUMPTION]). [EXPLICIT]
### Phase 2: Analyze
1. Apply domain-specific analysis methodology. [EXPLICIT]
2. Tag all findings with evidence tags. [EXPLICIT]
3. Score/evaluate using the skill's specific metrics (see Scoring). [EXPLICIT]
### Phase 3: Document
1. Produce the analysis deliverable in markdown. [EXPLICIT]
2. Include evidence tag summary (% by tag type). [EXPLICIT]
3. If >30% [ASSUMPTION], add WARNING banner. [EXPLICIT]
## Scoring (feature matrix + SWOT)
- Feature cell values: `Yes` / `No` / `Partial` / `Unknown` — `Unknown` forces an [ASSUMPTION] or [INFERENCE] tag; never silently treat as `No`. [INFERENCE]
- Differentiation = capabilities where our position is `Yes` and ≥50% of the competitor set is `No`/`Partial`, ranked by feasibility under the Firebase Lens. [INFERENCE]
- SWOT: each entry one line, evidence-tagged; Opportunities/Threats must trace to a matrix row or a [DOC] source, not free-form opinion. [EXPLICIT]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Project context | Text/Files | Yes | What to analyze |
| Competitor set | List | No | Defaults to inferred set from context; flag as [INFERENCE] |
| Output | Type | Description |
|--------|------|-------------|
| Analysis deliverable | Markdown | Evidence-tagged feature matrix + stack + SWOT + differentiation |
## Worked example (feature matrix excerpt)
| Capability | Us | Comp-A | Comp-B | Evidence |
|------------|----|--------|--------|----------|
| Realtime sync | Yes | Partial | No | [DOC] vendor docs 2026-05 |
| On-device ML | No | Yes | Unknown | Comp-B unverified → [ASSUMPTION] |
→ Differentiation candidate: *Realtime sync* (us `Yes`, set mostly `Partial`/`No`), feasible on Firebase RTDB/Firestore. [INFERENCE]
## Acceptance criteria (deliverable is DONE when)
- [ ] ≥3 competitors OR an explicit [ASSUMPTION] noting why fewer. [EXPLICIT]
- [ ] Every matrix cell + SWOT line carries an evidence tag; no untagged claims. [EXPLICIT]
- [ ] Evidence tag summary present; WARNING banner if >30% [ASSUMPTION]. [EXPLICIT]
- [ ] Each differentiation opportunity is actionable and Firebase-feasibility noted. [EXPLICIT]
- [ ] Zero implementation/pricing detail (phase + anti-scope separation). [EXPLICIT]
## Validation Gate
- [ ] All findings have evidence tags
- [ ] Firebase feasibility assessed
- [ ] Deliverable follows R-008 output standards
- [ ] No implementation details (phase separation)
- [ ] Actionable recommendations included
## 5. Self-Correction Triggers
> [!WARNING]
> IF >30% claims are [ASSUMPTION] THEN add prominent WARNING banner.
> IF analysis contains implementation details THEN move to plan (Art. 1.5 phase separation).
> IF a competitor capability is unverifiable THEN mark `Unknown` + [ASSUMPTION], never assume parity or absence.

## Usage

Example invocations:

- "/competitive-intelligence" — Run the full competitive intelligence workflow
- "competitive intelligence on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Snapshot in time: findings decay as competitors ship; date-stamp the deliverable [EXPLICIT]
- No paywalled/non-public competitor internals — those stay [ASSUMPTION]/[INFERENCE] [EXPLICIT]

## Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Single / no real competitor | State market-creation posture; SWOT vs. status-quo alternative, tag [INFERENCE] |
| Stale or undated source | Tag [ASSUMPTION]; note staleness; do not present as [DOC] |
| Marketing copy as the only source | Treat as vendor claim ([DOC] of a *claim*, not of fact); seek corroboration |
| Drifts into pricing/architecture | Stop; redirect to pricing/plan skill per anti-scope |
