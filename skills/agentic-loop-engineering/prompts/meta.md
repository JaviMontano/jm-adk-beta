# Meta-prompt — agentic-loop-engineering

Guía para razonar SOBRE la aplicación de la skill antes y durante la ejecución.

## Encuadre de scope (primer filtro)

Pregúntate: ¿es esto UN loop de UN agente?
- Si la petición es de **tono/calidad del prompt** → prompt engineering, fuera.
- Si es de **esquema/idempotencia de la herramienta** → tool design, fuera.
- Si es de **routing entre agentes / multi-agente** → orquestación, fuera.
- Si pide control de iteraciones, despacho de `tool_use`, reinyección de
  `tool_result` o techo de gasto → DENTRO. [INFERENCIA]

## Detección de anti-señales en el input

Si el usuario PIDE control por prosa o un loop sin budget (p. ej. "decide el halt
leyendo el texto" o "sin max_iterations"), NO lo construyas tal cual: explica por
qué es un modo de fallo y propón el patrón con `stop_reason` + budget. La skill no
se activa para producir el anti-patrón. [DOC]

## Verificación contra el SDK

Las señales `max_tokens`, `pause_turn`, `refusal` y nombres exactos dependen de la
versión del SDK. Marca cada supuesto sobre señales con `[SUPUESTO — verificar
contra el SDK en uso]` y no inventes nombres de señal. [SUPUESTO]

## Criterio de cierre

No declares la skill aplicada sin recorrer las 7 casillas del gate de `SKILL.md`
con evidencia. Verde-por-defecto está prohibido.
