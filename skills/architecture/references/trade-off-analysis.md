<!-- distilled from alfa skills/trade-off-analysis -->
<!-- > -->
# Trade-Off Analysis

> "Every architecture is the result of trade-offs, whether conscious or not." — Mark Richards

## TL;DR

Performs structured trade-off analysis using weighted scoring matrices, decision matrices, and ATAM to make explicit, defensible architectural and technology decisions. Use when facing architectural trade-offs (consistency vs. availability, flexibility vs. simplicity), choosing between technologies, or when the team disagrees on approach. [EXPLICIT]

**Use when:** ≥2 viable options exist and the choice is contested or hard to reverse. **Skip when:** the decision is trivial, reversible at near-zero cost (a "two-way door"), or already constrained to one option by hard requirements — record a one-line ADR and move on. [INFERRED]

## Procedure

### Step 1: Discover
- Define the decision and the options under consideration (name 3+; if only 2, add "do nothing" / "defer" as a baseline). [INFERRED]
- Identify quality attributes at stake (performance, security, maintainability, cost).
- Gather constraints: budget, timeline, team skills, existing commitments.
- Collect stakeholder priorities: which quality attributes matter most, and *who* owns each.

### Step 2: Analyze
- Apply ATAM method:
  1. Present the business drivers and architectural approaches
  2. Identify architectural approaches and their associated quality attributes
  3. Generate quality attribute scenarios (stimulus, response, measure)
  4. Analyze approaches against scenarios to identify sensitivity points and trade-offs
- Build a weighted decision matrix with stakeholder-validated weights (weights sum to 1.0 or 100%). [INFERRED]
- Score each option per criterion on a fixed scale (e.g., 1–5) with one line of rationale per cell; weighted score = Σ(weight × score). [INFERRED]
- Identify risks: where a decision could cause problems.
- Find sensitivity points: where small changes significantly impact quality attributes.

### Step 3: Execute
- Produce a decision matrix with alternatives scored against weighted criteria.
- Document trade-off pairs: "We chose X over Y because Z quality attribute is more critical."
- Write an Architecture Decision Record (ADR) capturing context, decision, consequences.
- Create a risk catalog from identified sensitivity points and trade-offs.
- Provide a recommendation with confidence level and explicit conditions for revisiting (the trigger to re-open the decision). [INFERRED]

### Step 4: Validate
- Verify weights reflect actual stakeholder priorities, not assumed ones.
- Confirm scoring is evidence-based with supporting rationale per cell.
- Check that the analysis reveals genuine trade-offs (not a predetermined conclusion).
- Sensitivity check: perturb each weight ±20%; if the winner flips, the result is fragile — flag it and widen the evidence base before recommending. [INFERRED]

## Worked Example

Decision: datastore for an order service. Criteria/weights: consistency 0.4, ops cost 0.3, team familiarity 0.3. Scores (1–5): [INFERRED]

| Option | Consistency (0.4) | Ops cost (0.3) | Familiarity (0.3) | Weighted |
|--------|:-:|:-:|:-:|:-:|
| Postgres | 5 | 3 | 5 | **4.4** |
| DynamoDB | 3 | 5 | 2 | 3.3 |
| Mongo | 3 | 4 | 3 | 3.3 |

Trade-off pair: chose Postgres over DynamoDB because strong consistency (weight 0.4) outranks ops elasticity for this order flow. Revisit if write volume exceeds single-node headroom. Sensitivity: dropping consistency weight to 0.25 ties Postgres with DynamoDB — so the call hinges on the consistency requirement holding. [INFERRED]

## Quality Criteria

- [ ] Decision matrix includes ≥3 alternatives with weighted criteria; weights sum to 1.0
- [ ] Every score cell has a one-line evidence-based rationale
- [ ] Trade-off pairs are explicitly documented (chose X over Y because...)
- [ ] ADR captures context, decision, and consequences
- [ ] Sensitivity analysis validates robustness of recommendation
- [ ] Recommendation states confidence level and revisit trigger
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- **False trade-off:** presenting options as mutually exclusive when they are not.
- **Analysis paralysis:** over-analyzing when options are close enough — for two-way doors, decide fast and revisit.
- **Confirmation bias:** scoring to justify a predetermined decision (smell: all weights set *after* the favored option is known).
- **Weight laundering:** the analyst sets the weights, then attributes them to "stakeholders." Capture sign-off. [INFERRED]
- **Precision theater:** false confidence from decimal scores over unreliable estimates — keep the scale coarse (1–5). [INFERRED]

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Fragile winner | recommendation flips under small weight changes | run sensitivity check; gather more evidence on the pivotal criterion |
| Missing option | best choice never entered the matrix | force a "do nothing" baseline + one wildcard alternative |
| Stale ADR | decision context changed, ADR not updated | record revisit trigger; supersede rather than edit prior ADRs |
| Score gaming | cells tuned to a foregone conclusion | require per-cell rationale and independent review |

## Related Skills

- `scenario-analysis` — complementary evaluation using Tree-of-Thought
- `system-architecture` — trade-offs drive architectural decisions
- `feasibility-validation` — validates that chosen trade-offs are feasible

## Usage

Example invocations:

- "/trade-off-analysis" — Run the full trade off analysis workflow
- "trade off analysis on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Quantitative scores are decision *aids*, not proofs — a high weighted score does not authorize skipping the qualitative trade-off review. [INFERRED]
- Out of scope: cost estimation in currency (use FTE-months), and procurement/vendor negotiation. [INFERRED]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Options score within rounding | Declare a near-tie; pick on reversibility or lowest switching cost, not the decimal [INFERRED] |
| No stakeholder available to weight | Use equal weights, label as provisional, flag for later validation [INFERRED] |
| Single forced option | Skip the matrix; write a one-line ADR recording the forcing constraint [INFERRED] |
