# Verification tags — familia Jarvis OS `{...}`

qbr-quarterly es operador-facing y usa **una sola familia** de tags: la familia
Jarvis OS con llaves `{...}`. NUNCA se mezcla con la familia Alfa `[...]` en el
mismo documento. {DOC}

## Taxonomia

| Tag | Significado | Cuando en el QBR |
|---|---|---|
| `{MEMORIA}` | Proviene de bitacora/MEMORY ya persistida | Baseline de OKRs recuperado en frio del trimestre que cierra |
| `{EXTRAIDO_HILO}` | Tomado literal del hilo/sesion auditada | Metrica o entregable citado de un commit, log o entrada de bitacora |
| `{CONOCIMIENTO}` | Regla de dominio QBR estable | Definicion de estado, regla "sin metrica no es objetivo" |
| `{INFERENCIA}` | Deduccion razonada, no literal | Asignacion de estado parcial, priorizacion valor/esfuerzo, causa raiz |
| `{SUPUESTO}` | Asuncion no confirmada | Capacidad del proximo Q a valor nominal, constraint reconstruido |
| `{AUTOCOMPLETADO}` | Valor rellenado por defecto | Trimestre destino = Q calendario siguiente cuando no es explicito |
| `{VACIO_CRITICO}` | Falta un input obligatorio; hay que preguntar | Baseline de OKRs ausente: detente y pide los originales |
| `{POR_CONFIRMAR}` | Pendiente de verificacion con paso definido | Meta sin metrica medible, conflicto entre fuentes, riesgo cross-quarter |
| `{DOC}` | Respaldado por archivo/commit/doc verificable | Estado de meta que cuelga de evidencia citable |
| `{WEB}` | Respaldado por fuente web citada | Solo valido **con** cita; sin cita es invalido |

## Reglas de uso

1. **Exactamente un tag** por afirmacion no obvia. No apiles `{DOC}{INFERENCIA}`.
2. **Una familia por documento.** Jarvis `{...}` xor Alfa `[...]`. Mezclar = invalido.
3. **`{WEB}` sin cita es invalido** — degrada a `{POR_CONFIRMAR}` o elimina.
4. **No verde-como-exito.** Una meta no se declara "logrado" sin metrica observada ligada.
5. **`{SUPUESTO}`/`{POR_CONFIRMAR}` nunca se presentan como hecho** en el scorecard final.

## Mapeo a los checks del Acceptance Gate

- Estado de meta (logrado/parcial/fallido) sin `{DOC}` o `{EXTRAIDO_HILO}` con traza → falla "evidencia tagueada".
- Sin baseline registrado → `{VACIO_CRITICO}` terminal: no se audita de memoria, se pide.
- Objetivo nuevo sin metrica u owner → falla "cada objetivo es medible y tiene owner".
- Lecion sin objetivo/riesgo asociado → huerfano: falla "sin huerfanos".
- Cualquier `[...]` en el doc → falla "sin mezclar familias".
