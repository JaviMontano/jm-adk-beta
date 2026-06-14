# Assets — plan-mode-workflow

Este bundle define el **contrato determinístico** del gate de dos modos. No es
documentación de prosa: son los datos que un hook `PreToolUse` lee para hacer
cumplir la separación entre Plan Mode (read-only) y Execute Mode (escritura tras
firma por hash).

## Contenido

| Archivo | Tipo | Para qué sirve | Consumido por |
|---------|------|----------------|---------------|
| `gate-policy.json` | config | Modo inicial, transiciones por firma de hash y re-firma por mismatch, read-allowlist, write-blocklist (tools + patrones Bash mutante), campos del evento de aprobación, enforcement fail-closed. | `SKILL.md`, `prompts/primary.md`, `templates/output.md` |
| `quality-rubric.json` | rubric | Los 6 criterios del gate de aceptación, cada uno con `fail_if` y tag de evidencia. | `agents/guardian.md`, `prompts/meta.md` |
| `manifest.json` | manifest | Índice declarativo de los assets y sus consumidores. | — |

## Cómo se usan

1. **Diseño:** `prompts/primary.md` y `templates/output.md` parten de `gate-policy.json`
   para enumerar la blocklist y el contrato de modo.
2. **Enforcement:** el hook `PreToolUse` lee `gate-policy.json` para decidir
   `allow`/`deny` según el modo y los patrones.
3. **Validación:** el guardian corre `quality-rubric.json`; ningún caso bloqueado
   (`bypassPermissions`, Bash mutante, entrada vacía) pasa en verde.

Toda validación es **offline**: sin red, sin reloj, sin aleatoriedad. Sin precios.
Single-brand (JM Labs).
