# Prompt — daily-close (meta / self-check)

Meta-prompt para auto-evaluar un cierre diario antes de declararlo hecho. Recorre
estos triggers de auto-correccion y corrige en sitio.

## Self-correction triggers
- **Item ambiguo** entre Cerrado y Pendiente → re-clasifica como Pendiente (el
  cierre se gana, no se asume). {INFERENCIA}
- **Eje Aprendido vacio** → relee la jornada por fricciones/decisiones antes de
  declararlo vacio; el vacio real es legitimo, el vacio por pereza no.
- **Semilla > 3 items** → re-prioriza a top 1-3 por impacto-en-arranque.
- **Fecha o fuente ausente** → `{VACIO_CRITICO}`, detente y pregunta.
- **Item Cerrado sin evidencia** → no es Cerrado; degrada a Pendiente o liga el
  artefacto con `{DOC}`/`{EXTRAIDO_HILO}`.
- **Semilla sin primer paso en frio** → escribe el paso concreto o no la cuentes
  como sembrada.

## Auto-check de tags
- ¿Cada afirmacion no obvia tiene exactamente un tag `{...}`? 
- ¿Hay algun `[...]` colado? → falla familia unica, corrige.
- ¿Algun `{WEB}` sin cita? → degrada a `{POR_CONFIRMAR}` o elimina.

## Auto-check de persistencia
- ¿El cierre es append y no sobrescribe historico?
- ¿El bloque esta fechado al dia real (no al de captura si es retroactivo)?
- ¿Se respeto el workspace activo (marca unica)?

Si todo pasa, entrega al guardian. Si algo falla, no marques completo.
