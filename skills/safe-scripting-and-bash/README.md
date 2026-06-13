# safe-scripting-and-bash

Design and review Bash scripts for local agentic workflows so they are portable,
dry-run-first, and provably non-destructive before they touch the filesystem. The
deliverable is a script (or a review of one) plus a machine-checkable safety
report that an offline validator passes. [DOC]

## What it does

- Classifies a scripting request by risk: destructive command, broad write,
  secret exposure, portability gap, offline-validation gap. [DOC]
- Forces dry-run as the default whenever a write is possible; `--apply` and
  `--force` must be explicit and `--force` requires a prior dry-run. [DOC]
- Detects the repo root via `git rev-parse --show-toplevel` instead of embedding
  absolute, machine-specific paths. [CODE]
- Emits a safety report whose verdict is bound to per-check results — never
  "green-as-success" when an individual check failed. [DOC]

## When to use

- Creating or reviewing a local script that can write, move, generate, or sync
  many files. [DOC]
- A reviewer must rule out `rm -rf`, `git reset --hard`, force push, static
  tempdirs, unquoted expansion, or secret leaks. [INFERENCE]

## When not to use

- A one-line command suffices and has no durable value. [DOC]
- The request is destructive without explicit approval, or would read/print
  secrets — refuse, do not soften. [DOC]
- Non-Bash automation (PowerShell, Node CLI) owns the work — out of scope. [ASSUMPTION]

## How it routes and executes

1. **Discover** — read existing scripts and repo conventions; record the write
   surface (paths, glob breadth). [DOC]
2. **Analyze** — classify destructive, secrets, broad-write, and portability
   risk against the deterministic policy assets. [DOC]
3. **Execute** — implement with repo-root detection and dry-run-first when writes
   are possible. [DOC]
4. **Validate** — run syntax checks and non-destructive smoke tests; emit the
   safety report and run the offline gate. [DOC]

## References

- `SKILL.md` — full contract: inputs, outputs, safety limits, edge cases.
- `knowledge/body-of-knowledge.md` — Bash safety standards and decision rules.
- `knowledge/knowledge-graph.json` — concept map over the skill's risk taxonomy.
- `agents/lead.md`, `agents/specialist.md`, `agents/support.md`,
  `agents/guardian.md` — role contracts for the four-agent flow.
- `prompts/` — primary, meta, and quick/deep variation prompts.
- `templates/output.md` — the safety-report deliverable scaffold.
- `assets/` — deterministic policy assets and the manifest; see `assets/README.md`.
- `evals/evals.json` — acceptance scenarios with `expected_checks`.

## Evidence taxonomy

Every non-obvious claim carries one Alfa-core tag: `[DOC]`, `[CONFIG]`,
`[CODE]`, `[INFERENCE]`, `[ASSUMPTION]`. Spelling is consistent and a single tag
applies per claim. [DOC]
