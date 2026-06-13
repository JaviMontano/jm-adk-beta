# Body of Knowledge — Evaluation Confidence Design

## Conceptos clave

### 1. Confidence cruda vs calibrada
La `raw_confidence` que emite un modelo es un score interno, **no** una probabilidad de acierto. No es comparable entre versiones del modelo ni entre categorías. La **confidence calibrada** mapea la cruda a la precisión observada en un labeled set, de modo que "0.8 calibrada" significa "≈80% de los aceptados a este nivel fueron correctos". El corte de aceptar/rechazar se elige siempre sobre la calibrada. [DOC]

### 2. Calibration map
Estructura que traduce `raw_confidence → precisión observada`. Métodos:
- **Binning**: agrupa por rangos y calcula precisión por bin. Simple, robusto con sets chicos.
- **Platt scaling**: ajusta una sigmoide logística. Bueno con poca data, asume forma sigmoidea.
- **Isotonic regression**: ajuste monótono no paramétrico; captura no-monotonías pero exige más data.
Regla: elegir por **tamaño del labeled set**, no por moda. Un mapa **no monótono o vacío** indica fit defectuoso → rechazar, no aplicar. [SUPUESTO]

### 3. Muestreo estratificado
Particionar el labeled set por una **dimensión de riesgo** (`document_type`) y muestrear con un **mínimo por estrato**. El muestreo global aleatorio invisibiliza los estratos raros — que suelen ser los de mayor riesgo. Estratificar por riesgo, no por volumen. [INFERENCIA]

### 4. Criterios categóricos por severidad
Cada categoría debe tener criterio explícito con **ejemplos positivos y negativos** por nivel de severidad. Las instrucciones vagas ("sé conservador") no son auditables ni reproducibles. [DOC]

### 5. FP rate por categoría
La tasa de falsos positivos calculada **por categoría**. Una categoría ruidosa puede arrastrar la precisión global sin que una accuracy agregada lo revele. Es la métrica que rompe el falso verde. [DOC]

### 6. Disable temporal
Flag (`disabled_categories`) para suspender una categoría con FP alto mientras se rediseña su criterio, **sin** subir el umbral global (que sacrificaría recall en categorías sanas). [INFERENCIA]

### 7. Reporte desglosado
Salida primaria por **estrato + categoría**, no una sola accuracy agregada. La agregada solo acompaña, nunca reemplaza al desglose. [DOC]

## Estándares y prácticas

- **Ground truth primero:** sin labeled set humano +/- no hay calibración posible. Detener y pedirlo. [SUPUESTO]
- **Reproducibilidad:** misma entrada → mismo reporte; muestreo semillado.
- **Re-calibración por drift:** un cambio de versión del modelo invalida el `calibration_map`; re-ajustar antes de reusar umbrales. [INFERENCIA]
- **Gate bloqueante:** la calibración es condición previa a promover el evaluador a producción. [DOC]

## Reglas de decisión

| Situación | Decisión |
|---|---|
| Labeled set chico | Platt o binning, no isotonic [SUPUESTO] |
| Estratos raros de alto riesgo | Estratificar por riesgo con mínimo por estrato [INFERENCIA] |
| Una categoría con FP alto | Disable temporal, no subir umbral global [INFERENCIA] |
| Mapa no monótono/vacío | Rechazar el fit [SUPUESTO] |
| Estrato con bucket insuficiente | Marcar no-calibrado, no rellenar [INFERENCIA] |
| Cambio de versión del modelo | Re-calibrar antes de reusar [INFERENCIA] |

## Anti-scope

No entrena/re-entrena el modelo, no etiqueta documentos crudos desde cero, no tunea prompts del productor. Evalúa salidas etiquetadas. [INFERENCIA]

## Katas y skills relacionadas

- Katas: 29 (confidence + stratified sampling), 30 (false positive criteria). [DOC]
- Skills: `katas-confidence-stratified-sampling`, `katas-false-positive-criteria`. [DOC]
