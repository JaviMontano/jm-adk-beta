# Observability Output — {{topic}} ({{depth}})

> Routed deliverable. One playbook applied. Every non-obvious claim tagged
> `[EXPLICIT]/[DOC]/[CONFIG]/[INFERENCIA]/[SUPUESTO]`.

## 1. Routing decision
- **Topic resolved:** {{topic}} — `references/{{topic}}.md`
- **Depth:** {{quick|deep}}
- **Target system:** {{service / stack}}
- **Rationale:** {{why this topic, by intent — 1 line}} [INFERENCIA]
- **Open gaps / `{VACIO_CRITICO}`:** {{missing inputs, or "none"}}

## 2. Discover
- {{inventory specific to the topic — golden signals / candidate alerts / health
  surface / log sources / incident detection + first-seen}} [EXPLICIT]

## 3. Analyze
- {{decisions: SLO targets, severity classes, thresholds, retention tiers — each
  with provenance tag}} [DOC|CONFIG|SUPUESTO]

## 4. Execute — topic deliverable

### monitoring-setup
| Signal | Source | Scrape | SLI | SLO target / window |
|--------|--------|--------|-----|----------------------|
| latency | | | p99 | |
- Cardinality budget: {{}} · Retention/cost ceiling: {{}} [DOC]

### alerting-strategy
| Name | Owner | Sev | Signal/query | Threshold | `for:` | Runbook | Dashboard |
|------|-------|-----|--------------|-----------|--------|---------|-----------|
| | | P1 | | | 5m | | |
- Routing/escalation timers: {{}} · Fatigue controls (dedup/group/suppress): {{}} [CONFIG]

### health-check-automation
| id | target | observed | threshold (dir+units) | severity | evidence (src@time) | status |
|----|--------|----------|------------------------|----------|---------------------|--------|
| | | | warn ≥ / fail ≥ | | | pass/warn/fail/unknown |
- Overall rollup: {{healthy/degraded/unhealthy}} (precedence applied) [CONFIG]

### log-management
- Schema: `timestamp` `level` `service` `correlation_id` `message` `context{}`
- Level discipline + retention tiers (hot/warm/cold): {{}}
- PII redaction at emit boundary: {{}} [DOC]

### incident-response
- Severity (matrix): {{SEV?}} · IC: {{}} · Scribe: {{}}
- Mitigation (reversible first): {{}} · Resolution criteria: {{}}
- Postmortem stub: summary / timeline / root cause / detection gap / dated actions

## 5. Validate
- [ ] Exactly one playbook applied; topic matches intent
- [ ] Every non-obvious claim tagged
- [ ] Deterministic validator GREEN (alerting-strategy / health-check-automation) [CONFIG]
- [ ] Topic quality criteria met (see playbook)
- [ ] No invented prices · no client PII · single-brand · not green-as-success

## 6. Residual risk & follow-ups
- {{provisional thresholds, deferred SLOs, skipped optional checks}} [SUPUESTO]
