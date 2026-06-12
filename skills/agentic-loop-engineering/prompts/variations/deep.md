# Variación profunda — agentic-loop-engineering

Para un loop de producción: tool calls en paralelo, política de handler fallido
explícita, budget que podría migrar a tokens, y auditoría completa.

```
Diseña el loop de control de producción de mi agente:

1. CONTRATO PRIMERO
   - assets/loop-contract.schema.json + assets/loop-policy.json antes del código.
   - Rechaza el contrato si: no hay budget, control por prosa, tool_result fuera
     de rol user, o señal desconocida sin UnhandledStop.

2. MÁQUINA DE ESTADOS
   - Taxonomía completa de stop_reason (end_turn / tool_use / max_tokens /
     pause_turn / refusal / desconocida). Verifica cada señal contra {{sdk}} y
     marca [SUPUESTO] lo no confirmado.
   - tool_use: recolecta los N tool_result en UN mensaje user; mantén el orden
     assistant(tool_use) -> user(tool_result).

3. POLÍTICA DE FALLO
   - Decide explícitamente: propagar el error del handler o devolver tool_result
     con is_error: true tipado. Nunca except: pass.

4. BUDGET
   - for range(max_iterations) hoy; documenta cómo migrar a while True + tokens
     si el gasto pasa a medirse por tokens consumidos. [INFERENCIA]

5. AUDITORÍA
   - Traza por iteración + cómo se reconstruye el camino del loop tras el fallo.

Cierra recorriendo las 7 casillas del gate de aceptación con evidencia por casilla.
```

Salida: contrato + diseño + código + reporte de auditoría, todo con taxonomía de
evidencia. Single-brand, sin precios.
