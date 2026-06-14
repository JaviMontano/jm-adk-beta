# frontload-prompt

Pre-procesa un input antes de ejecutarlo. Toma un request largo, desordenado o
de objetivo implícito y lo reformatea a **SPEC** (Situation / Purpose /
Expectations / Context), detectando vacíos críticos antes de que un ejecutor los
herede. No entrega la tarea: produce el **contrato de trabajo** que otra skill o
agente ejecutará. {DOC}

## Qué hace

- Normaliza cualquier input a 4 campos S/P/E/C con tags de procedencia inline.
- Distingue tres tipos de hueco: inferible (`{INFERENCIA}`), autocompletable
  (`{AUTOCOMPLETADO}`) y bloqueante (`{VACIO_CRITICO}`).
- Emite un veredicto binario: **READY** (4 secciones accionables) o **BLOCKED**
  (≥1 vacío crítico + la pregunta mínima que lo desbloquea).
- Nunca ejecuta la tarea ni sobrescribe archivos.

## Cuándo usarla

- Input crudo pegado (hilo, ticket, transcript) sin pedido explícito.
- Antes de delegar a una skill costosa (genera / refactoriza / escribe) donde un
  malentendido se paga caro.
- **No usar** cuando el input ya es una instrucción atómica y sin ambigüedad —
  frontload añadiría latencia sin reducir riesgo.

## Cómo enruta y ejecuta

Discover → Analyze → Structure → Validate. En *Discover*, si el request
referencia archivos/repo, se inspeccionan con Read/Grep/Glob antes de inferir.
El **Validation Gate** decide READY/BLOCKED. Toda afirmación no obvia lleva
exactamente un tag de la familia Jarvis OS `{...}`; nunca se mezcla con la
familia Alfa `[...]`.

Roles que orquesta esta skill:

- `agents/lead.md` — conduce el flujo Discover→Validate y emite el veredicto.
- `agents/specialist.md` — criterio SPEC: a qué eje va cada fragmento y qué hueco
  es realmente bloqueante.
- `agents/support.md` — lectura de fuentes, extracción de fragmentos, ensamblado
  del bloque SPEC con tags.
- `agents/guardian.md` — gate de aceptación: bloquea READY si algún criterio falla.

## Referencias y soporte

- `knowledge/body-of-knowledge.md` — concepto SPEC, reglas de decisión, estándar
  de tags.
- `knowledge/knowledge-graph.json` — grafo de conceptos clave.
- `prompts/` — prompt primario, meta, y variaciones quick/deep.
- `templates/output.md` — scaffold del bloque SPEC + veredicto.
- `examples/` — un input crudo y su SPEC resultante.
- `assets/` — rúbrica de calidad y checklist del gate (ver `assets/README.md`).
- Taxonomía canónica de tags: `references/verification-tags.md` (raíz del repo).

## Skills relacionadas

- `input-analysis` — interpreta el input en profundidad (esta skill lo estructura).
- `revisor-veracidad` — verifica afirmaciones tras la ejecución.
- `cierre-conversacion` — cierre y handoff.
