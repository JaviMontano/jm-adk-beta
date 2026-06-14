<!-- distilled from alfa skills/system-architecture -->
<!-- > -->
# System Architecture

> "Architecture is about the important stuff. Whatever that is." — Ralph Johnson

## TL;DR

Designs software system architectures using C4 model diagrams, documents decisions via ADRs, and evaluates quality attribute trade-offs to produce maintainable, scalable systems. Use this skill when starting a new system, evaluating architectural fitness, or when the team needs shared understanding of system structure. [EXPLICIT]

**In scope:** structure, boundaries, quality-attribute trade-offs, decision records. **Out of scope (anti-scope):** detailed API contracts (→ `api-design`), diagram rendering syntax (→ `mermaid-diagramming`), implementation/coding, capacity sizing math, and vendor procurement. [DOC] Route those elsewhere rather than expanding this skill.

## Procedure

### Step 1: Discover
- Identify architectural drivers: key quality attributes, constraints, and business goals
- Inventory existing systems, integrations, and technology stack
- Review non-functional requirements: performance, scalability, security, availability
- Examine existing architectural documentation and decisions
- **Rank** drivers; an unranked driver list silently makes everything top priority, which defeats trade-off analysis in Step 2. [INFERENCIA]

### Step 2: Analyze
- Identify architectural styles: monolith, microservices, event-driven, serverless, hybrid
- Evaluate quality attribute trade-offs (e.g., consistency vs. availability)
- Map system boundaries and integration points
- Assess technology fitness: does the current stack support the required quality attributes?
- Every style choice is a trade-off, never a free win — record the cost, not just the benefit (see Decisions table). [DOC]

### Step 3: Execute
- Create C4 diagrams: Context, Container, Component, (Code when needed)
- Write Architecture Decision Records (ADRs) for significant decisions
- Document quality attribute scenarios with stimulus, response, and measure
- Define cross-cutting concerns: logging, monitoring, auth, error handling
- Produce a technology stack decision with rationale

### Step 4: Validate
- Verify C4 diagrams are consistent across levels (no phantom systems)
- Confirm ADRs capture context, decision, and consequences (not just the decision)
- Check quality attribute scenarios are testable and measurable
- Review with development team for implementability

## Quality Criteria

- [ ] C4 diagrams cover Context and Container levels minimum
- [ ] ADRs follow status/context/decision/consequences format
- [ ] Quality attributes have measurable scenarios
- [ ] Cross-cutting concerns are addressed explicitly
- [ ] Evidence tags applied to all claims

## Acceptance Criteria

Done means all of the following hold; any unmet item blocks handoff. [DOC]
- [ ] Each ranked driver maps to at least one decision or scenario (no orphan drivers). [INFERENCIA]
- [ ] Every Container in the C4 diagram appears in exactly one ADR or is justified as trivial. [INFERENCIA]
- [ ] Each quality attribute scenario states a **measure** (number + unit), not an adjective ("fast"). [DOC]
- [ ] Every significant decision lists at least one rejected alternative with its reason. [DOC]
- [ ] Cross-cutting concerns (logging, monitoring, auth, error handling) each have a named owner mechanism, not "TBD". [SUPUESTO] — verify with the dev team in the Step 4 review.

## Quality Attribute Scenario — Worked Example

Form: *source → stimulus → artifact → environment → response → measure*. [DOC]

> Under peak load (1000 req/s, normal ops), a user request to the checkout API returns a response within **300 ms at p95**, or sheds load with a 503 within **50 ms**. [EXPLICIT]

This is testable (drive 1000 req/s, assert p95) and falsifiable. Contrast the anti-pattern "checkout should be fast" — no source, no measure, untestable. [INFERENCIA]

## Decisions & Trade-Offs

Default to the simplest style that meets ranked drivers; escalate only on evidence. [SUPUESTO] — confirm against the actual driver ranking, not habit.

| Decision | Choose when | Pay with (trade-off) |
|----------|-------------|----------------------|
| Monolith first | Small team, unproven domain, low scale | Coupling grows; later split costs refactor [INFERENCIA] |
| Microservices | Independent scaling/deploy, clear bounded contexts | Operational + network + data-consistency overhead [DOC] |
| Event-driven | Async flows, decoupling, audit/replay needs | Eventual consistency; harder debugging/tracing [DOC] |
| Serverless | Spiky/low baseline load, minimal ops | Cold starts, vendor lock-in, execution limits [DOC] |

Rule of thumb: prefer the least operationally costly option until a ranked driver forces otherwise; "we might need to scale" is `[SUPUESTO]`, not a driver. [INFERENCIA]

## Failure Modes

| Failure mode | Symptom | Mitigation |
|--------------|---------|------------|
| Phantom system | Diagram shows a system no code/contract backs | Cross-check each node to repo or integration evidence [INFERENCIA] |
| Decision-only ADR | ADR states choice, omits why | Reject in Step 4; require context + consequences [DOC] |
| Unmeasurable scenario | "Highly available", no number | Demand measure + unit before acceptance [DOC] |
| Driver drift | Late requirement invalidates style choice | Re-rank drivers, supersede affected ADRs (don't edit in place) [INFERENCIA] |
| Hidden cross-cutting gap | Auth/logging assumed, never specified | Acceptance checklist forces named mechanism [INFERENCIA] |

## Anti-Patterns

- Architecture astronaut: over-engineering for hypothetical future requirements
- PowerPoint architecture: beautiful diagrams disconnected from reality
- Decision by default: choosing technology without explicit evaluation
- Big-bang rewrite proposed in lieu of incremental evolution when drivers don't demand it [INFERENCIA]

## Related Skills

- `mermaid-diagramming` — renders C4 and other architecture diagrams
- `trade-off-analysis` — structured quality attribute trade-off evaluation
- `api-design` — detailed contract design for system interfaces

## Usage

Example invocations:

- "/system-architecture" — Run the full system architecture workflow
- "system architecture on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Covers logical/structural design; does not produce capacity/cost models or runnable infrastructure code [SUPUESTO] — route sizing and IaC to the relevant skill.
- ADRs are append-and-supersede; this skill does not retro-edit accepted decisions [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No existing docs (greenfield) | Start at C4 Context; infer drivers from goals, tag each `[SUPUESTO]` and confirm |
| Legacy with no ADR trail | Reconstruct decisions as retroactive ADRs marked `[INFERENCIA]`; flag for owner sign-off |
| Two equally fit styles | Pick lower operational cost; record the tie and rejected option in the ADR |
