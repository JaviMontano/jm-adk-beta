<!-- distilled from alfa skills/katas-defensive-structured-extraction -->
<!-- Extraccion defensiva con JSON Schema, tool_choice forzado, enums con valvula de escape y nullable explicito; nunca prosa. -->
# Katas Defensive Structured Extraction

## Qué es

Kata 05 del kit JM-ADK. Enseña a extraer datos estructurados de forma defensiva: se fuerza `tool_choice` con un JSON Schema que declara los `required` reales, modela los campos opcionales como union nullable, y define enums con una válvula de escape (`'other'`, `'unclear'`) acompañada de un campo `details`. El modelo nunca devuelve prosa: siempre invoca la herramienta de extracción y el schema actúa como contrato.

Escenarios canónicos: Structured Extraction y Customer Support.

## Por qué importa (falla que evita)

Pedir "devuélveme JSON" en prosa garantiza alucinación silenciosa. Sin schema forzado el modelo inventa campos faltantes, llena vacíos con `''`, o fuerza valores fuera del dominio del enum. Como la salida parece JSON válido, el `json.loads(resp.text)` pasa y el dato corrupto entra al pipeline sin que nadie lo note. La extracción defensiva convierte esos fallos silenciosos en estados explícitos (`null`, `'unclear'`, `'other'` + `details`).

## Modelo mental

- `required` = el campo siempre está presente en la fuente. Si puede faltar, no es `required`: modélalo como union nullable. `required` no garantiza que el modelo lo pueble bien, solo que la clave existirá.
- Default `''` es alucinación. Si el modelo no sabe el valor, debe ser `null` o `'unclear'`, nunca cadena vacía. El `0` numérico y el `false` booleano son la misma trampa: distingue "ausente" de "cero real".
- Enums sin escape obligan a mentir cuando el valor real no encaja en ninguna opción. Añade siempre `'other'`/`'unclear'` más un campo `details` libre que capture el valor crudo.
- `tool_choice` forzado evita la respuesta "best-effort en prosa": el modelo está obligado a poblar el schema. El schema es el contrato; el prompt solo aporta contexto, no estructura.
- Fechas y opcionales se modelan como `{"type":["string","null"],"format":"date"}`. `format` es documental: Anthropic no valida `format`/`pattern` server-side, así que normaliza y revalida en cliente.
- Confianza por campo es ortogonal: si el pipeline necesita umbral, añade `*_confidence` o un `needs_review` booleano, no lo infieras del texto.

## Supuestos y límites (anti-scope)

- Aplica al tool-use de Anthropic Messages API con `input_schema` (subset de JSON Schema). NO cubre el modo "JSON output" de otros proveedores ni grammars/structured-outputs con validación estricta server-side.
- El schema restringe la *forma*, no la *veracidad*: el modelo puede poblar un `string` con un dato inventado pero bien tipado. La extracción defensiva ataca el fallo silencioso de forma, no la corrección factual: para eso, citación a la fuente o un paso de verificación aparte.
- `tool_choice` forzado deshabilita el chain-of-thought previo a la llamada. Si la extracción requiere razonamiento, usa un campo `reasoning` como primera propiedad del schema o un paso previo sin forzar.
- NO aplica cuando una respuesta híbrida (texto + extracción) es legítima, ni cuando el modelo debe elegir entre varias tools.

## Patrón correcto

```python
EXTRACT_TOOL = {
    "name": "extract_invoice",
    "input_schema": {
        "type": "object",
        "required": ["invoice_id", "currency", "status"],
        "properties": {
            "invoice_id": {"type": "string"},
            "currency": {"type": "string", "enum": ["USD", "EUR", "COP", "other"]},
            "currency_other_details": {"type": ["string", "null"]},
            "status": {"type": "string", "enum": ["paid", "pending", "overdue", "unclear"]},
            "due_date": {"type": ["string", "null"], "format": "date"}
        }
    }
}

resp = client.messages.create(
    model=MODEL,
    tools=[EXTRACT_TOOL],
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=[{"role": "user", "content": source_text}],
)
```

## Anti-patrón

```python
# ✗ ANTI: prompt en prosa pidiendo JSON + parseo ciego
prompt = "Devuelve JSON con invoice_id, currency, status, due_date..."
resp = client.messages.create(model=MODEL, messages=[{"role": "user", "content": prompt}])
data = json.loads(resp.text)  # alucina campos, llena vacíos con '', valores fuera de dominio
# Además: resp.text puede traer markdown fences o prosa antes/después → json.loads lanza o, peor, parsea basura parcial.
```

## Cómo leer la salida (correcto)

```python
# tool_choice forzado garantiza UN bloque tool_use; aún así, valida.
block = next(b for b in resp.content if b.type == "tool_use")
data = block.input  # ya es dict tipado, no json.loads(resp.text)
if data["currency"] == "other" and not data.get("currency_other_details"):
    raise ValueError("escape 'other' sin details: contrato incompleto")  # ver edge cases
```

## Edge cases y modos de fallo

- **Escape sin `details`.** El modelo elige `'other'`/`'unclear'` pero deja `details` en `null`. Mitigación: validación condicional en cliente (arriba); el schema no puede expresar "si X entonces Y requerido".
- **Enum case/locale drift.** El modelo devuelve `"Paid"` o `"USD "` con espacio. Normaliza (`strip().lower()`) y revalida contra el enum antes de persistir; trata el miss como `'unclear'`, no como excepción.
- **`max_tokens` corta el tool_use** → JSON del `input` truncado e inválido. Detecta `stop_reason == "max_tokens"` y reintenta con presupuesto mayor o menos campos; nunca persistas un `input` de una respuesta truncada.
- **Múltiples entidades en la fuente.** Schema de objeto único colapsa N facturas en una. Modela `{"items": {"type": "array", ...}}` cuando la cardinalidad es >1.
- **Campo obligatorio ausente en la fuente real.** Si marcaste `required` algo que el documento a veces no trae, el modelo alucina para cumplir el contrato. Síntoma de un `required` mal calibrado → muévelo a nullable.

## Argumento de certificación

La extracción usa `tool_choice` forzado + schema con `required` reales + enums con escape + nullable explícito; nunca prosa. Quien certifica debe demostrar, con un caso donde el dato falta o no encaja, que: (1) el campo ausente sale `null` y no `''`; (2) el valor fuera de dominio cae en `'other'`/`'unclear'` con `details` poblado; (3) el consumidor lee `block.input` del `tool_use`, no `json.loads(resp.text)`; (4) existe validación de cliente para el contrato condicional escape→`details`.

Criterios de aceptación: ningún `required` puede faltar en >0% de la fuente real; todo enum cerrado lleva válvula de escape; todo opcional es union nullable; el parseo nunca depende de prosa.

## Cuándo activar

- Cuando hay que extraer campos estructurados de texto libre (facturas, tickets de soporte, formularios).
- Cuando el pipeline consume el JSON aguas abajo y un campo corrupto rompe silenciosamente.
- NO forzar `tool_choice` cuando el modelo debe decidir entre varias tools, o cuando una respuesta híbrida (texto + extracción) es válida.

## Skills relacionadas

- `katas-structured-errors-mcp`
- `katas-deterministic-guardrails-pretooluse`
- `katas-posttooluse-normalization`
