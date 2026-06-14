# Assets — prompt-chaining-design

Bundle de contrato determinístico para el diseño de cadenas de pases. Estos archivos
definen el estándar de calidad que el Guardian aplica offline (sin red, sin tiempo
real, sin aleatoriedad).

## Contenido

- **`quality-rubric.json`** — rúbrica de 6 gates bloqueantes (sin crudos en el pase 2,
  schema por pase, error tipado, pase local de una unidad, schema de transición,
  justificación vs single-pass) + reglas de gobernanza. La consume `SKILL.md` como
  referencia del contrato determinístico.
- **`checklist.md`** — checklist legible espejo de la rúbrica, para validar un diseño a
  mano o como guía del entregable. Referenciada por `SKILL.md`.
- **`manifest.json`** — índice tipado del bundle: cada asset con `path`, `type`,
  `purpose` y `used_by`.

## Uso

`SKILL.md` apunta a `assets/` en su sección "Assets y validación offline". El Guardian
recorre `quality-rubric.json` gate por gate; cualquier `block` devuelve el diseño con el
gate nombrado. La checklist se reutiliza como sección de validación del entregable
(`templates/output.md`).

## Evidencia

`[CÓDIGO]` para los contratos verificables en este directorio · `[CONFIG]` para el
manifest.
