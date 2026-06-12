# Observability — Body of Knowledge

Domain knowledge for the observability router. Concepts, standards, and decision
rules that the five playbooks depend on. [DOC]

## 1. Core concepts

### The three pillars + the fourth signal
- **Metrics** — numeric time series (counters, gauges, histograms). Cheap to
  store, aggregatable, low-cardinality. Home of SLIs. [DOC]
- **Logs** — discrete structured events. High-cardinality detail; the place for
  `correlation_id`, request context, and per-event diagnostics. [DOC]
- **Traces** — causal spans across services for one request. Where high-cardinality
  dimensions (user_id, request_id) belong — never as metric labels. [DOC]
- **Health checks** — synthesized liveness/readiness/dependency status derived
  from the above plus probes; deterministic and gradeable offline. [DOC]

### The four golden signals (per service)
Latency, Traffic, Errors, Saturation. Each is recorded as observed, derivable,
or unavailable, tagged with its source (exporter/log/trace) and scrape interval. [DOC]

### SLI / SLO / error budget
- **SLI** — a measured ratio of good events to total (e.g. p99 latency under
  300ms, 5xx ratio under 2%).
- **SLO** — target + window bound to the SLI (e.g. 99.9% over 28 days).
- **Error budget** — `1 − SLO`; fast burn of the budget is the canonical paging
  trigger. No metric ships without a consumer (dashboard or SLO). [DOC]

## 2. Standards and references
- **OpenTelemetry** — vendor-neutral emit format for metrics/logs/traces; keeps
  the backend swappable, mitigating lock-in. [SUPUESTO]
- **Google SRE golden signals + symptom-based alerting** — alert on user-visible
  effect, not cause. [DOC]
- **ISO-8601 UTC timestamps** — mandatory in the log schema. [DOC]
- **Severity taxonomies** — alerting uses P1–P4 (only P1/P2 page); incidents use
  SEV1–SEV4 (impact-driven, round ambiguous up). [DOC]
- **Constitution XIII/XIV + Alfa evidence tags** — governance baseline for every
  output. [CONFIG]

## 3. Key data shapes

### Structured log schema (minimum)
`timestamp` (ISO-8601 UTC), `level`, `service`, `correlation_id`, `message`,
`context{}`. Never log secrets, tokens, full PANs, or passwords. [DOC]

### Alert rule anatomy
`name`, `owner team`, `severity`, `signal/query`, `threshold`, `for:` (sustained-
breach window), `runbook link`, `triage dashboard`. A threshold with no `for:`
and no runbook fails validation. [CONFIG]

### Health check record
`id`, `target`, `observed_value`, `threshold` (direction + units), `severity`,
`evidence` (source + capture time), `status` ∈ {pass, warn, fail, unknown}. [CONFIG]

## 4. Decision rules
1. **Symptom over cause** — alert and classify on user-visible effect. [INFERENCIA]
2. **Consumer-bound metrics** — a metric with no dashboard/SLO is deleted. [DOC]
3. **Cardinality budget** — high-cardinality dims go to logs/traces, never metric
   labels (TSDB cost explosion). [DOC]
4. **Only P1/P2 page** — a P3/P4 that pages is misclassified. [INFERENCIA]
5. **`for:` window mandatory** — kills flapping on transient blips. [DOC]
6. **Mitigate before root-cause** — stop the bleeding with reversible actions
   first. [INFERENCIA]
7. **Evidence over default** — never infer "safe" thresholds/retention from
   defaults; tag `[SUPUESTO]` until SLO/legal confirms. [SUPUESTO]
8. **Determinism for JSON topics** — same evidence ⇒ same status; no network,
   wall-clock, or randomness. [CONFIG]
9. **No PII in the stream** — redact at the emit boundary; stop and flag if PII is
   found in existing logs. [DOC]
10. **Rollup precedence** — required `fail` → unhealthy; required `unknown`/stale
    → degraded; `warn` → degraded; all required `pass` → healthy. [CONFIG]

## 5. Topic boundaries (anti-scope)
- Metrics/tracing setup → `monitoring-setup` (not log-management).
- Paging/severity/fatigue → `alerting-strategy` (not monitoring-setup).
- Probes/dependency status → `health-check-automation` (does not run live probes).
- Structured logs/retention/PII → `log-management` (feeds, doesn't replace, alerts).
- Live outage lifecycle → `incident-response` (assumes detection exists). [DOC]

## 6. Common failure modes
Cause-based alerting; missing `for:` window; orphan alerts; threshold guessing;
alert sprawl; metric cardinality explosion; ERROR-level noise eroding paging
trust; unknown/stale evidence claiming `healthy`; splitting incident command;
root-causing before mitigating. [INFERENCIA]
