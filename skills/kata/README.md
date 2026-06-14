# kata — Agentic Engineering Katas (router)

A single-entry router over 30 distilled agentic-engineering playbooks ("katas")
from JM Labs. Each kata captures one proven pattern for building Claude agents:
loop control, tool selection, structured extraction, hooks, memory, multi-agent
topology, sampling, caching, and review harnesses. [DOC]

## What it does

Resolves a `topic` to EXACTLY ONE playbook under `references/`, reads only that
file, and applies its recipe and acceptance criteria. It is a hub: it does not
hold the recipes itself, it routes to the spoke that does. [DOC]

## When to use

Use when a request maps to a known agentic pattern and you want the certified
JM Labs recipe instead of improvising — for example: "my agent loops forever",
"the reviewer flags too many false positives", "how do I force structured JSON",
"where should the guardrail live", "the subagent inherits too much context". [INFERENCIA]

Do NOT use as generic chat. If no `topic` in `routes:` fits, say so and route the
user elsewhere rather than guessing a near-match. [DOC]

## How it routes / executes

1. Map request → `topic` (one of the 30 `routes:` keys in `SKILL.md`). If two are
   genuinely plausible, present both and ask. [DOC]
2. Read EXACTLY ONE playbook. Loading several "to compare" dilutes context and
   defeats the hub-and-spoke isolation the kit teaches. [INFERENCIA]
3. Execute along the spine: Discover → Analyze → Execute → Validate. [DOC]
4. Apply the playbook's own acceptance criteria before declaring done. Honor the
   `depth` param: `quick` → essentials + validation gate; `deep` → exhaustive. [DOC]

## Evidence taxonomy

All claims carry an Alfa-core tag — `[DOC]`, `[CÓDIGO]`, `[CONFIG]`, `[INFERENCIA]`,
`[SUPUESTO]` — never mixed with the Jarvis operator family. See
`../../references/verification-tags.md`. [DOC]

## References

The 30 katas live under `references/` and are indexed in `routes.json` (key →
playbook path + Alfa source id). Representative spokes: [DOC]

- `references/deterministic-agent-loop.md` — halt by typed `stop_reason`, not prose.
- `references/false-positive-criteria.md` — categorical criteria with P/N examples.
- `references/defensive-structured-extraction.md` — JSON Schema + forced `tool_choice`.
- `references/pretooluse-guardrails.md` — deterministic deny in a PreToolUse hook.
- `references/hub-and-spoke-isolation.md` — empty-context subagents via Task.
- `references/prefix-caching.md` — static-first / dynamic-last cache ordering.

## Bundle

- `agents/` — lead, specialist, support, guardian role contracts for this router.
- `knowledge/` — body of knowledge + knowledge graph over the kata clusters.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — the kata-application deliverable scaffold.
- `evals/evals.json` — routing + application test cases.
- `examples/` — a worked routing-and-application example.
- `assets/` — quality rubric and routing checklist (see `assets/README.md`).
