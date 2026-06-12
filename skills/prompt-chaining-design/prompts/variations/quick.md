# Prompt variación — quick (prompt-chaining-design)

Diseño express de la cadena cuando el lote y la unidad atómica ya están claros.

## Entradas mínimas

- Tipo y conteo aproximado de unidades.
- Objetivo del pase de integración en una frase.

## Salida en 5 líneas

1. **Unidad atómica**: <qué es una unidad>.
2. **Schema local**: `unit_id`, <campos>, `status: ok|error`, `error_detail`.
3. **Schema de transición**: `list[UnitSummary]` (sin crudos).
4. **Pase 2**: <síntesis/agregación> sobre `ok`, reporta `error` sin abortar.
5. **Justificación**: <volumen | paralelismo | aislamiento>.

## Gate rápido (todo debe ser sí)

- Pase 2 sin crudos · schema por pase · error tipado · pase local de una unidad ·
  schema de transición presente · chaining justificado.

Si algún input falta → `{VACIO_CRITICO}`. Si single-pass cabe holgado → degrada.
Etiqueta con evidencia (`[DOC]`/`[INFERENCIA]`).
