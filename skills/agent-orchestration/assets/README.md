# Assets — agent-orchestration

Reusable, deterministic artifacts that back the router's gates. They are
referenced by `SKILL.md`, the agent role contracts, and the output template — not
generated fresh each run. [DOC]

## Bundle

| File | Type | Purpose | Used by |
|---|---|---|---|
| `quality-rubric.json` | rubric (JSON) | Score a dispatch packet across routing discipline, spine completeness, script-first, evidence tags, and governance. | `agents/guardian.md` |
| `routing-checklist.md` | checklist (Markdown) | Pre-emit gate the router walks top-to-bottom before returning a packet. | `SKILL.md`, `templates/output.md` |

## Rules

- Every `used_by` target in `manifest.json` is an existing file in this skill.
- The rubric's verdict rule mirrors the Guardian gate: any dimension at `fail`
  caps the verdict at PARTIAL; never report success-as-green before the gate
  runs. [DOC]
- Keep these lean and stable — they are the contract, not scratch space. [CONFIG]
