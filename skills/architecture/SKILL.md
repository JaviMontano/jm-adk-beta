---
name: architecture
version: 1.0.0
description: "Software/system architecture router: API design, DDD, events, realtime, caching, performance, migrations, structured trade-off analysis. Topics: api-design, caching-strategy, domain-driven-design, event-architecture, migration-planning, performance-architecture, realtime-architecture, system-architecture, trade-off-analysis."
params:
  topic:
    enum: [api-design, caching-strategy, domain-driven-design, event-architecture, migration-planning, performance-architecture, realtime-architecture, system-architecture, trade-off-analysis]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  api-design: references/api-design.md
  caching-strategy: references/caching-strategy.md
  domain-driven-design: references/domain-driven-design.md
  event-architecture: references/event-architecture.md
  migration-planning: references/migration-planning.md
  performance-architecture: references/performance-architecture.md
  realtime-architecture: references/realtime-architecture.md
  system-architecture: references/system-architecture.md
  trade-off-analysis: references/trade-off-analysis.md
---

# architecture

Router skill: resolve ONE `topic`, Read EXACTLY ONE playbook from `routes:`,
execute it. Never load the cluster. [DOC]

## When to use
Any architecture decision or design task matching a `topic` enum. If the request
spans several (e.g. "event-driven system with caching"), pick the dominant
concern, run it, then chain a second invocation — do NOT merge playbooks. [INFERENCE]

## Inputs / Outputs
- **In:** `topic` (required; infer from request, ask only if genuinely
  ambiguous), `depth` (`quick` default | `deep`). [DOC]
- **Out:** the resolved playbook's deliverable, claims carrying Alfa-core tags
  (`[DOC]`/`[CONFIG]`/`[CODE]`/`[INFERENCE]`/`[ASSUMPTION]`; one family, one
  spelling — see references/verification-tags.md). [DOC]

## Routing
1. Map request → exactly one `topic`. Ambiguous between two → ask, do not guess. [DOC]
2. Read that route's file. `depth=deep` → apply exhaustively, validate each step;
   `quick` → essentials only, name what you skipped. [DOC]
3. Spine: Discover → Analyze → Execute → Validate.
4. Gates: constitution v6.0.0 (enforcement), evidence tags, script-first. [CONFIG]
5. Gate enforced via `assets/quality-rubric.json`; pre-flight via `assets/routing-checklist.md`. [CONFIG]

## Acceptance gate (done = all true)
- Exactly one playbook loaded; topic ∈ enum; no cross-playbook bleed. [DOC]
- Every non-obvious claim tagged, single family, consistent spelling. [DOC]
- Trade-offs stated with the rejected option and why. [INFERENCE]
- `[ASSUMPTION]` claims each paired with a verification step. [DOC]

## Anti-patterns
- Loading 2+ playbooks "to be safe" — defeats the router. [INFERENCE]
- Guessing `topic` instead of asking when truly ambiguous. [INFERENCE]
- Recommending a pattern with no named trade-off or rejected alternative. [INFERENCE]
- Inventing prices, or marking green/done without the gate above. [DOC]
