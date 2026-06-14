---
name: market-intel
version: 1.0.0
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

Router skill. Resolves one `topic`, then Reads EXACTLY ONE playbook from
`routes:`. Never loads the whole cluster — one topic per invocation. Covers
market/competitive intelligence: positioning, pricing, sector context,
benchmarks, partnerships. NOT product specs, GTM execution, or financial
modeling — route those elsewhere. [INFERENCIA]

## Routing
- `topic` (required): one enum value (`params.topic.enum`). Infer from the
  request; ask only if genuinely ambiguous between two topics. [CONFIG]
- `depth` (default `quick`): `deep` → apply the playbook exhaustively with
  verification at each step; `quick` → essentials only. [CONFIG]
- Read that topic's file from `routes:` — nothing else — then run its spine:
  Discover → Analyze → Execute → Validate. [DOC]

Topic cues: competitor matrix/stack/SWOT → `competitive-intelligence`;
where-we-win → `competitive-positioning`; vs-peer metrics →
`benchmarking-analysis`; TAM/trends/demand → `market-intelligence`;
vertical/regulatory → `sector-intelligence`; messaging/channel →
`marketing-context`; ally/OEM → `partnership-strategy`; packaging/tiers →
`pricing-strategy`. [INFERENCIA]

## Acceptance criteria
- Exactly one playbook loaded; topic ∈ enum. [DOC]
- Every non-obvious claim tagged (`[CÓDIGO]` `[CONFIG]` `[DOC]`
  `[INFERENCIA]` `[SUPUESTO]`); one tag per claim, consistent throughout. [DOC]
- No invented prices — FTE-months + disclaimers only. [DOC]
- `depth=deep` runs the playbook's validation step before output. [DOC]

## Anti-patterns
- Loading 2+ topic files "to be safe" — defeats the router. [INFERENCIA]
- Guessing an ambiguous topic instead of asking. [INFERENCIA]
- Emitting market figures as fact without a `{WEB}`+citation or `[DOC]` tag. [DOC]

Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first
rule. The guardian applies `assets/quality-rubric.json` and
`assets/routing-checklist.md` before any deliverable is emitted. [CONFIG]
