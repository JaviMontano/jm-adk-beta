<!-- distilled from alfa skills/katas-deterministic-agent-loop -->
<!-- Control de bucle agentico por stop_reason tipado (tool_use vs end_turn), nunca por prosa del modelo; halt y budget deterministas. -->
# Katas Deterministic Agent Loop

## Qué es

Un bucle agéntico que decide continuar o detenerse mirando SOLO el campo estructurado `stop_reason` que devuelve la API (`tool_use` vs `end_turn`), nunca la prosa que escribe el modelo. Cada iteración llama a `create(...)`, inspecciona `stop_reason` y enruta: `tool_use` despacha la herramienta y reinyecta el `tool_result`; `end_turn` finaliza; cualquier otro valor (`max_tokens`, `pause_turn`, etc.) eleva un error explícito. Aplica a Customer Support y Multi-Agent Research, donde el control del turno debe ser predecible. [DOC]

**Alcance.** Define el contrato de control del bucle. NO cubre: selección/diseño de herramientas, política de reintentos de red, persistencia de historial, ni rate-limiting — esos son katas vecinos. [DOC]

## Por qué importa (falla que evita)

Detener el bucle por heurística de texto convierte una frase casual ("task complete", "listo") en un halt silencioso a destiempo o, peor, en un bucle infinito cuando el modelo nunca pronuncia la frase esperada. El parseo de prosa es no determinista por construcción: depende del idioma, del tono y de la redacción del modelo. El control debe vivir en el contrato estructurado de la API, no en la superficie textual. [INFERENCIA]

## Modelo mental

- Cada iteración produce un `stop_reason`: `tool_use` → dispatch, `end_turn` → halt, otros → error explícito. [CÓDIGO]
- El `tool_result` se reinyecta como `role=user`, manteniendo el contrato turn-by-turn de la conversación. [CÓDIGO]
- `max_tokens` / `pause_turn` inesperados deben fallar fuerte (raise), nunca silenciosamente. [DOC]
- El bucle se acota con un budget configurable (`max_iterations`) que eleva `BudgetExceeded` al excederse. [CÓDIGO]
- La prosa del modelo es output para el humano, no señal de control para la máquina. [INFERENCIA]

## Patrón correcto

```python
while True:
    resp = create(...)
    if resp.stop_reason == "tool_use":
        dispatch(resp)
        continue
    elif resp.stop_reason == "end_turn":
        return resp
    else:
        raise UnhandledStop(resp.stop_reason)
```

El `else` exhaustivo es deliberado: un `stop_reason` nuevo introducido por la API (p.ej. `pause_turn`) debe romper ruidosamente, no caer en una rama de halt asumida. Trade-off: prefiere fallo visible sobre continuidad silenciosa; el costo es que valores legítimos nuevos exigen una decisión explícita de manejo. [INFERENCIA]

## Anti-patrón

```python
DONE = ["task complete", "done", "listo"]
if any(p in text for p in DONE):
    return  # parsea prosa: halt silencioso o bucle infinito
```

## Bucle acotado (budget)

```python
for i in range(max_iterations):
    resp = create(...)
    if resp.stop_reason == "tool_use":
        dispatch(resp); continue
    if resp.stop_reason == "end_turn":
        return resp
    raise UnhandledStop(resp.stop_reason)
raise BudgetExceeded(max_iterations)  # nunca caer fuera del for en silencio
```

El budget es obligatorio, no opcional: sin él, un modelo que pide herramientas en bucle (o un `tool_result` que reabre la pregunta) nunca termina. `BudgetExceeded` debe ser distinguible de `UnhandledStop` para que el operador sepa si fue tope de iteraciones o `stop_reason` desconocido. [INFERENCIA]

## Casos límite y fallas

- **`pause_turn` (server-side tools / long-running):** no es halt ni tool_use; la rama `else` lo eleva. Si se decide soportarlo, es continuación (reinyectar y seguir), nunca fin. [SUPUESTO] Verificar: contrastar con la respuesta real de la API antes de tratarlo como halt.
- **`max_tokens`:** la respuesta está truncada; reanudar o abortar es decisión del llamador, jamás un halt limpio implícito. [DOC]
- **`tool_use` con varios bloques:** despachar TODOS y devolver un `tool_result` por `tool_use_id`; omitir uno deja el turno mal formado. [CÓDIGO]
- **Herramienta que lanza excepción:** capturar y devolver `tool_result` con `is_error=true`; no abortar el bucle — el modelo puede recuperarse. [SUPUESTO] Verificar contra la kata de error-propagation.
- **`max_iterations=0` o negativo:** el `for` no entra y cae directo a `BudgetExceeded`; tratar como error de configuración, no como ejecución vacía válida. [INFERENCIA]

## Argumento de certificación

El control del bucle vive en `stop_reason` + budget + handlers tipados, no en heurísticas de texto. Una implementación certificada (1) enruta exclusivamente por `stop_reason`, (2) trata todo valor no manejado como error explícito, y (3) acota la ejecución con un budget configurable que eleva `BudgetExceeded`. [DOC]

## Criterios de aceptación

- Cero ramas de halt/continuación que dependan del contenido textual de la respuesta. [DOC]
- Toda rama de `stop_reason` es explícita; el default es `raise`, no `return`. [DOC]
- Existe `max_iterations` y agotarlo eleva `BudgetExceeded` (distinto de `UnhandledStop`). [CÓDIGO]
- Cada `tool_use` produce exactamente un `tool_result` por `tool_use_id`, reinyectado como `role=user`. [CÓDIGO]
- Errores de herramienta viajan como `tool_result is_error`, sin abortar el bucle. [SUPUESTO]

## Cuándo activar

- Diseñar o revisar un bucle agéntico que llama a la API en iteraciones.
- Detectar control de flujo basado en parseo de texto ("done", "task complete").
- Definir condiciones de halt, manejo de `tool_use`/`end_turn` o límites de iteración.
- Triggers: `deterministic loop`, `stop_reason`, `agent loop control`, `budget exceeded`.

## Skills relacionadas

- `katas-pretooluse-guardrails`
- `katas-error-propagation-multi-agent`
- `katas-human-handoff-protocol`
