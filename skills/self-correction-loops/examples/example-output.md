# Ejemplo de salida — self-correction-loops

Reporte de verificacion cruzada para el lote de `example-input.md`.

## Encabezado

- **Fuente verificada**: lote ERP (2 facturas + 1 conteo de inventario)
- **Campos verificables**: 3  ·  **Huerfanos (unverifiable)**: 0
- **Resultado global**: 2 MISMATCH ESCALADOS a finanzas-control@interno

## Registro por campo

| field            | data_type | declared | computed | delta (declared - computed) | epsilon | mismatch | action               |
|------------------|-----------|----------|----------|------------------------------|---------|----------|----------------------|
| F-1001.total     | moneda    | 100.00   | 100.00   | 0.00                         | 0.005   | false    | --                   |
| F-1002.total     | moneda    | 250.00   | 240.00   | +10.00                       | 0.005   | true     | escalate_to_human    |
| BOG-01.conteo    | entero    | 12       | 10       | +2                           | 0       | true     | escalate_to_human    |

> `mismatch = abs(declared - computed) > epsilon`. El `declared` permanece intacto.

## Justificacion de epsilon

- Totales de factura (moneda): `0.005` — medio centavo por redondeo [CONFIG].
- Conteo de inventario (entero): `0` — un conteo no tolera diferencia [CONFIG].

## Formulas de recomputo (rastro de auditoria)

- `F-1001.total` = `40.00 + 35.00 + 25.00 = 100.00` (suma de lineas) [CODE].
- `F-1002.total` = `120.00 + 90.00 + 30.00 = 240.00` (suma de lineas) [CODE].
- `BOG-01.conteo` = `len(items) = 10` (conteo real) [CODE].

## Mismatches escalados

1. **field**: `F-1002.total`
   - declared: 250.00 · computed: 240.00 · delta: +10.00 (sobre-declaracion)
   - action: `escalate_to_human` -> finanzas-control@interno
   - estado del campo: intacto (NO se reescribio a 240.00)
2. **field**: `BOG-01.conteo`
   - declared: 12 · computed: 10 · delta: +2 (sobre-declaracion)
   - action: `escalate_to_human` -> finanzas-control@interno
   - estado del campo: intacto (NO se reescribio a 10)

## Verificacion estructural

- [x] Caso con mismatch inyectado (F-1002, BOG-01) produce `mismatch=true`.
- [x] Reporte conforme a `assets/self-correction-loops-contract.json`.
- [x] `scripts/check.sh` pasa fixtures positivas (F-1001) y negativas (F-1002).

## Por que esto es correcto

`F-1002` y el conteo se sobre-declararon; el bucle NO ajusto los campos para que
cuadraran. Marco el conflicto, mostro ambos valores y lo derivo a finanzas, que es
donde pertenece la decision. Un sistema que silenciosamente hubiera escrito 240.00
y 10 habria propagado datos con apariencia de validados ocultando el problema de
origen [INFERENCIA].

Evidencia: `[CODE]` `[CONFIG]` `[INFERENCIA]`. Sin precios · single-brand JM Labs.
