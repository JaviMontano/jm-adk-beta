# Example Output — Evaluation Confidence Design

# Reporte de Evaluación con Confidence Calibrada — Contract-Review Agent

> Brand: JM Labs · Fecha: 2026-06-12 · Versión del evaluador: 1.1.0

## 1. Labeled set

| Métrica | Valor |
|---|---|
| Total etiquetado | 600 [DOC] |
| Estratificación | `document_type` |
| Categorías | indemnity, termination, data_privacy, payment_terms |
| Balance +/- | 372 / 228 [DOC] |

Ground truth presente → calibración posible. [DOC]

## 2. Muestreo estratificado

`per_stratum = 30`.

| Estrato | Labels | `per_stratum` | Estado |
|---|---|---|---|
| contract | 420 | 30 | calibrado [DOC] |
| nda | 150 | 30 | calibrado [DOC] |
| dpa | 30 | 30 | calibrado (límite) [INFERENCIA] |

Se estratifica por riesgo: `dpa` es el estrato más raro y de mayor exposición; un muestreo global lo habría diluido a ~5% y lo habría invisibilizado. [INFERENCIA]

## 3. Calibration map

- Método: **binning** (set de 600, suficiente para bins estables, sin la data que exige isotonic). [SUPUESTO]
- Monotonicidad: verificada, monótona creciente.

| `raw_upper` | precisión observada |
|---|---|
| 0.60 | 0.44 [DOC] |
| 0.75 | 0.67 [DOC] |
| 0.90 | 0.85 [DOC] |
| 1.00 | 0.93 [DOC] |

**Hallazgo:** el corte crudo de 0.70 correspondía a ~0.60 de precisión calibrada — muy por debajo del 88% reportado. **Umbral calibrado elegido: precisión >= 0.85** (equivale a raw ~0.88). [DOC]

## 4. Criterios categóricos (+/- por severidad)

### data_privacy
| Severidad | Criterio | Ejemplo + | Ejemplo - |
|---|---|---|---|
| Alta | Transferencia de datos personales a tercero sin base legal citada | "datos se comparten con procesadores en jurisdicción X sin DPA" | "el contrato menciona 'datos' en una cláusula de confidencialidad genérica" |
| Media | Retención sin plazo definido | "se conservan indefinidamente" | "retención por el plazo legal aplicable" |

(Reemplaza el criterio previo vago "sé conservador". [DOC])

## 5. FP rate por categoría

| Categoría | Aceptados | FP rate | Estado |
|---|---|---|---|
| indemnity | 96 | 4% | activa [DOC] |
| termination | 74 | 6% | activa [DOC] |
| payment_terms | 51 | 8% | activa [DOC] |
| data_privacy | 60 | 31% | **suspendida** [DOC] |

La agregada de 88% ocultaba que `data_privacy` arrastraba 31% de FP. [DOC]

## 6. Disabled categories

- `data_privacy` — FP 31% (concentrado en `nda`); suspendida mientras se rediseña el criterio. Listada como **suspendida**, no como 0% FP. [INFERENCIA]

## 7. Métricas por estrato

| Estrato | Accuracy (calibrado) | Nota |
|---|---|---|
| contract | 0.90 | — [DOC] |
| nda | 0.71 | arrastrado por data_privacy (ahora suspendida) [DOC] |
| dpa | 0.83 | muestra al límite [INFERENCIA] |

No se reporta una única accuracy agregada como métrica primaria. [DOC]

## 8. Riesgos y edge cases

- Drift: si sube la versión del modelo, el `calibration_map` se invalida → re-calibrar. [INFERENCIA]
- `dpa` con 30 labels está en el límite mínimo; si baja, marcar no-calibrado. [INFERENCIA]

## 9. Veredicto del gate de QA

| Gate | Resultado |
|---|---|
| Umbral calibrado (no crudo) | pass [DOC] |
| Muestreo estratificado | pass [DOC] |
| Criterios +/- por severidad | pass [DOC] |
| FP por categoría reportado | pass [DOC] |
| Disable temporal disponible | pass [DOC] |
| `scripts/check.sh` | pass [SUPUESTO] |

**Veredicto final:** LISTA para promover, con `data_privacy` suspendida hasta rediseño del criterio.
