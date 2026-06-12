# Example output — observability router (alerting-strategy, deep)

## 1. Routing decision
- **Topic resolved:** `alerting-strategy` — `references/alerting-strategy.md`
- **Depth:** deep
- **Target system:** `checkout-api` + `payments-svc`, ALB, Prometheus +
  Alertmanager, PagerDuty
- **Rationale:** request is about paging volume and fatigue, not instrumentation;
  routed by intent. [INFERENCIA]
- **Open gaps:** on-call roster + quiet-hours ownership not supplied — escalation
  finalized only after confirmation. [SUPUESTO]

## 2. Discover
- 312 pages last week, ~20 actioned → precision ≈ 6%; fatigue is the dominant
  failure mode. [EXPLICIT]
- Bulk of noise: host CPU/memory (cause-based) and a latency alert with no
  sustained-breach window (flapping). [EXPLICIT]
- SLO present: 99.9% successful checkouts / 28d → error budget = 0.1%. [EXPLICIT]

## 3. Analyze
- Retire cause-based host alerts; they fire on conditions users never feel. Keep
  saturation only where it predicts SLO burn. [INFERENCIA]
- Derive paging thresholds from the SLO burn rate, not from guessed host numbers;
  tag provenance. [SUPUESTO]
- Only P1/P2 may page; CPU/memory become P4 dashboard signals. [CONFIG]

## 4. Execute — alert rules

| Name | Owner | Sev | Signal/query | Threshold | `for:` | Runbook | Dashboard |
|------|-------|-----|--------------|-----------|--------|---------|-----------|
| checkout-slo-fast-burn | checkout | P1 | `1 - (good/total)` 1h burn | > 14.4x budget | 5m | `/runbooks/checkout-burn` | `/d/checkout-slo` |
| checkout-slo-slow-burn | checkout | P2 | 6h burn rate | > 6x budget | 15m | `/runbooks/checkout-burn` | `/d/checkout-slo` |
| payments-5xx | payments | P1 | `5xx_ratio` | > 2% | 5m | `/runbooks/pay-5xx` | `/d/pay-health` |
| host-cpu-saturation | platform | P4 | node CPU | > 85% | — | dashboard only | `/d/infra` |

- **Routing/escalation:** primary on-call → secondary after 10 min unacked →
  incident commander; quiet-hours ownership pending roster confirmation. [SUPUESTO]
- **Fatigue controls:** dedup identical firings; group `checkout-*` into one page;
  `checkout-slo-fast-burn` (P1) inhibits the correlated `payments-5xx` symptom so
  on-call gets one page, not two; monthly review retires never-actioned alerts. [CONFIG]

## 5. Validate
- [x] Exactly one playbook applied; topic matches intent
- [x] Every non-obvious claim tagged
- [x] `scripts/validate_alerting_strategy.py` reported GREEN against `assets/*.json` [CONFIG]
- [x] Every alert has owner, severity, threshold, `for:` window, runbook (P4 routes async)
- [x] Only P1/P2 page; host CPU demoted to P4
- [x] No invented prices · no client PII · single-brand · not green-as-success

## 6. Residual risk & follow-ups
- Escalation timers and quiet-hours owner are `[SUPUESTO]` until the on-call
  roster is supplied — confirm before go-live.
- Slow-burn 6x multiplier is provisional; tune against 30 days of historical burn
  data. [SUPUESTO]
- Expected effect: page volume drops from ~312/wk toward the actioned ~20, raising
  precision and restoring paging trust. [INFERENCIA]
