# Stage 03 — Build (ICM Layer 2 contract)

One stage, one job: implementar. Working code first, minimal prose (vibe-coder).

## Inputs
- Layer 4 (working): `../02_spec/output/spec.md`.
- Layer 3 (reference): `../../../references/ontology/constitution-must.md` (MUST/MUST NOT slice — fino, cabe budget L3; full constitution es source-of-truth humano).
- Layer 3 (reference): skill resuelto en 02 (leer `skills/<id>/SKILL.md` verbatim).

## Process
0. `scripts/stage-context-manifest.sh .` — confirmar contexto scoped ≤8000t (sensor ICM).
1. Extraer MUST/MUST NOT del constitution (hard rule #5) antes de ejecutar.
2. Ejecutar plan de 02 en orden.
3. Tests first (vibe-coder non-negotiable: production behavior test-first).
4. Evidence tags en claims; `[SUPUESTO]` ≤30%.
5. No debilitar assertions para pasar.
6. Escribir cambios + diff a `output/build.md`.

## Outputs
- `output/build.md` — diff/cambios, estado tests, notas.
- Código/diffs van al repo objetivo (no a output/).
- **Review gate**: humano valida `build.md` + tests verdes antes de 04_validate.