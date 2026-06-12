<!-- distilled from alfa skills/alerting-strategy -->
<!-- > -->
# Alerting Strategy
> "Method over hacks."
## TL;DR
Design alerts that page a human only for actionable, user-impacting problems. Three pillars: severity classification (what woke you up), routing/escalation (who fixes it), fatigue control (so signals stay trusted). [EXPLICIT]

## Deterministic Hardening Contract

Produce an alerting strategy checkable offline — no network, wall-clock, or random dependencies. `assets/` is the contract source:

- `assets/alerting-strategy-contract.json`: required report sections and validation checks.
- `assets/severity-policy.json`: allowed severity levels and response targets.
- `assets/rule-policy.json`: alert rule fields and threshold requirements.
- `assets/escalation-policy.json`: ownership, routing, and escalation requirements.
- `assets/fatigue-policy.json`: deduplication, suppression, grouping, and review cadence controls.
- `assets/evidence-policy.json`: allowed evidence tags and provenance rules.

Validate any JSON alerting strategy (request or handoff) with `scripts/validate_alerting_strategy.py`. Fixture smoke test: `bash skills/alerting-strategy/scripts/check.sh`. The validator is the source of truth; if prose and `assets/*.json` disagree, the JSON wins. [EXPLICIT]

## Procedure
### Step 1: Discover
- Gather SLOs, existing alerts, on-call roster, paging channels. Establish what "user impact" means for this system. [EXPLICIT]
### Step 2: Analyze
- Classify each candidate alert by severity (below) per Constitution XIII/XIV. Reject any alert with no owner or no documented response — un-actionable alerts are noise. [INFERENCIA]
### Step 3: Execute
- Write rules against the rule anatomy; wire routing/escalation; configure fatigue controls. Tag every threshold's provenance. [EXPLICIT]
### Step 4: Validate
- Run the validator and quality criteria. Confirm every page maps to a runbook. [EXPLICIT]

## Severity Classification
Symptom-based (alert on user-visible effect), not cause-based. Targets are policy defaults from `severity-policy.json`; tune per SLO, never invent. [CONFIG]

| Sev | Trigger | Notify | Response target |
|-----|---------|--------|-----------------|
| P1 / Critical | User-facing outage or SLO burn that exhausts budget fast | Page on-call now | Ack minutes; mitigate first |
| P2 / High | Degradation, imminent breach, no redundancy left | Page on-call | Same business hours |
| P3 / Warning | Trending toward a threshold; capacity headroom shrinking | Ticket / async | Next working day |
| P4 / Info | Notable, no action required | Dashboard / log only | None — never pages |

Rule: only P1/P2 may page. If a P3/P4 pages, it is misclassified. [INFERENCIA]

## Alert Rule Anatomy
Every rule (fields per `rule-policy.json`) carries: name, owner team, severity, signal/query, threshold, `for:` duration (sustained-breach window to kill flapping), runbook link, and the dashboard for triage. A threshold with no `for:` window and no runbook fails validation. [CONFIG]

## Escalation & Routing
- Each alert resolves to exactly one owning team at fire time — no "everyone" channels. [CONFIG]
- Tiered escalation: primary on-call -> secondary after N minutes unacked -> manager/incident-commander. Timers come from `escalation-policy.json`. [CONFIG]
- Quiet hours/handoff: routing must name a 24/7 owner or an explicit "no page overnight" decision per severity. [EXPLICIT]

## Fatigue Control
Controls per `fatigue-policy.json` — fatigue is the top failure mode of alerting [INFERENCIA]:
- **Dedup**: collapse identical firings into one notification.
- **Group**: batch related alerts (same service/incident) into a single page.
- **Suppress/inhibit**: a P1 mutes its downstream P2/P3 symptoms; suppress during known maintenance windows.
- **Review cadence**: periodically retire alerts that never led to action (noisy/low-precision). Track per-alert actionability. [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Every alert has owner, severity, threshold, `for:` window, and runbook link [EXPLICIT]
- [ ] Only P1/P2 page; P3/P4 route async [EXPLICIT]
- [ ] Validator passes against `assets/*.json` [EXPLICIT]

## Acceptance Criteria
Done means: validator green; no orphan alerts (every alert -> owner -> runbook); no severity can page that policy forbids; thresholds are SLO-derived and tagged, not guessed. [EXPLICIT]

## Worked Example
API error rate: `5xx_ratio > 2% for 5m`, sev P1, owner=payments, runbook=`/runbooks/api-5xx`, dashboard=`/d/api-health`. A `for: 5m` window stops a 30-second blip from paging; the P1 inhibits the correlated "checkout latency" P2 so on-call gets one page, not two. [INFERENCIA]

## Failure Modes
| Failure | Symptom | Fix |
|---------|---------|-----|
| Cause-based alerting | Pages on CPU/disk that users never feel | Alert on symptoms (latency, errors, SLO burn) [INFERENCIA] |
| No `for:` window | Flapping, repeated pages on transient blips | Add sustained-breach duration |
| Orphan alert | Fires, nobody owns it, ignored | Assign owner + runbook or delete |
| Threshold guessing | Too sensitive or too lax vs. reality | Derive from SLO/historical data, tag source [SUPUESTO] |
| Alert sprawl | Page volume rises, trust falls | Run review cadence; retire never-actioned alerts |

## Usage

Example invocations:

- "/alerting-strategy" — Run the full alerting strategy workflow
- "alerting strategy on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) and existing SLO/on-call definitions [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions; defines the strategy, not the per-tool deployment syntax [EXPLICIT]
- Anti-scope: not an incident-response runbook (see `incident-response.md`) nor a monitoring/instrumentation setup (see `monitoring-setup.md`) [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No SLOs defined | Flag as blocker; thresholds become `[SUPUESTO]` until SLOs exist |
| Alert with no owner | Reject — assign owner or delete before shipping |
