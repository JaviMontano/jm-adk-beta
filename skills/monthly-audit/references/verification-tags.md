# Verification tags — familia Jarvis OS `{...}`

monthly-audit es operador-facing y usa **una sola familia** de tags: la familia
Jarvis OS con llaves `{...}`. NUNCA se mezcla con la familia Alfa `[...]` en el
mismo documento. {DOC}

## Taxonomia

| Tag | Significado | Cuando en la auditoria |
|---|---|---|
| `{MEMORIA}` | Proviene de bitacora/MEMORY ya persistida | Contexto recuperado en frio, read-before-write del mes |
| `{EXTRAIDO_HILO}` | Tomado literal del hilo/sesion auditada | Evidencia citada de una entrada de bitacora o commit |
| `{INFERENCIA}` | Deduccion razonada, no literal | Priorizacion riesgo x impacto, clasificacion de un eje |
| `{SUPUESTO}` | Asuncion no confirmada | Eje sin evidencia disponible reconstruido de memoria |
| `{AUTOCOMPLETADO}` | Valor rellenado por defecto | Mes auditado = mes en curso cuando no es explicito |
| `{VACIO_CRITICO}` | Falta un input obligatorio; hay que preguntar | Mes o fuente de evidencia ausente: detente y pregunta |
| `{POR_CONFIRMAR}` | Pendiente de verificacion con paso definido | Score sin evidencia, riesgo sistemico abierto al mes siguiente |
| `{DOC}` | Respaldado por archivo/commit/doc verificable | Score que cuelga de evidencia citable |
| `{WEB}` | Respaldado por fuente web citada | Solo valido **con** cita; sin cita es invalido |

## Reglas de uso

1. **Exactamente un tag** por afirmacion no obvia. No apiles `{DOC}{INFERENCIA}`.
2. **Una familia por documento.** Jarvis `{...}` xor Alfa `[...]`. Mezclar = invalido.
3. **`{WEB}` sin cita es invalido** — degrada a `{POR_CONFIRMAR}` o elimina.
4. **No verde-como-exito.** Un eje no se puntua 3 sin evidencia ligada.
5. **`{SUPUESTO}`/`{POR_CONFIRMAR}` nunca se presentan como hecho** en el scorecard final.

## Mapeo a los checks del gate P22

- Score 0-3 sin `{DOC}` o `{EXTRAIDO_HILO}` con traza → falla "evidencia ligada".
- Primera corrida sin baseline → deltas n/a y scores `{POR_CONFIRMAR}`, no inventados.
- Riesgo sistemico abierto sin `{POR_CONFIRMAR}` + paso → falla "validacion".
- Cualquier `[...]` en el doc → falla "sin mezclar familias".
