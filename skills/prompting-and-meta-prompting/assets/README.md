# Assets — prompting-and-meta-prompting

Deterministic, machine-checkable artifacts that back the skill's quality and safety
gates. Each is declared in `manifest.json` with its `used_by` target. [CONFIG]

## Bundle

- **`quality-rubric.json`** — weighted, machine-checkable rubric for scoring a
  prompt or prompt-system deliverable. Encodes the validation-gate dimensions
  (explicit output contract, one-pass executability, embedded anti-drift,
  missing-data handling, eval coverage, safety boundary, evidence tagging) and the
  block rule: a `safety_boundary` fail blocks regardless of total score. Used by
  the Guardian gate (`agents/guardian.md`) and referenced from `SKILL.md`. [CONFIG]
- **`checklist.md`** — the human-readable delivery checklist mirroring the rubric;
  run before delivery. Used by `templates/output.md` consumers and the Guardian. [DOC]

## Relationship to SKILL.md policies

`SKILL.md` additionally names deterministic policy contracts
(`prompting-and-meta-prompting-contract.json`, `prompt-component-policy.json`,
`meta-prompt-policy.json`, `acceptance-criteria-policy.json`, `eval-case-policy.json`,
`safety-anti-drift-policy.json`). Those are validated at runtime by
`scripts/check.sh` when a JSON prompt-system report is produced; this bundle ships
the rubric and checklist that gate every deliverable, JSON report or not. [CONFIG]

## Conventions

- Every asset entry in `manifest.json` lists `path`, `type`, `purpose`, and a
  non-empty `used_by` of existing files. [CONFIG]
- Green is never reported as success on its own — a passing rubric still requires
  no safety breach. [DOC]
