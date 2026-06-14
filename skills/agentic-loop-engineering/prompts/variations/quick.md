# Variación rápida — agentic-loop-engineering

Para un loop pequeño con pocos handlers y budget por iteraciones.

```
Construye el loop de control de mi agente:
- Enruta SOLO por stop_reason: end_turn -> return; tool_use -> despacha TODOS
  los bloques y reinyecta tool_result (rol user, con tool_use_id); otra señal ->
  raise UnhandledStop.
- for iteration in range(max_iterations); tras el loop raise BudgetExceeded.
- Sin "done" in text, sin while True sin techo, sin except: pass en handlers.
- Instrumenta (iteración, señal, herramienta, latencia).
Handlers: {{handlers}}. max_iterations={{n}}. SDK: {{sdk}}.
```

Salida esperada: el patrón correcto de `SKILL.md` adaptado, con tags de evidencia
y el checklist del gate marcado. Sin precios. Un solo agente.
