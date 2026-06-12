# Example input — monthly-audit

Contexto de una corrida real de la cadencia P22 sobre un workspace de JM Labs.

## Solicitud del operador

> auditoria-mensual del workspace `jm-claude-desktop-workspace`, mes 2026-05.
> Tengo la auditoria de abril como baseline.

## Fuentes disponibles

- `MEMORY.md` — actualizado por ultima vez el 2026-05-28.
- `TAREAS.md` — 14 tareas abiertas, 3 sin tocar desde hace 5 semanas.
- Bitacora diaria: 18 entradas de daily-close en mayo (de ~22 dias habiles).
- `git log` de mayo: 41 commits, 2 outputs sin evidencia ligada.
- Auditoria de abril (`2026-04` scorecard) como baseline:
  Memoria 2 · Cadencias 2 · Tareas 2 · Estructura/AI 3 · Guardrails 2 · Friccion 1.

## Observaciones crudas

- MEMORY.md recuperable en frio pero le falta el cierre de 3 dias de la ultima semana.
- daily-close corrio 18/22 dias (cobertura ~82%).
- 3 tareas stale silenciosas en el backlog, sin re-priorizar.
- Estructura de informacion y rutas de skills sin cambios incoherentes.
- 2 outputs de mayo sin tag de evidencia (rompe disciplina de guardrails).
- Friccion recurrente: el script de sync se corrio a mano 4 veces (deuda no atendida).
