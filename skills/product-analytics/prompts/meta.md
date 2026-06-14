# Meta prompt — product-analytics

Guidance for reasoning about how to run the router, not the run itself.

## Self-checks before answering
- Did I pick ONE topic, or am I hedging across two? If hedging, apply the
  cheatsheet; only ask the user when it is still genuinely ambiguous.
- Am I about to read more than one playbook? Stop — the contract is one in,
  one out.
- Is any number in my draft sourced, or did I invent a baseline/traffic/
  benchmark? Invented numbers must become `not verified` requirements gaps.
- Am I about to call a test a "win"? Confirm sample size + method first; reject
  "green = win".

## Routing tie-breakers
- analytics-events stops at the contract; metrics-instrumentation is the code-
  level capture. If the user wants names/schema, it's events; if they want the
  parameters/dimensions/scope that make a metric computable, it's instrumentation.
- funnel-analytics answers *where*; ab-testing answers *did the change cause it*.
  A funnel finding ends in a hypothesis, not a redesign.
- kpi-framework selects/defines metrics; data-visualization renders them; neither
  computes significance (that's ab-testing).

## Depth calibration
- `quick`: essentials and the one decision the user needs, fewer rows.
- `deep`: full playbook, per-step verification, validity-threat sweep,
  explicit gap report.

## Evidence reflex
Tag every non-obvious claim. Pair each `[SUPUESTO]` with how to verify it.
Prefer "not verified" over a confident fabrication.
