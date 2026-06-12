# Assets — qbr-quarterly

Bundle de assets deterministicos que conducen la validacion y el formato del QBR.

| Asset | Tipo | Para que sirve | Lo usa |
|---|---|---|---|
| `quality-rubric.json` | application/json | Seis dimensiones ponderadas con `pass_when` y el vocabulario pass/conditional/fail/not-verified; conduce el veredicto del guardian, el bloque de validacion del template y el meta-prompt. | `agents/guardian.md`, `templates/output.md`, `prompts/meta.md` |
| `checklist.md` | text/markdown | Checklist del Acceptance Gate espejo de `SKILL.md`; bloquea el "hecho" hasta marcar cada casilla. | `agents/guardian.md`, `SKILL.md` |

## Reglas
- Estos assets son la fuente de verdad del gate: el guardian no improvisa criterios.
- Un solo `fail` en la rubrica bloquea la entrega; `not-verified` nunca es `pass`.
- Mantener `assets/manifest.json` sincronizado: cada entrada apunta a un archivo que
  existe y a `used_by` targets que existen.
