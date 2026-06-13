# Variacion quick — revisor-veracidad

Pase rapido para textos cortos (un parrafo, un mensaje, un commit). Misma taxonomia, menos ceremonia.

## Cuando

- El texto es breve y la audiencia es obvia.
- Solo necesitas marcar los claims de mayor riesgo y un cierre por cada uno.

## Pasos

1. ¿Hay texto? Si no -> `{VACIO_CRITICO}`, para.
2. Familia por audiencia (default: Jarvis OS si es para operador).
3. Tagea solo lo no obvio, tag mas debil.
4. `{WEB}` sin cita -> degrada o elimina.
5. Una linea de cierre por cada `{SUPUESTO}`/`{POR_CONFIRMAR}`.

## Salida minima

- Texto con tags inline.
- 1-3 pasos de cierre.
- Conteo por tag en una linea.

## No hagas

- No expandas a tabla completa si el texto no lo amerita.
- No reescribas el contenido.
- No mezcles familias.

Ejemplo: "El job corre cada noche y nunca falla" -> "El job corre cada noche `{POR_CONFIRMAR}` y nunca falla `{SUPUESTO}`." Cierre: revisar el cron y el log de fallos de los ultimos 30 dias.
