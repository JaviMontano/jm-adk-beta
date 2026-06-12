# Meta-prompt — context-window-engineering

Guía para enrutar, escalar y auto-corregir la skill. Úsalo antes de aplicar el prompt primario.

## Decisión de activación

Activa si el usuario construye/tunea un context assembler o system prompt, le importa latencia/costo con reuso de prefijo, reporta olvido de reglas en contextos largos, decide dónde poner estado por-turno, o fija política de compactación.

**No actives** (y dilo explícitamente) si:
- Es un prompt de un solo turno sin reuso de prefijo.
- El proveedor no soporta prefix caching (no inventes ahorro).
- El usuario pide solo mejorar la redacción (eso es prompt engineering).
- El usuario pide algo contradictorio con el dominio (p. ej. "pon el timestamp al inicio del prefijo y olvídate del cache") → señala el conflicto en vez de obedecer.

## Enrutamiento de roles

- **lead**: secuencia y contrato del ensamblado.
- **specialist**: byte-identidad, curva en U, trade-offs de compactación.
- **support**: implementación + paquete determinístico + mediciones.
- **guardian**: gate de aceptación, rechazo automático.

## Auto-corrección

| Síntoma | Hipótesis | Acción |
|---|---|---|
| Cache-hit bajo/inestable | Valor por-turno en el prefijo | `grep timestamp\|now\|request_id\|uuid\|counter` en el bloque estático |
| Regla crítica falla en contexto largo | No está en ambos bordes, o compactación los toca | Re-aplica edge placement; audita la compactación |
| Latencia no baja pese a estático-first | Proveedor sin caching o prefijo no byte-idéntico | Verifica soporte; normaliza orden/whitespace |

## Gobernanza

Voz de harness. Evidencia con tags. Sin precios inventados. Nunca trates "ejecutó sin error" como éxito: el verde exige cache-hit + retención medidos. Una sola marca/dominio por salida.
