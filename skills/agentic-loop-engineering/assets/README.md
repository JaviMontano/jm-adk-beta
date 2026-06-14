# Assets — agentic-loop-engineering

Bundle de artefactos que materializan el "Paquete determinístico" de `SKILL.md`.
El contrato y la política se declaran ANTES de escribir el loop; la rúbrica
gobierna el gate de aceptación.

## Contenido

| Archivo | Tipo | Para qué sirve | Usado por |
|---------|------|----------------|-----------|
| `loop-contract.schema.json` | JSON Schema | Valida el contrato estructurado del loop (control por `stop_reason`, señales, budget, contrato de `tool_result`). | `SKILL.md` |
| `loop-policy.json` | config JSON | Política por defecto: señales→acción, budget, manejo de handler fallido, instrumentación. Editar por agente. | `SKILL.md` |
| `quality-rubric.json` | rúbrica JSON | Los 7 criterios del gate, cada uno con `fail_if` y tag de evidencia, para el guardian. | `agents/guardian.md` |

## Uso

1. Copia `loop-policy.json` y ajusta `budget.limit` y `tool_result.on_handler_error`
   para tu agente. [CONFIG]
2. Valida tu contrato contra `loop-contract.schema.json` (rechaza contratos sin
   budget, con control por prosa, o con `tool_result` fuera del rol `user`). [DOC]
3. El guardian recorre `quality-rubric.json`: PASS solo con evidencia por criterio.

> Verificar los nombres de señal (`max_tokens`, `pause_turn`, `refusal`) contra la
> versión del SDK en uso antes de fijarlos en la policy. [SUPUESTO]
