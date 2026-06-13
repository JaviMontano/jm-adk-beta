# Assets Bundle — Tool Use Design

Prescribed, skill-owned artifacts that make the routing-contract gate enforceable and repeatable. These are consumed by `SKILL.md` (validation gate, output rules) and the skill `README.md`.

## Contents

| Asset | Type | Purpose |
|-------|------|---------|
| `quality-rubric.json` | rubric | Per-criterion fail/pass rubric the guardian scores a report against (contract completeness, reciprocal boundary, overload resolution, repo strategy, Edit safety, determinism, evidence discipline). |
| `checklist.md` | checklist | Pre-close checklist mapping each gate item to its Alfa-core evidence tag. |

## How they are used

- `SKILL.md` references the `assets/` bundle from its Output Rules and Validation gate; the rubric encodes those acceptance criteria as scoreable items.
- The guardian agent scores a draft report against `quality-rubric.json` before allowing close.
- `checklist.md` is the human-runnable pre-close pass.

## Governance

All assets carry Alfa-core evidence tags only. No client PII, no prices, single brand. The policy JSONs named in `SKILL.md` (`description-contract-policy.json`, `boundary-policy.json`, `repo-strategy-policy.json`, `edit-safety-policy.json`, `anti-pattern-policy.json`, `tool-use-contract.json`) are created on demand by the skill before validation when a kit run requires them.
