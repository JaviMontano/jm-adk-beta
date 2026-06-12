---
name: structured-output-design
version: 1.1.0
description: "Disenar extraccion estructurada Claude como contrato de datos: JSON Schema defensivo (required reales, union nullable, enum con valvula de escape), tool_choice forzado y parseo desde tool_use.input."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - structured output design
  - json schema output
  - defensive schema
  - forced tool_choice
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Structured Output Design

## Capacidad

Diseñar la extracción estructurada de un modelo Claude como un **contrato de datos verificable**, no como prosa que luego se parsea. Se define un JSON Schema defensivo y se fuerza `tool_choice` para que el modelo emita exactamente ese schema: `required` que reflejan campos realmente presentes en la fuente, uniones `nullable` para opcionales (en vez de defaults silenciosos como `''` o `0`), y enums con válvula de escape (`'other'` + `*_details`) para no perder señal cuando el dato no encaja en el catálogo. El resultado es una salida parseable de forma determinista, auditable y resistente a alucinación de campos. [DOC]

## Cuándo usarla

- Claude debe devolver datos que **otro sistema consume por código** (pipelines de extracción, ETL, ingest a base de datos). [DOC]
- La salida en prosa + `json.loads(text)` se rompe de forma intermitente (code fences, prosa adicional). [INFERENCIA]
- Un campo opcional ausente se rellena con un default falso (`''`, `0`, `"N/A"`) que contamina el dataset aguas abajo. [DOC]
- Un enum cerrado pierde casos reales que no encajan en las categorías previstas. [DOC]
- El modelo a veces "conversa" en vez de emitir la estructura y necesitas forzar la herramienta. [INFERENCIA]

### Cuándo NO usarla (anti-scope)

- **Salida en prosa libre legítima** (un correo, un resumen para humano): no impongas schema. [INFERENCIA]
- **El modelo debe elegir entre varias tools** (extraer factura *o* abrir ticket): no fuerces una sola; usa `tool_choice="auto"`. Forzar mata la decisión real. [INFERENCIA] → ver kata `multi_tool_choice_boundary`.
- **Te piden saltarte la validación del schema o conservar defaults falsos** "para ir rápido": rechaza; eso anula el contrato. La skill no degrada a texto. [SUPUESTO]
- **Fallback de texto libre + regex** cuando la tool no sale: prohibido. Un fallo de tool va a retry/escalada, nunca a parseo best-effort. [INFERENCIA]

## Inputs / Outputs

- **Inputs.** Inventario de campos de la fuente (garantizados vs. ocasionales), catálogo de enums con sus casos raros, identidad del consumidor (p. ej. Postgres) y su tolerancia a `null`. [DOC]
- **Outputs.** (1) Definición de tool con `input_schema` defensivo; (2) configuración de `tool_choice`; (3) ruta de parseo desde `tool_use.input`; (4) gate de validación contra schema con salida a retry/escalada. [DOC]

## Cómo construir

1. **Inventaria los campos de la fuente.** Distingue lo garantizado en cada documento (→ `required`) de lo que aparece a veces (→ opcional). No marques `required` por deseo: marca por **presencia real**. [DOC]
2. **Modela opcionales como unión nullable.** Un opcional es `["string", "null"]`, nunca `string` con default `''`. Ausente debe ser representable como `null`, no como cadena vacía. [DOC]
3. **Añade válvula de escape a los enums.** Todo enum cerrado incluye `'other'` y un campo hermano `*_details` para capturar el valor textual cuando no encaja. El catálogo evoluciona con evidencia en vez de perder filas. [DOC]
4. **Cierra el objeto.** `type=object` + `additionalProperties=false`: el modelo no puede inventar campos fuera del contrato. [CONFIG]
5. **Define la tool con el schema como `input_schema`.** El schema vive en la definición de la herramienta, no en el prompt en prosa. [DOC]
6. **Fuerza `tool_choice` solo cuando no hay decisión de tool que tomar.** Si la única acción válida es emitir la estructura → `tool_choice={"type":"tool","name":"..."}`. Si el modelo debe elegir entre varias → `auto`, no fuerces. [DOC]
7. **Parsea desde `tool_use.input`, nunca desde el texto.** El consumidor lee el bloque `tool_use` tipado; ni regex ni `json.loads` sobre prosa. [DOC]
8. **Valida el bloque emitido contra el schema** antes de aceptarlo, y enruta los fallos al loop de retry/escalada (`stop_reason` anómalo, refusal, schema inválido). [DOC]

## Patrón correcto

