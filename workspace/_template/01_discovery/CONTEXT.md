# Stage 01 — Discovery (ICM Layer 2 contract)

One stage, one job: entender la fricción/tarea real antes de especular solución.

## Inputs
- Layer 4 (working): input del usuario (prompt, notas, repo objetivo).
- Layer 3 (reference): `../../../references/ontology/constitution-v7.0.0.md`.
- Layer 3 (reference): `../../../skills/adaptive-investigation-method/SKILL.md` (si dominio desconocido).

## Process
1. Parafrasear la intención → `ENTENDIDO:`.
2. Listar supuestos `[SUPUESTO]` (ratio ≤30%, vibe-coder profile).
3. Señalar gaps → `coverage_gap` + pedir bloqueante.
4. Emitir `first-prompt-router.sh --json` para detectar modo (create/resume/new/resume_task).
5. Escribir resumen de descubrimiento a `output/discovery.md`.

## Outputs
- `output/discovery.md` — intención, supuestos, gaps, modo, blast radius.
- Edit surface: el humano edita `discovery.md` antes de pasar a 02_spec.