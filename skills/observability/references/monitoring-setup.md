<!-- distilled from alfa skills/monitoring-setup -->
<!-- > -->
# Monitoring Setup
> "Method over hacks."

## TL;DR
First-time instrumentation: metrics, dashboards, SLOs/SLIs. Output names every
signal, binds each to a source and an SLO, and states retention + cardinality
budget before declaring coverage. Not alerting (→ alerting-strategy), not
liveness probes (→ health-check-automation). [EXPLICIT]

## Procedure
### Step 1: Inventory Signals
- Enumerate the four golden signals per service: latency, traffic, errors,
  saturation. Record each as observed, derivable, or unavailable. [DOC]
- Tag each signal with its source (exporter, log, trace) and scrape interval.
### Step 2: Define SLIs/SLOs
- Per user journey pick one SLI (p99 latency, error rate); bind SLO target +
  window. No metric ships without a consumer (dashboard or SLO). [INFERENCIA]
- Set a label cardinality budget; high-cardinality labels (user_id, request_id)
  go to traces/logs, never metric labels — they explode TSDB cost. [DOC]
### Step 3: Instrument & Store
- Implement with evidence tags; prefer existing exporters over custom code. [INFERENCIA]
- Declare retention per resolution (raw / rollup) and a cost ceiling. [SUPUESTO]
### Step 4: Validate
- Each dashboard panel maps to a named SLI and renders real data, not
  placeholders; metric names survive a service restart. [INFERENCIA]
## Quality Criteria
- [ ] Every metric has a named source and a consumer (dashboard or SLO).
- [ ] SLOs have target + window; cardinality budget + retention/cost stated.
- [ ] Evidence tags applied; Constitution XIII/XIV honored.

## Edge Cases
| Scenario | Handling |
|----------|----------|
| No baseline traffic | Ship instrumentation; defer SLO targets, flag provisional |
| Metric explosion / spend | Move high-cardinality dims to logs/traces |
| Vendor lock-in risk | Emit OpenTelemetry; keep backend swappable [SUPUESTO] |
