# Prompt variación — deep (prompt-chaining-design)

Diseño exhaustivo para lotes grandes, heterogéneos o con modos de fallo ricos.

## Fase 1 — Caracterización del lote

- Enumera tipos de unidad y su distribución (¿homogéneas o mixtas?).
- Estima volumen real y cuánto cabría con calidad en una sola ventana.
- Mapea dependencias entre unidades; confirma independencia o documenta `[SUPUESTO]`.

## Fase 2 — Diseño de schema local con modos de fallo

- Enumera explícitamente los modos de fallo de una unidad (parseo, contenido vacío,
  formato inesperado) y cómo cada uno se representa en `status="error"` + `error_detail`.
- Justifica cada campo del resumen contra su consumo en el pase 2 (sin campos muertos).

## Fase 3 — Schema de transición y contrato

- Define la colección tipada y su invariante: solo resúmenes, nunca crudos.
- Especifica qué hace el pase 2 con la partición `ok` vs `error` (cuántos `error`
  toleran antes de invalidar la síntesis).

## Fase 4 — Paralelización y costo

- Confirma idempotencia e independencia para paralelizar el pase local.
- Compara costo estimado chaining (lineal + reduce acotado) vs mega-prompt
  (cuadrático). Documenta el cruce.

## Fase 5 — Validación completa de Guardian

- Recorre los 6 gates de diseño + gates de gobernanza (activación, input vacío,
  upgrade seguro).
- Para cada gate: veredicto + evidencia `[CÓDIGO]`/`[DOC]`. Cualquier bloqueo devuelve
  el diseño con el gate nombrado.

## Entregable

`templates/output.md` completo, con sección de modos de fallo y análisis de costo.
