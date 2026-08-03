# Stage 02 — Spec (ICM Layer 2 contract)

One stage, one job: definir done + plan proporcional al blast radius.

## Inputs
- Layer 4 (working): `../01_discovery/output/discovery.md`.
- Layer 3 (reference): `../../../profiles/vibe-coder.md` (ceremony proporcional).

## Process
0. `scripts/stage-context-manifest.sh .` — confirmar contexto scoped ≤8000t (sensor ICM).
1. Definir criterio de done (test-first, assertions no se debilitan).
2. Descomponer en sub-tareas (estimation: decomposition + scripts, horas/story points).
3. Plan de 3 pasos mínimo; ceremony proporcional (typo → skip, feature → spec+plan+tests).
4. Identificar skill/router candidato del catálogo `catalog/skills.json`.
5. Escribir spec a `output/spec.md`.

## Outputs
- `output/spec.md` — done, plan, skill candidato, estimación decomposed.
- **Review gate**: humano valida `spec.md` antes de pasar a 03_build.