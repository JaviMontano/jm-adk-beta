---
name: task-subfolder
version: 0.2.0
description: "Crea/retoma una sub-tarea T-NNN multi-sesion con CLAUDE.md, task.md y log.md (P33); idempotente y missing-only salvo --force."
owner: "JM Labs"
triggers:
  - task-subfolder
  - crear-subtarea
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Task Subfolder

Scaffolds (or resumes) the canonical **T-NNN** sub-task folder that survives
across sessions: `CLAUDE.md` (the local operating contract), `task.md` (goal +
acceptance criteria), `log.md` (append-only session journal). Convention P33.
Operator-facing → use the **Jarvis OS** tag family ({MEMORIA}, {EXTRAIDO_HILO},
{INFERENCIA}, {SUPUESTO}, {POR_CONFIRMAR}, {VACIO_CRITICO}); never mix in Alfa
`[…]` tags (see `references/verification-tags.md`). [DOC]

## When to use / not

- **Use** when a task is multi-session, needs its own persistent memory, or the
  operator says "crear subtarea / task-subfolder / T-NNN". [EXTRAIDO_HILO]
- **Don't use** for a single-turn deliverable (no folder needed) or to author a
  *skill* under `skills/` — that is `skill-creator`, not this. [INFERENCIA]

## Inputs

| Input | Required | Notes |
|---|---|---|
| Task goal (one line) | yes | Empty → `{VACIO_CRITICO}`, stop and ask. |
| Parent dir | no | Default: current workspace `tasks/` root. {AUTOCOMPLETADO} |
| T-NNN id | no | Auto-assigned: next free zero-padded number. |
| Acceptance criteria | no | If absent, draft a checklist and mark {POR_CONFIRMAR}. |
| Context / constraints / audience | no | Carried into `task.md`. |

## Outputs

- Folder `T-NNN-<slug>/` containing `CLAUDE.md`, `task.md`, `log.md`. [DOC]
- A first dated `log.md` entry recording creation (or resumption).
- Console summary: id, path, files written vs skipped, open {POR_CONFIRMAR}.

## Procedure

### 1 · Resolve id + path (read before write)
- `Bash`: list parent dir; find the highest existing `T-NNN`, assign N+1.
  If the operator named an existing id, **resume** it instead of creating. [INFERENCIA]
- Slug the goal: lowercase, ASCII, hyphens (see `naming-and-slugging` if present).

### 2 · Probe existing files (idempotency)
- For each of the three files, check existence. **Missing-only by default:**
  write only absent files; never clobber present ones unless `--force`. [DOC]

### 3 · Write the three artifacts
- **`CLAUDE.md`** — local contract: scope boundary, allowed tools, the tag
  family to use, "read `log.md` first each session", links to parent memory.
- **`task.md`** — goal, context, constraints, audience, and an acceptance
  checklist (`- [ ]`). Unknowns → `{POR_CONFIRMAR}` with a verification step.
- **`log.md`** — header + first append-only entry:
  `## YYYY-MM-DD · session N — created` then a one-line status. Newest at top
  or bottom — pick one and state it in `CLAUDE.md`; never reorder later. [SUPUESTO]

### 4 · Validate (gate — all must hold before "done")
Run the deterministic gate in `assets/` (`assets/dod-checklist.md` + `assets/quality-rubric.json`). [DOC]
- [ ] Three files exist and parse as Markdown. [DOC]
- [ ] `T-NNN` id is unique in the parent dir (no collision). [DOC]
- [ ] `task.md` has ≥1 acceptance-criteria checkbox.
- [ ] `log.md` has exactly one creation/resume entry for this run.
- [ ] No pre-existing file was overwritten without `--force` in the summary.
- [ ] Every non-obvious line carries one Jarvis tag; no Alfa tags leaked.

## Edge cases & self-correction

- **Empty goal** → `{VACIO_CRITICO}`: stop, ask for the objective; do not fabricate.
- **Id collision / folder exists** → resume (read `log.md`, append), don't recreate.
- **Conflicting requirements** → state the conflict in `task.md`, pick the safer
  reading, mark `{SUPUESTO}` + next step. [INFERENCIA]
- **`--force` requested** → diff each target first; only then overwrite. [DOC]
- **Operator asks to skip validation/evidence** → refuse the skip; the gate is
  non-negotiable (matches the `conflicting_requirements` eval → no-activation). [DOC]
- **`.local` / personal variant** → write under the local/user-context path,
  keep it missing-only, never touch the shared canonical folder. [DOC]

## Anti-patterns (do NOT)

- Overwrite `log.md`/`task.md` on resume — it is **append-only** history.
- Renumber or rename an existing `T-NNN` (breaks cross-session links).
- Infer the workspace architecture from caches/conversation; read the Golden
  Reference / parent memory instead. [SUPUESTO]
- Emit prices, mix brands, or paint failing checks as success.

## Assumptions & limits

- Not a substitute for expert review on high-risk legal/medical/financial/security work.
- If evidence is unavailable, mark `{SUPUESTO}`/`{POR_CONFIRMAR}`, never assert.

## Related skills

- `naming-and-slugging` — deterministic T-NNN slugs.
- `skill-creator` — when the artifact is a skill, not a task folder.
- `workflow-forge` — chaining multiple T-NNN tasks.

## Update-safety

- Generated support files are **missing-only** by default.
- Use `--force` only after reviewing per-file diffs.
