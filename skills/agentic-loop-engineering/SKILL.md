---
name: agentic-loop-engineering
version: 1.1.0
description: "Construir el bucle de control agentico que enruta por stop_reason tipado con budget duro y handlers explicitos, no por prosa."
owner: "JM Labs"
triggers:
  - agentic loop engineering
  - agent control loop
  - stop_reason routing
  - loop budget
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Agentic Loop Engineering

## Capacidad

Construir el bucle de control de un agente que enruta por `stop_reason` tipado, con budget duro y handlers explícitos por señal, en lugar de inferir el control desde la prosa del modelo. El loop es la columna vertebral del agente: cada iteración decide entre despachar herramientas, detenerse o fallar fuerte. La capacidad es diseñar esa máquina de estados para que sea **determinista, observable y acotada** en producción. [DOC]

## Cuándo usarla

- Implementar el bucle que llama al modelo, ejecuta herramientas y reinyecta resultados.
- Un agente entra en bucles infinitos, se detiene a destiempo o produce halts impredecibles.
- Hay que poner un techo de iteraciones o tokens al gasto de un agente autónomo.
- Migrar un agente desde control por texto (`"done" in text`) hacia control por señal estructurada.

**No usarla cuando** (anti-scope): el problema es de *calidad del prompt* o tono (eso es prompt engineering), de *diseño de la herramienta* en sí (esquema de inputs, idempotencia), o de orquestación *multi-agente* / routing entre agentes. Esta skill cubre un único loop de un único agente. [INFERENCIA]

## Inputs / Outputs

**Inputs** [DOC]
- `messages` inicial (historial), catálogo de `tools` (schemas), mapa `handlers` `{nombre → callable}`.
- Budget configurable: `max_iterations` y/o presupuesto de tokens.
- Cliente del modelo (p. ej. SDK Anthropic) ya construido.

**Outputs** [DOC]
- La respuesta final del modelo en el halt limpio (`end_turn`).
- O una excepción tipada: `UnhandledStop(stop_reason)` / `BudgetExceeded(limit)` — nunca un retorno ambiguo.
- Traza por iteración (señal, herramienta, latencia) para auditoría.

## Cómo construir

1. Define el loop como `while True` (o `for ... in range(max_iterations)`) y resuelve el control **únicamente** con el campo `stop_reason` tipado de la respuesta. [CÓDIGO]
2. `stop_reason == "tool_use"`: despacha cada bloque a su handler, recoge el resultado y reinyéctalo en el historial como mensaje `user` con `tool_result`; continúa. Procesa **todos** los bloques de la respuesta (puede haber tool calls en paralelo), no solo el primero. [CÓDIGO]
3. `stop_reason == "end_turn"`: detén y devuelve el resultado final (halt limpio). [CÓDIGO]
4. Cualquier otra señal no contemplada: `raise UnhandledStop(stop_reason)` — falla fuerte, nunca un halt silencioso. Esto incluye señales que SÍ existen pero que aún no manejas (`max_tokens`, `pause_turn`, `refusal`): explícitas o `raise`. [CÓDIGO]
5. Acota el gasto: contador `iterations` contra `max_iterations` que dispara `BudgetExceeded`. Configurable, no constante mágica. [CÓDIGO]
6. Instrumenta cada transición (iteración, señal, herramienta, latencia) para auditar el loop después. [CÓDIGO]

**Decisión — `for range()` vs `while True` + contador.** El patrón usa `for iteration in range(max_iterations)` porque hace el budget *estructural*: es imposible olvidar incrementar el contador y el techo duro es la línea tras el loop. Trade-off: si más adelante el budget pasa a ser por *tokens* (no por iteraciones), conviene `while True` con chequeo explícito de tokens consumidos. [INFERENCIA]

## Patrón correcto

```python
# GOOD: control enrutado por stop_reason tipado, budget duro, fallo fuerte
def run_agent_loop(client, messages, tools, handlers, max_iterations=20):
    for iteration in range(max_iterations):
        resp = client.messages.create(model=MODEL, messages=messages, tools=tools)
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "end_turn":
            return resp                       # halt limpio

        if resp.stop_reason == "tool_use":
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    handler = handlers[block.name]   # KeyError = fallo fuerte
                    result = handler(**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})
            continue

        raise UnhandledStop(resp.stop_reason)  # señal no contemplada
    raise BudgetExceeded(max_iterations)        # techo duro
```

