# Example input — observability router

## Request
> "Our on-call rotation is burning out. Last week they got 312 pages and acted on
> maybe 20 of them. A lot of it is host-level CPU and memory alerts plus a latency
> alert that fires on every brief spike. We run a `checkout-api` and a
> `payments-svc` behind an ALB, with Prometheus + Alertmanager and PagerDuty.
> We have an SLO of 99.9% successful checkouts over 28 days. Please redesign our
> alerting so people only get paged for things that matter."

## Parsed inputs
- **topic (inferred):** `alerting-strategy` — the symptom is paging volume and
  fatigue, not missing dashboards (which would be `monitoring-setup`) and not a
  live outage (`incident-response`). [INFERENCIA]
- **depth:** `deep` — the user wants a full redesign, not a quick patch. [INFERENCIA]
- **target system:** `checkout-api` + `payments-svc`, ALB, Prometheus +
  Alertmanager, PagerDuty. [EXPLICIT]
- **known SLO:** 99.9% successful checkouts / 28-day window — basis for
  symptom-based thresholds. [EXPLICIT]

## Critical gaps to confirm
- On-call roster and quiet-hours/24-7 ownership per severity — not supplied;
  must ask before finalizing escalation. [SUPUESTO]
- Which existing alerts have runbooks — needed to flag orphans. [SUPUESTO]

## Routing decision
Load EXACTLY ONE playbook: `references/alerting-strategy.md`. Do not pull in
`monitoring-setup.md` even though dashboards are mentioned — the request is about
paging, not instrumentation. [DOC]
