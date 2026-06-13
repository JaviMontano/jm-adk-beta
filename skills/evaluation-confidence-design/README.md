# Evaluation Confidence Design

Diseña el sistema de evaluación de un agente o pipeline de clasificación para que aceptar/rechazar un hallazgo dependa de un umbral **calibrado contra un labeled set** — no de la `confidence` cruda del modelo. Reemplaza la métrica agregada engañosa por un reporte **desglosado por estrato y categoría**.

## Qué hace

- Calibra `raw_confidence` → precisión observada (binning, isotonic o Platt) sobre ground truth humano.
- Estratifica el muestreo por `document_type` (u otra dimensión de riesgo) con mínimo por estrato, para que los estratos raros no desaparezcan de la métrica.
- Convierte criterios vagos ("sé conservador") en criterios **categóricos con ejemplos +/- por severidad**.
- Aísla categorías ruidosas con **disable temporal** en vez de subir el umbral global.
- Reporta **FP rate por categoría** + accuracy por estrato, nunca una sola accuracy agregada como métrica primaria.

## Cuándo usarla

- Alguien propone cortar sobre la `confidence` cruda como umbral.
- Se evalúa con una sola muestra global y se reporta accuracy agregada.
- Una categoría dispara muchos falsos positivos y no hay forma de aislarla.
- Gate de release: la calibración es **bloqueante** antes de promover un evaluador a producción.

**Anti-scope:** no entrena/re-entrena el modelo, no etiqueta documentos crudos desde cero, no tunea prompts del agente productor. Evalúa salidas etiquetadas; no genera ground truth.

## Cómo enruta y ejecuta

1. Verifica que exista labeled set con `document_type`, `category`, `label` y `raw_confidence`. Sin ground truth → detente y pídelo (vacío crítico).
2. Estratifica por `document_type` con `per_stratum` mínimo.
3. Ajusta el `calibration_map` y elige el corte sobre la confidence **calibrada**.
4. Redacta criterios categóricos +/- por severidad.
5. Calcula FP rate por categoría; flaggea `disabled_categories` con FP alto.
6. Emite el reporte desglosado y corre el gate de QA.

## Referencias

- [`SKILL.md`](./SKILL.md) — contrato de capacidad, patrón/anti-patrón, edge cases, validation gate.
- [`knowledge/body-of-knowledge.md`](./knowledge/body-of-knowledge.md) — conceptos, estándares y reglas de decisión.
- [`knowledge/knowledge-graph.json`](./knowledge/knowledge-graph.json) — grafo de conceptos clave.
- [`prompts/`](./prompts/) — prompt primario, meta y variaciones quick/deep.
- [`templates/output.md`](./templates/output.md) — scaffold del reporte de evaluación.
- [`examples/`](./examples/) — ejemplo de input/output trabajado.
- [`assets/`](./assets/) — rúbrica de calidad y checklist del gate (ver `assets/README.md`).
- [`agents/`](./agents/) — contratos de rol lead/specialist/support/guardian.

## Roles

- **lead** orquesta el flujo de diseño de evaluación.
- **specialist** aporta profundidad en calibración, estratificación y diseño de criterios.
- **support** ejecuta el muestreo, el ajuste del mapa y el cómputo de métricas.
- **guardian** valida los gates: calibrada-no-cruda, estratificado, +/- por severidad, FP por categoría, disable temporal.

## Taxonomía de evidencia

Toda afirmación lleva tag: `[DOC]` `[CÓDIGO]` `[CONFIG]` `[INFERENCIA]` `[SUPUESTO]`. Nunca presentes verde como éxito si una categoría está suspendida o un estrato quedó no-calibrado.
