# Assets — mcp-engineering

Deterministic contract bundle for the mcp-engineering skill. These files are the
machine-checkable backbone of the acceptance gate: the guardian agent and the
deterministic scripts evaluate a deliverable against them.

## Contents

| Asset | Type | Purpose | Consumed by |
|---|---|---|---|
| `quality-rubric.json` | JSON | Binary acceptance criteria (scope, env-var secrets, typed error fields, error→retryability mapping, bounded client retry, leak remediation, MCP-vs-built-in, deterministic evidence). | `agents/guardian.md`, `SKILL.md` |
| `checklist.md` | Markdown | Human-readable checklist mirroring the rubric for the guardian gate. | `agents/guardian.md` |
| `manifest.json` | JSON | Asset registry validated by the DoD gate. | tooling |

## How to use

1. The guardian agent loads `quality-rubric.json` and walks `checklist.md` item by
   item against the deliverable.
2. Required criteria must all hold; `leak_remediation_complete` is conditional on a
   secret having leaked.
3. When the deliverable is JSON, certify only after `scripts/check.sh` accepts the
   valid fixture and rejects mutated ones — never green-as-success.

## Conventions

Evidence tags (`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`) accompany
every rubric criterion. Single-brand, no invented prices, no client PII.
