# Workspace CONTEXT.md — Layer 1 router (ICM)

> Generated from `workspace/_template/` by `scripts/workspace-bootstrap.sh`.
> Edit-source principle: fix routing here, not in outputs. [DOC]

## Intenciones → stage

| Intención | Leer primero | Leer después | Escribir en |
|---|---|---|---|
| Entender fricción/tarea | `01_discovery/CONTEXT.md` | `_config/` si existe | `01_discovery/output/` |
| Definir done + plan | `02_spec/CONTEXT.md` | `01_discovery/output/` | `02_spec/output/` |
| Implementar | `03_build/CONTEXT.md` | `02_spec/output/` | `03_build/output/` |
| Validar (gates + tests) | `04_validate/CONTEXT.md` | `03_build/output/` | `04_validate/output/` |
| Reanudar | `logs/log.md`, último `output/` | stage del `last_stage` | stage activa |
| Tarea nueva | `tasks/` (skill `task-subfolder`) | `02_spec/CONTEXT.md` | `tasks/T-NNN-*/` |
| Tarea ongoing | `tasks/T-NNN-*/log.md` | `task.md` checkboxes | `tasks/T-NNN-*/log.md` |

## Política de lectura

No leas todo el workspace si una ruta basta. Carga solo Layers 0-2 + la stage activa
(2-8k tok, anti lost-in-the-middle, notebook 13845882 §3.2). Si falta dato,
marca `coverage_gap` y pide bloqueante antes de editar. [DOC]

## Capas ICM en este workspace

- Layer 0: `CLAUDE.md` (raíz repo) — identidad harness.
- Layer 1: este archivo — routing workspace.
- Layer 2: `0N_*/CONTEXT.md` — contratos de stage.
- Layer 3: `references/`, `_config/` (estable, factory).
- Layer 4: `0N_*/output/`, `tasks/` (working artifacts, volátil).