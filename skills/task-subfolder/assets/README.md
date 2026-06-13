# Assets — task-subfolder

Deterministic backing for the validation gate. These files make the guardian's
verdict reproducible across sessions instead of vibes-based.

| Asset | Type | Purpose | Used by |
|---|---|---|---|
| `dod-checklist.md` | checklist | Binary yes/no gate run before "done": existence, identity, spec, journal, idempotency, evidence, governance. | `agents/guardian.md`, `SKILL.md` |
| `quality-rubric.json` | rubric | 0–3 scored dimensions (completeness, identity, idempotency, journal discipline, evidence tagging, governance) with a pass threshold. | `agents/guardian.md`, `prompts/meta.md` |

## How they are used

1. The **guardian** runs `dod-checklist.md` as the hard gate — any `no` blocks
   completion (SKILL.md §4).
2. It then scores the run with `quality-rubric.json`; pass requires every
   dimension ≥ 2 and no hard-gate failure.
3. `prompts/meta.md` and `prompts/variations/deep.md` cite these so the quick and
   deep paths share one definition of quality.

No prices, single brand, Jarvis tags only — consistent with the skill contract.
