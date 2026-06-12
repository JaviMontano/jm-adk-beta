<!-- distilled from alfa skills/risk-assessment -->
<!-- Risk identification across 7 categories (technical, operational, security, scalability, data, team, timeline). Severity x likelihood. [EXPLICIT] -->
# risk-assessment {Analysis} (v1.1)
> **"Analyze with evidence. Every claim tagged. Every finding actionable."**
## Purpose
Risk identification across 7 categories. Severity x likelihood scoring. [EXPLICIT]
**When to use:** During analysis mode (MAO DNA), before architecture or development begins.
**Anti-scope:** Not a plan — no implementation steps, schedules, or owners-with-dates (those belong in plan mode, Art. 1.5). Not a security pentest. Not a final go/no-go decision (informs it). [EXPLICIT]
## Core Principles
1. **Law of Evidence:** Every finding tagged [CODE], [CONFIG], [DOC], [INFERENCE], or [ASSUMPTION] (R-001). [EXPLICIT]
2. **Law of Completeness:** No deliverable ships without all 7 categories addressed (or marked N/A with reason). [EXPLICIT]
3. **Law of Firebase Lens:** All assessments evaluated through Firebase/Google/Hostinger feasibility. [EXPLICIT]
## The 7 Categories [EXPLICIT]
| # | Category | Probe |
|---|----------|-------|
| 1 | Technical | unproven tech, coupling, tech debt, single points of failure |
| 2 | Operational | deploy/rollback, monitoring gaps, runbook absence, on-call |
| 3 | Security | authn/z, secrets handling, PII exposure, dependency CVEs |
| 4 | Scalability | load ceilings, N+1, quota/rate limits, cold-start cost |
| 5 | Data | integrity, migration, backup/restore, retention/residency |
| 6 | Team | bus factor, skill gaps, capacity, handoff/context loss |
| 7 | Timeline | external dependencies, estimate confidence, critical path |
## Scoring [EXPLICIT]
- **Severity** 1–5: 1 cosmetic · 3 degraded feature · 5 data loss / breach / launch-blocking.
- **Likelihood** 1–5: 1 rare · 3 plausible · 5 near-certain absent mitigation.
- **Score = Severity × Likelihood** (1–25). Bands: 1–6 Low · 8–12 Medium · 15–25 High → High requires named mitigation before sign-off. [INFERENCE]
- Tie-break: when two risks share a score, rank the higher-severity one first (impact dominates probability). [ASSUMPTION]
## Core Process
**Phase 1 — Gather:** Collect inputs (docs, code, conversations, existing systems); parse for requirements, constraints, context. [EXPLICIT]
**Phase 2 — Analyze:** Walk all 7 categories; tag each finding; score Severity × Likelihood; propose one mitigation per High/Medium. [EXPLICIT]
**Phase 3 — Document:** Emit the risk register (below) + evidence-tag summary (% by tag type). If >30% [ASSUMPTION], add WARNING banner. [EXPLICIT]
## Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Project context | Text/Files | Yes | What to analyze |
| Constraints/NFRs | Text | No | Sharpens severity calibration |

| Output | Type | Description |
|--------|------|-------------|
| Risk register | Markdown table | Evidence-tagged, scored, mitigated findings |
| Evidence summary | Markdown | % by tag type; WARNING if >30% [ASSUMPTION] |
### Risk register schema [EXPLICIT]
`| ID | Category | Risk | Sev | Lik | Score | Evidence | Mitigation |`
- IDs sequential per run: `RISK-001`. One row per distinct risk; do not merge categories. [EXPLICIT]
## Worked Example [EXPLICIT]
`| RISK-001 | Security | Firebase rules allow unauthenticated writes to /orders | 5 | 4 | 20 (High) | [CONFIG] firestore.rules:12 | Require request.auth != null; add owner check |`
→ Score 20 = High → mitigation named → eligible for sign-off. Evidence is [CONFIG] (read from rules file), not [ASSUMPTION], so it counts toward the high-confidence majority.
## Validation Gate
- [ ] All 7 categories addressed or marked N/A with reason
- [ ] Every finding has an evidence tag and Sev/Lik scores
- [ ] Every High/Medium risk has a named mitigation
- [ ] Firebase feasibility assessed
- [ ] Deliverable follows R-008 output standards
- [ ] No implementation details (phase separation, Art. 1.5)
## Self-Correction Triggers
> [!WARNING]
> IF >30% claims are [ASSUMPTION] THEN add prominent WARNING banner (evidence is thin). [EXPLICIT]
> IF analysis contains implementation details THEN move to plan (Art. 1.5 phase separation). [EXPLICIT]
> IF a category yields zero findings THEN state "no risks identified" explicitly — never silently omit (absence must be a deliberate, visible claim). [EXPLICIT]
## Failure Modes [INFERENCE]
| Symptom | Cause | Correction |
|---------|-------|------------|
| All risks scored 4–5 | severity inflation | re-anchor to the 1/3/5 rubric; reserve 5 for irreversible harm |
| Findings with no mitigation | stopped at identification | every Med/High gets a mitigation or is downgraded with rationale |
| Untagged claim | skipped R-001 | block deliverable until tagged |
| Category silently empty | scan gap | apply the zero-findings trigger above |
## Usage
- "/risk-assessment" — Run the full risk assessment workflow
- "risk assessment on this project" — Apply to current context
## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs); without them, findings default to [ASSUMPTION] and the WARNING banner likely triggers. [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Scoring is relative within one run, not an absolute cross-project benchmark. [ASSUMPTION]
- Does not replace domain-expert judgment for final go/no-go. [EXPLICIT]
## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Single category in scope (e.g. security-only) | Mark other 6 N/A with reason; gate still passes |
| Risk spans two categories | File under primary impact; cross-reference the other in the Risk text |
