# Assets — data-platform

Reusable, skill-specific artifacts that the data-platform router and its agents
load at runtime. All assets are real files registered in `manifest.json`.

## Bundle

- **`quality-rubric.json`** — weighted scoring rubric over the eight DoD
  dimensions (routing, on-task, idempotency, watermark safety, batch cap,
  rollback, reconciliation, evidence tags) with a 0.85 pass threshold. Consumed
  by the validation gate referenced in `SKILL.md` and the guardian agent.
- **`checklist.md`** — the done checklist that mirrors the SKILL.md validation
  gate; used by `agents/guardian.md` and the gate section of
  `templates/output.md`.

## How to use
1. During **Execute**, fill `templates/output.md`.
2. During **Validate**, walk `checklist.md` item by item.
3. Score the run against `quality-rubric.json`; a weighted score ≥ 0.85 with no
   zero-scored dimension passes the gate.

Every `used_by` target in `manifest.json` is an existing file in this skill.
