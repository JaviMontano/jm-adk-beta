# Session Lifecycle Management — README

## Qué hace

Decide de forma **auditable** entre tres transiciones de sesión de agente —`resume`, `fork`, `fresh`— a partir de la **validez del contexto** y la **detección de staleness** de tool results cacheados. Cuando el mundo cambió, comprime el scratchpad en un `TypedSummary` (hechos verificables con evidencia), no en un transcript crudo. [DOC]

La decisión nunca es por intuición del modelo: se apoya en un contrato de validez (`timestamp`, `tool_results` con `mtime`+hash, invariantes del mundo: HEAD de git, hash del lockfile, esquema de BD) y una matriz de reglas explícitas. [CODE]

## Cuándo usarla

- Agente de larga duración que sobrevive a varios turnos/reinicios y debe decidir si reusar el contexto previo. [DOC]
- Hubo refactor, migración o despliegue entre dos turnos y dudas de si la memoria sigue confiable. [DOC]
- Quieres explorar varias hipótesis en paralelo sin contaminación cruzada. [DOC]
- El scratchpad creció tanto que pegarlo completo es caro y ruidoso. [DOC]

**No activar (anti-scope):** tareas de dominio sin sesión persistente, un solo turno sin contexto previo, input vacío. Sin `SessionContext` previo no hay transición que decidir. [INFERENCIA]

## Cómo enruta y ejecuta

1. **Contrato de validez** — modela qué hace válido un `SessionContext`.
2. **Detector de staleness** — compara cada result cacheado contra su fuente actual (`mtime` como filtro barato, hash/HEAD como verdad). Una stale **crítica** invalida el `resume`.
3. **Matriz de decisión** — válido + objetivo continuo → `resume`; ramificable sin estado mutable compartido → `fork`; staleness crítico o mundo cambiado → `fresh`.
4. **`TypedSummary`** — `goal`, `decisions[]`, `open_questions[]`, `verified_facts[]` (cada uno con `source`), `stale_dropped[]`.
5. **Aislamiento de forks** — scratchpad y workspace propios por rama.
6. **Trazabilidad** — la transición queda registrada con su razón y pasa el gate `scripts/check.sh`.

## Roles (agents/)

- `agents/lead.md` — orquesta el flujo de decisión de extremo a extremo y emite la `Transition` + reporte.
- `agents/specialist.md` — profundidad de dominio: semántica de staleness, criticidad de invariantes, diseño del `TypedSummary`.
- `agents/support.md` — ejecución determinista: corre el detector, computa hashes/HEAD, invoca el gate.
- `agents/guardian.md` — puertas de validación: ningún `verified_fact` desde fuente droppeada, `stale_dropped` no vacío cuando hubo staleness, no-activación en casos fuera de alcance.

## Conocimiento y prompts

- `knowledge/body-of-knowledge.md` — conceptos, estándares y reglas de decisión del dominio.
- `knowledge/knowledge-graph.json` — grafo de conceptos clave.
- `prompts/primary.md`, `prompts/meta.md`, `prompts/variations/quick.md`, `prompts/variations/deep.md`.
- `templates/output.md` — scaffold del reporte de decisión.
- `examples/` — ejemplo de entrada y salida trabajados.
- `assets/` — rúbrica de calidad y checklist del gate (ver `assets/README.md`).

## Evidencia

Toda afirmación lleva tag: `[DOC]` `[CODE]` `[CONFIG]` `[INFERENCIA]` `[SUPUESTO]`. Nunca verde-como-éxito sin evidencia; sin PII de cliente; marca única JM Labs.
