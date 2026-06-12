# Assets — custom-tooling-extension

Bundle de artefactos deterministas que respaldan la skill. Cada asset está
declarado en `manifest.json` con su `used_by`.

## Contenido

- **`quality-rubric.json`** — los 7 criterios del gate de aceptación, cada uno con su `fail_if` y etiqueta de evidencia. Lo consume el guardian (`agents/guardian.md`) para decidir verde-con-evidencia.
- **`checklist.md`** — checklist operativo del gate para correr a mano antes de mergear la extensión. Referenciado desde `SKILL.md`.
- **`manifest.json`** — índice del bundle: ruta, tipo, propósito y `used_by` de cada asset.

## Uso

El guardian aplica `quality-rubric.json` criterio por criterio; el operador
recorre `checklist.md` antes de declarar la extensión lista. Ningún asset
inventa precios, expone PII de cliente ni mezcla marcas.
