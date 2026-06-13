# Assets — Session Lifecycle Management

Bundle de artefactos reutilizables que respaldan la decisión de transición de sesión. Todos son específicos del dominio resume/fork/fresh, staleness y `TypedSummary`.

## Contenido

- **`quality-rubric.json`** — rúbrica ponderada de evaluación con 5 dimensiones (rigor de staleness, corrección de la matriz, integridad del `TypedSummary`, aislamiento de forks, trazabilidad). La consume `SKILL.md` como criterio de calidad del gate de aceptación, y el `guardian` para emitir su veredicto.
- **`checklist.md`** — checklist operativo del gate, alineado 1:1 con el "Gate de aceptación" de `SKILL.md` y con el scaffold de `templates/output.md`. Se marca antes de emitir la transición.

## Uso

1. Antes de emitir el reporte (`templates/output.md`), recorre `checklist.md`.
2. Puntúa el reporte contra `quality-rubric.json`; cualquier `fail_signal` bloquea el done.
3. El manifiesto (`manifest.json`) declara cada asset, su tipo, propósito y qué archivo lo usa.

## Gobernanza

Evidencia tipada (`[CODE] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`); verde solo con evidencia; sin PII de cliente; marca única JM Labs.
