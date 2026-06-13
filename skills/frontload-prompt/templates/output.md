# SPEC — <título corto del request>

> Contrato de trabajo. No es el entregable. Cada campo derivado o rellenado lleva
> un tag de la familia Jarvis OS `{...}`.

## S — Situation
<Estado actual y origen del input.>
Fuente: `{ADJUNTO}` | `{EXTRAIDO_HILO}` | `{MEMORIA}`

## P — Purpose
<El resultado deseado en UNA frase, accionable.>
Procedencia: explícito | `{INFERENCIA}` | `{VACIO_CRITICO}`

## E — Expectations
- Forma/formato de salida: <…> `{AUTOCOMPLETADO}` si es default
- Longitud / límites: <…>
- Criterios de aceptación: <…>
- Restricciones duras: <…>
- Conflictos de requisitos (si los hay): <interpretación elegida> `{SUPUESTO}`

## C — Context
- Archivos relevantes inspeccionados: <ruta + qué aportó>
- Audiencia: <…> `{AUTOCOMPLETADO}` si se asume
- Evidencia disponible: <…>
- Dependencias: <…>

---

## Veredicto

- [ ] **READY** — 4 secciones accionables, cero `{VACIO_CRITICO}`, sin ejecución.
- [ ] **BLOCKED** — vacíos críticos pendientes:
  - `{VACIO_CRITICO}` en <campo> → **Pregunta que desbloquea:** <pregunta exacta>

## Checklist del gate (todos deben cumplirse para READY)
- [ ] S/P/E/C presentes, ninguno vacío sin tag
- [ ] Purpose accionable sin re-preguntar
- [ ] Cada campo derivado/rellenado con UN tag Jarvis OS
- [ ] Cero `{VACIO_CRITICO}` pendientes
- [ ] No se ejecutó la tarea ni se tocó ningún archivo
