# Body of knowledge — task-subfolder (P33)

## 1. The P33 convention

P33 is the JM Labs convention for a **multi-session sub-task**: a self-describing
folder named `T-NNN-<slug>/` that holds everything a future session needs to
resume the task without re-deriving context from chat history. Three canonical
files:

- `CLAUDE.md` — the *local operating contract*. Project-style memory scoped to
  this one task: scope boundary, allowed tools, which tag family to use, the
  rule "read `log.md` first each session", and links up to parent memory
  (`MEMORY.md`, the Golden Reference). It is the first file a resuming agent
  reads after `log.md`.
- `task.md` — the *spec*: goal, context, constraints, audience, and an
  acceptance checklist of `- [ ]` items. The single source of truth for "what
  done means" for this task.
- `log.md` — the *append-only journal*. One dated entry per session. Records
  creation, resumptions, decisions, and status. Never rewritten or reordered.

## 2. Identity & naming

- `T-NNN` is a zero-padded, monotonically increasing id per parent `tasks/` root
  (e.g. `T-007`). The id is **immutable**: renaming or renumbering breaks
  cross-session links and is forbidden.
- `<slug>` is derived from the goal via `naming-and-slugging`: lowercase, ASCII,
  hyphen-separated, deduplicated. The slug is cosmetic; the `T-NNN` is the key.
- Next-id resolution = `max(existing T-NNN) + 1`. A named existing id switches
  the run from **create** to **resume**.

## 3. Idempotency model (missing-only)

The skill is safe to re-run. Default behavior is **missing-only**: each of the
three files is written only if absent. A present file is left untouched and
reported as `skipped (present)`. `--force` is the sole escape hatch and requires
a per-file diff review before any overwrite. This makes the skill convergent —
re-running on a partially-built folder completes it without data loss.

## 4. Append-only journal discipline

`log.md` is history. On resume, the agent **appends** a new dated entry; it never
edits or reorders prior entries. Ordering (newest-at-top vs newest-at-bottom) is
chosen once and declared in `CLAUDE.md`; it must stay consistent for the life of
the task. Violating append-only is the top anti-pattern for this skill.

## 5. Evidence taxonomy (Jarvis OS, operator-facing)

This skill is operator-facing, so artifacts use the Jarvis tag family —
`{MEMORIA}`, `{EXTRAIDO_HILO}`, `{INFERENCIA}`, `{SUPUESTO}`, `{POR_CONFIRMAR}`,
`{VACIO_CRITICO}`, `{AUTOCOMPLETADO}` — and never the Alfa `[…]` tags. See
`references/verification-tags.md` for the full boundary.

## 6. Decision rules (quick reference)

| Situation | Rule | Tag |
|---|---|---|
| Empty goal | Stop, ask; do not fabricate. | `{VACIO_CRITICO}` |
| No parent dir given | Default to workspace `tasks/`. | `{AUTOCOMPLETADO}` |
| No acceptance criteria | Draft a checklist; flag each item. | `{POR_CONFIRMAR}` |
| Existing id / folder | Resume; append to `log.md`. | `{MEMORIA}` |
| Conflicting requirements | Pick safer reading + next step. | `{SUPUESTO}` |
| Inferred but unstated value | State the inference. | `{INFERENCIA}` |
| File present, no `--force` | Skip, report `skipped (present)`. | — |
| `--force` requested | Diff each target first, then overwrite. | — |

## 7. Quality bar

A correct run yields: three parsing Markdown files, a unique `T-NNN`, ≥1
acceptance checkbox, exactly one creation/resume log entry, no un-forced
overwrites, fully-tagged non-obvious lines, zero Alfa tag leakage, no prices,
single brand. The guardian gate enforces all of these before "done".

## 8. Standards & cross-references

- `naming-and-slugging` — deterministic slug rules.
- Golden Reference reading order (CLAUDE.md → _ESTRUCTURA.md → _INDICE.md →
  MEMORY.md → memory/_INDICE.md) — never infer workspace architecture from
  caches or chat; read parent memory.
- `skill-creator` is the sibling for authoring *skills*; `workflow-forge` chains
  multiple T-NNN tasks.
