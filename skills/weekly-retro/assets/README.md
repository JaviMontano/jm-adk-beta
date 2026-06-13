# Assets — weekly-retro

Bundle de assets que conduce el gate de aceptacion de la retro semanal. Cada
asset esta declarado en `manifest.json` con su `used_by`.

## Contenido

- **`quality-rubric.json`** — Rubrica de cinco dimensiones ponderadas (evidence,
  three_axes, promotion_threshold, quality_criteria, upgrade_safety) con
  `pass_when` y vocabulario `pass/conditional/fail/not-verified`. La consume
  `agents/guardian.md` para emitir veredicto y `templates/output.md` para el
  bloque de validacion.
- **`checklist.md`** — Checklist operativa del gate, agrupada por los tres checks
  de `evals/evals.json`. La consumen `agents/guardian.md` y `SKILL.md`.

## Uso

El guardian no aprueba la retro hasta que la rubrica de `quality-rubric.json` da
`pass` y cada casilla de `checklist.md` esta marcada. Una promocion P12 pendiente
de confirmacion mantiene el veredicto en `conditional`, no en `pass`. {DOC}
