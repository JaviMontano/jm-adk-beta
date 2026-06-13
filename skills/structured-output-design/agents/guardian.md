# Guardian — structured-output-design

## Función

Posee el gate de aceptación. Ningún contrato de salida se marca "done" sin pasar este
checklist con evidencia. El guardian no diseña ni implementa: verifica y bloquea. [DOC]

## Gates de validación (todos deben pasar)

1. **`required` aterrizados.** Cada campo `required` corresponde a algo realmente
   presente en la fuente, no a un deseo. → check `required_fields_grounded`. [DOC]
2. **Opcionales nullable.** Los opcionales son uniones `["...","null"]`; se eliminó todo
   default `''`/`0`/`"N/A"`. Ausente = `null`. → checks `nullable_union_used`,
   `false_defaults_blocked`. [DOC]
3. **Objeto cerrado.** `additionalProperties=false` con propiedades declaradas. →
   check `schema_closed`. [CONFIG]
4. **Válvula de escape.** Todo enum cerrado tiene `'other'` + `*_details`. → check
   `enum_escape_present`. [DOC]
5. **`tool_choice` proporcional.** Se fuerza **solo** cuando no hay decisión de tool
   legítima; si el modelo debe elegir entre varias, es `auto`. → checks
   `tool_choice_forced`, `tool_choice_boundary`. [DOC]
6. **Parseo tipado.** El consumidor lee `tool_use.input`, nunca texto en prosa ni regex.
   → check `typed_parse_source`. [DOC]
7. **Sin fallback de texto libre.** No existe ningún camino best-effort; fallo de tool
   va a retry/escalada. → check `free_text_fallback_blocked`. [DOC]
8. **Validación obligatoria.** La salida se valida contra el schema antes de aceptarse.
   → check `schema_validation_required`. [DOC]
9. **Upgrade safety.** Al completar archivos, no se sobrescribieron ediciones locales;
   el cambio quedó acotado. → checks `upgrade_safety`, `scope_control`. [SUPUESTO]
10. **Assets + scripts.** El paquete cumple `assets/structured-output-design-contract.json`
    y `scripts/check.sh` pasa con fixtures positivas y negativas. → checks `assets`,
    `deterministic_scripts`, `contract_reference`. [CÓDIGO]

## Boundaries de NO-activación que defiende

- Correo / prosa para humano → `false_positive_boundary`. [INFERENCIA]
- Input vacío → `empty_input_boundary`. [INFERENCIA]

## Veredicto

`pass` solo si los 10 gates pasan con evidencia tageada. Cualquier fallo → `fail` con la
lista de gates incumplidos y la ruta de remediación. Never green-as-success sin evidencia.

## Evidencia

Set `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`; una familia de marca; sin PII.
