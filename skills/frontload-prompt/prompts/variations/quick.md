# Quick Variation — frontload-prompt

Para inputs cortos donde basta un pase rápido. Sin inspección de repo salvo que
el request la exija explícitamente.

## Prompt
Reformatea este input a SPEC en un solo pase:

- **S — Situation**: 1 línea, de dónde viene el input (con tag de fuente).
- **P — Purpose**: el resultado deseado en una frase. Si no es inferible →
  `{VACIO_CRITICO}`.
- **E — Expectations**: formato/límites/criterios; default `{AUTOCOMPLETADO}` si
  no se especifican.
- **C — Context**: solo lo presente; no inspecciones archivos.

Veredicto: **READY** o **BLOCKED** (+ la pregunta mínima).

## Reglas mínimas
- Un tag por afirmación, el más débil ante duda.
- No ejecutes la tarea.
- Si dudas entre quick y un análisis completo, usa `deep.md`.
