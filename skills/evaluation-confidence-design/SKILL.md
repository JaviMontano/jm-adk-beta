---
name: evaluation-confidence-design
version: 1.1.0
last_updated: 2026-06-11
description: "Disenar evaluacion con confidence calibrada contra labeled set, stratified sampling y criterios categoricos por severidad para reducir falsos positivos sin ocultar sesgo en metricas agregadas."
owner: "JM Labs"
triggers:
  - evaluation confidence design
  - confidence calibration
  - stratified sampling
  - false positive criteria
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Evaluation Confidence Design

## Capacidad

Diseñar el sistema de evaluación de un agente o pipeline de clasificación para que aceptar/rechazar un hallazgo dependa de un umbral **calibrado contra un labeled set**, no de la `confidence` cruda del modelo. Incluye: muestreo estratificado por `document_type` (u otra dimensión de riesgo) con mínimo por estrato, criterios categóricos con ejemplos +/- por severidad, disable temporal de categorías con FP rate alto, y reporte de accuracy + FP **desglosado** por estrato y categoría en vez de una métrica agregada que oculta el sesgo. [DOC]

## Cuándo usarla

- Alguien propone cortar sobre la `confidence` cruda como umbral. [DOC]
- Se evalúa con una sola muestra global y se reporta accuracy agregada. [DOC]
- Una categoría dispara muchos falsos positivos y no hay forma de aislarla. [DOC]
- El criterio de una categoría es vago ("sé conservador") en vez de categórico con +/-. [DOC]
- Gate de release: antes de promover un evaluador a producción. La calibración es bloqueante. [DOC]

**No la uses (anti-scope)** para entrenar/re-entrenar el modelo, etiquetar documentos crudos desde cero, ni para tunear prompts del agente productor. Esta skill evalúa salidas etiquetadas; no genera ground truth ni modifica el clasificador. [INFERENCIA]

## Inputs → Outputs

**Inputs:** labeled set humano (positivo/negativo) etiquetado además por `document_type` y por `category`; `raw_confidence` por hallazgo; dimensión de estratificación. [DOC]
**Outputs:** calibration map (raw→precisión observada), umbral sobre confidence calibrada, criterios categóricos +/- por severidad, FP rate por categoría, lista de `disabled_categories`, y reporte desglosado por estrato+categoría. [DOC]

**Vacío crítico:** sin ground truth etiquetado no hay calibración posible — detén y pide el labeled set, no inventes umbrales. [SUPUESTO]

## Cómo construir

1. **Labeled set.** Reúne ejemplos humanos +/- etiquetados también por `document_type` y `category`. [DOC]
2. **Estratificar.** Muestrea por `document_type` con mínimo por estrato; los estratos raros no deben desaparecer de la métrica. [DOC]
3. **Calibrar.** Ajusta un mapeo (binning, isotonic o Platt) de `raw_confidence` a precisión observada en el labeled set. El corte se elige sobre la calibrada. [DOC]
4. **Criterios categóricos.** Por categoría, criterio con ejemplos +/- por nivel de severidad. Evita instrucciones vagas. [DOC]
5. **FP rate por categoría.** Una categoría puede arrastrar la precisión sin que la métrica agregada lo muestre. [DOC]
6. **Disable temporal.** Flag para desactivar una categoría con FP alto mientras se rediseña su criterio, sin tumbar el resto. [DOC]
7. **Reportar desglosado** por estrato y categoría; corre el gate de QA. [DOC]

## Decisiones y trade-offs

- **Calibrada vs cruda:** la calibrada cuesta un labeled set y re-ajuste cuando el modelo cambia, pero la cruda no es comparable entre versiones ni entre categorías. Trade-off aceptado: el coste de mantenimiento compra umbrales con significado de precisión real. [INFERENCIA]
- **Estratificado vs aleatorio global:** el global es más barato pero invisibiliza estratos raros (justo los de mayor riesgo). Estratifica por la dimensión de riesgo, no por volumen. [INFERENCIA]
- **Disable temporal vs subir el umbral global:** subir el umbral global sacrifica recall en categorías sanas para tapar una ruidosa. Aislar la categoría preserva el resto. [INFERENCIA]
- **Método de calibración:** isotonic necesita más datos pero captura no-monotonías; Platt/binning bastan con labeled sets chicos. Elige por tamaño del set, no por moda. [SUPUESTO]

## Patrón correcto

