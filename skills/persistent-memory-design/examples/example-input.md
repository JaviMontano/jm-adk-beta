# Example Input — persistent-memory-design

## Request

"Estoy auditando una API de pagos multi-servicio durante varios dias. Cada vez que la sesion hace `/compact`, el agente olvida que endpoints ya audite y vuelve a leer los mismos archivos, repitiendo trabajo. Quiero una memoria persistente en disco que:

- sobreviva al `/compact` y a reiniciar la sesion manana,
- solo guarde conclusiones que ya verifique (con la fuente y la fecha),
- no rompa el prompt cache releyendose en cada turno.

Dos sub-agentes (uno de seguridad, uno de contratos) van a escribir hallazgos. Path destino: `.agent/scratchpad.md`."

## Extracted parameters

- **Goal:** auditoria multi-dia de una API de pagos que excede una ventana de contexto. [DOC]
- **Path:** `.agent/scratchpad.md` (repo-relative, seguro). [DOC]
- **Evidence required:** cada hallazgo con `source` + `date`. [DOC]
- **Writers:** dos (seguridad, contratos) → se necesita politica de concurrencia. [INFERENCE]
- **Pain points:** olvido tras `/compact`, retrabajo, relectura por turno que rompe el cache. [DOC]

## Expected behavior

Activate the skill, design the four-section scratchpad with an entry filter (validated-only + provenance), a read-once bootstrap, upsert-by-key writes, a concurrency policy for the two writers, and a `/compact`+reset survival check — then run the acceptance gate. No raw transcript, no per-turn re-read.
