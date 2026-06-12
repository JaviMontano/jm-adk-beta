# Body of Knowledge — agentic-loop-engineering

Conocimiento de dominio para construir el bucle de control de un agente que
enruta por `stop_reason` tipado, con budget duro y handlers explícitos.

## 1. Conceptos clave

- **Loop de control.** Máquina de estados que en cada iteración llama al modelo,
  inspecciona la señal de parada y decide despachar / detener / fallar. Es la
  columna vertebral del agente. [DOC]
- **`stop_reason` (señal tipada).** Campo estructurado de la respuesta del modelo
  que indica por qué se detuvo. Único origen de verdad para el control. [CÓDIGO]
- **Handler.** Callable asociado a un nombre de herramienta: `handlers[name]`. El
  catálogo de `tools` y el mapa `handlers` deben estar sincronizados. [CÓDIGO]
- **Budget duro.** Techo de iteraciones (o tokens) que detiene el agente con una
  excepción tipada, no con un return ambiguo. [CONFIG]
- **Fallo fuerte.** Toda señal no contemplada produce `raise`, nunca un halt
  silencioso. `KeyError` en `handlers[name]` es fallo fuerte deseado. [CÓDIGO]

## 2. Taxonomía de `stop_reason`

| Señal | Significado | Acción del loop |
|-------|-------------|-----------------|
| `end_turn` | el modelo terminó | halt limpio: `return resp` |
| `tool_use` | pide ejecutar herramientas | despacha N bloques, reinyecta `tool_result` |
| `max_tokens` | respuesta truncada | NO feliz: continuar o `raise`, nunca `end_turn` |
| `pause_turn` | pausa de ejecución larga | no contemplada por defecto → `UnhandledStop` |
| `refusal` | rechazo del modelo | no contemplada por defecto → `UnhandledStop` |
| desconocida | señal nueva del SDK | `raise UnhandledStop(stop_reason)` |

> La existencia y el nombre exacto de cada señal dependen de la versión del SDK
> del proveedor. Verificar siempre contra el SDK en uso. [SUPUESTO]

## 3. Contrato de mensajes

1. Tras llamar al modelo, append del `assistant` con `resp.content`. [CÓDIGO]
2. Si `tool_use`: por CADA bloque `tool_use`, construir
   `{type:"tool_result", tool_use_id: block.id, content: result}`. [CÓDIGO]
3. Recolectar TODOS los `tool_result` en UN mensaje con rol `user`. [CÓDIGO]
4. Orden invariante: `assistant`(tool_use) ANTES de `user`(tool_result). [CÓDIGO]
5. `tool_result` con rol `assistant` o sin `tool_use_id` rompe la correlación. [CÓDIGO]

## 4. Reglas de decisión

- Control SOLO por `stop_reason`, nunca por `"done" in text`. [CÓDIGO]
- `for iteration in range(max_iterations)` → budget estructural (imposible
  olvidar incrementar; techo duro = línea tras el loop). [INFERENCIA]
- Migrar a `while True` + chequeo de tokens solo si el budget pasa a ser por
  tokens consumidos. [INFERENCIA]
- Política de handler fallido decidida explícitamente: propagar o `tool_result`
  con `is_error: true` tipado. Nunca `except: pass`. [INFERENCIA]

## 5. Modos de fallo (anti-patrones a vetar)

- Control por prosa (`if "done" in text`): el modelo dice "not done" y sale. [CÓDIGO]
- `while True` sin techo: bucle infinito si la condición de salida nunca aparece. [CÓDIGO]
- Procesar solo `resp.content[0]`: tool calls en paralelo perdidos, `tool_result`
  huérfanos que rompen el siguiente turno. [INFERENCIA]
- `except: pass` / `return ""` alrededor del handler: éxito vacío fantasma, peor
  que el crash. [INFERENCIA]
- Budget hardcodeado en el cuerpo: no auditable, no testeable. [INFERENCIA]

## 6. Estándares y gate

El loop está listo solo si los 7 criterios de aceptación de `SKILL.md` se cumplen
con evidencia. Self-correction obligatoria: si aparece `if ... in text`,
`while True` sin techo, `except: pass` en un handler, o `tool_result` fuera del
rol `user` → detener y corregir antes de declarar la skill aplicada. [INFERENCIA]

## 7. Taxonomía de evidencia

`[CÓDIGO]` control/loop verificable · `[CONFIG]` budget/policy · `[DOC]` contrato
· `[INFERENCIA]` decisión derivada · `[SUPUESTO]` señal del SDK por verificar.
