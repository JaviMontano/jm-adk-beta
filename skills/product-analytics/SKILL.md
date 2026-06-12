---
name: product-analytics
version: 1.0.0
description: "Product and business analytics router: event instrumentation, KPIs, A/B tests, cohorts, funnels, real-time pipelines, and data visualization. Topics: ab-testing, analytics-events, cohort-analysis, data-visualization, funnel-analytics, kpi-framework, metrics-instrumentation, real-time-analytics."
params:
  topic:
    enum: [ab-testing, analytics-events, cohort-analysis, data-visualization, funnel-analytics, kpi-framework, metrics-instrumentation, real-time-analytics]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  ab-testing: references/ab-testing.md
  analytics-events: references/analytics-events.md
  cohort-analysis: references/cohort-analysis.md
  data-visualization: references/data-visualization.md
  funnel-analytics: references/funnel-analytics.md
  kpi-framework: references/kpi-framework.md
  metrics-instrumentation: references/metrics-instrumentation.md
  real-time-analytics: references/real-time-analytics.md
---

# product-analytics

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`.
Never preload the cluster — one topic in, one playbook out. [CONFIG]

## When to use
A request touches product/business measurement: defining metrics, instrumenting
or auditing events, designing or reading an experiment, building cohorts/funnels,
or charting results. Not for app feature code, infra, or generic data-engineering
ETL — route those to their own clusters. [INFERENCIA]

## Inputs → Outputs
- **In:** `topic` (required; infer from request, ask only if two routes fit),
  `depth` (`quick`=essentials, `deep`=full playbook with per-step verification).
- **Out:** the single resolved playbook applied to the user's case, with
  Alfa-core evidence tags (`[DOC]` `[CONFIG]` `[CÓDIGO]` `[INFERENCIA]` `[SUPUESTO]`)
  on every non-obvious claim. [DOC]

## Topic disambiguation (pick the right route) [INFERENCIA]
- Event schema/naming → `analytics-events`; wiring SDK/server emit → `metrics-instrumentation`.
- "Did the change work?" → `ab-testing`; "where do users drop?" → `funnel-analytics`.
- Retention by signup week → `cohort-analysis`; live dashboards/streaming → `real-time-analytics`.
- "What do we even measure?" → `kpi-framework`; rendering a chart/figure → `data-visualization`.

## Spine
Discover → Analyze → Execute → Validate. Gates: constitution v6.0.0, evidence tags, script-first. [CONFIG]

## Validation gate (done = all true)
- Exactly one playbook Read; topic matches the enum verbatim. [CONFIG]
- Every statistical/numeric claim carries a tag; `[SUPUESTO]` paired with a
  verification step. [DOC]
- A/B claims state sample size + significance, never "green = win" before the
  experiment powers out. [INFERENCIA]

## Assets
Routing guard and gate live in `assets/` — `assets/routing-checklist.md`
(resolve one topic) and `assets/quality-rubric.json` (guardian gate). [CONFIG]

## Anti-patterns
Loading multiple playbooks; guessing a topic instead of asking when two fit;
reporting metrics without instrumentation provenance; calling a test before it
reaches significance; inventing benchmark numbers. [SUPUESTO]