# Example Output — frontload-prompt

SPEC resultante para el input de `example-input.md`. Nótese que NO se diagnostica
el bug ni se redacta material de steering: solo se estructura el contrato.

---

# SPEC — Export PDF lento/timeout para steering Acme

## S — Situation
6 tickets de Acme esta semana por export a PDF >30s y timeouts intermitentes.
Infra reporta que el job corre síncrono en el request. `{EXTRAIDO_HILO}`
Evidencia adjunta: `services/export/pdf_job.py` y un log de timeout
(`ExportTimeout` en `pdf_job.py:88`, req=8821). `{ADJUNTO}`

## P — Purpose
Producir, para el steering del jueves, un diagnóstico de causa raíz del timeout
de export PDF más una recomendación de fix priorizada. `{INFERENCIA}`
(Lectura alternativa: solo material de presentación sin diagnóstico técnico. Se
eligió la lectura con diagnóstico por ser la menos destructiva; ver Expectations.)

## E — Expectations
- Audiencia: comité de steering. `{EXTRAIDO_HILO}`
- Plazo: jueves de esta semana. `{EXTRAIDO_HILO}`
- Forma de salida: resumen ejecutivo (1 página) + causa raíz + opciones de fix
  con esfuerzo relativo. `{AUTOCOMPLETADO}`
- Profundidad técnica: media — orientada a decisión, no a implementación. `{SUPUESTO}`

## C — Context
- `services/export/pdf_job.py` — archivo a inspeccionar para confirmar el modelo
  síncrono antes de afirmar causa raíz. `{POR_CONFIRMAR}`
- Dependencia: confirmar si el fix (async/queue) toca infra compartida. `{INFERENCIA}`

---

## Veredicto

**BLOCKED** — 1 vacío crítico:
- `{VACIO_CRITICO}` en Purpose → ¿El entregable del jueves es (a) diagnóstico +
  recomendación técnica, o (b) solo el resumen para el comité sin profundizar en
  el fix? La interpretación cambia el alcance.

**Pregunta mínima que desbloquea:** "Para el steering del jueves, ¿necesitas el
diagnóstico técnico con recomendación de fix, o basta un resumen ejecutivo del
impacto?"

## Checklist del gate
- [x] S/P/E/C presentes y tagueados
- [ ] Purpose accionable sin re-preguntar  ← falla: lectura ambigua
- [x] Cada campo derivado con UN tag Jarvis OS
- [ ] Cero `{VACIO_CRITICO}` pendientes  ← 1 pendiente
- [x] No se ejecutó la tarea ni se tocó ningún archivo
