# Prompt — daily-close (deep)

Cierre extendido para jornadas densas, multi-hilo, o cierres retroactivos que hay
que reconstruir con cuidado.

## Procedimiento
1. **Discover exhaustivo.** Lee TODAS las fuentes (TAREAS.md, hilos, notas) y la
   bitacora/MEMORY destino. Reporta lo recuperado con `{MEMORIA}`. Si el cierre es
   retroactivo, fecha al dia real y marca `{SUPUESTO}` lo reconstruido de memoria.
2. **Classify con traza.** Cada item a un eje, con su evidencia explicita:
   - Cerrado → liga commit/archivo/ancla de hilo (`{DOC}`/`{EXTRAIDO_HILO}`).
   - Pendiente → motivo de no-cierre + dependencia (bloqueado vs no-empezado) +
     primer paso.
   - Aprendido → captura cada friccion/decision reusable; no las pierdas en el
     volumen. Dia desbordado = captura cabeceras, no transcripcion.
3. **Seed priorizada.** Top 1-3 por: (a) desbloqueo aguas abajo, (b) ventana
   temporal, (c) menor costo de re-arranque. Primer paso en frio por cada una.
4. **Bloqueos cruzados.** Todo bloqueo abierto que pasa al manana → `{POR_CONFIRMAR}`
   con su paso de verificacion.
5. **Persist aditivo.** Append fechado; revisa diff antes de cualquier `--force`.
   Respeta marca unica (un workspace).
6. **Validate completo.** Corre el gate de `assets/checklist.md` y puntua contra
   `assets/quality-rubric.json`. Solo `pass` habilita declarar cerrado.

## Disciplina
Familia Jarvis `{...}` unica; un tag por afirmacion; `{WEB}` solo con cita. No
verde-como-exito: ausencia de evidencia es falla, no aprobacion.
