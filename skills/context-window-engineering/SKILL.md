---
name: context-window-engineering
version: 1.1.0
description: "Disena el ensamblado de la ventana de contexto de un agente para maximizar reuso de prefix/KV cache (estatico-first) y mitigar dilucion softmax con edge placement (curva en U) y compactacion sobre umbral fijo."
owner: "JM Labs"
triggers:
  - context window engineering
  - prefix cache optimization
  - context dilution
  - edge placement
  - kv cache reuse
  - system prompt assembly
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Context Window Engineering

## Capacidad

Ingeniería para diseñar el ensamblado de la ventana de contexto de un agente de modo que (1) maximice el reuso de prefix cache (KV cache) y (2) minimice la pérdida de instrucciones por dilución softmax. Se logra organizando el contexto **estático-first / dinámico-last** —el prefijo estable se cachea y se reutiliza con factores cercanos a ~10x [SUPUESTO: verifica el factor real midiendo cache-hit rate en tu proveedor]— y colocando lo que el modelo no puede olvidar en los **bordes** del contexto (apertura y cierre), donde la atención es más alta (curva en U). Al acercarse al límite, se **compacta** por encima de un umbral fijo para preservar las instrucciones de borde. [DOC]

## Cuándo usarla

- Construyes o tuneas un system prompt / context assembler de un agente de producción. [DOC]
- El costo o la latencia de inferencia importan y quieres habilitar prefix caching real. [DOC]
- El modelo "olvida" reglas críticas en conversaciones largas (síntoma de dilución). [DOC]
- Inyectas estado por-turno (timestamps, contadores, recordatorios) y debes decidir dónde colocarlo. [DOC]
- Vas a fijar una política de compactación / truncado para sesiones largas. [DOC]

**Cuándo NO usarla (anti-scope).** Prompts de un solo turno sin reuso de prefijo (el caching no aporta); proveedores/SDKs sin prefix caching (la ganancia es nula, no inventes una); recortar el contenido del prompt por calidad de redacción —eso es prompt engineering, no ensamblado de ventana. [INFERENCIA]

## Inputs / Outputs

- **Inputs:** estructura actual del contexto (bloques y su orden), señal de qué cambia por-turno, capacidad de cache del proveedor, límite de ventana objetivo. [DOC]
- **Outputs:** orden de bloques estático-first; ubicación del estado volátil; ubicación y reafirmación de reglas críticas; umbral de compactación explícito; plan de medición de cache-hit y retención. [DOC]

## Cómo construir

1. **Particiona estático vs dinámico.** Separa bloques que no cambian entre turnos (rol, herramientas, políticas, esquema) de los que cambian cada turno (hora, estado, último mensaje). [DOC]
2. **Ordena estático-first.** El bloque estático va al inicio, byte-idéntico entre turnos, para que el prefijo sea cacheable. NUNCA pongas un valor por-turno (timestamp, request-id) en el prefijo: invalida el cache completo. [DOC]
3. **Empuja lo dinámico al final.** Renderiza el estado volátil en un bloque `<reminder>` al cierre, después del prefijo estable. [DOC]
4. **Coloca reglas críticas en los bordes.** Las instrucciones que el modelo no debe olvidar van al inicio (parte del prefijo) y se reafirman al final (en el `<reminder>`), nunca enterradas en el centro de un bloque largo. [DOC]
5. **Fija un umbral de compactación.** Define un porcentaje de ocupación explícito a partir del cual se compacta/resume el historial intermedio, preservando intactos los bordes. El default de referencia es **>55%** [SUPUESTO: calíbralo a tu ventana y tasa de crecimiento del historial]. [CONFIG]
6. **Valida cache y retención.** Mide el cache-hit rate y verifica con una prueba de retención que la regla crítica sobrevive a un contexto largo. [DOC]

## Decisiones y trade-offs

- **Umbral fijo vs adaptativo.** Fijo (>55%) es reproducible y testeable; adaptativo recupera más ventana pero introduce no-determinismo difícil de validar. Elige fijo salvo evidencia de presión real de ventana. [INFERENCIA]
- **Compactar vs truncar.** Compactar (resumir) preserva señal a costa de cómputo; truncar es barato pero pierde contexto medio de forma silenciosa. Nunca truques los bordes en ninguno de los dos. [INFERENCIA]
- **Reafirmar reglas (coste de tokens) vs riesgo de olvido.** Duplicar la regla crítica al cierre gasta tokens pero es el mecanismo barato contra la dilución; el coste cae fuera del prefijo cacheable, así que no rompe el cache. [INFERENCIA]

