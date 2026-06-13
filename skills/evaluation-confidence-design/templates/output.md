# Reporte de Evaluación con Confidence Calibrada — {{nombre_del_evaluador}}

> Brand: JM Labs · Fecha: {{YYYY-MM-DD}} · Versión del evaluador: {{x.y.z}}
> Cada afirmación lleva tag: `[DOC]` `[CÓDIGO]` `[CONFIG]` `[INFERENCIA]` `[SUPUESTO]`

## 1. Labeled set

| Métrica | Valor |
|---|---|
| Total de hallazgos etiquetados | {{n}} |
| Dimensión de estratificación | {{document_type}} |
| Categorías | {{lista}} |
| Balance +/- | {{positivos}} / {{negativos}} |

Vacío crítico: {{"sin ground truth → detener" o "cubierto"}}. [SUPUESTO]

## 2. Muestreo estratificado

| Estrato (`document_type`) | Labels disponibles | `per_stratum` | Estado |
|---|---|---|---|
| {{contract}} | {{n}} | {{k}} | calibrado |
| {{nda}} | {{n}} | {{k}} | {{calibrado / no-calibrado}} |

Justificación de estratificar por riesgo, no por volumen: {{...}}. [INFERENCIA]

## 3. Calibration map

- Método: {{binning / Platt / isotonic}} — justificado por tamaño del set. [SUPUESTO]
- Monotonicidad verificada: {{sí/no}} (no monótono → rechazado).

| `raw_upper` | precisión observada |
|---|---|
| {{0.5}} | {{0.41}} |
| {{0.7}} | {{0.68}} |
| {{0.9}} | {{0.86}} |

**Umbral sobre confidence calibrada:** {{>= 0.80}}. [DOC]

## 4. Criterios categóricos (+/- por severidad)

### {{categoria}}
| Severidad | Criterio | Ejemplo + | Ejemplo - |
|---|---|---|---|
| Alta | {{...}} | {{...}} | {{...}} |
| Media | {{...}} | {{...}} | {{...}} |

## 5. FP rate por categoría

| Categoría | Aceptados | FP rate | Estado |
|---|---|---|---|
| {{indemnity}} | {{n}} | {{4%}} | activa |
| {{data_privacy}} | {{n}} | {{31%}} | **suspendida** |

## 6. Disabled categories (disable temporal)

- `{{data_privacy}}` — FP {{31%}} sobre {{nda}}; suspendida mientras se rediseña el criterio. **No** se reporta como 0% FP. [INFERENCIA]

## 7. Métricas por estrato

| Estrato | Accuracy | Cobertura | Nota |
|---|---|---|---|
| {{contract}} | {{0.89}} | {{ok}} | — |
| {{nda}} | {{n/a}} | {{insuficiente}} | no-calibrado |

> No se reporta una única accuracy agregada como métrica primaria. [DOC]

## 8. Riesgos y edge cases

- Drift de versión del modelo: invalida el `calibration_map`; re-calibrar. [INFERENCIA]
- Buckets aceptados vacíos: reportados como "sin aceptados", no como precisión perfecta. [INFERENCIA]

## 9. Veredicto del gate de QA

| Gate | Resultado |
|---|---|
| Umbral calibrado (no crudo) | {{pass/fail}} |
| Muestreo estratificado | {{pass/fail}} |
| Criterios +/- por severidad | {{pass/fail}} |
| FP por categoría reportado | {{pass/fail}} |
| Disable temporal disponible | {{pass/fail}} |
| `scripts/check.sh` | {{pass/fail}} |

**Veredicto final:** {{LISTA / NO LISTA}}.
