# Assets — validation-retry-design

This bundle holds the deterministic, version-controlled inputs the skill validates against and scores with. Each asset is wired to a consumer via `manifest.json` (`used_by`).

## Contents

- **quality-rubric.json** — the 7-criterion scoring rubric (fail/weak/pass) for a designed retry loop. Each criterion maps to an `expected_check` (e.g. `actionable_validator -> quality_criteria`, `no_silent_failure -> silent_failure_blocker`). Consumed by the acceptance gate in `SKILL.md`.
- **checklist.md** — the pre-ship Definition-of-Done checklist; one line per gate item with its `expected_check`. Consumed by `SKILL.md` and mirrors `agents/guardian.md`.

## Policy assets referenced by SKILL.md

`SKILL.md` also references these policy files by name (`error-feedback-policy.json`, `recoverability-policy.json`, `retry-budget-policy.json`, `systematic-error-policy.json`, `escalation-policy.json`, `anti-pattern-policy.json`) and the deterministic contract `retry-loop-contract.json`. The two assets shipped here (rubric + checklist) are the scoring/gate layer; they are what the manifest tracks as existing, used-by files in this skill.

## Determinism

All assets are static JSON/Markdown so the same plan always yields the same verdict — `offline=true`, `network_required=false`, `deterministic=true`.

_Single-brand: JM Labs. No client PII in any asset._
