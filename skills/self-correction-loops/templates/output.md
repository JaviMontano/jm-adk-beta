# Reporte de verificacion cruzada — self-correction-loops

## Encabezado

- **Fuente verificada**: <nombre del documento / lote>
- **Campos verificables**: <n>  ·  **Huerfanos (unverifiable)**: <n>
- **Resultado global**: <SIN MISMATCH | MISMATCH(es) ESCALADO(s)>

## Registro por campo

| field | data_type | declared | computed | delta (declared - computed) | epsilon | mismatch | action |
|-------|-----------|----------|----------|------------------------------|---------|----------|--------|
| total | moneda    | <decl>   | <comp>   | <delta con signo>            | 0.005   | <true/false> | <-- o escalate_to_human> |
| count | entero    | <decl>   | <comp>   | <delta>                      | 0       | <true/false> | <-- o escalate_to_human> |

> Regla: `mismatch = abs(declared - computed) > epsilon` (comparador estricto).
> El campo `declared` NUNCA se sobreescribe.

## Justificacion de epsilon

- `total` (moneda): 0.005 — medio centavo por redondeo [CONFIG].
- `count` (entero): 0 — los conteos no toleran diferencia [CONFIG].

## Formulas de recomputo (rastro de auditoria)

- `total` = `sum(line.amount for line in lines)` [CODE].
- `balance` = `debe - haber` por cuenta [CODE].
- `count` = `len(items)` [CODE].

## Mismatches escalados

Por cada `mismatch=true`:
- **field**: <campo>
- **declared**: <valor de la fuente> · **computed**: <valor recalculado> · **delta**: <con signo>
- **action**: `escalate_to_human` -> <destino de escalada>
- **estado del campo**: intacto (no corregido)

## Agregados huerfanos (degradados)

- <field>: sin componentes para recomputar -> `[POR_CONFIRMAR]` / `unverifiable`,
  derivado a revision humana. No se fabrico un calculado.

## Verificacion estructural

- [ ] Caso con mismatch inyectado produce `mismatch=true` (no `total=computed`).
- [ ] Reporte conforme a `assets/self-correction-loops-contract.json`.
- [ ] `scripts/check.sh` pasa fixtures positivas y negativas.

## Evidencia

Tags por afirmacion: `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`.
Sin precios · single-brand JM Labs · sin PII de cliente.
