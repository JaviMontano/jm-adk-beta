---
name: market-intel
description: "Market and competitive intelligence: positioning, pricing, sector context, benchmarks, and partnerships. Topics: benchmarking-analysis, competitive-intelligence, competitive-positioning, market-intelligence, marketing-context, partnership-strategy, pricing-strategy, sector-intelligence."
params:
  topic:
    enum: [benchmarking-analysis, competitive-intelligence, competitive-positioning, market-intelligence, marketing-context, partnership-strategy, pricing-strategy, sector-intelligence]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  benchmarking-analysis: references/benchmarking-analysis.md
  competitive-intelligence: references/competitive-intelligence.md
  competitive-positioning: references/competitive-positioning.md
  market-intelligence: references/market-intelligence.md
  marketing-context: references/marketing-context.md
  partnership-strategy: references/partnership-strategy.md
  pricing-strategy: references/pricing-strategy.md
  sector-intelligence: references/sector-intelligence.md
---

# market-intel

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
