# Deep variation — observability router

Use when `depth=deep`: apply the routed playbook exhaustively with verification at
each spine step. One playbook only; depth is in thoroughness, not topic breadth.

## Steps (verify each before advancing)
1. **Resolve topic** and confirm scope; record the resolution rationale.
2. **Discover** — exhaustively inventory the surface for the topic:
   - monitoring-setup: every service's four golden signals, sources, scrape
     intervals; observed/derivable/unavailable per signal.
   - alerting-strategy: full candidate alert list, on-call roster, paging
     channels, current SLOs.
   - health-check-automation: services, dependencies, jobs, storage, queues,
     credentials, resource limits; observed/synthetic/unavailable per signal.
   - log-management: all log sources, formats, volume/day, retention, consumers,
     correlation-ID presence.
   - incident-response: detection source, first-seen timestamp, blast radius.
3. **Analyze** — evaluate options per Constitution XIII/XIV; decide SLO targets,
   severity classes, retention tiers, thresholds — each tagged with provenance.
4. **Execute** — implement every rule/check/panel/schema/mitigation; wire routing,
   escalation, fatigue controls, PII redaction as the topic requires.
5. **Validate exhaustively**:
   - Run the deterministic validator (alerting/health) and show it green. [CONFIG]
   - Walk the full quality-criteria checklist for the topic.
   - Confirm no orphan alerts, no consumer-less metrics, no PII, no
     unknown/stale-as-healthy.
6. **Document residual risk** — provisional thresholds, deferred SLOs, optional
   checks skipped — each as a dated `[SUPUESTO]` follow-up.

## Acceptance
Deep is done only when every spine step is verified, the validator is green for
JSON topics, and the full quality checklist passes with evidence.
