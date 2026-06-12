# Assets — pm-delivery

Reusable, skill-specific artifacts the pm-delivery router and its guardian role
consume. These are not deliverables; they are the validation scaffolding that
keeps every routed run honest. [EXPLICIT]

## Bundle contents
- **`quality-rubric.json`** — weighted scoring rubric (single-route, evidence
  tags, no-prices, topic completeness, governance, actionability) with the 30%
  `[ASSUMPTION]` warning threshold and the pass rule. Used by `SKILL.md`'s
  acceptance gate and the `guardian` role.
- **`checklist.md`** — the human-readable acceptance checklist the guardian
  walks item by item before emitting `dod=pass`. Used by `SKILL.md` and
  `agents/guardian.md`.
- **`manifest.json`** — machine-readable index of this bundle (see below).

## How they are used
`SKILL.md` references the `assets/` bundle from its acceptance gate; the
guardian role applies `checklist.md` and scores against `quality-rubric.json`.
Every `used_by` target in `manifest.json` points to a file that exists in this
skill.

## Governance
Single brand. No prices in any asset. No client PII. Constitution v6.0.0.
[EXPLICIT]
