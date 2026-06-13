# Assets — safe-scripting-and-bash

Deterministic assets that make this skill's safety verdict machine-checkable.
The manifest (`manifest.json`) is the index; each entry names a real file, its
type, its purpose, and which existing skill files consume it. [DOC]

## Bundle

| Asset | Type | Purpose | Used by |
|-------|------|---------|---------|
| `quality-rubric.json` | json-rubric | Blocking + high safety checks, pass-when rules, bound-verdict rule. | `SKILL.md`, `templates/output.md`, `agents/guardian.md` |
| `checklist.md` | markdown-checklist | Pre-ship self-verification mirroring the rubric. | `README.md`, `prompts/meta.md` |

## How they are used

- The Guardian (`agents/guardian.md`) maps each hazard to a `quality-rubric.json`
  check and refuses a PASS when any blocking check fails. [CONFIG]
- The safety report (`templates/output.md`) renders the rubric's checks as the
  per-check results table. [DOC]
- The Lead runs `checklist.md` via `prompts/meta.md` before declaring done. [DOC]

## Relationship to SKILL.md policy assets

`SKILL.md` also lists policy assets under "Deterministic Assets" (write-surface,
dry-run, destructive-command, portability, validation policies) that the
offline validator enforces. This README documents the DoD bundle's rubric and
checklist; both layers share the same blocking-check semantics. [DOC]

## Governance

Single-brand (JM Labs). No client PII. No invented prices. Evidence tags
(`[DOC]` `[CONFIG]` `[CODE]` `[INFERENCE]` `[ASSUMPTION]`) on non-obvious
claims. [DOC]
