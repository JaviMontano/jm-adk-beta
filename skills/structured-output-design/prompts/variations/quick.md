# Variación quick — structured-output-design

Modo rápido: contrato mínimo defensivo cuando el inventario ya está claro y solo se
necesita el schema y la config de tool. Sin exploración de casos límite extensos.

## Pide en una línea

Inventario de campos (garantizados vs. ocasionales), enums con casos raros, consumidor.

## Entrega

1. **Tool** con `input_schema`:
   - `type=object`, `additionalProperties=false`.
   - `required` = solo los garantizados.
   - opcionales como `["tipo","null"]`.
   - cada enum cerrado con `'other'` + `*_details` nullable.
2. **`tool_choice`**: forzado `{"type":"tool","name":...}` si emitir la estructura es la
   única acción válida; `"auto"` si hay decisión real entre tools.
3. **Parseo**: leer `block.input` del bloque `tool_use`; nada de `json.loads` sobre prosa.
4. **Validación**: validar el dict contra el schema; fallo → retry/escalada.

## Guardarraíles

Sin defaults falsos; sin fallback de texto libre; no marques `required` por deseo.
Tags `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`.
