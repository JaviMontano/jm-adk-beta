# Quick variation — product-analytics

Fast path: `depth=quick`. The user wants the essential measurement answer, not
the full playbook.

1. Resolve the single topic from the request (cheatsheet; ask only if two routes
   truly fit).
2. Read the one matching playbook; apply only its essentials.
3. Return the minimum viable artifact for that route:
   - ab-testing → hypothesis + metric contract + sample-size readiness (or gap).
   - analytics-events → 3–6 canonical event rows with owner + trigger + props.
   - kpi-framework → North Star + 2–3 leading drivers, each with owner + decision.
   - funnel-analytics → step table + biggest drop-off + one hypothesis.
   - cohort-analysis → retention read for the named cohorts + denominator note.
   - metrics-instrumentation → the metric's params/scope/aggregation + capture side.
   - real-time-analytics → transport + window vs latency budget + one alert rule.
   - data-visualization → chart type + library + palette note.
4. Tag every numeric claim. Mark missing inputs `not verified`; do not guess.

Keep it tight. One topic, one playbook, the decision the user needs.
