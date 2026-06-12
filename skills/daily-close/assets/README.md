# Assets — daily-close

Bundle de activos deterministas que respaldan el gate de calidad del cierre diario.

## Contenido

- **`quality-rubric.json`** — cinco dimensiones ponderadas (tres ejes, evidencia
  en lo Cerrado, semilla sembrada, disciplina de tags, persistencia aditiva) con
  sus `pass_when` y el vocabulario de estado `pass/conditional/fail/not-verified`.
  Conduce el veredicto del guardian (`agents/guardian.md`) y el bloque "Estado de
  validacion" de `templates/output.md`.
- **`checklist.md`** — checklist accionable del gate, espejo del gate de aceptacion
  de `SKILL.md`. Bloquea el "hecho" hasta marcar cada casilla. Usado por
  `agents/guardian.md` y referenciado desde `SKILL.md`.
- **`manifest.json`** — indice declarativo de estos assets con `used_by` apuntando
  a los archivos que los consumen.

## Como se usan

El guardian carga `checklist.md` para correr el gate y puntua contra
`quality-rubric.json`. Solo `pass` habilita declarar el cierre cerrado.
