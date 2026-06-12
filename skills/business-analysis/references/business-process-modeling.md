<!-- distilled from alfa skills/business-process-modeling -->
<!-- > -->
# Business Process Modeling

> "Every system is perfectly designed to get the results it gets." — W. Edwards Deming

## TL;DR

Models business processes using BPMN 2.0 notation, value stream maps, and capability maps to identify waste, bottlenecks, and automation opportunities. Use this skill when digitizing manual processes, optimizing existing workflows, or establishing a shared understanding of how the business operates. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the process scope: end-to-end or subprocess. Fix explicit start/end events — an unbounded scope is the top cause of rework. [INFERENCE]
- Gather existing process documentation, SOPs, and tribal knowledge
- Interview process participants to understand as-is state including workarounds; the workarounds *are* the real process. [EXPLICIT]
- Capture ≥2 perspectives per handoff (sender + receiver) — single-source maps miss the gaps where work stalls. [INFERENCE]

### Step 2: Analyze
- Map the as-is process in BPMN 2.0 with pools (orgs), lanes (roles), gateways, and events
- Perform value stream analysis: classify each step value-add / business-non-value-add / waste (the 8 wastes: defects, overproduction, waiting, non-utilized talent, transport, inventory, motion, extra-processing). [EXPLICIT]
- Calculate process metrics: cycle time, lead time, wait time, rework rate, and **process cycle efficiency** (value-add time ÷ lead time). [EXPLICIT]
- Identify automation candidates using a complexity (low/high) × frequency (low/high) matrix: high-freq + low-complexity = automate first; high-freq + high-complexity = redesign then automate; low-freq = leave manual. [INFERENCE]

### Step 3: Execute
- Produce BPMN 2.0 diagrams for as-is and to-be processes
- Create a value stream map showing information and material flow with a timeline ladder (process vs. wait time)
- Build a capability map linking processes to business capabilities
- Document improvement recommendations with expected impact metrics and the baseline they move from. [EXPLICIT]

### Step 4: Validate
- Walk through BPMN diagrams with process owners for accuracy ("token simulation": trace one case end-to-end). [INFERENCE]
- Verify all exception paths and escalation procedures are modeled — every gateway needs every branch resolved (no dangling paths). [EXPLICIT]
- Confirm to-be process addresses identified bottlenecks and waste, not just the symptom. [EXPLICIT]
- Validate improvement metrics are measurable, baselined, and realistic

## Worked Example (invoice approval)

As-is: 4 lanes (AP clerk, manager, finance, vendor), lead time 11 days, value-add time 40 min → PCE = 0.6%. [EXPLICIT]
Diagnosis: 9.5 days of the 11 are *waiting* at the manager-approval gateway (waste: waiting + extra-processing from manual re-keying). [INFERENCE]
To-be: auto-route <$5k invoices (high-freq, low-complexity → automate), exception-only manager review. Target lead time 2 days, PCE > 4%. [EXPLICIT]
Evidence the fix is real, not cosmetic: the bottleneck step is removed for 80% of volume, not merely sped up. [INFERENCE]

## Quality Criteria

- [ ] BPMN diagrams follow 2.0 notation standards; every gateway branch and end event resolved, no orphan tasks
- [ ] Value stream map distinguishes value-add from waste and reports PCE
- [ ] Process metrics are quantified with a stated baseline (cycle time, wait time, error rate)
- [ ] To-be process has measurable improvement targets tied to a named bottleneck
- [ ] Every non-obvious claim carries exactly one tag from the Alfa core set (`references/verification-tags.md`) [DOC]

## Acceptance Criteria (done = all true)

- Each modeled process has explicit start + end events and ≥1 role lane. [EXPLICIT]
- To-be improvement is traceable to a specific as-is waste category. [EXPLICIT]
- Process owner has signed off on as-is accuracy before to-be is drafted. [EXPLICIT]
- No metric is asserted without its measurement source or `[ASSUMPTION]` tag. [DOC]

## Anti-Patterns & Failure Modes

- Modeling the ideal process instead of the actual as-is state (interview-says vs. reality gap). [EXPLICIT]
- BPMN diagrams without proper swimlanes — responsibility becomes unattributable. [EXPLICIT]
- Automating a broken process: you scale the defect. Fix flow first, then automate. [EXPLICIT]
- "Happy-path only" maps — exception volume is where cost hides; unmodeled exceptions invalidate the metrics. [INFERENCE]
- Boiling-the-ocean scope: modeling the whole enterprise instead of one painful value stream. [INFERENCE]
- Confusing a flowchart for BPMN — no pools/lanes means no accountability. [INFERENCE]

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
| No as-is documentation exists | Build map live from participant interviews; tag every step `[ASSUMPTION]` until owner-validated |
| Process varies by region/case type | Model the dominant variant; note variants as separate sub-flows, don't average them away |
| Owner disputes the as-is map | The map is correct, the assumption was wrong — re-interview, never overwrite reality with intent |
