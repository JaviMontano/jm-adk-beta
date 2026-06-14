# Assets bundle — project-create

Reusable, deterministic assets that the skill and its agents consume.

| Asset | What it is | Consumed by |
|---|---|---|
| `quality-rubric.json` | Weighted pass/partial/fail rubric for the six gate criteria (placement, missing-only, Rule-9, NOW band, registry, evidence). | `agents/guardian.md`, `SKILL.md` |
| `checklist.md` | Run-before-done acceptance checklist mapping 1:1 to the guardian gate. | `README.md`, `SKILL.md` |

## Usage

- The **guardian** scores each run against `quality-rubric.json`; any `fail`
  blocks the overall verdict. [DOC]
- The lead/support walk `checklist.md` before emitting the scaffold summary. [DOC]

These assets carry no prices and no client PII, and stay single-brand (JM Labs). [DOC]
