# Assets — self-correction-loops

Bundle de politicas y rubricas que rigen el bucle de verificacion cruzada
declarado-vs-calculado. Estos archivos son la fuente de verdad para las
tolerancias, los gates y el contrato del reporte.

## Contenido

- **quality-rubric.json** — rubrica de los 8 criterios de aceptacion (recomputo
  independiente, epsilon justificado, comparador estricto, delta con signo, sin
  correccion silenciosa, valores visibles, huerfanos degradados, test estructural).
  La consume `SKILL.md` (checklist de validacion) y `README.md` (routing del guardian).
- **checklist.md** — version operativa de cabecera del gate de aceptacion, lista
  para copiar al reporte de salida. La consume `SKILL.md`.

## Politicas referenciadas por SKILL.md (contrato del skill)

`SKILL.md` ademas referencia, como contrato del bucle, estos assets de politica
que se completan al implementar los scripts deterministicos del skill:
`self-correction-loops-contract.json`, `epsilon-policy.json`, `mismatch-policy.json`,
`escalation-policy.json` y `structural-test-policy.json`. La rubrica y la checklist
de este bundle codifican las mismas invariantes en forma verificable.

## Uso

- El **guardian** valida el reporte contra `quality-rubric.json`.
- El **support** copia `checklist.md` al pie del reporte para el rastro de auditoria.
- Cada entrada del `manifest.json` declara `path`, `type`, `purpose` y `used_by`
  (archivos existentes que consumen el asset).

Sin precios · single-brand JM Labs · sin PII de cliente.
