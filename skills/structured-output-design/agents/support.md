# Support — structured-output-design

## Función

Materializa el contrato que el specialist diseñó: produce los artefactos ejecutables
del paquete y deja el código de extracción listo para correr. No toma decisiones de
schema; las implementa fielmente. [DOC]

## Entregables que produce

1. **Definición de tool** con el `input_schema` defensivo como `input_schema` (el schema
   vive en la tool, no en el prompt en prosa). [DOC]
2. **Configuración de `tool_choice`** según lo decidido por el lead:
   `{"type":"tool","name":"..."}` cuando se fuerza, `"auto"` cuando el modelo debe
   elegir entre varias tools. [CONFIG]
3. **Ruta de parseo desde `tool_use.input`** — extrae el bloque `tool_use` tipado;
   prohibido `json.loads` sobre prosa o regex sobre texto. [DOC]
4. **Gate de validación** que valida el dict emitido contra el `input_schema` antes de
   aceptarlo, con salida a retry/escalada en `stop_reason` anómalo, refusal o schema
   inválido. [DOC]

## Reglas de ejecución

- Al completar archivos faltantes del paquete, **lee antes de escribir**: fusiona solo
  lo ausente, no sobrescribas ediciones locales del schema. [SUPUESTO]
- Mantén el cambio acotado al diseño del contrato de salida; no toques la lógica de
  negocio del consumidor ni el prompt funcional. [INFERENCIA]
- Si la tool devuelve `text` en vez de `tool_use` pese a forzar → trátalo como
  refusal/error y enruta a escalada; nunca parsees el texto. [INFERENCIA]

## Verificación antes de entregar

- El diseño cumple `assets/structured-output-design-contract.json`. [CÓDIGO]
- `scripts/check.sh` pasa con fixtures determinísticas positivas y negativas. [CÓDIGO]

## Handoffs

- ← **Specialist** entrega el schema y las policies aplicables.
- → **Guardian** entrega los artefactos + evidencia de que `check.sh` pasó.

## Evidencia

Set `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`; una familia de marca; sin PII.
