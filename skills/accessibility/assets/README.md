# assets/ — accessibility bundle

Reusable artifacts that back the accessibility router's gates and deliverables.
Each is grounded in the four playbooks (audit, design, testing, writing) and their
Quality Gates. [DOC]

## Contents
- **quality-rubric.json** — five weighted scoring dimensions (routing integrity,
  criterion traceability, evidence completeness, no-green-as-success, tag &
  governance) with `pass_when` conditions and the status vocabulary. Used by
  `agents/guardian.md` to render the final verdict and by `templates/output.md`'s
  gate section.
- **checklist.md** — the deliverable gate checklist mirroring the playbooks' Quality
  Gates. Used by `agents/guardian.md` and `SKILL.md`'s validation gate before
  declaring "done".

## How to use
1. Run the routed playbook (Discover → Analyze → Execute → Validate).
2. Fill `templates/output.md`.
3. Score against `quality-rubric.json`; every dimension must pass.
4. Walk `checklist.md`; any unchecked box blocks completion.

See `manifest.json` for the machine-readable index and `used_by` mapping.
