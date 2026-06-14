# Body of Knowledge — weekly-retro (P12)

Dominio: cadencia personal de retro semanal del operador Jarvis OS. Convierte la
experiencia de la semana en mejoras accionables y, condicionalmente, en reglas
persistentes. Este archivo fija los conceptos, estandares y reglas de decision
que el flujo aplica. {DOC}

## Conceptos clave

- **P12 (promocion de aprendizaje).** El mecanismo central: una friccion o un
  acierto recurrente "asciende" a una regla persistente que cambia el default de
  trabajo. La retro es el ritual donde se evalua esa promocion. {DOC}
- **Tres ejes.** Toda retro produce: **Ayudo** (que aceleró), **Friccion** (que
  costó tiempo/retrabajo), **Regla candidata** (que se vuelve default). Los tres
  siempre presentes; un eje vacio requiere justificacion explicita. {DOC}
- **Ventana.** El rango temporal revisado (default: ultimos 7 dias). Acota la
  evidencia: lo de fuera de la ventana no entra sin marcarse. {AUTOCOMPLETADO}
- **Observacion vs regla.** Una friccion vista una vez es observacion (se
  registra, no asciende). Vista **>=2 veces** es candidata a regla. {INFERENCIA}
- **Memoria destino.** Archivo de reglas/MEMORY donde aterriza una promocion.
  Sin destino nombrado no hay promocion. {SUPUESTO}

## Estandares

- **Familia de tags Jarvis OS** (`references/verification-tags.md`): `{MEMORIA}`
  `{ADJUNTO}` `{EXTRAIDO_HILO}` `{WEB}` `{CONOCIMIENTO}` `{SUPUESTO}`
  `{INFERENCIA}` `{AUTOCOMPLETADO}` `{POR_CONFIRMAR}` `{VACIO_CRITICO}`. Una sola
  familia por documento; un tag por claim; ante duda, el mas debil. {DOC}
- **Read-before-write.** Leer fuentes y memoria destino antes de escribir.
- **upgrade_safety.** Toda escritura a memoria pasa por diff mostrado +
  confirmacion explicita; persistencia aditiva; nunca `--force` a ciegas. {CONFIG}
- **Marca unica.** Un solo workspace/marca por bloque; no fusionar bitacoras.

## Reglas de decision

1. **Umbral de promocion.** Asciende a regla solo friccion >=2 ocurrencias o un
   acierto que se quiera volver default. Si no, observacion.
2. **Forma de la regla.** Imperativo, una linea, accionable y verificable.
3. **Conflicto con regla existente.** No sobrescribir; exponer el conflicto y
   delegar al operador.
4. **Ambiguedad.** Item entre observacion y regla → observacion (la regla se
   gana con recurrencia). {INFERENCIA}
5. **Sin evidencia legible.** `{VACIO_CRITICO}`: detente y pide la fuente; no
   reconstruyas la semana de memoria. {DOC}

## Anti-patterns

- Promover en automatico sin confirmacion (rompe `upgrade_safety`). {CONFIG}
- Ascender ruido de una sola semana (inflacion de reglas). {INFERENCIA}
- Retro como prosa libre sin los tres ejes ni tags de evidencia. {DOC}
- Mezclar familias de tags (Jarvis vs Alfa) en el mismo bloque. {DOC}

## Limites

Cadencia personal de operador, no facilitacion de equipo. No reemplaza revision
experta en decisiones legales/medicas/financieras/seguridad de alto riesgo. {DOC}
