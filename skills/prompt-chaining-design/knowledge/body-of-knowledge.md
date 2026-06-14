# Body of Knowledge — prompt-chaining-design

## Conceptos clave

### Unidad atómica
La pieza mínima que el pase local procesa de forma aislada: un archivo, un commit, un
ticket, un registro, un PR. Regla dura: **el pase local nunca ve más de una unidad por
invocación**. Si la unidad N necesita el crudo de la unidad M, no son atómicas y el
patrón map→reduce no aplica. [DOC]

### Pase local tipado (map)
Función idempotente y aislada `local_pass(unit) -> UnitSummary`. Procesa una unidad,
emite un resumen contra un schema, y **tipa el fallo como dato** (`status="error"`),
nunca lo lanza como excepción. Al ser sin estado compartido, es paralelizable. [DOC]

### Schema de transición
Contrato explícito de qué viaja entre el pase local y el pase de integración: una
**colección tipada de resúmenes** (`list[UnitSummary]`). Los datos crudos no viajan.
Sin este schema "no hay cadena, hay pegamento". [DOC]

### Pase de integración (reduce)
`integration_pass(summaries) -> Result`. Sintetiza, agrega o decide leyendo **solo**
los resúmenes. Separa `ok` de `error`, razona sobre los `ok` y reporta los `error` sin
abortar. Si necesita un crudo, el schema local está incompleto. [DOC]

### Error tipado vs excepción global
El error por unidad viaja en el schema (`status="error"`, `error_detail`) para que un
fallo aislado no tumbe el lote ni contamine la síntesis. La excepción global que aborta
todo está prohibida. [DOC]

## Estándares y reglas de decisión

### Single-pass gate
Antes de chainear, comprobar: ¿single-pass cabe holgado y razona mejor con el contexto
completo? Si sí → single-pass; el chaining añade overhead de schemas y orquestación que
debe justificarse. El chaining solo gana con **volumen alto**, **paralelismo real** o
**aislamiento de fallos**. [INFERENCIA]

### Regla del crudo en el pase 2
"El pase 2 necesita un crudo" no es permiso para pasar el crudo; es señal de que el
schema local está incompleto. Enriquecer el schema, no abrir un atajo. [DOC]

### Regla de completitud del schema
Todo campo del resumen debe ser consumido o reportado por el pase de integración. Lo
que no se usa ni se reporta no va en el schema. [INFERENCIA]

### Costo
Mega-prompt único: atención saturada y costo que crece de forma cuadrática con el
volumen concatenado. Cadena tipada: costo lineal por unidad + un reduce acotado sobre
resúmenes. [INFERENCIA]

## Checklist canónica (gates bloqueantes)

1. ¿El pase de integración nunca ve crudos, solo resúmenes?
2. ¿Cada pase tiene schema de salida explícito y tipado?
3. ¿El estado de error está tipado por unidad (no excepción global)?
4. ¿El pase local procesa una sola unidad y es paralelizable e idempotente?
5. ¿Existe un schema de transición explícito?
6. ¿Se justifica el chaining frente a single-pass?

Cualquier "no" es bloqueante. [DOC]

## Anti-scope

- Single-pass cabe holgado → no chainear.
- Unidades con dependencia oculta → map→reduce no aplica.
- Tarea no de lote (redactar un correo) → no activar.
- Exigir crudos en el pase 2 o saltarse schemas → Guardian bloquea.

## Taxonomía de evidencia

`[DOC]` documentado · `[CÓDIGO]` verificable en assets/scripts · `[CONFIG]`
frontmatter/manifest · `[INFERENCIA]` derivado del patrón · `[SUPUESTO]` pendiente de
confirmar.
