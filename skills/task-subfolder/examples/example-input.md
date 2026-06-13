# Example input — task-subfolder

Operator request (Spanish, as it typically arrives):

> Crear subtarea para migrar el job de ETL nocturno de cron a Airflow. Es algo
> que va a tomar varias sesiones. El workspace de tareas es
> `~/jm-claude-desktop-workspace/workspaces/tasks`. Audiencia: el equipo de
> plataforma. Todavía no tengo los criterios de aceptación definidos.

Parsed inputs:

| Input | Value |
|---|---|
| Goal | Migrar el job de ETL nocturno de cron a Airflow. |
| Parent dir | `~/jm-claude-desktop-workspace/workspaces/tasks` |
| T-NNN id | (none given → auto-assign) |
| Acceptance criteria | (none → draft + `{POR_CONFIRMAR}`) |
| Audience | Equipo de plataforma |
| Constraints | (none stated) |

Parent dir state at run time (from `Bash` listing):

```
T-005-onboarding-checklist/
T-006-presupuesto-q3/
```

Expected resolution: next free id is **T-007**; slug `migrar-etl-nocturno-airflow`.
Mode = **create** (no collision). Multi-session intent is explicit, so the skill
activates.
