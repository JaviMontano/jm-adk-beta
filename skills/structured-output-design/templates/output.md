# Contrato de salida estructurada — <nombre_de_la_tool>

> Entregable de `structured-output-design`. Reemplaza los campos angulares con el
> contrato real. Cada claim lleva tag `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`.

## 1. Inventario de la fuente

| Campo | Presencia | Tipo base | Clasificación |
|-------|-----------|-----------|---------------|
| <invoice_id> | en cada documento | string | required |
| <total_amount> | en cada documento | number | required |
| <due_date> | ocasional | string | opcional → nullable |
| <status> | en cada documento | enum | required + válvula de escape |

Consumidor: <p. ej. Postgres, tabla invoices>. Tolerancia a `null`: <sí / columnas NOT NULL>.

## 2. Definición de tool (`input_schema` defensivo)

```python
<nombre_de_la_tool> = {
    "name": "<nombre_de_la_tool>",
    "description": "<emit ... exactly as they appear in the source>",
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "<invoice_id>": {"type": "string"},
            "<total_amount>": {"type": "number"},
            "<due_date>": {"type": ["string", "null"]},
            "<status>": {"type": "string", "enum": ["<...>", "other"]},
            "<status_details>": {"type": ["string", "null"]}
        },
        "required": ["<invoice_id>", "<total_amount>", "<status>"]
    }
}
```

## 3. Configuración de `tool_choice`

- Decisión: <forzado | auto> — Justificación: <única acción válida es emitir la
  estructura | el modelo debe elegir entre varias tools>. [DOC]
- Config: `tool_choice={"type":"tool","name":"<nombre_de_la_tool>"}` (forzado) **o**
  `tool_choice="auto"` (decisión real).

## 4. Ruta de parseo

```python
block = next(b for b in resp.content if b.type == "tool_use")
data = block.input  # dict tipado, sin json.loads sobre prosa
```

## 5. Gate de validación y escalada

- `validate(data, <nombre_de_la_tool>["input_schema"])` antes de aceptar.
- Fallos enrutados a retry/escalada: `stop_reason="max_tokens"`, `text` en vez de
  `tool_use` (refusal), schema inválido. Sin fallback de texto libre.

## 6. Checklist de aceptación

- [ ] `required` por presencia real.
- [ ] Opcionales nullable; cero defaults falsos.
- [ ] Objeto cerrado (`additionalProperties=false`).
- [ ] Enums con `'other'` + `*_details`.
- [ ] `tool_choice` proporcional a la decisión.
- [ ] Parseo desde `tool_use.input`.
- [ ] Validación obligatoria con ruta a escalada.
- [ ] Sin fallback de texto libre.
- [ ] Cumple `assets/structured-output-design-contract.json` y `scripts/check.sh` pasa.
