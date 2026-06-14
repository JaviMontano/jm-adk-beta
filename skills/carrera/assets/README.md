# carrera — assets bundle

Deterministic, offline support files for the `carrera` router. Each asset is
declared in `manifest.json` with its `used_by` targets, all of which exist in
this skill. [DOC]

## Contents

| Asset | Type | What it does | Used by |
|-------|------|--------------|---------|
| `quality-rubric.json` | rubric | Gate dimensions the guardian applies before a deliverable ships (single-playbook, contract shape, evidence-tied, one tag family, determinism, stop-on-empty, governance). All gates must pass. | `agents/guardian.md`, `templates/output.md`, `SKILL.md` |
| `routing-keywords.json` | lookup | Intent-keyword hints that help the router disambiguate the twelve `routes.json` topics. On a tie, ask one question — do not auto-pick. | `README.md`, `prompts/primary.md`, `SKILL.md` |

## Rules
- Assets are reference data, not a substitute for reading the active playbook.
- Keep them offline and deterministic: no network, no wall-clock, no randomness. [CONFIG]
- Per-topic policy assets (acceptance filters, PIVOTE rubric, status/evidence/date
  policies, output contracts) live in each Alfa playbook's own `assets/` and are
  invoked by that playbook, not duplicated here. [DOC]
