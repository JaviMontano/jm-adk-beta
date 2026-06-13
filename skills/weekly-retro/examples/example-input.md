# Example input — weekly-retro

Contexto que el operador pasa al iniciar la retro de la semana.

---

Cierra mi semana del 2026-06-05 al 2026-06-11. Fuentes:

- `TAREAS.md` — cerré la migracion del scaffold de skills y dejé a medias el
  gate de evals.
- `orchestration/changelog.md` — dos entradas: una sobre re-correr el validador
  porque se me olvidó el flag `--skip-script-checks`, otra igual la semana
  pasada (mismo olvido).
- Hilo de hoy: perdí ~40 min depurando un JSON de knowledge-graph mal formado
  porque lo escribí a mano sin validar.

Lo que ayudó: usar el sibling `daily-close` como plantilla aceleró muchísimo el
armado del bundle.

Memoria destino para reglas: `orchestration/preferences-log.md`.

Quiero el bloque de tres ejes y, si algo se repite, propon la regla — pero
muéstrame el diff antes de tocar nada.
