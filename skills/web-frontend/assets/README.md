# web-frontend — assets bundle

Reusable artifacts the `web-frontend` router and its guardian agent consume while routing and validating a frontend task. These are skill-specific (not generic scaffolding) and tie directly to the router's gates.

## Contents
| File | Type | What it's for | Consumed by |
|------|------|---------------|-------------|
| `quality-rubric.json` | rubric (JSON) | Machine-readable scoring rubric: blocking router gates plus per-topic gates (build budgets, WCAG AA, FOUC, Profiler, PWA offline). The guardian scores deliverables against it. | `agents/guardian.md` |
| `routing-checklist.md` | checklist (Markdown) | Top-to-bottom checklist for resolving `topic`, loading one playbook, executing, and clearing the validation gate. | `README.md` |

## How to use
1. **At route time:** walk `routing-checklist.md` to land on exactly one `topic` and one playbook.
2. **At gate time:** apply `quality-rubric.json` — the blocking router gates always, plus the `topic_gates` block for the routed topic. A deliverable passes only when every blocking gate scores 2 (met-with-evidence).

## Governance
Evidence taxonomy is Alfa-core: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Never green-as-success; single brand; no client PII; Constitution v6.0.0, script-first.

See `manifest.json` for the machine-readable index of this bundle.
