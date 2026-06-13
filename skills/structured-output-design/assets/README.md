# Assets — structured-output-design

Paquete de soporte para diseñar y verificar el contrato de salida estructurada.

## Contenido

- **`quality-rubric.json`** — rúbrica del gate de aceptación. Diez criterios pass/fail
  (required aterrizados, unión nullable, sin defaults falsos, objeto cerrado, válvula de
  escape de enum, `tool_choice` proporcional, parseo tipado, validación obligatoria, sin
  fallback de texto libre, upgrade safety). Cada criterio lleva su `evidence_tag` y la
  condición `fail_if`. La consume `agents/guardian.md` para emitir el veredicto y la
  referencia `SKILL.md` desde su checklist de validación.

## Policies declaradas en SKILL.md

`SKILL.md` referencia además un conjunto de policies JSON que documentan el contrato
ejecutable del paquete (`structured-output-design-contract.json`, `json-schema-policy.json`,
`nullable-policy.json`, `enum-escape-policy.json`, `tool-choice-policy.json`,
`refusal-error-policy.json`) validadas offline por `scripts/validate_structured_output_design.py`
y `scripts/check.sh`. Este README documenta el asset versionado en este bundle
(`quality-rubric.json`); las policies viven junto a sus scripts de validación.

## Uso

El `guardian` carga `quality-rubric.json`, recorre los diez criterios contra el contrato
producido y devuelve `pass` solo si todos pasan con evidencia tageada. Never green-as-success.
