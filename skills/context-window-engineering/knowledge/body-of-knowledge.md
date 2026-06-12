# Body of Knowledge — context-window-engineering

Conocimiento de dominio para ensamblar la ventana de contexto de un agente con reuso de prefix cache y mitigación de dilución softmax. Toda afirmación lleva tag de evidencia.

## Conceptos clave

### Prefix / KV cache
El proveedor cachea las claves/valores (KV) del prefijo más largo que sea **byte-idéntico** desde el primer token. Reutilizar ese prefijo entre turnos evita recomputar atención sobre los mismos tokens, bajando latencia y costo. El factor de ahorro depende del proveedor y del tamaño del prefijo estable; el ~10x es referencial hasta medir el cache-hit rate real. [SUPUESTO]

### Estático-first / dinámico-last
El contexto se parte en (a) bloques **estáticos** que no cambian entre turnos (rol, herramientas, políticas, esquema, few-shot) y (b) bloques **dinámicos** que cambian cada turno (hora, contadores, último mensaje). Los estáticos van primero para formar el prefijo cacheable; los dinámicos van al final para no invalidarlo. [DOC]

### Invalidación del cache
Cualquier byte distinto dentro del prefijo (un timestamp, un `request_id`, whitespace reordenado, un orden de bloques no determinista) corta el prefijo común y obliga a recomputar todo lo que sigue. Por eso ningún valor por-turno puede vivir en el prefijo. [DOC]

### Dilución softmax y curva en U
La distribución de atención (softmax) reparte peso entre todos los tokens; en contextos largos la atención efectiva es máxima en la **apertura** y el **cierre** y mínima en el **centro** ("lost in the middle"). Las instrucciones críticas enterradas en el centro se pierden. [DOC]

### Edge placement
Colocar las reglas irrenunciables en ambos bordes: al inicio (parte del prefijo) y reafirmadas al final (en el bloque `<reminder>`). La reafirmación gasta tokens pero cae **fuera** del prefijo cacheable, así que no rompe el cache. [INFERENCIA]

### Compactación sobre umbral fijo
Al superar un porcentaje de ocupación (default >55%), se **resume** el historial intermedio preservando intactos los bordes. Distinto de truncar, que es barato pero descarta el centro sin señal. La compactación nunca recorta ni reordena los bordes. [CONFIG]

## Estándares y reglas de decisión

| Decisión | Regla | Evidencia |
|---|---|---|
| Orden de bloques | Estático-first, dinámico-last, byte-idéntico entre turnos | [DOC] |
| Valor por-turno | Solo en el bloque `<reminder>` final, jamás en el prefijo | [DOC] |
| Regla crítica | En ambos bordes; solo las irrenunciables se reafirman | [INFERENCIA] |
| Umbral de compactación | Fijo (>55% default), no adaptativo salvo presión real | [CONFIG] |
| Compactar vs truncar | Compactar para preservar señal; truncar nunca toca bordes | [INFERENCIA] |
| Proveedor sin caching | Conserva estático-first por retención de bordes; no prometas ahorro | [SUPUESTO] |
| Tool definitions | En el prefijo solo si son estables en la sesión | [INFERENCIA] |
| Few-shot largos | En el prefijo estático, nunca intercalados con estado por-turno | [INFERENCIA] |

## Validación

Toda aplicación se cierra con dos mediciones obligatorias: **cache-hit rate** (¿el prefijo realmente se reutiliza?) y **prueba de retención** (¿la regla crítica sobrevive a un contexto largo?). Sin ambas, el gate no pasa. [DOC]

## Anti-scope

- Prompts de un solo turno sin reuso de prefijo: el caching no aporta. [INFERENCIA]
- Proveedores/SDKs sin prefix caching: la ganancia de costo es nula. [SUPUESTO]
- Mejorar la redacción del prompt: eso es prompt engineering, no ensamblado de ventana. [INFERENCIA]
