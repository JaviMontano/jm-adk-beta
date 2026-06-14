# agentic-loop-engineering

## Qué hace

Construye el **bucle de control** de un agente que enruta por `stop_reason` tipado,
con budget duro y handlers explícitos por señal. El loop es la columna vertebral
del agente: cada iteración decide entre despachar herramientas (`tool_use`),
detenerse limpio (`end_turn`) o fallar fuerte (`UnhandledStop` / `BudgetExceeded`).
La meta es una máquina de estados **determinista, observable y acotada** en
producción — nunca control inferido desde la prosa del modelo (`"done" in text`).

## Cuándo usarla

- Implementar el bucle que llama al modelo, ejecuta herramientas y reinyecta
  `tool_result`.
- Un agente entra en bucle infinito, se detiene a destiempo o produce halts
  impredecibles.
- Poner un techo de iteraciones/tokens al gasto de un agente autónomo.
- Migrar control por texto (`"done" in text`) hacia control por señal estructurada.

**No usarla cuando** el problema es calidad/tono del prompt (prompt engineering),
diseño del esquema de la herramienta (idempotencia, inputs), u orquestación
multi-agente. Esta skill cubre **un único loop de un único agente**.

## Cómo enruta / ejecuta

1. Declara el contrato estructurado en `assets/loop-contract.schema.json` +
   `assets/loop-policy.json` ANTES de escribir código.
2. El control vive en `stop_reason`: `end_turn` → halt limpio; `tool_use` →
   despacha TODOS los bloques y reinyecta `tool_result` como mensaje `user` con
   `tool_use_id`; cualquier otra señal → `raise UnhandledStop`.
3. Budget estructural (`for iteration in range(max_iterations)`): tras el loop,
   `raise BudgetExceeded`.
4. Cada transición (iteración, señal, herramienta, latencia) se instrumenta para
   auditoría.
5. Verifica contra el gate de aceptación de `SKILL.md` antes de declarar la skill
   aplicada.

## Referencias

- `SKILL.md` — capacidad, patrón correcto, anti-patrones, casos límite, gate.
- `knowledge/body-of-knowledge.md` — taxonomía de `stop_reason`, reglas de decisión,
  contrato de mensajes, modos de fallo.
- `knowledge/knowledge-graph.json` — grafo de conceptos del loop.
- `prompts/` — prompts primario, meta y variaciones (`quick`, `deep`).
- `templates/output.md` — scaffold del entregable (contrato + diseño del loop).
- `examples/` — ejemplo trabajado de migración de control-por-prosa a `stop_reason`.
- `assets/` — contrato/política del loop y rúbrica de calidad (ver `assets/README.md`).

## Taxonomía de evidencia

`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]` — toda afirmación de
control del loop debe llevar tag. Verificar señales del SDK contra la versión en
uso; nunca asumir que `max_tokens`/`pause_turn`/`refusal` existen sin comprobarlo.
