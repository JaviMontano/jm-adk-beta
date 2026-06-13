# Prompt meta — structured-output-design

Meta-prompt para razonar sobre *cuándo* y *cómo de profundo* aplicar el contrato de
salida antes de ejecutarlo. Úsalo para calibrar scope, no para producir el schema.

## Preguntas de calibración

1. **¿Otro sistema consume esta salida por código?** Si la salida es prosa para humano
   (correo, resumen), NO impongas schema → `false_positive_boundary`. [INFERENCIA]
2. **¿El modelo debe elegir entre varias tools?** Si extraer factura *o* abrir ticket son
   ambas válidas, NO fuerces `tool_choice`; usa `auto` → `tool_choice_boundary`. [DOC]
3. **¿Me piden degradar el contrato?** Saltar validación, conservar defaults falsos,
   fallback de texto + regex → rechaza; la skill no degrada a texto. [SUPUESTO]
4. **¿Tengo el inventario de campos?** Sin garantizado-vs-ocasional no puedo decidir
   `required` con honestidad → pide el inventario.
5. **¿Profundidad?** `quick` → contrato mínimo defensivo (closed object, nullable, escape
   valve). `deep` → además casos límite (`max_tokens` truncado, enum saturado de `other`,
   consumidor NOT NULL) y fixtures positivas/negativas.

## Auto-crítica antes de entregar

- ¿Cada `required` tiene evidencia de presencia real, o lo marqué por deseo?
- ¿Eliminé todo default falso y lo reemplacé por unión nullable?
- ¿Todo enum cerrado tiene válvula de escape?
- ¿Forcé `tool_choice` solo cuando no había decisión de tool?
- ¿El parseo lee `tool_use.input` y existe el gate de validación con ruta a escalada?
- ¿No introduje ningún camino de fallback a texto libre?

## Disciplina de evidencia

Una familia de marca por output. Tags `[CÓDIGO] [CONFIG] [DOC] [INFERENCIA] [SUPUESTO]`.
Sin precios inventados, sin PII. Lee antes de escribir; no sobrescribas ediciones locales.
