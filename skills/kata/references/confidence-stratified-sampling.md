<!-- distilled from alfa skills/katas-confidence-stratified-sampling -->
<!-- Confidence calibration contra labeled set y stratified sampling por document_type; accuracy desglosada, nunca agregada. -->
# Kata 29 · Confidence Calibration y Stratified Sampling

## Qué es

En extracciones masivas el modelo emite `field_confidence` scores a nivel de campo. Esos scores deben CALIBRARSE contra un labeled validation set, porque la confianza raw está sesgada: un `0.9` raw no significa 90% de probabilidad real de correctitud. Una vez calibrados, los scores enrutan el trabajo: high confidence calibrada va a procesamiento automático con stratified sampling de control; low confidence va a revisión humana. La accuracy se mide siempre desglosada por `document_type` y por field, nunca agregada.

**Anti-scope** (qué NO es esta kata): no es model fine-tuning ni reentrenamiento; calibra el uso de scores existentes, no produce mejores scores. No es active learning. No reemplaza al labeled set: si no hay verdad de referencia, no hay calibración posible — degrada a 100% revisión humana hasta tenerla. [INFERENCIA]

## Por qué importa (falla que evita)

Reportar "97% accuracy global" y automatizar todo lo high-confidence suena seguro hasta que un `document_type` específico falla en silencio dentro del promedio. El número agregado oculta que un segmento minoritario tiene 60% de accuracy. El stratified sampling es la red que detecta nuevos modos de error que un validation set viejo no captura, especialmente drift en segmentos poco frecuentes.

## Modelo mental

- `field_confidence` raw != probabilidad real de correctitud: el score crudo está sesgado.
- Calibración: comparar score raw vs accuracy empírica por bucket en el labeled validation set.
- Stratified sampling: muestrear proporcionalmente por `document_type` y por rango de score, no aleatorio sobre el total.
- La accuracy agregada miente; reportar siempre desglosada por `document_type` y field.
- Routing operativo: high confidence calibrada → auto + muestreo de control; low → revisión humana.

## Supuestos y límites

- **Labeled set representativo y fresco.** La calibración solo es válida si el validation set refleja la distribución de producción actual; un set viejo calibra para un mundo que ya cambió (drift). [SUPUESTO] · Verificación: comparar mix de `document_type` del set vs producción del último período.
- **Suficiencia estadística por bucket.** Un bucket con pocas muestras da accuracy empírica con varianza alta y engañosa. Define un `min_samples` por celda (`document_type` × `score_bucket`); celdas por debajo del umbral no enrutan a auto — van a revisión hasta acumular evidencia. [INFERENCIA]
- **Independencia de campos.** Calibrar por field asume que el confidence de un campo no depende del de otro en el mismo documento; si hay correlación fuerte (p. ej. campos derivados), trátalos como una unidad. [SUPUESTO]
- **Monotonicidad no garantizada.** No asumas que mayor score raw implica mayor accuracy calibrada; la curva puede ser no monótona. El routing usa la accuracy empírica de la celda, nunca el orden del score raw. [INFERENCIA]

## Patrón correcto

```python
# Schema: cada extracción exige field_confidence tipado y acotado
EXTRACT_WITH_CONF = {
    "field_value": {"type": "string"},
    "field_confidence": {"type": "number", "min": 0, "max": 1},  # required
}

def calibrate(predictions, labeled_set):
    # buckets por threshold; compara confianza predicha vs verdad
    buckets = {}
    for pred, truth in zip(predictions, labeled_set):
        b = round(pred["field_confidence"], 1)
        buckets.setdefault(b, []).append(pred["field_value"] == truth)
    # accuracy empírica por bucket = confianza calibrada
    return {b: sum(hits) / len(hits) for b, hits in buckets.items()}

def stratified_sample(extractions, n_per_type=10):
    # muestrea high-confidence proporcional por document_type
    by_type = {}
    for e in extractions:
        by_type.setdefault(e["document_type"], []).append(e)
    return {t: sample_high_conf(items, n_per_type) for t, items in by_type.items()}

# Routing por accuracy empírica calibrada, no por score raw
```

## Anti-patrón

```python
if extraction["field_confidence"] >= 0.9:
    return "auto"  # confía ciegamente en el score raw, sin calibrar

print(f"Accuracy: {global_acc}")  # 97% global que oculta 60% en un segmento
```

## Edge cases y modos de falla

