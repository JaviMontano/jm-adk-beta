<!-- distilled from alfa skills/intelligent-routing -->
<!-- > -->
# Intelligent Routing

> "Method over hacks. Evidence over assumption."

## TL;DR

Match user intent to the best domain for Lead agent selection using BM25 + semantic similarity. This is an orchestration-layer skill used internally by Pristino and the adk-orchestrator. Protocol details in PRISTINO.md. [EXPLICIT]

## Procedure

### Step 1: Discover
- Gather input and context
- Load relevant indexes and configuration

### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV
- Score candidates by relevance and confidence

### Step 3: Execute
- Apply the selected approach
- Tag all outputs with evidence markers

### Step 4: Validate
- Verify quality criteria met
- Confirm confidence >= 0.95

## Quality Criteria

- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Confidence >= 0.95
- [ ] Actionable output

## Related Skills

- See PRISTINO.md for full orchestration protocol

## Usage

Example invocations:

- "/intelligent-routing" — Run the full intelligent routing workflow
- "intelligent routing on this project" — Apply to current context


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
