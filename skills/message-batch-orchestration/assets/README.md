# Assets — message-batch-orchestration

Determinism bundle that backs the acceptance gate for this skill. These are the
scoring and gating artifacts; the JSON **policy** contracts referenced inline by
`SKILL.md` (`message-batch-orchestration-contract.json`, `workload-policy.json`,
`custom-id-policy.json`, `lifecycle-policy.json`, `retry-fragmentation-policy.json`,
`evidence-policy.json`) define the report contract validated by
`scripts/check.sh`. [CONFIG]

## Files in this bundle

| Asset | Type | Used by | Purpose |
|---|---|---|---|
| `quality-rubric.json` | rubric | `agents/guardian.md`, `prompts/variations/deep.md` | Score the deliverable across the seven gate/quality dimensions (offline gate, custom_id uniqueness, lifecycle, fragmentation, selective retry + cap, no sync loop, evidence). |
| `acceptance-checklist.md` | checklist | `SKILL.md`, `templates/output.md`, `prompts/variations/deep.md` | Pre-emit gate walked before declaring a batch run done. |
| `manifest.json` | manifest | (validator) | Declares the bundle for the DoD validator; every `used_by` target exists. |

## How to use

1. Run the lifecycle (`prompts/primary.md`).
2. Walk `acceptance-checklist.md`.
3. Score with `quality-rubric.json` — every gate dimension must reach 2.
4. If evidence is required, validate the JSON report with `scripts/check.sh`.

All scoring uses the skill's evidence taxonomy
(`[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`), single brand, no
invented prices. [DOC]
