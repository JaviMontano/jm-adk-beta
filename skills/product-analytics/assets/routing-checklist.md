# Routing checklist — product-analytics

Run this before reading any playbook. It enforces the one-in/one-out router
contract and prevents the most common misroutes. [CONFIG]

## Resolve the topic (pick exactly one)
- [ ] schema / naming / property contract → **analytics-events**
- [ ] code-level params, dimensions, scope to make a metric computable → **metrics-instrumentation**
- [ ] "did the change work / can we ship?" → **ab-testing**
- [ ] "where do users drop?" (ordered journey) → **funnel-analytics**
- [ ] retention / lifecycle by acquisition cohort → **cohort-analysis**
- [ ] "what do we even measure?" / North Star → **kpi-framework**
- [ ] live dashboard / streaming / alert threshold → **real-time-analytics**
- [ ] render a chart / figure → **data-visualization**

## Tie-breakers
- [ ] events vs instrumentation: names/schema → events; params/scope → instrumentation.
- [ ] funnel vs ab-testing: *where* → funnel; *did it cause it* → ab-testing.
- [ ] kpi vs visualization: define/select metric → kpi; render it → visualization.
- [ ] Two routes still fit after tie-breakers → ask the user; do NOT load both.

## Contract guards
- [ ] Exactly ONE playbook will be read (no cluster preload).
- [ ] `topic` matches the enum string verbatim.
- [ ] `depth` set: `quick` (essentials) or `deep` (full + verification).

## Before declaring done
- [ ] Numeric/statistical claims carry evidence tags; `[SUPUESTO]` paired with verification.
- [ ] No invented baselines/traffic/benchmarks; gaps marked `not verified`.
- [ ] No significance/lift/causality claimed before data + method exist.
- [ ] No client PII in the deliverable.
