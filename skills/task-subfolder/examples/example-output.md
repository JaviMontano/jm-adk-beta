# Example output — task-subfolder

Worked result for the input in `example-input.md` (id resolved to **T-007**,
slug `migrar-etl-nocturno-airflow`, mode = create).

## `T-007-migrar-etl-nocturno-airflow/CLAUDE.md`

```markdown
# T-007 · migrar-etl-nocturno-airflow — local contract

## Scope
Migrar el job de ETL nocturno desde cron a Airflow; no incluye refactor del
pipeline de transformación. {EXTRAIDO_HILO}

## Allowed tools
Read, Write, Edit, Bash.

## Session protocol
- Read `log.md` first, then `task.md`, every session.
- Parent memory: ../../MEMORY.md.
- Log ordering: newest-at-bottom (fixed for this task's life).

## Tag family (Jarvis OS; never mix Alfa [...])
{MEMORIA} {EXTRAIDO_HILO} {INFERENCIA} {SUPUESTO} {POR_CONFIRMAR}
{VACIO_CRITICO} {AUTOCOMPLETADO}
```

## `T-007-migrar-etl-nocturno-airflow/task.md`

```markdown
# T-007 · migrar-etl-nocturno-airflow

## Goal
Migrar el job de ETL nocturno de cron a Airflow. {EXTRAIDO_HILO}

## Context
Job nocturno actual corre por cron; se quiere orquestar en Airflow para
retries, visibilidad y dependencias. {EXTRAIDO_HILO}

## Constraints
Ninguna declarada todavía. {POR_CONFIRMAR}

## Audience
Equipo de plataforma. {EXTRAIDO_HILO}

## Acceptance criteria
- [ ] DAG de Airflow reproduce el schedule nocturno actual. {POR_CONFIRMAR}
- [ ] Retries y alertas configurados; cron viejo deshabilitado. {POR_CONFIRMAR}
- [ ] Una corrida nocturna exitosa validada en staging. {POR_CONFIRMAR}
```

## `T-007-migrar-etl-nocturno-airflow/log.md`

```markdown
# T-007 · migrar-etl-nocturno-airflow — session log (append-only)

## 2026-06-12 · session 1 — created
- Status: carpeta P33 creada; criterios de aceptación en borrador. {INFERENCIA}
- Próximo paso: confirmar criterios con el equipo de plataforma. {POR_CONFIRMAR}
```

## Console summary

```
task-subfolder · T-007 · migrar-etl-nocturno-airflow
path:    ~/jm-claude-desktop-workspace/workspaces/tasks/T-007-migrar-etl-nocturno-airflow/
written: CLAUDE.md, task.md, log.md
skipped: (none — fresh create)
forced:  (none)
open:    4 {POR_CONFIRMAR} items, 0 {SUPUESTO}
gate:    pass
```

## Gate verdict (guardian)

- [x] Three files exist and parse as Markdown.
- [x] `T-007` unique in parent dir.
- [x] `task.md` has 3 acceptance checkboxes.
- [x] `log.md` has exactly one creation entry.
- [x] No un-forced overwrite (fresh create).
- [x] Every non-obvious line Jarvis-tagged; zero Alfa-tag leakage.
- [x] No prices; single brand (JM Labs).
