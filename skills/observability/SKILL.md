---
name: observability
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
