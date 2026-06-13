# Tool Use Design — Overview

Design every tool description as a **deterministic routing contract** a planner can act on with zero hidden context. The skill turns vague tool surfaces into a set of descriptions where the model picks the right tool by name + boundary, never by guessing or asking.

## What it does

- Inventories a tool surface (≥2 tools) and detects **overloading** (two tools a human would confuse).
- Rewrites each description as a contract: purpose · input format · output shape · 1–2 invocation examples · **reciprocal boundary** ("use X for A; for B use Y" — and Y points back to X).
- Resolves overload with **rename + split**, not clarifying prose.
- Encodes the built-in repo strategy `Grep → Read → Edit` and bans `Glob("**/*") + Read all` upfront.
- Documents the `Edit` failure mode (non-unique `old_string`) and its `Read + Write` full-rewrite fallback.
- Emits an offline-validable JSON report plus the rewritten contracts.

## When to use it

Activate when at least one holds: two tools overlap in purpose; the agent picks the wrong tool or asks for clarification when the decision should be immediate; a description is generic (`"Analyzes content"`); you operate on an unknown repo with no read protocol; or `Edit` fails intermittently with no documented fallback.

Do **not** activate for: drafting email/prose, running a single shell command, or any task without a routing decision between ≥2 tools (see `evals/evals.json` false-positive cases).

## How it routes / executes

1. Inventory the surface → flag overlaps.
2. Write each description as a contract (input format, output shape, examples, reciprocal boundary).
3. Split overloaded tools (rename, do not narrate).
4. Document the `Edit` fallback.
5. Encode `Grep → Read → Edit`; forbid read-all upfront.
6. Validate against the acceptance gate before closing.

## References

- `SKILL.md` — full contract, pattern/anti-pattern, validation gate.
- `knowledge/body-of-knowledge.md` — concepts, standards, decision rules.
- `knowledge/knowledge-graph.json` — concept graph over the skill's key ideas.
- `templates/output.md` — deliverable scaffold (report JSON + rewritten contracts).
- `assets/` — prescribed policy + rubric kit (`assets/README.md`, `assets/manifest.json`, `assets/checklist.md`).

## Evidence taxonomy

Every claim carries one Alfa-core tag: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Never mix families in one output.
