# Ejemplo — entrada

## Contexto del solicitante

"Tengo un pipeline que extrae facturas de PDFs con Claude. Hoy le pido en el prompt
'devuelve la factura como JSON' y hago `json.loads(resp.content[0].text)`. Falla una de
cada veinte veces porque el modelo a veces antepone una frase o envuelve el JSON en un
code fence. Además, cuando una factura no trae fecha de vencimiento, mi código guarda
`""`, y aguas abajo eso se confunde con una fecha real. Y mi enum de `status`
(`paid`/`pending`/`overdue`) deja fuera estados como `disputed` que sí aparecen."

## Inventario de la fuente

| Campo | Presencia observada | Tipo base |
|-------|--------------------|-----------|
| `invoice_id` | en cada PDF | string |
| `total_amount` | en cada PDF | number |
| `due_date` | ocasional (facturas al contado no la traen) | string (fecha) |
| `status` | en cada PDF | enum: paid, pending, overdue, **y casos sueltos** (disputed, partial) |

## Consumidor

Postgres, tabla `invoices`. La columna `due_date` admite `NULL`. La columna `status` es
`text` libre hoy, pero el equipo quiere normalizarla.

## Pregunta

"Diséñame la extracción como un contrato: schema defensivo, decide `tool_choice` y
dime exactamente cómo debo parsear la respuesta para que esto deje de romperse."
