# product-analytics — README

Router skill for product and business measurement. One request comes in, the
skill resolves a single `topic`, reads exactly one playbook, and applies it to
the user's case with Alfa-core evidence tags. [CONFIG]

## What it does
Covers the measurement lifecycle end to end across eight routes:
- **analytics-events** — event taxonomy, naming, property/identity contracts.
- **metrics-instrumentation** — code-level capture: dimensions, params, scope.
- **kpi-framework** — metric trees, North Star, leading→lagging chains, OKRs.
- **funnel-analytics** — ordered journeys, denominators, drop-off, hypotheses.
- **cohort-analysis** — retention curves, cohort-vs-cohort, lifecycle stages.
- **ab-testing** — experiment design, sample size, decision rules, validity.
- **real-time-analytics** — streaming transport, latency budgets, alerting.
- **data-visualization** — chart selection, library choice, a11y, live updates.

## When to use
A request touches defining metrics, instrumenting or auditing events, designing
or reading an experiment, building cohorts/funnels, streaming live data, or
charting results. Not for app feature code, infra, or generic ETL. [INFERENCIA]

## How it routes / executes
1. Resolve `topic` from the request (ask only if two routes genuinely fit).
2. Read EXACTLY ONE playbook from `routes:` — never preload the cluster.
3. Apply the playbook's Discover → Analyze → Execute → Validate spine at the
   requested `depth` (`quick` essentials vs `deep` full playbook).
4. Pass the validation gate: one playbook read, evidence tags on every numeric
   claim, no significance claimed before an experiment powers out. [CONFIG]

## Disambiguation cheatsheet
- Event schema/naming → `analytics-events`; wiring SDK emit → `metrics-instrumentation`.
- "Did the change work?" → `ab-testing`; "where do users drop?" → `funnel-analytics`.
- Retention by signup week → `cohort-analysis`; live dashboards → `real-time-analytics`.
- "What do we measure?" → `kpi-framework`; rendering a chart → `data-visualization`.

## References
- [SKILL.md](SKILL.md) — router contract, params, validation gate.
- [references/](references/) — the eight topic playbooks (one read per run).
- [knowledge/body-of-knowledge.md](knowledge/body-of-knowledge.md) — domain concepts and decision rules.
- [templates/output.md](templates/output.md) — deliverable scaffold.
- [assets/](assets/) — quality rubric and routing checklist (see assets/README.md).

## Governance
Single-brand, harness voice. Evidence tags `[DOC] [CONFIG] [CÓDIGO]
[INFERENCIA] [SUPUESTO]` on every non-obvious claim. No invented benchmark
numbers, no prices, never "green = win" before significance. No client PII in
deliverables. [CONFIG]
