# Validation Gate Checklist — Evaluation Confidence Design

Marca cada ítem antes de declarar el evaluador LISTA. Todos los bloqueantes deben pasar.

## Bloqueantes

- [ ] El umbral usa confidence **calibrada** contra el labeled set, no la cruda. [DOC]
- [ ] El muestreo es **estratificado** por `document_type` con mínimo por estrato. [DOC]
- [ ] Cada categoría tiene **criterio categórico con ejemplos +/-** por severidad. [DOC]
- [ ] Se reporta **FP rate por categoría**, no solo accuracy agregada. [DOC]
- [ ] Existe **disable temporal** para categorías con FP alto. [DOC]
- [ ] El `calibration_map` es no vacío y **monótono** antes de aplicarse. [SUPUESTO]
- [ ] Hay **ground truth**; sin él, el flujo se detiene y lo pide. [SUPUESTO]
- [ ] Sin **falso verde**: categoría suspendida listada como suspendida; estrato no-calibrado no cuenta como métrica; bucket aceptado vacío no se reporta como precisión perfecta. [INFERENCIA]

## No bloqueantes

- [ ] Cada afirmación con **tag de evidencia**. [DOC]
- [ ] Anti-scope respetado: no entrenar, no etiquetar crudo, no tunear prompts del productor. [INFERENCIA]
- [ ] Reporte sigue `templates/output.md`. [DOC]

## Script gate

- [ ] `bash skills/evaluation-confidence-design/scripts/check.sh` pasa (cuando los scripts estén materializados). [SUPUESTO]
