# Assets — brand-output

Deterministic helper assets for the brand-output router. These support the
routing decision and the validation gate; they do not themselves generate
artifacts (each downstream playbook owns its own generators and contract JSON).

## Contents

| Asset | Type | Purpose | Used by |
|---|---|---|---|
| `quality-rubric.json` | json | Pass/partial/fail criteria across routing, brand, determinism, execution, validation, and governance dimensions. | `SKILL.md`, `agents/guardian.md` |
| `routing-checklist.md` | markdown | Top-to-bottom Discover→Route→Execute→Validate checklist the lead/guardian walk before delivery. | `README.md`, `agents/lead.md` |

## Conventions
- Evidence kit is Alfa core: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]`
  `[SUPUESTO]`. JSON values spell `[CODIGO]` without the accent for ASCII safety.
- Never report a criterion as `pass` by default — only when verified by evidence.
- `manifest.json` is the machine-readable index of this bundle; every `used_by`
  target is an existing file in the skill.
