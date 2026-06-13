# Quick Variation — Evaluation Confidence Design

Para un diagnóstico rápido cuando el usuario ya tiene labeled set y solo quiere el corte calibrado + FP por categoría.

## Prompt
Tengo un labeled set con `document_type`, `category`, `label` y `raw_confidence`. En modo express:
1. Estratifica por `document_type` con un mínimo por estrato.
2. Ajusta un `calibration_map` por binning (set chico) y dame el umbral sobre la confidence **calibrada**.
3. Reporta **FP rate por categoría** y marca cuáles candidatean a `disabled_categories`.
4. Entrega solo el desglose por estrato+categoría y el veredicto del gate; sin la narrativa larga.

## Reglas mínimas
- No uses confidence cruda como corte.
- No reportes una sola accuracy agregada como primaria.
- Si falta ground truth, detente y pídelo.
- Tags de evidencia en cada número.
