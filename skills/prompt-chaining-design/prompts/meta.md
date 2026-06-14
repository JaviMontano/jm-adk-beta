# Meta-prompt — prompt-chaining-design

Guía de razonamiento para auto-evaluar un diseño de cadena de pases antes de
entregarlo. Úsala como capa de metacognición sobre `prompts/primary.md`.

## Preguntas de calibración

1. **¿Esto es realmente un lote?** Si la tarea es puntual (un correo, una respuesta
   única), no actives la skill. Activación incorrecta es un fallo de gate.
2. **¿El chaining gana algo medible?** Nombra la ganancia: volumen que no cabe,
   paralelismo real, o aislamiento de fallos. Si no puedes nombrarla → single-pass.
3. **¿Las unidades son independientes?** Busca dependencias ocultas. Si la unidad N
   necesita el crudo de M, el patrón está mal elegido.

## Auto-crítica de schemas

- ¿Cada campo del resumen se consume o se reporta en el pase 2? Elimina lo que no.
- ¿El `status="error"` cubre todos los modos de fallo de una unidad?
- ¿El schema de transición es explícito, o lo estoy asumiendo implícito? (Implícito =
  pegamento, no cadena.)

## Trampas frecuentes (detéctalas en ti mismo)

- Pasar un crudo "solo esta vez" al pase 2 → señal de schema incompleto, no excepción.
- Un `try/except` que aborta el lote → conviértelo en `status="error"`.
- Granularidad de unidad mal elegida (demasiado fina infla overhead; demasiado gruesa
  satura atención).

## Evidencia

Cada veredicto de auto-evaluación lleva etiqueta: `[DOC]` `[CÓDIGO]` `[INFERENCIA]`
`[SUPUESTO]`. No declares un gate verde sin evidencia que lo respalde.
