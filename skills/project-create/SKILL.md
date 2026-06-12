---
name: project-create
version: 0.2.0
description: "Scaffold a Jarvis OS project P-NNN-slug under 02_Proyectos/ with compliant CLAUDE.md, MEMORY.md and TAREAS.md (P07); missing-only, never clobbers local edits."
owner: "JM Labs"
triggers:
  - project-create
  - crear-proyecto
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Project Create

Scaffold a new Jarvis OS project folder and its three governance files. One job:
turn an intent ("start project Atlas") into a placed, Rule-9-compliant project
skeleton ready for its first cadence. Anything past scaffolding (planning,
execution, reporting) belongs to downstream skills. [DOC]

## When to use

- A project does not yet exist under `02_Proyectos/<slug>/` and work is starting. [INFERENCE]
- Invoked by `jarvis-os` routing or directly via trigger. [DOC]

**Do NOT use when** — the folder already exists (route to its cadence/skill
instead, never re-scaffold); the target is a sector or station (use
`station-create`); or the request is a one-off task inside an existing project
(use `task-subfolder`). [DOC]

## Inputs

| Input | Required | Default if absent |
|---|---|---|
| Project name / intent | Yes | `[VACIO_CRITICO]` → stop, ask |
| Slug | No | Derive kebab-case from name `[INFERENCE]` |
| P-NNN id | No | Next free id from project registry `[INFERENCE]` |
| Sector | No | `III Core → 02_Proyectos/` `[ASSUMPTION]` |
| One-line objective | No | Mark `{POR_CONFIRMAR}` in MEMORY.md |

## Outputs

- `02_Proyectos/<slug>/CLAUDE.md` — project memory, **≤70 lines** (Rule-9). [DOC]
- `02_Proyectos/<slug>/MEMORY.md` — persistent context, objective, stakeholders. [DOC]
- `02_Proyectos/<slug>/TAREAS.md` — task ledger seeded with **NOW ≤ 3**. [DOC]
- A registry entry binding `P-NNN ↔ slug ↔ path`. [INFERENCE]
- Summary: id, slug, path, and the next cadence to invoke. [INFERENCE]

## Procedure

### 1 · Discover
Resolve name → slug (kebab-case `^[a-z0-9]+(-[a-z0-9]+)*$`, per placement
naming policy) and reserve the next free `P-NNN`. Read the project registry and
the parent sector `CLAUDE.md` before writing. [CONFIG]

### 2 · Guard
Check `02_Proyectos/<slug>/` does not exist. If it does → **stop**, report the
existing path, route to its cadence. Never overwrite. [DOC]

### 3 · Scaffold (missing-only)
Write the three files only where absent. Each existing file is left byte-for-byte
intact unless `--force` is passed after a reviewed diff. CLAUDE.md must fit
Rule-9 (≤70 lines) by construction — link out rather than inline. [DOC]

### 4 · Register
Add/confirm the `P-NNN ↔ slug ↔ path` entry. Idempotent: re-running updates
nothing if the entry already matches. [INFERENCE]

### 5 · Validate
Run the acceptance gate below before declaring done. [DOC]

## Acceptance gate (all must hold)

- [ ] Folder placed at `02_Proyectos/<slug>/`, slug matches the naming regex. [CONFIG]
- [ ] All three files exist; none pre-existing was modified without `--force`. [DOC]
- [ ] Project `CLAUDE.md` ≤ 70 lines (Rule-9). [DOC]
- [ ] `TAREAS.md` has **NOW ≤ 3** seeded tasks. [DOC]
- [ ] Registry maps `P-NNN ↔ slug ↔ path` with no duplicate id or slug. [INFERENCE]
- [ ] Tags use one family consistently (Alfa core in kit context). [DOC]

## Edge cases

- **Empty intent** → `{VACIO_CRITICO}`: stop and ask for the objective; never auto-name. [DOC]
- **Slug collision** (slug exists, different P-NNN) → stop, surface both, ask which to reuse/rename. [INFERENCE]
- **Id collision** (P-NNN taken) → pick the next free id, report the substitution. [INFERENCE]
- **Partial scaffold** (1–2 of 3 files present) → fill only the missing ones; do not touch the present ones. [DOC]
- **CLAUDE.md would exceed 70 lines** → factor content into MEMORY.md / links before writing, not after. [INFERENCE]
- **Wrong sector inferred** → `III Core` is a default `[ASSUMPTION]`; confirm if the name implies another sector.

## Anti-patterns

- Re-scaffolding an existing project "to refresh it" — destroys local state. Route instead. [DOC]
- Inlining plan/report content into CLAUDE.md to "save a file" — breaks Rule-9. [INFERENCE]
- Auto-filling the objective to avoid asking — emit `{POR_CONFIRMAR}`, do not invent. [DOC]
- Mixing tag families (`{MEMORIA}` + `[DOC]`) in one file — pick Alfa core here. [DOC]

## Self-correction triggers

- About to write a file that already exists → switch to missing-only, re-read it first. [DOC]
- CLAUDE.md draft > 70 lines → stop, refactor before writing. [INFERENCE]
- No active workspace (placement guard denies write) → run `workspace-manager.sh ensure`, then retry. [CONFIG]

## Related skills

- `jarvis-os` — routes intents here and consumes the scaffold. [DOC]
- `station-create` — sibling scaffolder for stations, not projects. [DOC]
- `task-subfolder` — adds task workspaces inside an existing project. [DOC]
- `claude-md-architecture` — Rule-9 sizing and CLAUDE.md structure. [DOC]

## Evidence & safety

- Tag non-obvious claims with one Alfa-core family
  (`[CODE]`/`[CONFIG]`/`[DOC]`/`[INFERENCE]`/`[ASSUMPTION]`); see
  `references/verification-tags.md`. [DOC]
- Generated files are **missing-only** by default; `--force` only after a
  reviewed diff. No prices, single-brand (JM Labs) discipline. [DOC]
- Gate scoring uses `assets/` (`quality-rubric.json`, `checklist.md`); see
  `assets/README.md`. [DOC]
