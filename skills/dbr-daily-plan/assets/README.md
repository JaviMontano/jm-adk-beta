# Assets — dbr-daily-plan

Recursos deterministas que apoyan la cadencia DBR y la validacion del **P09**.

| Asset | Tipo | Para que | Usado por |
|-------|------|----------|-----------|
| `quality-rubric.json` | JSON | Rubrica ponderada (6 dimensiones) para puntuar un P09: foco del tambor, resultados verificables, capacidad vs restriccion, buffer, no-hoy, evidencia. | `SKILL.md`, `agents/guardian.md` |
| `gate-checklist.md` | Markdown | Checklist del Validation Gate que el guardian marca antes de entregar. | `agents/guardian.md`, `templates/output.md` |

## Uso
- El `guardian` corre `gate-checklist.md` y solo entrega con todas las casillas en
  verde; en fallo, **degrada** el plan (menos prioridades) en vez de inflarlo.
- `quality-rubric.json` da una puntuacion auditable cuando se compara o mejora un
  P09 (p.ej. al revisar el plan de ayer).

El manifiesto canonico vive en `assets/manifest.json`. Cada `used_by` apunta a un
archivo existente del bundle.
