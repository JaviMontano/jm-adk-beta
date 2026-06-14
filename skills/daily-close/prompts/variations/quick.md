# Prompt — daily-close (quick)

Cierre express de fin de jornada cuando el dia fue corto o ya esta caliente.

1. Lee fuente del dia + destino (read-before-write). Fecha = hoy si no es explicita
   (`{AUTOCOMPLETADO}`).
2. Tres lineas, una por eje:
   - **Cerrado:** lo verificable hoy, con `{DOC}`/`{EXTRAIDO_HILO}`.
   - **Pendiente:** lo abierto + motivo breve.
   - **Aprendido:** un insight (o "sin avances/aprendizajes" explicito).
3. **Semilla:** 1 pendiente top + su primer paso en frio.
4. Append al destino. No sobrescribas historico.

Reglas minimas: un tag Jarvis `{...}` por afirmacion no obvia; sin mezclar `[...]`;
item ambiguo → Pendiente. No inventes para rellenar. Si falta fuente → pregunta.
