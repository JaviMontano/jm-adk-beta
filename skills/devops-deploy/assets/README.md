# Assets — devops-deploy

Deterministic, reusable artifacts that back the validation gate of this router
skill. They are referenced by SKILL.md, the Guardian agent, the output template,
and the eval cases — not throwaway samples. [DOC]

## Contents

| Asset | Type | Used by | Purpose |
|-------|------|---------|---------|
| `quality-rubric.json` | rubric | `SKILL.md`, `agents/guardian.md`, `evals/evals.json` | Weighted scoring across routing integrity, topic correctness, supply-chain security, release safety, and governance. All dimensions must `pass`. |
| `checklist.md` | checklist | `templates/output.md`, `agents/guardian.md` | Pass/fail reviewer checklist mirroring the SKILL.md validation gate. |
| `manifest.json` | index | — | Machine-readable map of this bundle; every `used_by` target exists. |

## How they are used

1. **Support** produces the artifact via `templates/output.md`.
2. **Guardian** scores it against `quality-rubric.json` and walks `checklist.md`.
3. A deliverable is **done** only when no rubric dimension is `fail` and every
   applicable checklist item is checked — green build alone never qualifies. [DOC]

## Governance
All assets follow the evidence taxonomy (`[CÓDIGO] [CONFIG] [DOC] [INFERENCIA]
[SUPUESTO]`), carry no secret values or prices, and stay single-brand.
Constitution v6.0.0. [DOC]
