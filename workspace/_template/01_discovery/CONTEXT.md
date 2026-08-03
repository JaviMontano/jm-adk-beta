# Stage 01 — Discovery (ICM Layer 2 contract)

One stage, one job: entender la fricción/tarea real antes de especular solución.

## Inputs
- Layer 4 (working): prompt del usuario (no es archivo; se carga del transcript).
- Layer 3 (reference): `../../../skills/adaptive-investigation-method/SKILL.md` (si dominio desconocido).

> Constitution (v7.0.0) NO se carga en discovery — sus MUST/MUST NOT aplican
> a ejecución (03_build/04_validate), no a entender fricción. Anti over-budget
> (paper §3.2: L3 500-2k tok; constitution sola = 5292t).

## Process
0. `scripts/stage-context-manifest.sh .` — confirmar contexto scoped ≤8000t (sensor ICM).
1. Parafrasear la intención → `ENTENDIDO:`.
2. Listar supuestos `[SUPUESTO]` (ratio ≤30%, vibe-coder profile).
3. Señalar gaps → `coverage_gap` + pedir bloqueante.
4. Emitir `first-prompt-router.sh --json` para detectar modo (create/resume/new/resume_task).
5. Escribir resumen de descubrimiento a `output/discovery.md`.

## Outputs
- `output/discovery.md` — intención, supuestos, gaps, modo, blast radius.
- **Review gate**: humano valida `discovery.md` antes de pasar a 02_spec (paper §3.3: edit surface en cada boundary).