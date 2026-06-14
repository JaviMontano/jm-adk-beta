# project-create — skill overview

Scaffold a new Jarvis OS project folder `02_Proyectos/<slug>/` together with its
three governance files (`CLAUDE.md`, `MEMORY.md`, `TAREAS.md`), placed and
Rule-9-compliant, ready for its first cadence. One job only: turn an intent
("start project Atlas") into a clean, registered skeleton. Everything past
scaffolding — planning, execution, reporting — belongs to downstream skills. [DOC]

## What it does

- Resolves a project name/intent into a kebab-case `slug` and a free `P-NNN` id. [INFERENCE]
- Guards against clobbering: existing folders/files are never overwritten without
  a reviewed `--force` diff (missing-only by default). [DOC]
- Writes the three governance files where absent, keeping `CLAUDE.md` ≤ 70 lines. [DOC]
- Registers the `P-NNN ↔ slug ↔ path` binding idempotently. [INFERENCE]

## When to use

- A project does not yet exist under `02_Proyectos/<slug>/` and work is starting. [INFERENCE]
- Invoked by `jarvis-os` routing or directly via the `project-create` /
  `crear-proyecto` triggers. [DOC]

**Do NOT use when** the folder already exists (route to its cadence), the target
is a sector/station (use `station-create`), or it is a one-off task inside an
existing project (use `task-subfolder`). [DOC]

## How it routes / executes

1. **Discover** — name → slug, reserve next free `P-NNN`, read registry + parent
   sector `CLAUDE.md`. [CONFIG]
2. **Guard** — verify `02_Proyectos/<slug>/` is absent; stop and route if present. [DOC]
3. **Scaffold (missing-only)** — write the three files only where absent. [DOC]
4. **Register** — add/confirm the `P-NNN ↔ slug ↔ path` entry, idempotently. [INFERENCE]
5. **Validate** — run the acceptance gate (slug regex, three files present,
   CLAUDE.md ≤ 70 lines, NOW ≤ 3 in TAREAS.md, registry has no dup id/slug). [DOC]

## References & bundle

- `SKILL.md` — full procedure, acceptance gate, edge cases, anti-patterns.
- `knowledge/body-of-knowledge.md` — Rule-9, slug policy, registry invariants,
  evidence taxonomy.
- `knowledge/knowledge-graph.json` — concept map over the skill's key entities.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — deliverable scaffold for the scaffold-summary report.
- `agents/` — lead, specialist, support, guardian role contracts.
- `assets/` — quality rubric and acceptance checklist consumed by the gate
  (see `assets/README.md`).

## Governance

Missing-only by default; `--force` only after a reviewed diff. No prices,
single-brand (JM Labs). Tag non-obvious claims with one Alfa-core family
(`[CODE]`/`[CONFIG]`/`[DOC]`/`[INFERENCE]`/`[ASSUMPTION]`). [DOC]
