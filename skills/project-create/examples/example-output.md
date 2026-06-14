# Example output — project-create

Result of scaffolding **"Atlas — Fase II"** from the example input.

## Identity

- **P-NNN**: `P-014` (next free after `P-013`) [INFERENCE]
- **Slug**: `atlas-fase-ii` (matches `^[a-z0-9]+(-[a-z0-9]+)*$`) [INFERENCE]
- **Path**: `02_Proyectos/atlas-fase-ii/` [CONFIG]
- **Sector**: `III Core` (default) [ASSUMPTION]
- **Objective**: consolidate the Atlas data pipelines into one orchestrated DAG [DOC]

## Files (missing-only)

| File | Action | Notes |
|---|---|---|
| `CLAUDE.md` | written | 38 / 70 lines (Rule-9 OK) [DOC] |
| `MEMORY.md` | written | objective recorded; stakeholders `{POR_CONFIRMAR}` [DOC] |
| `TAREAS.md` | written | NOW = 2 / 3 [DOC] |

Seeded NOW tasks in `TAREAS.md`:
1. Confirm objective + stakeholders with sponsor. [DOC]
2. Invoke first planning cadence. [DOC]

## Registry

- Entry added: `P-014 ↔ atlas-fase-ii ↔ 02_Proyectos/atlas-fase-ii/` [INFERENCE]
- No duplicate id or slug. [INFERENCE]

## Acceptance gate

| Check | Verdict |
|---|---|
| Folder placed, slug regex matches | pass |
| Three files exist; none clobbered | pass |
| `CLAUDE.md` ≤ 70 lines | pass (38) |
| `TAREAS.md` NOW ≤ 3 | pass (2) |
| Registry triple unique | pass |
| One Alfa-core tag family | pass |

**Overall**: PASS

## Next step

- Next cadence to invoke: project planning skill for `atlas-fase-ii`. [INFERENCE]
