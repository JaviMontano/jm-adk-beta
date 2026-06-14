# Assets — Provenance Engineering

Bundle determinista que convierte la invariante "no hay claim sin source" en un gate verificable, no aspiracional. [DOC]

## Contenido

- **`quality-rubric.json`** — rubrica de 7 dimensiones (invariante claim-source, integridad de inventario, preservacion de conflicto, escalacion-no-resolucion, visibilidad de `as_of`, test estructural, gobernanza de evidencia). Seis son criticas: requieren puntaje pleno para PASS. La usa el guardian (`agents/guardian.md`) y la cita `SKILL.md`.
- **`checklist.md`** — checklist operativo previo a "done", mapeado 1:1 con el gate de aceptacion de `SKILL.md`. Cubre vacio critico, claim/source, conflicto, escalacion/visibilidad, blindaje y evidencia. Lo usan `SKILL.md` y `README.md`.

## Como se usa

1. Durante el diseno, el flujo recorre `checklist.md` casilla por casilla; cualquier casilla sin evidencia bloquea el output.
2. En la validacion final, el guardian puntua con `quality-rubric.json`; PASS solo si toda dimension critica esta en pleno.
3. Cuando se materialice `scripts/check.sh`, la rubrica y el checklist son su contrato deterministico de referencia. [SUPUESTO: script previsto, aun no en repo — verificar con `ls skills/provenance-engineering/scripts/`.]

El manifiesto `manifest.json` declara cada asset con su `used_by`; todo target referenciado existe en el skill.