- **Bucket vacío o sub-umbral.** `document_type × score_bucket` sin muestras suficientes: no hay accuracy empírica fiable. Decisión: ese segmento NO se automatiza; enruta a humano y reporta `insufficient_evidence`, nunca extrapoles del bucket vecino. [INFERENCIA]
- **`document_type` nuevo en producción.** No existe en el labeled set. Falla silenciosa clásica: cae fuera de todo estrato. Decisión: cualquier tipo no visto durante calibración → revisión humana por defecto + alerta para etiquetar. [SUPUESTO]
- **Calibración invertida.** Si un bucket de score alto rinde menos accuracy que uno bajo, es señal de score corrupto o data leakage en el set; bloquea el routing y audita antes de operar. [INFERENCIA]
- **Drift entre recalibraciones.** La accuracy de control en el muestreo cae respecto a la calibrada: el modelo o los datos cambiaron. Trigger de recalibración; no esperes al siguiente ciclo planificado.
- **Overfitting al validation set.** Calibrar y reportar sobre el MISMO set infla la confianza. Separa calibration split de holdout de evaluación. [INFERENCIA]
- **Costo de etiquetado del control.** El muestreo de control solo cierra el loop si esas muestras se etiquetan y comparan; sin verdad sobre la muestra, es teatro. Presupuesta el etiquetado del control como parte del pipeline. [SUPUESTO]

## Decisiones y trade-offs

- **Calibración empírica por bucket vs paramétrica (Platt/isotónica).** Se elige binning empírico: es transparente, auditable offline y no asume forma funcional. Trade-off: peor uso de datos en colas escasas y fronteras de bucket arbitrarias. Mitigación: `min_samples` por celda y `bucket_width` documentado. [INFERENCIA]
- **Stratified vs random sampling de control.** Stratified garantiza cobertura de segmentos minoritarios que el random diluye; trade-off: más muestras totales para llenar cada estrato. Se acepta porque el modo de falla que importa vive en los segmentos raros. [INFERENCIA]
- **Umbral de routing por celda vs global.** Por celda evita que un buen promedio global automatice un mal segmento; trade-off: más complejidad operativa y más celdas que mantener. Se prioriza seguridad sobre simplicidad.

## Criterios de aceptación

- Existe un labeled validation set y la calibración es empírica por bucket; el routing NUNCA usa raw confidence. [DOC]
- Toda celda automatizada cumple `min_samples`; las que no, van a humano con motivo explícito.
- Los reportes son por `document_type` + field; un reporte aggregate-only es rechazado.
- El muestreo de control está etiquetado y su accuracy se compara contra la calibrada (cierre de loop).
- `document_type` no visto en calibración nunca cae en auto.
- `scripts/check.sh` pasa: valida labeled set, buckets, sampling, accuracy segmentada y routing.

## Argumento de certificación

- Diferenciar confianza raw de confianza calibrada y explicar por qué la raw está sesgada.
- Describir stratified sampling y por qué supera al random sampling para detectar drift en segmentos minoritarios.
- Rechazar reportar accuracy agregada; exigir desglose por `document_type` y field.
- Conectar la calibración con el routing operativo (auto vs human), incluyendo el manejo de tipos no vistos y celdas sub-umbral.
- Emitir reportes críticos compatibles con `assets/confidence-calibration-report-contract.json`.
- Validar labeled set, buckets, sampling, accuracy segmentada y routing con `scripts/check.sh`.

## Contrato determinístico

La skill usa `assets/` como contrato offline:

- `assets/calibration-policy.json`: exige labeled validation set y calibración empírica por bucket; bloquea routing por raw confidence.
- `assets/stratified-sampling-policy.json`: exige estratos por `document_type` y `score_bucket`, incluyendo segmentos minoritarios.
- `assets/accuracy-reporting-policy.json`: bloquea reportes aggregate-only y exige filas por `document_type` + field.
- `assets/routing-policy.json`: auto/human/control se decide por `calibrated_confidence`.
- `assets/evidence-policy.json`: evidencia local, sin red ni random.

Validación local:

```bash
bash skills/katas-confidence-stratified-sampling/scripts/check.sh
```

## Cuándo activar

Activar en extracciones estructuradas masivas donde el modelo emite confidence scores y hay que decidir qué se automatiza y qué va a revisión humana; o cuando se pide medir/repor­tar accuracy de un pipeline de extracción.

## Skills relacionadas

- `katas-provenance-preservation`
- `katas-false-positive-criteria`
- `katas-multipass-prompt-chaining`
