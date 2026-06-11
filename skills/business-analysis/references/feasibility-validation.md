<!-- distilled from alfa skills/feasibility-validation -->
<!-- > -->
# Feasibility Validation

> "The first 90% of the code accounts for the first 90% of the development time. The remaining 10% accounts for the other 90%." — Tom Cargill

## TL;DR

Assesses technical feasibility across 7 dimensions — architecture, team capability, timeline, cost, risk, integration complexity, and scalability — to produce a go/no-go recommendation with confidence levels. Use this skill before committing to a technical approach, responding to an RFP, or greenlighting a new initiative. [EXPLICIT]

## Procedure

### Step 1: Discover
- Define the scope of what is being assessed (feature, system, migration, product)
- Gather technical constraints, team profiles, timeline expectations, and budget
- Identify reference architectures, proof-of-concepts, or similar implementations

### Step 2: Analyze
- Evaluate each of the 7 dimensions (1-5 scale):
  1. **Architecture**: Can existing patterns support this? What new patterns are needed?
  2. **Team Capability**: Does the team have the skills? What ramp-up is needed?
  3. **Timeline**: Is the schedule realistic given scope and team velocity?
  4. **Cost**: Are effort estimates within budget constraints?
  5. **Risk**: What are the top 5 technical risks and their mitigations?
  6. **Integration**: How complex are third-party and legacy integrations?
  7. **Scalability**: Will the solution handle projected load growth?

### Step 3: Execute
- Produce a feasibility scorecard with dimension scores and overall assessment
- Write a risk register with probability, impact, and mitigation for top risks
- Identify showstoppers vs. manageable challenges
- Provide go/no-go/conditional-go recommendation with confidence percentage

### Step 4: Validate
- Verify each dimension score is supported by evidence
- Confirm risk mitigations are actionable, not aspirational
- Cross-check timeline estimates against team velocity data
- Review with technical leads for blind-spot identification

## Quality Criteria

- [ ] All 7 dimensions scored with evidence-backed justification
- [ ] Top 5 risks identified with probability, impact, and mitigation
- [ ] Showstoppers explicitly called out with resolution paths
- [ ] Go/no-go recommendation includes confidence level
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Feasibility theater: going through motions with predetermined conclusion
- Ignoring team capability dimension (assuming skills can be acquired instantly)
- Underestimating integration complexity with legacy systems

## Related Skills

- `cost-estimation` — detailed effort estimation for feasible approaches
- `risk-assessment` — deeper risk analysis beyond feasibility scope
- `scenario-analysis` — evaluating alternative approaches when feasibility is mixed

## Usage

Example invocations:

- "/feasibility-validation" — Run the full feasibility validation workflow
- "feasibility validation on this project" — Apply to current context


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
