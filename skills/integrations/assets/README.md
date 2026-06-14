# Assets — integrations

Supporting assets for the integrations router. Each is referenced by an existing
skill file (see `manifest.json` `used_by`).

## Contents
- **quality-rubric.json** — weighted scoring rubric across the six integration
  quality dimensions (routing discipline, verify-before-trust, idempotency,
  secrets handling, topic failure coverage, evidence governance). The guardian
  agent and the Validation gate score against it. Used by `agents/guardian.md`
  and `templates/output.md`.
- **checklist.md** — the run-before-done routing + gate checklist, mirroring the
  rubric in actionable form. Used by `SKILL.md` and `README.md`.

## How to use
1. While executing, work the `checklist.md` items in order.
2. At the gate, score each `quality-rubric.json` dimension `fail|partial|pass`.
3. Honor `gate_threshold`: no dimension at `fail`, and verify-before-trust plus
   idempotency must be `pass`. Otherwise return failing items to lead/support.

Assets are skill-local and provider-agnostic; they encode the cross-topic
security boundary, not any single provider's API surface.
