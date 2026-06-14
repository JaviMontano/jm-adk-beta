# Assets — workspace-setup

Concrete, load-bearing assets for designing and gating a `.jm-adk.local.json`
setup plan. Every entry here is registered in `manifest.json` with a real
`used_by` target.

| Asset | Type | What it does |
|-------|------|--------------|
| `workspace-setup-plan-contract.json` | JSON Schema | The deterministic contract a setup plan must satisfy: required blocks (`target_file`, `mode`, runtime preferences, command/privacy/write policy, evidence, validation checks), enumerated evidence tags, and the mandatory `assets` / `deterministic_scripts` / `quality_criteria` checks. The offline validator targets this. |
| `quality-rubric.json` | Rubric | Seven hard gates (dry-run default, secret containment, overwrite guard, offline determinism, policy completeness, git safety, evidence governance). Used by the guardian and the meta self-check. A single failed gate blocks apply. |
| `apply-checklist.md` | Checklist | The pre-apply / write-safety / governance gates run before any write. Used by support and embedded in the output template. |

## Rules
- The plan contract is referenced as a build target in `SKILL.md`; the matching
  validator (`scripts/validate_workspace_setup_plan.py`) and fixtures are the
  skill's planned deliverables and are tagged `[ASSUMPTION]` until present.
- No asset stores secrets or PII. Evidence tags use the Alfa core family only.
- Keep assets deterministic — no network, clock, or randomness baked in.
