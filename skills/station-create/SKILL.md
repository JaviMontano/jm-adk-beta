---
name: station-create
version: 0.2.0
description: "Scaffold a Jarvis OS station (universal or dedicated) with its own CLAUDE.md and P06/P23/P24-compliant structure; missing-only, never clobbers local edits."
owner: "JM Labs"
triggers:
  - station-create
  - crear-estacion
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Station Create

Turn an intent ("set up a station for X") into a placed, governance-compliant
station skeleton: its folder, its own `CLAUDE.md`, and the structure required by
the P06/P23/P24 protocols. One job — scaffolding. Anything past placement
(routing, cadences, execution, reporting) belongs to downstream skills. [DOC]

A **station** is a long-lived operating surface, not a one-off project: it
either is **universal** (shared, cross-cutting capability) or **dedicated**
(bound to a single sector/domain). Choosing that type is the first real
decision this skill makes. [INFERENCE]

## When to use

- A station does not yet exist at its target path and an operating surface is
  being stood up. [INFERENCE]
- Invoked by `jarvis-os` routing or directly via trigger. [DOC]

**Do NOT use when** — the station already exists (route to its cadence/skill,
never re-scaffold); the target is a project (use `project-create`) or a sector;
or the request is a one-off task inside an existing surface (use the task
scaffolder). [DOC]

## Inputs

| Input | Required | Default if absent |
|---|---|---|
| Station name / intent | Yes | `{VACIO_CRITICO}` → stop, ask |
| Type: universal \| dedicated | Yes | `{POR_CONFIRMAR}` → ask; never guess [INFERENCE] |
| Slug | No | Derive kebab-case from name [INFERENCE] |
| Bound sector (dedicated only) | Cond. | Required iff type=dedicated; else N/A [DOC] |
| One-line purpose | No | Mark `{POR_CONFIRMAR}` in CLAUDE.md |

## Outputs

- `<station-path>/CLAUDE.md` — station memory, **≤70 lines** (Rule-9); links
  out rather than inlining. [DOC]
- The P06/P23/P24 structure for the chosen type (universal vs dedicated differ
  in scope and binding). [SUPUESTO]
- A registry entry binding `station ↔ slug ↔ type ↔ path`. [INFERENCE]
- Summary: slug, type, path, and the next cadence/skill to invoke.

## Procedure

### 1 · Discover
Resolve name → slug (kebab-case `^[a-z0-9]+(-[a-z0-9]+)*$`, per naming policy)
and confirm the type. Read the station registry and the parent context
(`CLAUDE.md`) before writing. [CONFIG]

### 2 · Type-resolve
Universal → shared placement, no sector binding. Dedicated → requires a bound
sector; if absent, stop and ask. The type drives which P06/P23/P24 structure is
materialized. [SUPUESTO]

### 3 · Guard
Check the target path does not exist. If it does → **stop**, report the path,
route to its cadence. Never overwrite. [DOC]

### 4 · Scaffold (missing-only)
Write files only where absent; existing files stay byte-for-byte intact unless
`--force` is passed after a reviewed diff. `CLAUDE.md` must fit Rule-9 (≤70
lines) by construction. [DOC]

### 5 · Register
Add/confirm the `station ↔ slug ↔ type ↔ path` entry. Idempotent: re-running
changes nothing if the entry already matches. [INFERENCE]

### 6 · Validate
Run the acceptance gate below before declaring done. [DOC]

## Acceptance gate (all must hold)

- [ ] Station placed at its correct path; slug matches the naming regex. [CONFIG]
- [ ] Type recorded (universal \| dedicated); dedicated has a bound sector. [DOC]
- [ ] Structure matches the P06/P23/P24 requirement for that type. [SUPUESTO]
- [ ] `CLAUDE.md` exists and is ≤ 70 lines (Rule-9). [DOC]
- [ ] No pre-existing file was modified without `--force`. [DOC]
- [ ] Registry maps `station ↔ slug ↔ type ↔ path`, no duplicate slug/path. [INFERENCE]
- [ ] Tags use one family consistently (Alfa core in kit context). [DOC]

## Edge cases

- **Empty intent** → `{VACIO_CRITICO}`: stop and ask; never auto-name. [DOC]
- **Type unstated** → `{POR_CONFIRMAR}`: ask; do not default to universal. [INFERENCE]
- **Dedicated without sector** → stop, ask which sector to bind. [DOC]
- **Slug/path collision** → stop, surface the existing station, ask reuse vs rename. [INFERENCE]
- **Partial scaffold** (some structure present) → fill only what is missing;
  leave present files untouched. [DOC]
- **CLAUDE.md would exceed 70 lines** → factor content into links before
  writing, not after. [INFERENCE]
- **P06/P23/P24 semantics unknown** → treat the protocol requirement as
  `{POR_CONFIRMAR}` against the governing ontology; do not invent structure. [SUPUESTO]

## Anti-patterns

- Re-scaffolding an existing station "to refresh it" — destroys local state.
  Route instead. [DOC]
- Defaulting the type to universal to skip the question — emit
  `{POR_CONFIRMAR}`. [INFERENCE]
- Inlining cadence/report content into CLAUDE.md to "save a file" — breaks
  Rule-9. [INFERENCE]
- Mixing tag families (`{MEMORIA}` + `[DOC]`) in one file — pick Alfa core here. [DOC]
- Treating a project as a station (or vice versa) — wrong scaffolder, wrong
  lifecycle. [DOC]

## Self-correction triggers

- About to write a file that already exists → switch to missing-only, re-read
  it first. [DOC]
- CLAUDE.md draft > 70 lines → stop, refactor before writing. [INFERENCE]
- No active workspace (placement guard denies write) → ensure the workspace,
  then retry. [CONFIG]
- Materializing structure you cannot trace to the P06/P23/P24 ontology → stop,
  confirm, do not guess. [SUPUESTO]

## Related skills

- `jarvis-os` — routes intents here and consumes the scaffold. [DOC]
- `project-create` — sibling scaffolder for projects, not stations. [DOC]
- `claude-md-architecture` — Rule-9 sizing and CLAUDE.md structure. [DOC]

## Evidence & safety

- Tag non-obvious claims with one Alfa-core family
  (`[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`); see
  `references/verification-tags.md`. [DOC]
- Generated files are **missing-only** by default; `--force` only after a
  reviewed diff. No prices, single-brand (JM Labs) discipline. [DOC]
- The acceptance gate is scored against `assets/quality-rubric.json` (see the
  `assets/` bundle); pass requires all criteria met. [DOC]
