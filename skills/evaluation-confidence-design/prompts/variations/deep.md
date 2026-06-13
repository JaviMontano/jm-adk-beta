# Deep Variation — Evaluation Confidence Design

Para un diseño exhaustivo de evaluación con justificación de método, edge cases y gate completo.

## Prompt
Diseña el sistema completo de evaluación con confidence calibrada para nuestro pipeline. Cubre en detalle:

1. **Auditoría del labeled set:** cobertura por `document_type` y `category`, tamaño por estrato, balance +/-. Señala estratos con datos insuficientes.
2. **Estratificación:** define `per_stratum`, justifica por qué estratificas por riesgo y no por volumen, y marca estratos no-calibrados.
3. **Calibración:** compara binning vs Platt vs isotonic para el tamaño de set dado; justifica la elección. Valida monotonicidad del `calibration_map`; rechaza si es no monótono o vacío. Elige el corte sobre la calibrada.
4. **Criterios categóricos:** para cada categoría, criterio +/- por nivel de severidad con ejemplos concretos.
5. **FP rate por categoría:** identifica las categorías que arrastran la precisión sin que la agregada lo muestre.
6. **Disable temporal:** propón `disabled_categories` y el plan de rediseño de su criterio.
7. **Edge cases:** estrato con pocos labels, categoría 100% disabled, bucket aceptado vacío, drift de versión del modelo.
8. **Reporte desglosado** por estrato+categoría + sección de riesgos.
9. **Gate de QA:** corre los checks bloqueantes y emite veredicto.

## Reglas
- Cada afirmación con tag de evidencia.
- Nunca falso verde (categoría suspendida ≠ sana; estrato no-calibrado ≠ métrica válida).
- Anti-scope: no entrenes, no etiquetes crudo, no tunees prompts del productor.
- Single-brand JM Labs; sin PII.
