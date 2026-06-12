# Ejemplo — Output

## 1. Scope confirmado

Un único loop, un único agente (soporte). El bug de tono del prompt NO se toca
(fuera de scope). [INFERENCIA]

## 2. Diagnóstico del loop actual

- `if "listo" in text` → control por prosa: el modelo dice "todavía no estoy
  listo" y el `in` hace match, sale antes de tiempo. RECHAZADO. [CÓDIGO]
- `resp.content[0]` → solo se despacha el primer `tool_use`; `leer_kb` se pierde y
  deja un `tool_result` huérfano que rompe el siguiente turno. [CÓDIGO]
- `while`/`break` sin techo → bucle infinito posible. [CÓDIGO]

## 3. Contrato declarado

- `assets/loop-contract.schema.json`: señales {end_turn, tool_use}, budget por
  iteraciones, `tool_result` obligatorio en rol `user` con `tool_use_id`.
- `assets/loop-policy.json`: `max_iterations = 12`, handler fallido → propagar.

## 4. Loop corregido

```python
class UnhandledStop(Exception): ...
class BudgetExceeded(Exception): ...

def run_support_loop(client, messages, tools, handlers, max_iterations=12):
    for iteration in range(max_iterations):
        resp = client.messages.create(model=MODEL, messages=messages, tools=tools)
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "end_turn":
            return resp                                   # halt limpio [CÓDIGO]

        if resp.stop_reason == "tool_use":
            results = []
            for block in resp.content:                    # TODOS los bloques
                if block.type == "tool_use":
                    handler = handlers[block.name]        # KeyError = fallo fuerte
                    out = handler(**block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": out,
                    })
            messages.append({"role": "user", "content": results})  # rol user
            log(iteration, resp.stop_reason, [b.name for b in resp.content
                if b.type == "tool_use"])                 # instrumentación
            continue

        raise UnhandledStop(resp.stop_reason)             # max_tokens / refusal / etc.
    raise BudgetExceeded(max_iterations)                  # techo duro
```

## 5. Gate de aceptación

- [x] Control en `stop_reason`, no en texto. [CÓDIGO]
- [x] Señales no contempladas → `UnhandledStop`. [CÓDIGO]
- [x] `buscar_ticket` y `leer_kb` despachados en la misma iteración. [CÓDIGO]
- [x] `tool_result` en mensaje `user` con `tool_use_id`. [CÓDIGO]
- [x] `max_iterations=12` dispara `BudgetExceeded`. [CONFIG]
- [x] Fallos fuertes y observables. [CÓDIGO]
- [x] `log(...)` por iteración para auditoría. [CÓDIGO]

## 6. Supuesto a verificar

- `max_tokens`, `pause_turn`, `refusal`: confirmar nombres exactos contra la
  versión del SDK de Anthropic en uso antes de añadirles ramas dedicadas.
  [SUPUESTO — verificar contra el SDK]
