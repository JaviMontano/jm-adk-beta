---
name: observability
version: 1.0.0
description: "Production health: monitoring, logging, alerting, health checks, and incident response. Topics: alerting-strategy, health-check-automation, incident-response, log-management, monitoring-setup."
params:
  topic:
    enum: [alerting-strategy, health-check-automation, incident-response, log-management, monitoring-setup]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  alerting-strategy: references/alerting-strategy.md
  health-check-automation: references/health-check-automation.md
  incident-response: references/incident-response.md
  log-management: references/log-management.md
  monitoring-setup: references/monitoring-setup.md
---

# observability

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`. [DOC]
## When to use
Production-health work: stand up monitoring, design alerts, automate health
checks, manage logs, run an incident. Not app perf-tuning or CI/CD. [INFERENCIA]

## Inputs → Outputs
- **In:** `topic` (required), `depth` (quick|deep), target system/stack context.
- **Out:** routed playbook applied to the user's system — config, runbook, or
  remediation, with evidence tags on every non-obvious claim. [DOC]

## Resolve the topic
Pick the single best match; route by intent, not keyword overlap. [INFERENCIA]
- **monitoring-setup** — first-time metrics/dashboards/SLO instrumentation.
- **alerting-strategy** — thresholds, routing, noise/fatigue, on-call paging.
- **health-check-automation** — liveness/readiness probes, synthetic checks.
- **log-management** — structured logging, aggregation, retention, querying.
- **incident-response** — live outage: triage, comms, mitigation, postmortem.

Disambiguate: "alert too noisy" → alerting-strategy (not monitoring-setup);
"is it up?" automation → health-check-automation; "what broke just now?" →
incident-response. If still ambiguous after one read of the request, ASK —
never guess past a `{VACIO_CRITICO}`. [DOC]

## Spine, gates & done-when
Discover → Analyze → Execute → Validate. `deep` = apply playbook exhaustively
with verification each step; `quick` = essentials only. Enforce constitution
v6.0.0, Alfa evidence tags, the script-first rule. [CONFIG]
**Done when:** routed topic matches intent; exactly one playbook loaded; output
tagged; `deep` runs verified each step. [DOC]

## Anti-patterns
Loading the whole cluster; routing on a single keyword; auto-filling a missing
target system instead of asking; emitting untagged claims. [INFERENCIA]

## Assets
Routing and acceptance policies live in `assets/` (`routing-matrix.json`,
`quality-rubric.json`); see `assets/README.md`. [CONFIG]