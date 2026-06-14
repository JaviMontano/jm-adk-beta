# Runtime Routing — Overview

Decide **where** an agentic task should run — Claude, Codex, Gemini, Antigravity,
VS Code, or a local CLI/Markdown adapter — *before* it runs, grounded in repo
evidence rather than assumed runtime features. [DOC]

## What it does

- Maps a task's required capabilities (file edits, shell validators, `gh`/`git`
  PR flow, hooks, MCP servers, multimodal input, IDE rules, workspace state) onto
  the **lowest-permission runtime that has evidence for every one of them**. [INFERENCE]
- Emits a capability boundary table: `supported` / `pending` / `unsupported` per
  capability, with a citable evidence id behind every `supported` row. [DOC]
- Always ships a **local-first fallback** with `Dato requerido` or
  `validation pending` markers wherever evidence is absent. [DOC]

## When to use

- The user asks where to run work, or names a runtime/IDE (Codex, Antigravity,
  VS Code, Gemini, Claude). [DOC]
- A task depends on a runtime-specific capability that may not be observable. [DOC]
- Output must stay portable across two or more runtimes. [DOC]

## When not to use

- The task is runtime-independent and the current tool already does it. [INFERENCE]
- The user wants a *guarantee* about an unobservable capability — route, but mark
  it pending; never certify. [DOC]

## How it routes / executes

1. **Discover** — Grep/Read repo docs + adapters (`AGENTS.md`, `CODEX.md`,
   `.agent/`, MCP config) for runtime evidence. [DOC]
2. **Analyze** — Apply the rubric in `SKILL.md`; pick the lowest-permission
   runtime whose required capabilities are all evidence-backed. [INFERENCE]
3. **Execute** — Route to the matching doc, command, skill, or script. [DOC]
4. **Validate** — Mark every unverified capability `validation pending`; emit the
   fallback; run the offline gate (`scripts/check.sh`). [DOC]

The route is machine-checkable through the deterministic policy assets and is
**done** only when the offline gate is clean.

## References

- `SKILL.md` — full rubric, workflow, edge cases, anti-patterns. [DOC]
- `assets/` — deterministic policy bundle (catalog, evidence, capability matrix,
  fallback, contract) + quality rubric; see `assets/README.md`. [DOC]
- `knowledge/body-of-knowledge.md` — runtime/permission/evidence concepts. [DOC]
- `agents/` — lead, specialist, support, guardian role contracts. [DOC]
- `prompts/` — primary, meta, and quick/deep variations. [DOC]
- `evals/evals.json` — acceptance scenarios. [DOC]

## Evidence taxonomy

Every claim carries a tag: `[DOC]` (repo file/doc), `[CONFIG]` (config file),
`[CÓDIGO]` (code), `[INFERENCIA]/[INFERENCE]` (reasoned), `[SUPUESTO]` (assumption
to confirm). A capability is `supported` only with a `[DOC]`/`[CONFIG]`/`[CÓDIGO]`
evidence id; anything resting on `[SUPUESTO]`/`[INFERENCE]` is `validation pending`.
