# Meta Prompt — Evaluation Confidence Design

Guía de razonamiento y self-correction para operar la skill. Úsala para auto-auditar el proceso, no para producir el deliverable directamente.

## Pre-flight
- ¿La tarea es **evaluar salidas etiquetadas** o estoy a punto de entrenar/etiquetar? Si es lo segundo → fuera de scope, no activar.
- ¿Tengo labeled set con `document_type`, `category`, `label`, `raw_confidence`? Si no → detente y pídelo.

## Self-correction triggers (detente y reencuadra si te descubres…)
- comparando confidences **crudas** entre versiones;
- reportando una sola **accuracy agregada** como métrica primaria;
- muestreando **aleatorio global**;
- redactando un criterio **sin ejemplos +/-**;
- presentando una categoría **disabled como sana**;
- fijando umbrales **sin labeled set**.

## Decisiones a justificar explícitamente
- Método de calibración elegido **por tamaño del set** (no por moda).
- Estratificar por **dimensión de riesgo**, no por volumen.
- Aislar categoría ruidosa (disable) vs subir umbral global → preferir aislar.

## Chequeo de evidencia
Antes de afirmar, etiqueta: ¿es observado en el labeled set `[DOC]`, una inferencia de diseño `[INFERENCIA]`, un supuesto abierto `[SUPUESTO]`, o config/código verificable `[CONFIG]`/`[CÓDIGO]`?

## Falso verde — verificación final
- ¿Alguna categoría suspendida aparece como 0% FP o "sana"? → corrige.
- ¿Algún estrato no-calibrado cuenta como métrica válida? → corrige.
- ¿Algún bucket aceptado vacío se reporta como precisión perfecta? → corrige.