```python
# GOOD: defensive schema, forced tool_choice, parse from tool_use.input
extract_invoice = {
    "name": "extract_invoice",
    "description": "Emit invoice fields exactly as they appear in the source document.",
    "input_schema": {
        "type": "object",
        "additionalProperties": False,                  # closed: no invented fields
        "properties": {
            "invoice_id": {"type": "string"},           # required: always present
            "total_amount": {"type": "number"},         # required: always present
            "due_date": {"type": ["string", "null"]},   # optional -> nullable, not ""
            "status": {
                "type": "string",
                "enum": ["paid", "pending", "overdue", "other"],  # escape valve
            },
            "status_details": {"type": ["string", "null"]},       # captures 'other'
        },
        "required": ["invoice_id", "total_amount", "status"],
    },
}

resp = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=1024,
    tools=[extract_invoice],
    tool_choice={"type": "tool", "name": "extract_invoice"},  # forced
    messages=[{"role": "user", "content": document_text}],
)

block = next(b for b in resp.content if b.type == "tool_use")
data = block.input  # typed dict, no json.loads on prose
validate(data, extract_invoice["input_schema"])  # gate before accepting
```

## Anti-patrón

```python
# ANTI: "return JSON" in prose + json.loads(text); empty-string defaults; closed enum
resp = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": document_text + "\n\nReturn the invoice as JSON.",
    }],
)
text = resp.content[0].text
data = json.loads(text)          # breaks when the model adds prose or a code fence
due = data.get("due_date", "")   # "" hides a genuinely-absent value
status = data["status"]          # closed enum drops every unforeseen real case
# ...and on failure: regex fallback over free text -> silent garbage downstream
```

## Casos límite y self-correction

- **`stop_reason="max_tokens"` con `tool_use` truncado** → el JSON está incompleto; no lo aceptes, sube `max_tokens` o particiona la fuente, y reintenta. [INFERENCIA]
- **El modelo devuelve `text` y no `tool_use`** pese a forzar la tool → trátalo como refusal/error; ruta a escalada, nunca parsees el texto. [INFERENCIA]
- **Campo que creías `required` llega ausente** en datos reales → el inventario estaba mal; degrádalo a nullable, no fuerces un default. [INFERENCIA]
- **El enum se llena de `'other'`** → señal de catálogo incompleto; revisa `*_details` y promueve los casos recurrentes a categorías nuevas. [INFERENCIA]
- **Consumidor no acepta `null`** (columna NOT NULL) → resuélvelo en el consumidor (default explícito documentado), no metiendo `''` en el schema. [SUPUESTO]

## Checklist de validación (gate de aceptación)

- ¿Cada campo `required` corresponde a algo **realmente presente** en la fuente (no a un deseo)? [DOC]
- ¿Los opcionales son uniones `nullable` y se eliminó todo default `''`/`0`/`"N/A"`? Ausente = `null`/`unclear`, no cadena vacía. [DOC]
- ¿El objeto es cerrado (`additionalProperties=false`) con propiedades declaradas? [CONFIG]
- ¿Todo enum cerrado tiene válvula de escape (`'other'` + `*_details`)? [DOC]
- ¿`tool_choice` se fuerza **solo** cuando no hay una decisión de tool legítima que tomar? [DOC]
- ¿El consumidor parsea desde `tool_use.input` y **nunca** desde texto en prosa ni con regex? [DOC]
- ¿La salida se valida contra el schema antes de aceptarse, con ruta a retry/escalada en caso de fallo? [DOC]
- ¿No existe ningún camino de fallback a texto libre? [DOC]
- ¿El diseño cumple `assets/structured-output-design-contract.json` y pasa `scripts/check.sh` con fixtures determinísticas (positivas y negativas)? [CÓDIGO]

## Upgrade safety y control de scope

- Al completar archivos faltantes del paquete, **no sobrescribas ediciones locales** del schema: lee antes de escribir, fusiona solo lo ausente. [SUPUESTO]
- Mantén el cambio acotado al diseño del contrato de salida; no toques la lógica de negocio del consumidor ni el prompt funcional. [INFERENCIA]

## Assets y validación offline

- `assets/structured-output-design-contract.json` define el paquete JSON que documenta una tool estructurada. [CÓDIGO]
- `assets/json-schema-policy.json` exige `type=object`, `additionalProperties=false`, `required` reales y propiedades declaradas. [CÓDIGO]
- `assets/nullable-policy.json` prohíbe defaults falsos y requiere unión con `null`. [CÓDIGO]
- `assets/enum-escape-policy.json` exige `other` + campo `*_details` para todo enum cerrado. [CÓDIGO]
- `assets/tool-choice-policy.json` fija `tool_choice={"type":"tool","name":...}` cuando la única acción válida es emitir la estructura. [CÓDIGO]
- `assets/refusal-error-policy.json` exige canal de error/refusal y parseo desde `tool_use.input`. [CÓDIGO]
- `scripts/validate_structured_output_design.py` valida el paquete offline; `scripts/check.sh` ejecuta fixtures positivas y negativas. [CÓDIGO]

## Katas y skills relacionadas

- Kata: `05`. [CONFIG]
- Skills relacionadas: `katas-defensive-structured-extraction`, `katas-headless-code-review`. [CONFIG]
- Capacidades vecinas: `validation-retry-design`, `self-correction-loops`, `provenance-engineering`. [CONFIG]
