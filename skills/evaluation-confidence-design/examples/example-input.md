# Example Input — Evaluation Confidence Design

## Petición del usuario

> Nuestro agente de revisión de contratos emite hallazgos con un score de confianza crudo. Hoy cortamos en `raw_confidence >= 0.7` y reportamos 88% de accuracy agregada. Queremos un evaluador serio antes de promoverlo a producción.

## Datos provistos

Labeled set de 600 hallazgos, etiquetado por humanos, con columnas:

| campo | ejemplo |
|---|---|
| `document_type` | contract, nda, dpa |
| `category` | indemnity, termination, data_privacy, payment_terms |
| `raw_confidence` | 0.0–1.0 |
| `label` | positive / negative |

Distribución por estrato:

| document_type | hallazgos |
|---|---|
| contract | 420 |
| nda | 150 |
| dpa | 30 |

## Síntoma reportado

`data_privacy` sobre `nda` "se siente ruidoso" — muchos hallazgos que el revisor humano marcó como `negative`, pero la accuracy agregada de 88% se ve bien y no permite aislar el problema.

## Lo que se pide

1. Calibrar la confidence contra el labeled set y elegir el corte sobre la calibrada.
2. Muestrear estratificado por `document_type` con mínimo por estrato (el estrato `dpa` no debe desaparecer).
3. Criterios categóricos +/- por severidad.
4. FP rate **por categoría**.
5. Disable temporal para categorías con FP alto.
6. Reporte desglosado, no una sola accuracy agregada.

## Restricción

No re-entrenar el modelo ni re-etiquetar documentos; solo diseñar la evaluación sobre las salidas ya etiquetadas.
