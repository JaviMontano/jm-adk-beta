# Variación deep — structured-output-design

Modo profundo: diseño exhaustivo del contrato + verificación de casos límite + fixtures
determinísticas. Úsalo cuando la salida alimenta un pipeline crítico o el inventario es
incierto.

## Fase 1 — Inventario riguroso

- Distingue garantizado (presente en *cada* documento → `required`) de ocasional
  (→ opcional nullable). Pide muestras reales; no infieras presencia. [DOC]
- Mapea cada enum a su catálogo conocido y enumera los casos raros observados. [DOC]
- Identifica la tolerancia a `null` del consumidor (columnas NOT NULL). [DOC]

## Fase 2 — Schema defensivo

- `type=object` + `additionalProperties=false` + propiedades declaradas.
- Opcionales como unión `["tipo","null"]`; cero defaults falsos.
- Enums con `'other'` + `*_details` nullable; documenta la política de promoción de
  `*_details` recurrentes a categorías nuevas.

## Fase 3 — Tool, choice y parseo

- Schema como `input_schema` de la tool.
- `tool_choice` forzado solo si no hay decisión de tool; si la hay → `auto`.
- Parseo desde `tool_use.input`; gate de validación obligatorio.

## Fase 4 — Casos límite (verifica cada uno)

- `stop_reason="max_tokens"` con `tool_use` truncado → rechazar, subir `max_tokens` o
  particionar la fuente, reintentar. [INFERENCIA]
- Modelo devuelve `text` pese a forzar → refusal/error → escalada, nunca parsear. [INFERENCIA]
- `required` ausente en datos reales → degradar a nullable. [INFERENCIA]
- Enum saturado de `'other'` → catálogo incompleto; revisar `*_details`. [INFERENCIA]
- Consumidor NOT NULL → default explícito en el consumidor, no `''` en el schema. [SUPUESTO]

## Fase 5 — Aceptación

- Cumplir `assets/structured-output-design-contract.json`. [CÓDIGO]
- `scripts/check.sh` pasa con fixtures positivas y negativas. [CÓDIGO]
- Recorrer el checklist completo de `SKILL.md`.

Tags `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`. Una familia de marca; sin PII.
