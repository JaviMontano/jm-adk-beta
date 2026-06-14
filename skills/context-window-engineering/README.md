# context-window-engineering

Diseña el ensamblado de la ventana de contexto de un agente para (1) maximizar el reuso de prefix/KV cache organizando el contexto **estático-first / dinámico-last**, y (2) mitigar la dilución softmax con **edge placement** (curva en U) y **compactación** sobre un umbral fijo que nunca toca los bordes.

## Qué hace

Toma la estructura actual del contexto de un agente (bloques y su orden, señal de qué cambia por-turno, capacidad de cache del proveedor, límite de ventana) y produce un ensamblado verificable: orden estático-first, ubicación del estado volátil en un bloque `<reminder>` final, reglas críticas en ambos bordes, un umbral de compactación explícito, y un plan de medición de cache-hit y retención.

## Cuándo usarla

- Construyes o tuneas un system prompt / context assembler de producción.
- El costo o la latencia importan y quieres habilitar prefix caching real.
- El modelo "olvida" reglas críticas en conversaciones largas (síntoma de dilución).
- Inyectas estado por-turno (timestamps, contadores, recordatorios) y decides dónde colocarlo.
- Fijas una política de compactación / truncado para sesiones largas.

No la uses para prompts de un solo turno sin reuso de prefijo, proveedores sin prefix caching (la ganancia es nula), ni para mejorar la redacción del prompt (eso es prompt engineering).

## Cómo enruta y ejecuta

1. **lead** orquesta el flujo: particiona estático/dinámico, fija el orden y delega medición.
2. **specialist** aporta profundidad de dominio (KV cache, curva en U, byte-identidad del prefijo).
3. **support** ejecuta el ensamblado y corre el paquete determinístico (`compile-context-window.py`, `check.sh`).
4. **guardian** aplica el gate de aceptación de SKILL.md y rechaza cualquier violación de bordes/prefijo.

## Paquete determinístico y assets

El ensamblado se declara ANTES de escribir prompts vía `assets/context-assembly-schema.json` y `assets/context-policy.json`, y se compila/valida con los scripts del paquete determinístico. Ver `assets/README.md` y `assets/manifest.json` para el bundle completo.

## Referencias

- `SKILL.md` — capacidad, cómo construir, gate de validación, paquete determinístico.
- `knowledge/body-of-knowledge.md` — conceptos, estándares y reglas de decisión del dominio.
- `knowledge/knowledge-graph.json` — grafo de conceptos clave.
- `prompts/` — prompt primario, meta-prompt y variaciones quick/deep.
- `templates/output.md` — scaffold del entregable (plan de ensamblado de contexto).
- `examples/` — ejemplo trabajado de entrada y salida.
- `evals/evals.json` — casos de evaluación de activación y checks.

## Convención de evidencia

Toda afirmación lleva tag: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Nunca se promete un factor de ahorro sin medir el cache-hit rate real del proveedor.
