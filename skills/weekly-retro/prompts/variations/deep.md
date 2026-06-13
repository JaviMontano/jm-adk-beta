# Prompt — weekly-retro (deep)

Retro semanal extendida para cierres de sprint, semanas densas, o cuando varias
fricciones compiten por ascender a regla. Mas evidencia, mas rigor en el umbral.

## 1. Discover (amplio)
- Fija la ventana explicitamente (semana o sprint completo). Si abarca >7 dias,
  marca `{SUPUESTO}` lo reconstruido.
- Abre **todas** las fuentes: TAREAS.md/tasklog, changelog, hilos, commits. Cruza
  fuentes para una misma friccion (una mencion en hilo + un commit que la
  evidencia cuenta como traza mas fuerte). Lee la memoria destino completa.

## 2. Analyze (tres ejes con conteo de recurrencia)
- **Ayudo:** lista cada acierto con su fuente; separa los puntuales de los que
  ya son habito.
- **Friccion:** para cada una, **cuenta ocurrencias** en la ventana y, si aplica,
  en ventanas previas (de la propia bitacora de retros). Anota el conteo.
- **Regla candidata:** clasifica cada friccion:
  - <2 ocurrencias → observacion (registra, no asciende).
  - >=2 → candidata; redacta la regla en imperativo, una linea, con destino.
  - Acierto a volver default → candidata aunque sea unico.
- Revisa conflictos: ¿alguna candidata contradice una regla existente? Si si, no
  sobrescribas; documenta el conflicto.

## 3. Execute (promocion gated)
- Para cada candidata aprobada, construye el diff exacto sobre el destino y
  preséntalo agrupado. **Espera confirmacion item por item.** Append aditivo;
  historico y ediciones locales intactos; sin `--force`.
- Registra las observaciones no promovidas para la proxima ventana.

## 4. Validate (gate completo)
Corre `evidence`, `quality_criteria`, `upgrade_safety` contra
`assets/quality-rubric.json`. Lista de acciones priorizadas para la proxima
semana, cada una con primer paso. Solo `pass` cierra la retro.

Disciplina: un tag Jarvis `{...}` por claim; sin Alfa `[...]`; `{WEB}` con cita;
marca unica. No promuevas en automatico.
