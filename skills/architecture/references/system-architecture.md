<!-- distilled from alfa skills/system-architecture -->
<!-- > -->
# System Architecture

> "Architecture is about the important stuff. Whatever that is." — Ralph Johnson

## TL;DR

Designs software system architectures using C4 model diagrams, documents decisions via ADRs, and evaluates quality attribute trade-offs to produce maintainable, scalable systems. Use this skill when starting a new system, evaluating architectural fitness, or when the team needs shared understanding of system structure. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify architectural drivers: key quality attributes, constraints, and business goals
- Inventory existing systems, integrations, and technology stack
- Review non-functional requirements: performance, scalability, security, availability
- Examine existing architectural documentation and decisions

### Step 2: Analyze
- Identify architectural styles: monolith, microservices, event-driven, serverless, hybrid
- Evaluate quality attribute trade-offs (e.g., consistency vs. availability)
- Map system boundaries and integration points
- Assess technology fitness: does the current stack support the required quality attributes?

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

## Anti-Patterns

- Architecture astronaut: over-engineering for hypothetical future requirements
- PowerPoint architecture: beautiful diagrams disconnected from reality
- Decision by default: choosing technology without explicit evaluation

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

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
