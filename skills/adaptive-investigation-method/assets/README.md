# Assets Bundle — Adaptive Investigation Method

These assets back the deterministic compiler (`scripts/compile-adaptive-investigation.py`), the validation gate (`scripts/check.sh` / `agents/guardian.md`), and the human-facing checklist. They make the method auditable: a finished investigation spec is validated against the schema and policy, scored by the rubric, and rendered with the report template.

## Files

| File | Type | Purpose | Consumed by |
|---|---|---|---|
| `investigation-schema.json` | json-schema | Required fields of an investigation spec (goal, budget, surface map, hypotheses, deep-dives, replans, stop reason, deliverable). | compiler, guardian |
| `investigation-policy.json` | json-config | Budget rules, cheap/expensive tool split, the single legal re-plan trigger, stop reasons, blocked anti-patterns, governance. | compiler, guardian |
| `report-template.md` | template | Stable Markdown shape of the rendered report. | compiler |
| `quality-rubric.json` | json-rubric | Scored, mostly-blocking acceptance criteria mapped to the gate and the fail-closed evals. | guardian |
| `investigation-checklist.md` | checklist | Human pre-delivery checklist mirroring the acceptance gate, evidence-tagged. | guardian |

## How they fit together

1. The agent produces an investigation spec.
2. The compiler validates it against `investigation-schema.json` and enforces `investigation-policy.json` (rejects missing `budget.total` and reflexive re-plan — fail-closed).
3. The guardian scores it with `quality-rubric.json` and walks `investigation-checklist.md`.
4. The compiler renders the report via `report-template.md`.

## Governance

Single brand: JM Labs. No invented prices. No client PII in specs or reports. Green is not success without backing evidence; partial coverage is declared, never hidden.
