# Ejemplo — salida

Contrato de salida estructurada para la extracción de facturas. [DOC]

## 1. Inventario resuelto

- **`required` (presencia real):** `invoice_id`, `total_amount`, `status` — aparecen en
  cada PDF. [DOC]
- **Opcional → nullable:** `due_date` — ausente en facturas al contado; se modela
  `["string","null"]`, nunca `""`. [DOC]
- **Enum con válvula de escape:** `status` lleva `paid/pending/overdue/other` +
  `status_details` para capturar `disputed`, `partial` y futuros casos sin perder filas. [DOC]

## 2. Definición de tool (`input_schema` defensivo)

```python
extract_invoice = {
    "name": "extract_invoice",
    "description": "Emit invoice fields exactly as they appear in the source document.",
    "input_schema": {
        "type": "object",
        "additionalProperties": False,                  # cerrado: sin campos inventados
        "properties": {
            "invoice_id": {"type": "string"},           # required: siempre presente
            "total_amount": {"type": "number"},         # required: siempre presente
            "due_date": {"type": ["string", "null"]},   # opcional -> null, no ""
            "status": {
                "type": "string",
                "enum": ["paid", "pending", "overdue", "other"],  # válvula de escape
            },
            "status_details": {"type": ["string", "null"]},       # captura 'other'
        },
        "required": ["invoice_id", "total_amount", "status"],
    },
}
```

## 3. `tool_choice`

- Decisión: **forzado**. La única acción válida es emitir la estructura de la factura;
  no hay otra tool que el modelo deba considerar. [DOC]
- `tool_choice={"type":"tool","name":"extract_invoice"}`. [CONFIG]

## 4. Parseo desde `tool_use.input`

```python
resp = client.messages.create(
    model="claude-opus-4-1",
    max_tokens=1024,
    tools=[extract_invoice],
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=[{"role": "user", "content": document_text}],
)
block = next(b for b in resp.content if b.type == "tool_use")
data = block.input                                # dict tipado, sin json.loads sobre prosa
validate(data, extract_invoice["input_schema"])   # gate antes de aceptar
```

## 5. Gate y escalada

- `stop_reason="max_tokens"` con `tool_use` truncado → JSON incompleto; subir
  `max_tokens` o particionar la fuente y reintentar; no aceptar. [INFERENCIA]
- Respuesta con bloque `text` y sin `tool_use` pese a forzar → refusal/error → escalada,
  nunca parsear el texto. [INFERENCIA]
- Si `status_details` se llena de `disputed` recurrentemente → promover `disputed` a una
  categoría nueva del enum (catálogo evoluciona con evidencia). [INFERENCIA]
- `due_date` se persiste como `NULL` en Postgres; el equipo normaliza `status` leyendo el
  enum cerrado + `status_details`. [SUPUESTO]

## 6. Checklist de aceptación — resultado

- [x] `required` por presencia real (`invoice_id`, `total_amount`, `status`).
- [x] `due_date` nullable; eliminado el default `""`.
- [x] Objeto cerrado (`additionalProperties=false`).
- [x] Enum `status` con `'other'` + `status_details`.
- [x] `tool_choice` forzado, justificado (no hay decisión entre tools).
- [x] Parseo desde `tool_use.input`.
- [x] Validación obligatoria con ruta a retry/escalada.
- [x] Sin fallback de texto libre.
