# Verification tags — familia Jarvis OS `{...}`

daily-close es operador-facing y usa **una sola familia** de tags: la familia
Jarvis OS con llaves `{...}`. NUNCA se mezcla con la familia Alfa `[...]` en el
mismo documento. {DOC}

## Taxonomia

| Tag | Significado | Cuando |
|---|---|---|
| `{MEMORIA}` | Proviene de bitacora/MEMORY ya persistida | Read-before-write, contexto recuperado |
| `{EXTRAIDO_HILO}` | Tomado literal del hilo/sesion del dia | Items Cerrado/Pendiente con traza directa |
| `{INFERENCIA}` | Deduccion razonada, no literal | Clasificacion o priorizacion derivada |
| `{SUPUESTO}` | Asuncion no confirmada | Reconstruccion de memoria, default operativo |
| `{AUTOCOMPLETADO}` | Valor rellenado por defecto | Fecha = hoy cuando no es explicita |
| `{VACIO_CRITICO}` | Falta un input obligatorio; hay que preguntar | Fecha o fuente ausente |
| `{POR_CONFIRMAR}` | Pendiente de verificacion con paso definido | Bloqueos abiertos que cruzan al manana |
| `{DOC}` | Respaldado por archivo/commit/doc verificable | Evidencia de un item Cerrado |
| `{WEB}` | Respaldado por fuente web citada | Solo valido **con** cita; sin cita es invalido |

## Reglas de uso

1. **Exactamente un tag** por afirmacion no obvia. No apiles `{DOC}{INFERENCIA}`.
2. **Una familia por documento.** Jarvis `{...}` xor Alfa `[...]`. Mezclar = invalido.
3. **`{WEB}` sin cita es invalido** — degrada a `{POR_CONFIRMAR}` o elimina.
4. **No verde-como-exito.** Un cierre no se declara "ok" sin evidencia ligada.
5. **`{SUPUESTO}`/`{POR_CONFIRMAR}` nunca se presentan como hecho** en el bloque final.

## Mapeo a checks del gate

- Item Cerrado sin `{DOC}` o `{EXTRAIDO_HILO}` con traza → falla "evidencia ligada".
- Bloqueo sin `{POR_CONFIRMAR}` + paso → falla "bloqueos marcados".
- Cualquier `[...]` en el doc → falla "sin mezclar familias".
