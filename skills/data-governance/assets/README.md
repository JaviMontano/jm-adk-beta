# Assets — data-governance

Reusable artifacts that support the router's execution and validation. Each asset
is registered in `manifest.json` with a `used_by` pointer to the file that
consumes it.

## Contents
- **quality-rubric.json** — weighted scoring rubric (routing fidelity, on-topic
  output, topic-specific quality criteria, evidence discipline, governance
  guardrails) with a 0.90 pass threshold. Consumed by `agents/guardian.md` and
  referenced from `SKILL.md`.
- **checklist.md** — pre-flight + execution + gate checklist enforcing the
  single-playbook router contract. Consumed by `agents/lead.md` and `README.md`.

## How to use
1. The lead runs `checklist.md` pre-flight before loading a playbook.
2. The guardian scores the finished run against `quality-rubric.json`; a run
   passes only at ≥ 0.90 with every applicable topic criterion met.

These assets are deliberately deterministic so a run's pass/fail is auditable,
not a matter of taste. [CONFIG]
