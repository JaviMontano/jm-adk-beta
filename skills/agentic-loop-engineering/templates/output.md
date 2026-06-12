# Loop de control agéntico — <nombre del agente>

> Entregable de `agentic-loop-engineering`. Cada afirmación de control lleva tag
> de evidencia: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`.

## 1. Scope confirmado

- Agente: <nombre> · Un único loop, un único agente: Sí / No
- Fuera de scope detectado (prompt tuning / tool design / multi-agente): <…>

## 2. Inputs del loop

| Input | Valor / fuente | Evidencia |
|-------|----------------|-----------|
| `messages` inicial | <…> | [DOC] |
| `tools` (catálogo) | <…> | [DOC] |
| `handlers` `{nombre → callable}` | <…> | [CÓDIGO] |
| Budget (`max_iterations` / tokens) | <…> | [CONFIG] |
| Cliente del modelo / SDK | <…> | [DOC] |

## 3. Contrato declarado (antes del código)

- `assets/loop-contract.schema.json`: <resumen de campos>
- `assets/loop-policy.json`: budget=<…>, política de handler fallido=<propagar / is_error>

## 4. Máquina de estados (taxonomía de `stop_reason`)

| Señal | Acción | Evidencia |
|-------|--------|-----------|
| `end_turn` | return resp (halt limpio) | [CÓDIGO] |
| `tool_use` | despacha N bloques, reinyecta `user` + `tool_use_id` | [CÓDIGO] |
| `max_tokens` | truncado: continuar o `raise`, nunca `end_turn` | [SUPUESTO] |
| otra | `raise UnhandledStop(stop_reason)` | [CÓDIGO] |
| techo agotado | `raise BudgetExceeded(max_iterations)` | [CÓDIGO] |

## 5. Código del loop

```python
# Pega aquí el loop generado: for range(max_iterations), enrutado por
# stop_reason, tool_result en rol user con tool_use_id, fallos fuertes.
```

## 6. Instrumentación

- Campos por iteración: `(iteration, stop_reason, tool, latency)` — destino: <…> [CÓDIGO]

## 7. Gate de aceptación

- [ ] Control en `stop_reason`, no en texto. [CÓDIGO]
- [ ] Cada señal con handler explícito; no contempladas → `UnhandledStop`. [CÓDIGO]
- [ ] TODOS los bloques `tool_use` procesados (paralelo). [CÓDIGO]
- [ ] `tool_result` en mensaje `user` con `tool_use_id`. [CÓDIGO]
- [ ] Budget configurable que dispara `BudgetExceeded`. [CONFIG]
- [ ] Fallos fuertes y observables. [CÓDIGO]
- [ ] Cada transición instrumentada. [CÓDIGO]

## 8. Supuestos a verificar

- <señales del SDK marcadas [SUPUESTO] y cómo verificarlas>
