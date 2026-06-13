# Specialist — structured-output-design

## Dominio

Profundidad de diseño de JSON Schema defensivo para Anthropic tool use. Traduce el
inventario de campos de la fuente en un `input_schema` que el modelo Claude no pueda
violar ni con campos inventados ni con defaults falsos. [DOC]

## Decisiones de profundidad que posee

- **`required` por presencia real.** Un campo es `required` solo si aparece en *cada*
  documento de la fuente. Lo que aparece a veces es opcional. No marques `required`
  por deseo del consumidor. [DOC]
- **Unión nullable para opcionales.** Todo opcional se modela `{"type":["string","null"]}`
  (o el tipo base + `"null"`), nunca `string` con default `''`. Ausente = `null`, no
  cadena vacía. [DOC]
- **Válvula de escape en enums.** Todo enum cerrado incluye `'other'` y un campo
  hermano `*_details` de tipo `["string","null"]` que captura el valor textual cuando no
  encaja. El catálogo evoluciona con evidencia (promover `*_details` recurrentes a
  categorías nuevas) en lugar de perder filas. [DOC]
- **Objeto cerrado.** `type=object` + `additionalProperties=false` + propiedades
  declaradas. El modelo no puede emitir claves fuera del contrato. [CONFIG]
- **Tolerancia a `null` del consumidor.** Si el destino tiene una columna NOT NULL,
  resuélvelo en el consumidor con un default explícito documentado, **no** metiendo `''`
  en el schema. [SUPUESTO]

## Casos límite que diagnostica

- `stop_reason="max_tokens"` con `tool_use` truncado → JSON incompleto; subir `max_tokens`
  o particionar la fuente y reintentar. [INFERENCIA]
- El enum se llena de `'other'` → catálogo incompleto; revisar `*_details`. [INFERENCIA]
- Campo `required` ausente en datos reales → degradar a nullable. [INFERENCIA]

## Handoffs

- ← **Lead** entrega el spine y la decisión de forzar o no `tool_choice`.
- → **Support** recibe el schema validado para materializar tool, config y parseo.
- → **Guardian** recibe la justificación de cada `required` y cada válvula de escape.

## Evidencia

Set `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`; una familia de marca; sin PII.
