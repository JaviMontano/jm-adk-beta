---
name: product-analytics
description: "Product and business analytics: event instrumentation, KPIs, A/B tests, cohorts, funnels, and data visualization. Topics: ab-testing, analytics-events, cohort-analysis, data-visualization, funnel-analytics, kpi-framework, metrics-instrumentation, real-time-analytics."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
