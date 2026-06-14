<!-- distilled from alfa skills/feasibility-validation -->
<!-- > -->
# Feasibility Validation

> "The first 90% of the code accounts for the first 90% of the development time. The remaining 10% accounts for the other 90%." — Tom Cargill

## TL;DR

Assesses technical feasibility across 7 dimensions — architecture, team capability, timeline, cost, risk, integration complexity, scalability — to produce a go / no-go / conditional-go recommendation with an explicit confidence level. Use BEFORE committing to a technical approach, responding to an RFP, or greenlighting an initiative. [EXPLICIT]

**Not a substitute for:** detailed effort estimation (`cost-estimation`), deep risk modeling (`risk-assessment`), or final domain-expert sign-off. Feasibility answers "can this be built as scoped, by this team, in this window?" — not "should we build it?" (business case) nor "what will it cost to the dollar?" [INFERENCE]

## Procedure

### Step 1: Discover
- Define the unit under assessment (feature, system, migration, product) and its hard boundaries. [EXPLICIT]
- Gather constraints: technical (stack, NFRs), team profiles, timeline expectations, budget envelope. Each missing input is a `[ASSUMPTION]` that lowers confidence — log it.
- Identify reference architectures, PoCs, or analogous past implementations as evidence anchors.

### Step 2: Analyze — score each dimension 1–5

| # | Dimension | Question | 1 (red) | 3 (amber) | 5 (green) |
|---|-----------|----------|---------|-----------|-----------|
| 1 | Architecture | Do existing patterns support this? | Needs unproven net-new architecture | Extends known patterns with gaps | Fits proven patterns as-is |
| 2 | Team Capability | Has the team the skills? | Core skill absent, no ramp path | Ramp needed, mentor available | Skills in-house, demonstrated |
| 3 | Timeline | Is the schedule realistic vs velocity? | >50% over capacity | Tight, no slack | Fits with buffer |
| 4 | Cost | Effort within budget? | Exceeds envelope | At envelope, no contingency | Within envelope + contingency |
| 5 | Risk | Top-5 risks mitigable? | ≥1 unmitigable showstopper | Mitigations exist, unproven | All risks have proven mitigations |
| 6 | Integration | Third-party/legacy complexity? | Undocumented/unstable interfaces | Documented but brittle | Stable, well-documented APIs |
| 7 | Scalability | Handles projected load growth? | No headroom, redesign likely | Scales with known effort | Scales within current design |

Score against evidence, not optimism. A dimension with no evidence defaults to ≤3 and is tagged `[ASSUMPTION]`. [INFERENCE]

### Step 3: Execute — synthesize
- **Scorecard:** per-dimension score + one-line evidence-backed justification + overall.
- **Decision rule** (default; state any override): any dimension = 1 → **no-go** or **conditional-go** gated on resolving that dimension; mean ≥ 4 and no dimension < 3 → **go**; otherwise → **conditional-go** with named conditions. Trade-off to state explicitly: a strict rule front-loads honesty but can block high-value bets — record the override rationale when leadership accepts a red dimension. [INFERENCE]
- **Risk register:** top-5 risks with probability (L/M/H), impact (L/M/H), owner, and an *actionable* mitigation (a task, not a hope).
- **Confidence %:** lower it for each `[ASSUMPTION]`-tagged dimension and each missing input; state the single biggest unknown.

### Step 4: Validate
- Each dimension score traces to evidence (`[CODE]`/`[CONFIG]`/`[DOC]`); unsupported scores revert to `[ASSUMPTION]`.
- Mitigations are actionable, owned, and time-boundable — not aspirational.
- Timeline checked against actual team velocity data, not planned velocity.
- Review with technical leads for blind spots; an unreviewed assessment caps confidence at ~70%. [ASSUMPTION] — verify by securing one independent lead review.

## Worked example (abbreviated)

Migrating a monolith auth module to a managed IdP, 2-sprint window:
Architecture 4 [DOC ref-arch exists] · Team 2 [no SAML experience, no mentor] · Timeline 2 [velocity says 4 sprints] · Cost 3 · Risk 3 [token-migration rollback unproven] · Integration 4 · Scalability 5.
Mean 3.3, two dimensions = 2 → **conditional-go**: gate on (a) a SAML spike + external mentor for Team, (b) re-baseline to 4 sprints for Timeline. Confidence 60% — biggest unknown is rollback safety. [INFERENCE]

## Quality Criteria
- [ ] All 7 dimensions scored with evidence-backed justification
- [ ] Top-5 risks with probability, impact, owner, mitigation
- [ ] Showstoppers explicitly called out with resolution paths
- [ ] Recommendation states confidence level and the biggest unknown
- [ ] Every claim carries one tag from a single family (see `references/verification-tags.md`)

## Anti-Patterns & Failure Modes
- **Feasibility theater:** going through motions toward a predetermined conclusion — detect via scores that all cluster at 4–5 with thin evidence.
- **Capability hand-wave:** assuming skills are acquired instantly; treat ramp-up as schedule cost, not a footnote.
- **Legacy-integration optimism:** undocumented interfaces score ≤2 until proven by a spike.
- **Green-washing:** never present a score as "success." A 5 means low risk on that axis, not a guarantee. [EXPLICIT]
- **Average hides a showstopper:** a single 1 can sink a project even with mean 4 — apply the decision rule, never eyeball the mean.

## Related Skills
- `cost-estimation` — detailed effort estimation for feasible approaches
- `risk-assessment` — deeper risk analysis beyond feasibility scope
- `scenario-analysis` — evaluating alternative approaches when feasibility is mixed

## Usage
- `/feasibility-validation` — run the full workflow
- "feasibility validation on this project" — apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs); absent these, output is `[ASSUMPTION]`-heavy and confidence is capped. [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for the final decision, nor produce pricing — effort is expressed in FTE-time, never currency. [EXPLICIT]
- Scoring is point-in-time; re-run if scope, team, or constraints change materially. [INFERENCE]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding; do not auto-fill past a critical gap |
| Conflicting requirements | Flag conflicts explicitly, propose resolution, score affected dimensions ≤3 |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No velocity data | Timeline scores `[ASSUMPTION]`; recommend a one-sprint calibration spike |
| Leadership overrides a red dimension | Honor it, but record the accepted risk and named owner in the register |
| All scores identical | Treat as a theater signal; re-examine evidence before issuing a recommendation |
