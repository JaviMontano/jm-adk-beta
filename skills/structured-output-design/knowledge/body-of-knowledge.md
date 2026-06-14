# Body of Knowledge — structured-output-design

Conocimiento de dominio para diseñar la extracción estructurada de Claude como un
contrato de datos verificable. [DOC]

## Conceptos clave

- **Contrato de datos vs. prosa parseada.** El antipatrón es pedir "devuelve JSON" en
  prosa y hacer `json.loads(resp.content[0].text)`. Se rompe cuando el modelo añade un
  code fence o una frase introductoria. El patrón es definir una tool con `input_schema`
  y parsear desde `tool_use.input`, que ya es un dict tipado. [DOC]
- **`input_schema` defensivo.** Subconjunto de JSON Schema que Anthropic acepta en la
  definición de una tool. Defensivo = `additionalProperties=false`, `required` reflejan
  presencia real, opcionales nullable, enums con válvula de escape. [DOC]
- **Forced tool use.** `tool_choice={"type":"tool","name":"X"}` obliga al modelo a emitir
  un bloque `tool_use` de la tool X. Solo es legítimo cuando emitir la estructura es la
  única acción válida. [CONFIG]
- **Válvula de escape de enum.** Patrón `enum:[...,"other"]` + campo hermano `*_details`
  nullable. Evita perder filas cuando aparece un valor fuera del catálogo y permite que
  el catálogo evolucione con evidencia. [DOC]
- **Unión nullable.** `{"type":["string","null"]}` representa "ausente" como `null`, en
  lugar de un default falso (`''`, `0`, `"N/A"`) que se confunde con un valor real. [DOC]
- **Gate de validación.** Validar el dict emitido contra el `input_schema` antes de
  aceptarlo; los fallos van a retry/escalada, nunca a parseo best-effort. [DOC]

## Estándares y reglas

- **JSON Schema (subconjunto Anthropic).** `type=object`, `properties`, `required`,
  `additionalProperties=false`, `enum`, uniones de tipo vía lista (`["string","null"]`). [CÓDIGO]
- **Mensajes de Anthropic.** `stop_reason` relevantes: `tool_use` (éxito), `max_tokens`
  (posible truncado → JSON incompleto), `end_turn` con bloque `text` cuando se forzó la
  tool (anómalo → refusal/error). [DOC]
- **Política de defaults.** Prohibidos `''`, `0`, `"N/A"` como representación de ausencia;
  usar `null`. [CÓDIGO → `assets/nullable-policy.json`]
- **Política de enum.** Todo enum cerrado requiere `'other'` + `*_details`.
  [CÓDIGO → `assets/enum-escape-policy.json`]
- **Política de schema.** `object` + `additionalProperties=false` + `required` reales.
  [CÓDIGO → `assets/json-schema-policy.json`]
- **Política de tool_choice.** Forzar solo cuando no hay decisión de tool.
  [CÓDIGO → `assets/tool-choice-policy.json`]
- **Política de refusal/error.** Canal de error/refusal explícito; parseo desde
  `tool_use.input`. [CÓDIGO → `assets/refusal-error-policy.json`]

## Reglas de decisión

| Situación | Decisión |
|---|---|
| Campo presente en cada documento | `required` |
| Campo presente a veces | opcional → unión nullable |
| Valor que no encaja en el enum | `'other'` + `*_details` |
| Única acción válida = emitir estructura | `tool_choice` forzado |
| El modelo debe elegir entre varias tools | `tool_choice="auto"` |
| `stop_reason="max_tokens"` con `tool_use` | rechazar, subir tokens / particionar, retry |
| Modelo devuelve `text` pese a forzar | refusal/error → escalada |
| Columna del consumidor es NOT NULL | default explícito en el consumidor, no `''` en el schema |
| Te piden saltar validación / regex fallback | rechazar; anula el contrato |

## Anti-scope

- Prosa libre legítima para humano: no impongas schema.
- Decisión real entre tools: no fuerces; `auto`.
- Saltar validación o conservar defaults falsos: rechaza.
- Fallback de texto libre + regex: prohibido.

## Evidencia

Set de tags: `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`. Una familia de marca por
output; sin precios inventados; sin PII de cliente.