```python
# GOOD: corte sobre confidence CALIBRADA + muestreo estratificado + FP por categoria
from collections import defaultdict

def calibrate(raw_conf: float, calibration_map: list[tuple[float, float]]) -> float:
    # calibration_map: bins (raw_upper, observed_precision) fit on labeled set
    for upper, observed in calibration_map:
        if raw_conf <= upper:
            return observed
    return calibration_map[-1][1]

def stratified_sample(labeled: list[dict], per_stratum: int) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for row in labeled:
        buckets[row["document_type"]].append(row)
    sample = []
    for doc_type, rows in buckets.items():
        sample.extend(rows[:per_stratum])  # guarantee min per stratum
    return sample

def evaluate(findings, calibration_map, threshold, disabled_categories):
    fp_by_category: dict[str, list[bool]] = defaultdict(list)
    accepted = []
    for f in findings:
        if f["category"] in disabled_categories:
            continue  # temporal disable for high-FP category
        if calibrate(f["raw_confidence"], calibration_map) >= threshold:
            accepted.append(f)
            fp_by_category[f["category"]].append(f["label"] == "negative")
    fp_rate = {c: sum(v) / len(v) for c, v in fp_by_category.items()}
    return accepted, fp_rate  # report FP per category, not aggregate accuracy
```

## Anti-patrón

```python
# ANTI: confidence cruda como umbral, muestra global, accuracy agregada
def evaluate_bad(findings, raw_threshold=0.7):
    accepted = [f for f in findings if f["raw_confidence"] >= raw_threshold]
    # criterio vago: "be conservative" sin ejemplos +/-
    # sin estratificacion: estratos raros invisibles
    accuracy = sum(f["label"] == "positive" for f in accepted) / len(accepted)
    return accepted, accuracy  # metrica agregada oculta el sesgo por categoria
```

## Edge cases

- **Estrato con muy pocos labels:** `per_stratum` mayor que el bucket → reporta cobertura insuficiente y marca el estrato como no-calibrado, no rellenes con otro estrato. [INFERENCIA]
- **Categoría 100% en `disabled_categories`:** su FP rate no entra al reporte; lístala aparte como "suspendida", no como 0% FP (sería un falso verde). [INFERENCIA]
- **`calibration_map` vacío o no monótono:** rechaza; un mapa no monótono indica fit defectuoso, no lo apliques. [SUPUESTO]
- **Bucket aceptado vacío** (todo bajo umbral): `fp_rate` por categoría queda indefinido — repórtalo como "sin aceptados", nunca como precisión perfecta. [INFERENCIA]
- **Drift del modelo:** un cambio de versión invalida el calibration map; re-ajusta antes de reusar umbrales. [INFERENCIA]

## Self-correction triggers

Si te descubres haciendo cualquiera de esto, deténte y reencuadra: comparar confidences crudas entre versiones; reportar una sola accuracy agregada como métrica primaria; muestrear aleatorio global; redactar un criterio sin ejemplos +/-; presentar una categoría disabled como sana; o fijar umbrales sin labeled set. [INFERENCIA]

## Validation gate (antes de marcar lista)

- ¿El umbral usa confidence **calibrada** contra el labeled set, no la cruda? [DOC]
- ¿El muestreo es **estratificado** por `document_type` con mínimo por estrato? [DOC]
- ¿Cada categoría tiene **criterio categórico con ejemplos +/-** por severidad? [DOC]
- ¿Se reporta **FP rate por categoría**, no solo accuracy agregada? [DOC]
- ¿Existe **disable temporal** para categorías con FP alto? [DOC]
- ¿Corre `scripts/qa/run-confidence-fp-tests.py` y pasa como gate? [SUPUESTO]

## Paquete determinístico

- `assets/evaluation-schema.json` y `assets/confidence-policy.json` declaran el evaluador **antes** de fijar umbrales o disabled categories. [SUPUESTO]
- `scripts/compile-evaluation-confidence.py <evaluacion.json> --output <reporte.md>` genera un reporte reproducible (labeled set, muestreo, calibration map, criterios, métricas, riesgos). [SUPUESTO]
- `bash skills/evaluation-confidence-design/scripts/check.sh` antes de marcar lista. [SUPUESTO]
- Rechaza: corte sobre confidence cruda, muestreo global, categorías sin +/-, high-FP activo, accuracy agregada como métrica primaria. [DOC]

> Los assets/scripts anteriores son **contratos objetivo**, aún no presentes en repo; créalos al materializar la skill. Hasta entonces son `[SUPUESTO]`, no `[CÓDIGO]`. [INFERENCIA]

## Upgrade safety

- **No sobrescribir ediciones locales:** al completar archivos faltantes, crea solo lo ausente; nunca pises cambios locales sin diff explícito. [SUPUESTO]
- **Override experimental:** variantes de prueba van bajo `.local/` y tienen prioridad sobre la versión versionada; no edites el canónico para experimentar. [SUPUESTO]
- **Bump de versión:** sube `version` y `last_updated` al cambiar el contrato; no rompas `triggers` ni el `name` (rompe el catálogo y los cross-links). [DOC]

## Katas y skills relacionadas

- Katas: 29, 30. [DOC]
- Skills: `katas-confidence-stratified-sampling`, `katas-false-positive-criteria`. [DOC]
