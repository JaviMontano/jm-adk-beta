# Meta-prompt — self-correction-loops

Guia de seleccion y auto-chequeo antes de invocar el skill.

## Cuando enrutar a este skill

Activa SOLO si se cumplen ambas:
- Hay un agregado numerico (total, subtotal, balance, conteo) en el input.
- Existen los componentes crudos para recomputarlo de forma independiente.

## Cuando NO enrutar (desambiguacion)

- "Valida que el JSON parsee / el campo exista / el tipo sea correcto" ->
  `validation-retry-design` (formato, no numerico).
- "A donde mando el mismatch / con que SLA" -> `human-escalation-design`.
- "De donde vino el dato declarado" -> `provenance-engineering`.
- "Arregla los numeros para que cuadren" -> RECHAZAR; es correccion silenciosa.
- Input vacio o tarea no numerica -> no activar.

## Auto-chequeo antes de entregar (self-correction)

- ¿El `computed` deriva del mismo agregado que `declared`? -> recomputa desde crudos.
- ¿Hay `mismatch=true` con el campo sobreescrito? -> revierte y escala.
- ¿Epsilon de moneda sobre enteros, o epsilon sin justificacion? -> ajusta a
  `epsilon-policy.json`.
- ¿El reporte oculta `declared` o `computed` en un mismatch? -> hazlos visibles.
- ¿Falta el caso estructural con mismatch inyectado? -> agregalo.

## Gobernanza

Voz harness; tags de evidencia obligatorios; sin precios; single-brand JM Labs;
sin PII de cliente. Verde no es exito por defecto: exige evidencia por invariante.
