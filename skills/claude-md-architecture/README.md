# claude-md-architecture

Hierarchical `CLAUDE.md` memory design for Claude Code projects: split a growing,
always-loaded root file into a **user / team / module** layering connected by
`@imports`, with path-scoped rules activated by recursive globs (`frontend/**`,
`infra/**`). The engineering goal is a **stable cacheable prefix** (universal rules
at the root) plus on-demand subtree heuristics that load only when work touches that
subtree — keeping the KV cache economical turn after turn.

## What it does

- Inventories existing rules and classifies them into three buckets: **universal**
  (always), **per-module** (one subtree), **per-user** (personal, non-versioned).
- Emits a lean root `team CLAUDE.md` (universals + `@imports`), one
  `module/CLAUDE.md` per subtree with `apply to: "<glob>/**"`, and a documented
  **precedence table** (most-specific subpath wins; explicit tie-breaks).
- Moves personal preferences to `~/.claude/CLAUDE.md` (user scope) via `@import`,
  never into the versioned team repo.
- Validates the `@import` graph is a **DAG** with no broken or circular imports
  before any file is written.

## When to use it

- Root `CLAUDE.md` exceeded ~300 lines and now carries rules that apply to one
  module only.
- Rules that should be scoped to `frontend/**`, `infra/**`, or `tests/**` currently
  live in a single global file.
- Personal preferences (tone, individual shortcuts) are leaking into the versioned
  team repo.

**Do not use when** the repo is a single module with no divergent subtrees
(hierarchy = over-engineering), when the real problem is rule *content* rather than
*location*, or when asked to edit the user's global `~/.claude/CLAUDE.md` without
explicit confirmation.

## How it routes / executes

1. Classify rules (universal / per-module / per-user) — `agents/specialist.md`.
2. Declare the target architecture ontology-first in
   `assets/architecture-schema.json` + `assets/architecture-policy.json`.
3. Compile a reproducible report with
   `scripts/compile-claude-md-architecture.py <arch.json> --output <report.md>`.
4. Validate the gate via `bash scripts/check.sh` (DAG, no broken imports, recursive
   globs, precedence defined, no per-turn values in the prefix).

## References

- Capability, build steps, correct vs. anti-pattern, edge cases, acceptance gate:
  [`SKILL.md`](./SKILL.md)
- Domain concepts and decision rules: [`knowledge/body-of-knowledge.md`](./knowledge/body-of-knowledge.md)
- Concept map: [`knowledge/knowledge-graph.json`](./knowledge/knowledge-graph.json)
- Role contracts: [`agents/`](./agents/)
- Prompts: [`prompts/primary.md`](./prompts/primary.md), [`prompts/meta.md`](./prompts/meta.md)
- Deliverable scaffold: [`templates/output.md`](./templates/output.md)
- Worked example: [`examples/`](./examples/)
- Asset bundle: [`assets/README.md`](./assets/README.md)

## Evidence taxonomy

Every claim carries a tag: `[DOC]`, `[CONFIG]`, `[CÓDIGO]`, `[INFERENCIA]`, `[SUPUESTO]`.
Never report green as success without functional evidence; single-brand (JM Labs);
no client PII; no invented prices.
