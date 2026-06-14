# observability — skill overview

Router skill for production-health work. Resolves a single `topic`, then loads
EXACTLY ONE playbook and applies it to the user's system. Output is the routed
playbook's deliverable (config, runbook, policy, or remediation) with evidence
tags on every non-obvious claim. [DOC]

## What it does
Covers the five production-health surfaces and nothing else:

| topic | When | Playbook |
|-------|------|----------|
| `monitoring-setup` | First-time metrics/dashboards/SLO instrumentation | `references/monitoring-setup.md` |
| `alerting-strategy` | Severity, routing/escalation, alert-fatigue control | `references/alerting-strategy.md` |
| `health-check-automation` | Deterministic liveness/readiness/dependency checks | `references/health-check-automation.md` |
| `log-management` | Structured logging, levels, retention, PII, search | `references/log-management.md` |
| `incident-response` | Live outage: classify, mitigate, resolve, postmortem | `references/incident-response.md` |

## When to use
Stand up monitoring, design alerts, automate health checks, manage logs, or run
an incident. NOT app perf-tuning, NOT CI/CD. [INFERENCIA]

## How it routes
1. Resolve `topic` from the request by intent, not keyword overlap.
2. Read EXACTLY ONE playbook from `routes:`; never load the whole cluster.
3. Apply the spine: Discover → Analyze → Execute → Validate.
4. `depth=deep` applies the playbook exhaustively with verification at each step;
   `depth=quick` covers essentials only.

Disambiguation rule: "alert too noisy" → `alerting-strategy` (not
`monitoring-setup`); "is it up?" automation → `health-check-automation`; "what
broke just now?" → `incident-response`. If still ambiguous after one read, ASK —
never guess past a `{VACIO_CRITICO}`. [DOC]

## Evidence taxonomy
Every claim carries one tag: `[EXPLICIT]` (stated by user/source), `[DOC]`
(from a playbook/standard), `[CONFIG]` (from an `assets/*.json` policy),
`[INFERENCIA]` (reasoned), `[SUPUESTO]` (assumption pending confirmation).
The deterministic topics (`alerting-strategy`, `health-check-automation`) treat
their `assets/*.json` policies as source of truth: if prose and JSON disagree,
the JSON wins. [CONFIG]

## Deterministic backbone
`alerting-strategy` and `health-check-automation` ship offline validators
(`scripts/validate_alerting_strategy.py`, `scripts/validate_health_check.py`)
plus `scripts/check.sh` fixture smoke tests. A green validator is the acceptance
gate for those topics. [CONFIG]

## References
- `references/monitoring-setup.md`
- `references/alerting-strategy.md`
- `references/health-check-automation.md`
- `references/log-management.md`
- `references/incident-response.md`

## Assets
See `assets/README.md` and `assets/manifest.json` for the routing/quality bundle
used by `SKILL.md` and these agents.
