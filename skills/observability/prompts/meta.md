# Meta prompt — observability router self-check

Run this reflection before emitting any observability output. It guards the
router's invariants. [DOC]

## Routing self-check
- Did I resolve EXACTLY ONE topic, by the request's underlying symptom rather than
  a surface keyword? (e.g. "alert too noisy" is `alerting-strategy`, not
  `monitoring-setup`.)
- Did I load EXACTLY ONE playbook and avoid blending two?
- Is the chosen topic inside scope (production health), not app perf-tuning or
  CI/CD?

## Input integrity
- Is the target system/stack actually supplied, or did I invent it?
- Is any critical input missing? If so, did I stop and ASK instead of guessing
  past a `{VACIO_CRITICO}`?

## Evidence & determinism
- Does every non-obvious claim carry exactly one tag
  (`[EXPLICIT]/[DOC]/[CONFIG]/[INFERENCIA]/[SUPUESTO]`)?
- For `alerting-strategy` / `health-check-automation`: did I treat the
  `assets/*.json` policy as source of truth and run the validator to green?
- Would re-running the validator on the same evidence give the same result?

## Quality & governance
- Does the output match the routed topic's quality criteria (e.g. every alert has
  owner + `for:` + runbook; every metric has a consumer; no PII in logs)?
- Am I claiming "healthy/done" only with evidence (never green-as-success)?
- Single-brand, no invented prices, no client PII, harness voice?

## Depth calibration
- If `deep`: did I show verification at each spine step? If `quick`: did I cover
  the essentials without padding?

If any check fails, fix it before responding; if routing is still ambiguous,
ask one clarifying question.
