# Assets — revisor-veracidad

Bundle de soporte para la auditoria de veracidad. Son insumos estables que consumen `SKILL.md`, `README.md` y los agentes; no son contenido generado por ejecucion.

## Contenido

- **`quality-rubric.json`** — rubrica de calidad por dimensiones (un tag/una familia, tag mas debil, `{WEB}` con cita, pasos de cierre, no sobre-tageo, ortografia, no reescritura, `{VACIO_CRITICO}`). Escala 0-2; cualquier 0 bloquea. La usa el gate de `SKILL.md` y el `guardian`.
- **`checklist.md`** — checklist operativo del gate que corre el `guardian` antes de entregar, incluyendo el chequeo determinista `scripts/check.sh`.

## Como se usan

`agents/guardian.md` recorre `checklist.md` y puntua con `quality-rubric.json`. El gate de `SKILL.md` referencia este bundle como criterio de aceptacion. El mapeo `path -> type -> purpose -> used_by` esta en `manifest.json`.
