<!-- distilled from alfa skills/requirements-engineering -->
<!-- > -->
# Requirements Engineering

> "A requirement that is not testable is not a requirement — it is a wish." — Alan Davis

## TL;DR

Transforms stakeholder needs into structured, testable requirements: INVEST user stories with Given/When/Then (Gherkin) acceptance criteria and a requirement→objective traceability matrix. Use when starting a feature, capturing business rules, or formalizing ambiguous requirements. Out of scope: implementation design, estimation in hours/cost, and final domain decisions (advisory only). [DOC]

## Procedure

### Step 1: Discover
- Inventory existing artifacts: `.feature` files, `README.md`, issue trackers, specs, prior ADRs. [DOC]
- Gather stakeholder roles, business goals, constraints, and the system-of-record for each rule.
- Record source + date per requirement so later conflicts are traceable to who said what. [INFERENCIA]

### Step 2: Analyze
- Decompose needs into INVEST stories (Independent, Negotiable, Valuable, Estimable, Small, Testable).
- Surface implicit requirements, edge cases, and NFRs (performance, security, accessibility, compliance, observability).
- Map inter-story dependencies; flag stories too large to test in one acceptance run as split candidates. [INFERENCIA]

### Step 3: Execute
- Write stories as "As a [role], I want [goal], so that [benefit]".
- Define acceptance criteria in Given/When/Then per story — include happy path, negative paths, and boundary values.
- Build a traceability matrix linking each requirement to a business objective and to its acceptance criteria.
- Document assumptions, constraints, and out-of-scope items explicitly; tag every derived/assumed claim. [DOC]

### Step 4: Validate
- Verify each story meets INVEST and each criterion is atomic, deterministic, automatable.
- Coverage check: every business rule maps to ≥1 acceptance criterion and ≥1 objective (no orphans). [INFERENCIA]
- Review with stakeholders; resolve or explicitly defer every flagged conflict before sign-off.

## Worked Example

Need: "Users should reset their password."

- **Story** — As a registered user, I want to reset my password via email, so that I regain access without contacting support.
- **AC (happy)** — Given a registered email, When I request reset, Then a single-use link valid 15 min is sent. [SUPUESTO: 15 min TTL — confirm with security owner]
- **AC (negative)** — Given an unregistered email, When I request reset, Then the UI shows the same generic confirmation (no account enumeration). [INFERENCIA]
- **AC (boundary)** — Given an expired or already-used link, When I open it, Then reset is refused and a re-request is offered.
- **NFR** — Reset endpoint rate-limited to ≤5 requests / email / hour. [SUPUESTO: threshold — confirm with platform team]

## Quality Criteria

- [ ] Every story follows "As a / I want / So that".
- [ ] Acceptance criteria use Given/When/Then with concrete, automatable examples.
- [ ] Negative and boundary scenarios present, not just happy path.
- [ ] NFRs (performance, security, accessibility, compliance) captured where relevant.
- [ ] Stories are INVEST-compliant and right-sized.
- [ ] Traceability matrix has no orphan requirements and no orphan objectives.
- [ ] Evidence tags applied to all non-obvious claims; assumptions paired with a verification step.

## Decisions & Trade-offs

- **Gherkin over free-text AC** — executable/automatable and unambiguous; costs more authoring effort and can feel heavy for trivial CRUD. Accept the overhead because untestable AC is the dominant defect source. [INFERENCIA]
- **INVEST over exhaustive upfront spec** — favors small negotiable increments; trades some long-range completeness for faster feedback. Mitigate with the traceability matrix as the completeness ledger. [INFERENCIA]
- **Tag assumptions inline rather than a separate log** — keeps provenance next to the claim at the cost of slightly noisier prose. [SUPUESTO]

## Failure Modes

- **Solutioning in stories** — "I want a dropdown" prescribes UI; rewrite to the underlying goal. [INFERENCIA]
- **Untestable AC** — "system is fast" → restate as a measurable threshold (p95 latency, count, time window).
- **Silent conflict** — two rules contradict and one is dropped without record; always flag and resolve explicitly, never auto-pick. [INFERENCIA]
- **Coverage drift** — new rule added without a linked criterion; the orphan check in Step 4 is the gate. [INFERENCIA]
- **NFR omission** — only happy-path functionality captured; security/perf/accessibility surface late as rework.

## Anti-Patterns

- Gold plating: requirements nobody asked for.
- Ambiguous acceptance criteria that cannot be automated.
- Missing negative scenarios and error paths in Given/When/Then.

## Related Skills

- `stakeholder-mapping` — identifies who provides and validates requirements.
- `domain-driven-design` — supplies ubiquitous language for precise requirements.
- `scenario-analysis` — evaluates alternative requirement approaches.

## Usage

Example invocations:

- "/requirements-engineering" — Run the full requirements engineering workflow.
- "requirements engineering on this project" — Apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [SUPUESTO]
- Requires English-language output unless otherwise specified. [SUPUESTO]
- Advisory only — does not replace domain-expert judgment for final decisions. [DOC]
- Does not produce effort/cost estimates; sizing is relative (story points), never hours or price. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding; do not fabricate requirements. [SUPUESTO] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution, escalate if unresolved. |
| Out-of-scope request | Redirect to the appropriate skill or escalate. |
| Non-functional-only request | Capture as NFR with measurable thresholds; no story needed. [INFERENCIA] |
| No stakeholder available to validate | Mark criteria `[SUPUESTO]`, record the open question, proceed provisionally. |
