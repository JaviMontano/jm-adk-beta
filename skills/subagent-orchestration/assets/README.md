# Assets — subagent-orchestration

This bundle holds the deterministic, machine- and human-readable artifacts that
bind an orchestration plan to the skill's contract.

| Asset | Type | Purpose | Used by |
|---|---|---|---|
| `quality-rubric.json` | json | The 11 blocking gates the Guardian enforces on a plan (fan-out justification, fresh-session isolation, `last_message_only`, `AgentDefinition`+`Task`, minimal provisioning, typed errors, `valid_empty`≠`access_failure`, local recovery, degraded aggregation, validation flags, governance). | `SKILL.md` |
| `checklist.md` | markdown | Legible mirror of the rubric for hand-validating a plan or as the deliverable's validation section. | `SKILL.md`, `templates/output.md` |

The authoritative plan schema referenced by `SKILL.md`
(`assets/orchestration-contract.json`) and the four policy assets
(`isolation-policy`, `error-propagation-policy`, `aggregation-policy`,
`anti-pattern-policy`) are validated offline by
`scripts/validate_orchestration_plan.py`. This bundle's rubric and checklist are
the certification-layer artifacts that wrap that contract.

See `manifest.json` for the machine-readable index.
