# Quick variation — project-create

Fast path for a well-specified intent (name given, no collisions expected).

> Scaffold project **"<name>"** under `02_Proyectos/`. Derive the slug, reserve
> the next `P-NNN`, write the three governance files missing-only (`CLAUDE.md`
> ≤ 70 lines, `TAREAS.md` NOW ≤ 3, objective `{POR_CONFIRMAR}` if unknown),
> register `P-NNN ↔ slug ↔ path`, run the acceptance gate, and report id, slug,
> path, and the next cadence.

Stop conditions: empty name → `{VACIO_CRITICO}`; folder already exists → route
to its cadence, do not re-scaffold. [DOC]
