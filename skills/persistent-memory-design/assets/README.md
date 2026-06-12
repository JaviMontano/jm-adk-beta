# Assets — persistent-memory-design

Offline contracts that make the memory design **checkable**, not just described. The guardian and `scripts/check.sh` load these to accept or reject a design. `manifest.json` is the index; every `used_by` target is a real file in this skill.

## Bundle

| Asset | Type | Role |
|---|---|---|
| `memory-schema.json` | JSON Schema | Required fields of a design report: repo-relative path, fixed four sections, entry filter, read-once protocol, idempotent write policy, `survives_compact`. Used by `SKILL.md`, `agents/guardian.md`. |
| `memory-policy.json` | JSON config | Allowed-path rules, fixed sections, evidence rule (`[src:… @ …]`), read-once / idempotent-write / survives-compact policies, blocked anti-patterns, route-aways. Used by `SKILL.md`, `agents/guardian.md`. |
| `quality-rubric.json` | JSON rubric | Scored, mostly-blocking acceptance criteria mapped to the gate and eval cases. Used by `agents/guardian.md`, this README. |
| `memory-checklist.md` | Checklist | Human pre-delivery mirror of the acceptance gate, with evidence tags. Used by `knowledge/body-of-knowledge.md`, this README. |

## How they combine

1. A design report (JSON) is produced from `templates/output.md`.
2. `bash skills/persistent-memory-design/scripts/check.sh` validates it against `memory-schema.json` + `memory-policy.json`.
3. The guardian scores it with `quality-rubric.json`; the human runs `memory-checklist.md`.
4. The design is accepted only when every blocking criterion is met **with evidence**.

The blocked anti-patterns (`raw_transcript_dump`, `reread_each_turn`, `full_file_rewrite`, `variable_schema_across_sessions`, `unvalidated_in_findings`, `unsafe_path_escape`) are exactly the negative eval cases.

Governance: harness voice; evidence tags; single brand (JM Labs); no invented prices; no client PII.
