# Provenance Engineering — README

## Que hace

Disena e implementa pipelines de extraccion/sintesis donde **cada claim transporta su provenance tipada** y donde la invariante "no hay claim sin source" es estructural, no aspiracional. Convierte un output narrativo no auditable en un artefacto donde un humano traza cualquier dato hasta su origen y ve que fuentes lo respaldan o lo contradicen. [DOC]

Tres decisiones de ingenieria que cubre:

1. Modelar cada afirmacion como objeto con `source[]` obligatorio (`source_id`, `locator`, `as_of`). [DOC]
2. Detectar conflictos entre fuentes con `conflict=true` conservando **todas** las fuentes — nunca promediar ni elegir una en silencio. [DOC]
3. Escalar los conflictos a revision humana con la fecha visible; el pipeline no resuelve. [DOC]

## Cuando usarla

- Pipeline que extrae datos de multiples documentos (KYC, due diligence, research multi-fuente) cuyo output se usa para **decidir, firmar o citar**. [DOC]
- Distintas fuentes pueden contradecirse (dos fechas, dos cifras, dos direcciones) y promediar destruye informacion critica. [DOC]
- Necesitas un test estructural que **falle el build** si aparece un claim sin source. [DOC]

**No la uses** cuando el output es prosa exploratoria sin consecuencia de decision, o cuando una sola fuente de verdad es indiscutible y no hay posibilidad de conflicto. Forzarla ahi anade ceremonia sin valor de auditoria. [INFERENCIA]

## Como enruta y ejecuta

Flujo lead -> specialist -> support -> guardian:

1. **lead** (`agents/lead.md`) — resuelve el inventario de fuentes, los atributos a extraer y el consumidor/consecuencia; bloquea si falta el inventario o un locator (vacio critico). Orquesta el resto.
2. **specialist** (`agents/specialist.md`) — profundidad de dominio: tipado del `Claim`, normalizacion previa a comparacion, deteccion real de conflicto vs diferencia de formato.
3. **support** (`agents/support.md`) — ejecucion: captura provenance en extraccion, render con `as_of` visible, cola de escalacion, test estructural en CI.
4. **guardian** (`agents/guardian.md`) — gates de validacion: ningun claim sin source, ningun `source_id` fuera de inventario, ningun conflicto promediado/silenciado/no escalado; nunca trata green como prueba.

## Evidence taxonomy

Cada claim no obvio lleva exactamente un tag Alfa-core: `[DOC]`, `[CÓDIGO]`, `[CONFIG]`, `[INFERENCIA]`, `[SUPUESTO]`. Todo `[SUPUESTO]` se empareja con un paso de verificacion. Sin mezcla de familias de tags. [DOC]

## Referencias y assets

- Contrato completo, patron correcto, anti-patrones y gate de aceptacion: `SKILL.md`.
- Conocimiento de dominio (conceptos, reglas de decision): `knowledge/body-of-knowledge.md`.
- Grafo de conceptos: `knowledge/knowledge-graph.json`.
- Prompts: `prompts/primary.md`, `prompts/meta.md`, `prompts/variations/quick.md`, `prompts/variations/deep.md`.
- Scaffold de entregable: `templates/output.md`.
- Bundle determinista (rubrica + checklist): `assets/` (ver `assets/README.md`).
- Ejemplo trabajado: `examples/example-input.md`, `examples/example-output.md`.
