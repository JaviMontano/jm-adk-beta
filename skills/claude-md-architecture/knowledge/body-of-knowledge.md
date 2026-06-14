# Body of Knowledge — claude-md-architecture

Domain knowledge for designing hierarchical `CLAUDE.md` memory in Claude Code:
the layering, the import graph, path-scoped rules, precedence, and the KV-cache
economics that make the whole thing worth doing.

## Key concepts

### Memory scopes (three layers)
- **User scope** — `~/.claude/CLAUDE.md`. Personal preferences (tone, individual
  shortcuts). Not versioned in any project repo. `@import`-ed into the team prefix.
- **Team scope** — the repo root `CLAUDE.md`. Versioned. Holds **only universal**
  rules plus an `@imports` block. This is the **stable cacheable prefix**.
- **Module scope** — `module/CLAUDE.md` per subtree. Holds rules that apply only to
  that subtree, activated by a recursive glob. Loaded **on demand**.

### The cacheable prefix
The root + universal imports form the KV-cache prefix replayed on every turn. The
operative law: **a single volatile or subtree-only line in the prefix invalidates
the cached prefix for every turn**, not only the affected one. Therefore only
stable universals belong at the top. [INFERENCIA]

### Path-scoped (conditional) rules
A module rule is gated by `apply to: "<glob>/**"`. The glob **must be recursive**
(`frontend/**`) so subfolders are covered; `frontend/*` is an anti-pattern that
silently omits nested directories.

### The import graph
`@imports` form a directed graph that **must be a DAG**. Circular imports between
modules are prohibited and must be detected before writing. A broken import (path
removed by a rename) must **fail loud**, never degrade silently. [DOC]

### Precedence by subpath
When two globs overlap (`src/**` and `src/api/**`), the **most specific subpath
wins**. When specificity cannot order them, an **explicit tie-break** is declared in
the precedence table so resolution stays predictable and auditable. [SUPUESTO]

## Standards and decision rules

| Rule | Rationale | Tag |
|------|-----------|-----|
| Universals only in root prefix | Protect the KV cache | [INFERENCIA] |
| Recursive globs (`**`) for subtrees with subfolders | Avoid silent omission | [DOC] |
| Personal prefs in user scope, never team repo | Prevent scope leak | [INFERENCIA] |
| Import graph is a DAG | No circular load | [INFERENCIA] |
| Broken import fails loud | No silent degradation | [DOC] |
| No empty `module/CLAUDE.md` | Avoid graph noise | [INFERENCIA] |
| Dedupe rules to one level | Duplication = misclassification | [INFERENCIA] |
| Root >300 lines is a smell | Misassigned universal | [SUPUESTO] |
| Declare architecture before writing (ontology-first) | Reproducible compile | [CONFIG] |

## Classification heuristic (the core move)

1. Does the rule apply on **every** turn regardless of path? → **universal** (root).
2. Does it apply **only** when work touches a specific subtree? → **per-module**
   (glob-gated `module/CLAUDE.md`).
3. Is it a **personal** preference for one human, not a project contract? →
   **per-user** (`~/.claude/CLAUDE.md`).

A misclassified rule is the root cause of cache thrashing. [INFERENCIA]

## Anti-patterns (reject on sight)
- Monolithic 2000-line root loaded every turn.
- Personal preference (`prefer pnpm over npm`) leaked into the team repo.
- Subtree-only rule (design-system tokens) copied to the root.
- `@import` to a volatile path (timestamp, active branch) that breaks the prefix
  every turn.
- Ambiguous precedence between two overlapping globs with no tie-break.

## Determinism contract
- `assets/architecture-schema.json` + `assets/architecture-policy.json` declare the
  target architecture first.
- `scripts/compile-claude-md-architecture.py` produces a reproducible report.
- `scripts/check.sh` is the functional gate; green-as-success is rejected.

## Related
Katas `katas-08`, `katas-09`; `katas-hierarchical-claude-memory`,
`katas-path-conditional-rules`, `context-window-engineering`.
