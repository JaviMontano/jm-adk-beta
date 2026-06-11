---
name: architecture
description: "Software/system architecture: API design, DDD, events, realtime, caching, performance, migrations, and structured trade-off analysis. Topics: api-design, caching-strategy, domain-driven-design, event-architecture, migration-planning, performance-architecture, realtime-architecture, system-architecture, trade-off-analysis."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
