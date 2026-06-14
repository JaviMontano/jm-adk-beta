# Product-Analytics Deliverable

> Fill verified fields; mark anything unsourced `not verified`. Tag every
> non-obvious claim `[DOC] [CONFIG] [CÓDIGO] [INFERENCIA] [SUPUESTO]`.

## 1. Routing
- **Resolved topic:** `<one of: ab-testing | analytics-events | cohort-analysis | data-visualization | funnel-analytics | kpi-framework | metrics-instrumentation | real-time-analytics>`
- **Depth:** `<quick | deep>`
- **Why this route (and not the near-fit):** <one line>
- **Playbook read:** `references/<topic>.md`

## 2. Scope & evidence inventory
- **Business goal / decision this informs:**
- **Unit of analysis:** <user | account | session | order | lead | device>
- **Evidence available:** <events, tables, dashboards, specs, code>
- **Gaps (`not verified`):**

## 3. Definitions & contract
| Field | Value | Evidence |
|---|---|---|
| Primary metric / event | | |
| Definition (numerator / denominator) | | |
| Owner | | |
| Window / scope / aggregation | | |
| Guardrails | | |

## 4. Analysis / specification
<Route-specific body — pick the matching block:>
- **ab-testing:** hypothesis · MDE · power · α · sample size · method · duration · decision rule.
- **analytics-events:** event rows (name · domain · trigger · owner · properties · identity · privacy).
- **kpi-framework:** metric tree (North Star → leading drivers → levers); KPI rows with targets.
- **funnel-analytics:** funnel table (step · event · count · step rate · overall rate · status) + drop-off read.
- **cohort-analysis:** retention grid (cohort × period) + per-cohort one-line read.
- **metrics-instrumentation:** parameter spec (name · type · scope · unit · cardinality · PII · capture side).
- **real-time-analytics:** latency budget · transport · window sizing · alert config.
- **data-visualization:** goal · chart type · library · palette · interactivity · fallback.

## 5. Findings vs hypotheses
- **Verified findings:**
- **Hypotheses (not causal claims):**
- **Validity threats checked:** <SRM, peeking, Simpson's, survivorship, late data, flapping — as relevant>

## 6. Recommendations / next steps
1. Instrumentation fixes:
2. Experiments / research:
3. Product changes:

## 7. Validation gate
- [ ] Exactly one playbook read; topic matches enum verbatim.
- [ ] Every numeric/statistical claim carries an evidence tag.
- [ ] No fabricated baselines/traffic/benchmarks; gaps marked `not verified`.
- [ ] No significance/lift/causality claimed without data + method.
- [ ] No direct PII in the deliverable.

## 8. Residual risks & assumptions
-
