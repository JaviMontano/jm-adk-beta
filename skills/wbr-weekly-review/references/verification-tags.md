# Verification tags — familia Jarvis OS `{...}`

wbr-weekly-review es operador-facing y usa **una sola familia** de tags: la familia
Jarvis OS con llaves `{...}`. NUNCA se mezcla con la familia Alfa `[...]` en el
mismo documento. {DOC}

## Taxonomia

| Tag | Significado | Cuando en un WBR |
|---|---|---|
| `{CONOCIMIENTO}` | Conocimiento de dominio estable de la cadencia | Definicion del ritual, lentes, reglas |
| `{MEMORIA}` | Proviene de WBR previo / bitacora persistida | Arrastres, compromisos de la semana anterior |
| `{ADJUNTO}` | Respaldado por artefacto verificable | Avance ligado a commit, entregable, decision |
| `{INFERENCIA}` | Deduccion razonada, no literal | Causa raiz, clasificacion de lente |
| `{SUPUESTO}` | Asuncion no confirmada | Semana de vacaciones, reconstruccion |
| `{AUTOCOMPLETADO}` | Valor rellenado por defecto | Fecha de corte = hoy cuando no es explicita |
| `{VACIO_CRITICO}` | Falta input obligatorio; hay que preguntar | Periodo o alcance ausente |
| `{POR_CONFIRMAR}` | Pendiente de verificacion con paso definido | Arrastre ≥3 semanas escalado a bloqueo |
| `{DOC}` | Respaldado por archivo/commit/doc verificable | Evidencia de un avance cerrado |
| `{WEB}` | Respaldado por fuente web citada | Solo valido **con** cita; sin cita es invalido |

## Reglas de uso

1. **Exactamente un tag** por afirmacion no obvia. No apiles `{DOC}{INFERENCIA}`.
2. **Una familia por documento.** Jarvis `{...}` xor Alfa `[...]`. Mezclar = invalido.
3. **`{WEB}` sin cita es invalido** — degrada a `{POR_CONFIRMAR}` o elimina.
4. **No verde-como-exito.** Un avance no se declara cerrado sin evidencia ligada.
5. **`{SUPUESTO}`/`{POR_CONFIRMAR}` nunca se presentan como hecho** en compromisos.

## Mapeo a checks del gate

- Avance sin `{DOC}` o `{ADJUNTO}` con traza → falla "evidencia ligada".
- Estancado sin dueno + proximo paso fechado → falla "estancado accionable".
- Arrastre ≥3 semanas sin `{POR_CONFIRMAR}` + escalada → falla "arrastre escalado".
- Cualquier `[...]` en el doc → falla "una sola familia de tags".
