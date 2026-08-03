# Stage 04 — Validate (ICM Layer 2 contract)

One stage, one job: gates + verification antes de "done". Truth = filesystem.

## Inputs
- Layer 4 (working): `../03_build/output/build.md`.
- Layer 3 (reference): `../../../references/ontology/constitution-must.md` (MUST/MUST NOT slice — verificar respetados; full constitution para auditoría humana).
- Layer 3 (reference): `../../../scripts/check-prerequisites.sh` (gates).

## Process
0. `scripts/stage-context-manifest.sh .` — confirmar contexto scoped ≤8000t (sensor ICM).
1. `git status --short` — confirmar cambios.
2. `python3 scripts/validate-coverage.py`.
3. `python3 scripts/check-token-budget.py` (blocker pre-release si falla).
4. `python3 scripts/validate-evals.py`.
5. `bash scripts/first-prompt-router.sh --json` — registrar modo final.
6. Verificación antes de done: artifact existence, no aserto (hard rule #6).

## Outputs
- `output/validate.md` — gate results (pass/fail), coverage_gap residual.
- Block release si cualquier gate falla.
- **Review gate final**: humano valida gates verdes + deliverable antes de cerrar.