## Patrón correcto

```python
# GOOD: estatico-first (cacheable), dinamico-last, reglas criticas en bordes
def build_context(turn_state: TurnState, history: list[Message]) -> list[Block]:
    static_prefix = [
        Block("role", ROLE_AND_TOOLS),           # estable byte a byte -> cacheable
        Block("policies", CRITICAL_RULES),       # regla critica en el borde inicial
        Block("schema", OUTPUT_SCHEMA),
    ]
    compacted = compact_if_over(history, threshold=0.55)  # umbral fijo, no toca bordes
    dynamic_tail = [
        Block("reminder", render_reminder(
            now=turn_state.timestamp,             # volatil -> SOLO aqui, al final
            critical=CRITICAL_RULES_RESTATED,     # reafirma regla en borde final
        )),
    ]
    return static_prefix + compacted + dynamic_tail
```

## Anti-patrón

```python
# ANTI: timestamp al inicio invalida el cache; regla critica enterrada en el centro
def build_context(turn_state, history):
    return [
        Block("header", f"Current time: {turn_state.timestamp}"),  # rompe prefix cache
        Block("role", ROLE_AND_TOOLS),
        Block("history", history),                # regla critica queda sepultada aqui
        Block("rules", CRITICAL_RULES),           # zona de minima atencion (centro de la U)
    ]
    # Sin umbral de compactacion -> al crecer el historial, las reglas se diluyen.
```

## Casos borde

- **Tool definitions que cambian por sesión.** Pertenecen al prefijo solo si son estables en la sesión; si varían por-turno, trátalas como dinámicas o se invalida el cache. [INFERENCIA]
- **Few-shot examples largos.** Van en el prefijo estático (cacheable), nunca intercalados con estado por-turno. [INFERENCIA]
- **Una sola regla crítica vs muchas.** Si hay muchas, prioriza: solo las irrenunciables se reafirman al cierre; reafirmar todo rellena el borde y vuelve a diluir. [INFERENCIA]
- **Proveedor sin prefix caching.** El paso 2 no da ahorro de coste; conserva igual estático-first por la retención de bordes, pero no prometas ~10x. [SUPUESTO: confirma soporte de caching del proveedor]

## Gate de validación (criterios de aceptación)

Marca la skill como aplicada solo si TODO se cumple:

- [ ] El prefijo es estable byte a byte, sin ningún valor por-turno (timestamp, request-id, contador). [DOC]
- [ ] El estado dinámico vive en un bloque `<reminder>` al final del contexto. [DOC]
- [ ] Las reglas críticas están en los bordes (inicio + reafirmadas al final) y no en el centro. [DOC]
- [ ] Hay un umbral de compactación explícito y aplicado (>55% u otro valor justificado) que NO toca los bordes. [DOC]
- [ ] Se midió el cache-hit rate y se probó la retención de la regla crítica en contexto largo. [DOC]

## Auto-corrección (triggers de revisión)

- Cache-hit rate bajo o inestable → busca un valor por-turno filtrado al prefijo (`grep` de `timestamp|now|request_id|uuid|counter` dentro del bloque estático). [INFERENCIA]
- La regla crítica falla en contexto largo → no está en ambos bordes, o la compactación los está tocando. [INFERENCIA]
- La latencia no baja pese a estático-first → el proveedor no cachea, o el prefijo no es byte-idéntico (orden/whitespace cambian entre turnos). [INFERENCIA]

## Paquete determinístico

Declara el ensamblado ANTES de escribir prompts o adapters, y verifícalo con artefactos reproducibles:

- `assets/context-assembly-schema.json` y `assets/context-policy.json` para declarar el ensamblado. [SUPUESTO: crea estos assets; aún no están en el repo de la skill]
- `scripts/compile-context-window.py <contexto.json> --output <reporte.md>` genera un reporte de prefijo, zona compactable, cola dinámica, reglas críticas y validaciones. [SUPUESTO: script por crear]
- `bash skills/context-window-engineering/scripts/check.sh` antes de marcar la skill como lista. [SUPUESTO: script por crear]
- El compilador debe **rechazar**: timestamps en prefijo; reglas críticas solo en el centro; falta de compactación; dynamic tail que no sea final; y compactación que toque bordes. [DOC]

## Katas y skills relacionadas

- Katas: `katas-10`, `katas-11`. [CONFIG]
- Relacionadas: `katas-prefix-caching`, `katas-context-dilution-mitigation`. [CONFIG]