## Anti-patrón

```python
# ANTI: control por prosa -> halt silencioso o bucle infinito
while True:
    resp = client.messages.create(model=MODEL, messages=messages)
    text = resp.content[0].text
    if "done" in text.lower():     # frágil: el modelo dice "not done" y sale
        break
    if "use tool" in text.lower(): # no hay budget, no hay tool_result tipado
        run_some_tool()
    # sin max_iterations: si nunca aparece "done", bucle infinito
```

Anti-patrones adicionales a vetar [INFERENCIA]:
- Procesar solo `resp.content[0]` cuando hay varios `tool_use` → tool calls en paralelo perdidos y `tool_result` huérfanos que rompen el siguiente turno.
- Reinyectar `tool_result` con rol `assistant` o sin `tool_use_id` → el modelo no correlaciona la respuesta y diverge.
- `try/except` que traga la excepción del handler y devuelve `""` → el modelo cree que la herramienta tuvo éxito vacío (failure mode peor que el crash).
- Budget como constante hardcodeada en el cuerpo del loop → no auditable, no testeable.

## Casos límite

- **Tool calls en paralelo**: una sola respuesta `tool_use` puede traer N bloques; recolecta los N resultados en UN mensaje `user`. [CÓDIGO]
- **Handler que falla**: deja propagar (o captura y devuelve `tool_result` con `is_error: true` *tipado*) — nunca silencies. La política la decides explícitamente, no por omisión. [INFERENCIA]
- **`stop_reason == "max_tokens"`**: la respuesta está truncada; trátalo como señal no-feliz (continuar pidiendo más, o `raise`), nunca como `end_turn`. [SUPUESTO — verificar contra el SDK del proveedor en uso]
- **Handler desconocido**: `handlers[block.name]` con `KeyError` es el fallo fuerte deseado; documenta que el catálogo de `tools` y el mapa `handlers` deben estar sincronizados. [CÓDIGO]
- **Orden de mensajes**: el `assistant` con `tool_use` debe quedar en el historial ANTES del `user` con `tool_result`; invertirlo rompe la conversación. [CÓDIGO]

## Gate de validación (criterios de aceptación)

El loop está listo solo si TODO lo siguiente es cierto:

- [ ] El control vive en `stop_reason` (señal tipada), no en el texto del modelo. [CÓDIGO]
- [ ] Cada señal posible tiene handler explícito; las no contempladas hacen `raise UnhandledStop`. [CÓDIGO]
- [ ] Se procesan TODOS los bloques `tool_use` de cada respuesta (paralelo cubierto). [CÓDIGO]
- [ ] Los `tool_result` se reinyectan como mensaje `user` con el `tool_use_id` correcto. [CÓDIGO]
- [ ] Existe budget configurable (`max_iterations` / tokens) que dispara `BudgetExceeded`. [CÓDIGO]
- [ ] Los fallos son fuertes y observables, no halts silenciosos. [CÓDIGO]
- [ ] Cada transición del loop queda instrumentada para auditoría. [CÓDIGO]

**Self-correction** — si al revisar encuentras `if ... in text`, un `while True` sin techo, un `except: pass` alrededor de un handler, o un `tool_result` fuera del rol `user`, detente y corrige antes de declarar la skill aplicada. [INFERENCIA]

## Paquete determinístico

> Estos artefactos son los entregables esperados del paquete; verifica su presencia con `ls` antes de invocarlos (pueden no existir aún en un checkout parcial). [SUPUESTO]

- Declara el contrato estructurado del loop en `assets/loop-contract.schema.json` y `assets/loop-policy.json` ANTES de escribir código.
- `scripts/compile-agentic-loop.py <contrato.json> --output <loop.py> --report <reporte.md>` convierte el contrato en un esqueleto Python verificable.
- `bash skills/agentic-loop-engineering/scripts/check.sh` antes de marcar la skill como lista.
- Rechaza contratos sin budget, con control por prosa, con `tool_result` fuera del rol `user`, o con señales desconocidas que no terminen en `UnhandledStop`. [DOC]

## Katas y skills relacionadas

- Kata fundacional: `katas-01`.
- Skills relacionadas: `katas-deterministic-agent-loop`, `tool-result-injection`, `agent-budget-control`. [DOC]
