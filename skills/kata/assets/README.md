# Assets — kata

Reusable artifacts that back the `kata` router's quality gates. These are real,
load-bearing files referenced by the skill's contract and validation flow. [DOC]

## Contents

- `quality-rubric.json` — the five-dimension scoring rubric (routing precision,
  single-playbook isolation, pattern fidelity, acceptance-criteria met, evidence
  governance) used by the guardian gate in `SKILL.md` and `agents/guardian.md`.
  All dimensions must pass; green is not proof. [DOC]
- `routing-checklist.md` — the before/after checklist the router runs to enforce
  single-playbook reading, structure fidelity, and evidence tagging; referenced by
  `SKILL.md`. [DOC]
- `manifest.json` — machine-readable index of this bundle (path, type, purpose,
  and which existing skill file consumes each asset). [DOC]

## How they are used

`SKILL.md` points operators here for the acceptance rubric and routing checklist;
`agents/guardian.md` evaluates output against `quality-rubric.json`. Every
`used_by` target in `manifest.json` is an existing file in this skill. [DOC]
