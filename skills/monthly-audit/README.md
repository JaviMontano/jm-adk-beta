# monthly-audit

Cadencia **P22** de salud mensual del jarvis. Pasa el sistema por una rubrica de
**6 preguntas**, puntua cada eje 0-3 con evidencia ligada, calcula el delta vs el
mes previo y deja un **Top 3 de acciones** priorizadas por riesgo x impacto para
el mes siguiente.

## Que hace

- Audita el **sistema**, no el dia: memoria, cadencias, tareas, estructura/AI,
  guardrails y friccion/deuda.
- Produce un **scorecard P22** donde cada score cuelga de evidencia citable
  (archivo, commit, entrada de bitacora), nunca de impresion.
- Persiste el informe de forma **aditiva** (append) en la bitacora destino sin
  sobrescribir historico.

## Cuando usarla

- Trigger explicito `monthly-audit` / `auditoria-mensual` / `health-check`.
- Al cierre de mes de un workspace en operacion.
- **No** para cierre diario (eso es `daily-close` P10), retro de un proyecto
  puntual, ni revision de una sola tarea.

## Como enruta y ejecuta

Procedimiento de 6 pasos: **Discover** (lee fuentes y auditoria previa) →
**Score** (6 preguntas, 0-3 con evidencia) → **Delta** (vs mes previo) →
**Prioritize** (Top 3 acciones) → **Persist** (append aditivo) → **Validate**
(gate de aceptacion). Los roles de `agents/` orquestan, profundizan, ejecutan y
validan cada fase.

## Rubrica P22

1. Memoria · 2. Cadencias · 3. Tareas · 4. Estructura/AI · 5. Guardrails ·
6. Friccion/Deuda. Escala: 0 ausente · 1 fragil · 2 funcional · 3 solido.

## Referencias

- `SKILL.md` — contrato completo, inputs/outputs, gate y edge cases.
- `references/verification-tags.md` — taxonomia de tags Jarvis OS `{...}`.
- `knowledge/body-of-knowledge.md` — conceptos, estandares y reglas de decision.
- `knowledge/knowledge-graph.json` — grafo de conceptos clave.
- `prompts/` — prompt primario, meta y variaciones quick/deep.
- `templates/output.md` — scaffold del informe de auditoria.
- `examples/` — corrida trabajada de ejemplo (input + output).
- `assets/` — rubrica de puntuacion y checklist del gate (ver `assets/README.md`).

## Evidencia y gobernanza

Una sola familia de tags `{...}`, exactamente un tag por afirmacion no obvia,
`{WEB}` invalido sin cita, marca unica por auditoria, nunca verde-como-exito.
