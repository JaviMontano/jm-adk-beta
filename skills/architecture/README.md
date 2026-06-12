# architecture — skill overview

Router skill for **software and system architecture decisions**. It resolves a
request to exactly ONE `topic`, loads exactly ONE playbook from `routes:`, and
runs it along the spine **Discover → Analyze → Execute → Validate**. It never
loads the whole playbook cluster. [DOC]

## What it does

Given an architecture or design task, it produces the resolved playbook's
deliverable — an OpenAPI contract, a context map, an ADR, a C4 model, a
cache-tier plan, an event-flow design, a migration runbook, a performance
budget, a realtime transport choice, or a weighted decision matrix — with every
non-obvious claim tagged from the Alfa-core family
(`[DOC]` `[CONFIG]` `[CODE]` `[INFERENCE]` `[ASSUMPTION]`). [DOC]

## When to use

- Designing or evolving an API contract → `api-design`
- Placing a cache tier or invalidation policy → `caching-strategy`
- Drawing bounded contexts / aggregates → `domain-driven-design`
- Designing async/event flows, delivery semantics → `event-architecture`
- Modernizing legacy, switching stores/clouds → `migration-planning`
- Setting latency/throughput budgets, removing bottlenecks → `performance-architecture`
- Choosing a realtime transport (WS/SSE/polling) → `realtime-architecture`
- Structuring a whole system, C4 + ADRs → `system-architecture`
- Choosing between contested, hard-to-reverse options → `trade-off-analysis`

**Do NOT use** when the choice is a trivial two-way door, or when another
provider/skill clearly owns it — route out instead of widening this skill. [INFERENCE]

## How it routes / executes

1. Map request → exactly one `topic` in the enum. Ambiguous between two → ask,
   never guess. [DOC]
2. Read that one file from `routes:`. `depth=deep` applies it exhaustively and
   validates each step; `quick` does essentials and names what was skipped. [DOC]
3. Run Discover → Analyze → Execute → Validate; enforce the acceptance gate in
   SKILL.md before declaring done. [DOC]

## References (one per topic)

- [references/api-design.md](references/api-design.md)
- [references/caching-strategy.md](references/caching-strategy.md)
- [references/domain-driven-design.md](references/domain-driven-design.md)
- [references/event-architecture.md](references/event-architecture.md)
- [references/migration-planning.md](references/migration-planning.md)
- [references/performance-architecture.md](references/performance-architecture.md)
- [references/realtime-architecture.md](references/realtime-architecture.md)
- [references/system-architecture.md](references/system-architecture.md)
- [references/trade-off-analysis.md](references/trade-off-analysis.md)

## Bundle

- `agents/` — lead, specialist, support, guardian role contracts.
- `knowledge/` — body of knowledge + concept graph for the nine topics.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — deliverable scaffold (ADR + matrix + diagram refs).
- `evals/evals.json` — scenario cases with expected checks.
- `examples/` — one worked api-design example, input and output.
- `assets/` — quality rubric and routing checklist (see `assets/README.md`).
