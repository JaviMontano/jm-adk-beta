# prompt-chaining-design

## Qué hace

Convierte una tarea de procesamiento por lote en una **cadena de pases tipada** en
lugar de un mega-prompt único. El patrón canónico es **map → reduce con schemas**:

- **Pase local tipado**: procesa cada unidad atómica (archivo, ticket, registro, PR)
  de forma aislada e idempotente y emite un resumen contra un schema con estado
  `ok` / `error` por unidad.
- **Schema de transición**: contrato explícito —una colección tipada de resúmenes—
  que es lo único que viaja al segundo pase. Nunca viajan los crudos.
- **Pase de integración**: sintetiza, agrega o decide leyendo **solo** los resúmenes.

Sustituye saturación de atención y costo cuadrático por paralelización tipada,
aislamiento de fallos y trazabilidad. [DOC]

## Cuándo usarla

- El lote tiene más unidades de las que caben con calidad en una sola ventana
  (decenas de archivos, cientos de registros).
- Las unidades son independientes y solo se integran al final (map → reduce).
- Quieres paralelizar el pase local y aislar fallos por unidad sin abortar el lote.
- El resultado depende de una síntesis sobre resúmenes, no de cada byte crudo.

## Cuándo NO usarla

- Single-pass cabe holgado y razona mejor con el contexto completo.
- Las unidades tienen dependencias ocultas (la unidad N necesita el crudo de M).
- No es procesamiento por lote (redactar un correo, una respuesta puntual).
- Se exige meter crudos en el pase 2 o saltarse schemas → Guardian bloquea.

## Cómo enruta y ejecuta

1. **lead** delimita la unidad atómica y decide chaining vs single-pass.
2. **specialist** diseña los dos schemas (local + transición) y el patrón map→reduce.
3. **support** implementa el pase local idempotente y el pase de integración.
4. **guardian** valida los seis gates: sin crudos en el pase 2, schema por pase,
   error tipado por unidad, pase local de una sola unidad, schema de transición
   presente, y justificación frente a single-pass.

El contrato determinístico vive en `assets/` y se valida offline con
`scripts/check.sh` + `scripts/validate_prompt_chaining_design.py`.

## Referencias

- `SKILL.md` — capacidad, inputs/outputs, patrón y anti-patrón, checklist.
- `knowledge/body-of-knowledge.md` — conceptos, estándares y reglas de decisión.
- `knowledge/knowledge-graph.json` — grafo de conceptos clave.
- `agents/` — contratos de rol (lead, specialist, support, guardian).
- `prompts/` — prompts primario, meta y variaciones quick/deep.
- `templates/output.md` — scaffold del entregable de diseño de cadena.
- `examples/` — ejemplo trabajado (auditoría de repositorio multi-archivo).
- `assets/` — rúbrica de calidad y checklist determinísticos del bundle.

## Taxonomía de evidencia

`[DOC]` documentado en esta skill · `[CÓDIGO]` verificable en assets/scripts ·
`[CONFIG]` frontmatter/manifest · `[INFERENCIA]` derivado del patrón ·
`[SUPUESTO]` pendiente de confirmación con el solicitante.

## Skills relacionadas

`katas-multipass-prompt-chaining` · `workflow-forge` · `output-engineering`
