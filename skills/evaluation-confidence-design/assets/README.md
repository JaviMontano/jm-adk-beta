# Assets Bundle — Evaluation Confidence Design

Paquete de artefactos determinísticos que apoyan el diseño y la validación de la evaluación con confidence calibrada. Estos assets son consumidos por `SKILL.md` (paquete determinístico / validation gate) y por `templates/output.md` (sección de gate del reporte).

## Contenido

| Archivo | Tipo | Propósito |
|---|---|---|
| `quality-rubric.json` | rubric | Criterios pass/fail del gate (calibrada-no-cruda, estratificación, +/- por severidad, FP por categoría, disable temporal, no-falso-verde, mapa monótono, ground truth). Cada criterio marca si es bloqueante. |
| `checklist.md` | checklist | Lista operativa del validation gate para marcar antes de declarar el evaluador LISTA. |

## Cómo se usan

- El **guardian** corre `quality-rubric.json` como fuente de verdad de los gates bloqueantes.
- El **lead** y **support** usan `checklist.md` antes de cerrar y al llenar la sección 9 de `templates/output.md`.
- `SKILL.md` referencia este bundle como contrato determinístico previo a fijar umbrales o `disabled_categories`.

## Regla

Ningún asset declara verde si una categoría está suspendida o un estrato quedó no-calibrado. El gate atrapa el falso verde antes de promover a producción.
