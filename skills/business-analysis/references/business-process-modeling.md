<!-- distilled from alfa skills/business-process-modeling -->
<!-- > -->
# Business Process Modeling

> "Every system is perfectly designed to get the results it gets." — W. Edwards Deming

## TL;DR

Models business processes using BPMN 2.0 notation, value stream maps, and capability maps to identify waste, bottlenecks, and automation opportunities. Use this skill when digitizing manual processes, optimizing existing workflows, or establishing a shared understanding of how the business operates. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the process scope: end-to-end or subprocess
- Gather existing process documentation, SOPs, and tribal knowledge
- Interview process participants to understand as-is state including workarounds

### Step 2: Analyze
- Map the as-is process in BPMN 2.0 with pools, lanes, gateways, and events
- Perform value stream analysis: identify value-adding vs. non-value-adding steps
- Calculate process metrics: cycle time, lead time, wait time, rework rate
- Identify automation candidates using complexity vs. frequency matrix

### Step 3: Execute
- Produce BPMN 2.0 diagrams for as-is and to-be processes
- Create a value stream map showing information and material flow
- Build a capability map linking processes to business capabilities
- Document improvement recommendations with expected impact metrics

### Step 4: Validate
- Walk through BPMN diagrams with process owners for accuracy
- Verify all exception paths and escalation procedures are modeled
- Confirm to-be process addresses identified bottlenecks and waste
- Validate improvement metrics are measurable and realistic

## Quality Criteria

- [ ] BPMN diagrams follow 2.0 notation standards correctly
- [ ] Value stream map distinguishes value-add from waste
- [ ] Process metrics are quantified (cycle time, wait time, error rate)
- [ ] To-be process has measurable improvement targets
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Modeling the ideal process instead of the actual as-is state
- BPMN diagrams without proper swimlanes obscuring responsibilities
- Automating a broken process without fixing it first

## Related Skills

- `flow-mapping` — lighter-weight process visualization
- `workshop-design` — facilitating process discovery sessions
- `domain-driven-design` — aligning processes with domain boundaries

## Usage

Example invocations:

- "/business-process-modeling" — Run the full business process modeling workflow
- "business process modeling on this project" — Apply to current context


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
