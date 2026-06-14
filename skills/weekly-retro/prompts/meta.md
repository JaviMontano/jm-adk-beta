# Prompt — weekly-retro (meta / self-check)

Meta-prompt para auto-evaluar una retro semanal antes de declararla hecha.
Recorre estos triggers de auto-correccion y corrige en sitio.

## Self-correction triggers
- **Escribiste una regla pero no mostraste el diff destino** → vuelve a Execute;
  ninguna escritura a memoria sin diff + confirmacion. {INFERENCIA}
- **Item de Friccion sin fuente citable** → degradalo a observacion o marcalo
  `{POR_CONFIRMAR}` con su paso de verificacion. {DOC}
- **Friccion vista una sola vez ascendida a regla** → revierte a observacion; el
  umbral es >=2 ocurrencias (anti inflacion de reglas). {INFERENCIA}
- **La retro no produjo ni accion ni regla** → revisa: ¿faltó leer una fuente?
  ¿la ventana era correcta?
- **Regla candidata contradice una regla en memoria** → no sobrescribas; expon
  el conflicto y pide al operador resolver. {SUPUESTO}
- **Eje vacio sin justificar** → registra "sin patron nuevo" o relee la semana;
  el vacio real es legitimo, el vacio por pereza no.

## Auto-check de tags
- ¿Cada afirmacion no obvia tiene exactamente un tag `{...}`?
- ¿Hay algun `[...]` colado? → falla familia unica, corrige.
- ¿Algun `{WEB}` sin cita? → degrada a `{POR_CONFIRMAR}` o elimina.

## Auto-check de upgrade_safety
- ¿Toda promocion mostró diff y esperó confirmacion explicita?
- ¿La escritura fue append (historico y ediciones locales intactos)?
- ¿`--force` evitado? ¿Un solo workspace (marca unica)?

Si todo pasa, entrega al guardian. Si algo falla, no marques completo.
