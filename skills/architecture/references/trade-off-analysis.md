<!-- distilled from alfa skills/trade-off-analysis -->
<!-- > -->
# Trade-Off Analysis

> "Every architecture is the result of trade-offs, whether conscious or not." — Mark Richards

## TL;DR

Performs structured trade-off analysis using weighted scoring matrices, decision matrices, and ATAM to make explicit, defensible architectural and technology decisions. Use this skill when facing architectural trade-offs (consistency vs. availability, flexibility vs. simplicity), choosing between technologies, or when the team disagrees on approach. [EXPLICIT]

## Procedure

### Step 1: Discover
- Define the decision to be made and the options under consideration
- Identify quality attributes at stake (performance, security, maintainability, cost)
- Gather constraints: budget, timeline, team skills, existing commitments
- Collect stakeholder priorities: which quality attributes matter most

### Step 2: Analyze
- Apply ATAM method:
  1. Present the business drivers and architectural approaches
  2. Identify architectural approaches and their associated quality attributes
  3. Generate quality attribute scenarios (stimulus, response, measure)
  4. Analyze approaches against scenarios to identify sensitivity points and trade-offs
- Build a weighted decision matrix with stakeholder-validated weights
- Identify risks: where an architectural decision could cause problems
- Find sensitivity points: where small changes significantly impact quality attributes

### Step 3: Execute
- Produce a decision matrix with alternatives scored against weighted criteria
- Document trade-off pairs: "We chose X over Y because Z quality attribute is more critical"
- Write an Architecture Decision Record (ADR) capturing the analysis
- Create a risk catalog from identified sensitivity points and trade-offs
- Provide a recommendation with confidence level and conditions for revisiting

### Step 4: Validate
- Verify weights reflect actual stakeholder priorities, not assumed ones
- Confirm scoring is evidence-based with supporting rationale
- Check that the analysis reveals genuine trade-offs (not a predetermined conclusion)
- Review sensitivity: would different weights change the recommendation?

## Quality Criteria

- [ ] Decision matrix includes at least 3 alternatives with weighted criteria
- [ ] Trade-off pairs are explicitly documented (chose X over Y because...)
- [ ] ADR captures context, decision, and consequences
- [ ] Sensitivity analysis validates robustness of recommendation
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- False trade-off: presenting options as mutually exclusive when they are not
- Analysis paralysis: over-analyzing when the options are close enough
- Confirmation bias: scoring to justify a predetermined decision

## Related Skills

- `scenario-analysis` — complementary evaluation using Tree-of-Thought
- `system-architecture` — trade-offs drive architectural decisions
- `feasibility-validation` — validates that chosen trade-offs are feasible

## Usage

Example invocations:

- "/trade-off-analysis" — Run the full trade off analysis workflow
- "trade off analysis on this project" — Apply to current context


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
