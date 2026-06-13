# Prompt — weekly-retro (quick)

Retro express de fin de semana cuando la semana fue corta o el contexto ya esta
caliente.

1. Lee las fuentes de la ventana + la memoria destino (read-before-write).
   Ventana = ultimos 7 dias si no es explicita (`{AUTOCOMPLETADO}`).
2. Tres lineas, una por eje:
   - **Ayudo:** un acierto verificable, con `{EXTRAIDO_HILO}`/`{MEMORIA}`/commit.
   - **Friccion:** lo que costó tiempo + si fue ruido (1 vez) o patron (>=2).
   - **Regla candidata:** solo si hubo patron >=2; imperativo, una linea, con
     destino. Si no, "sin patron nuevo".
3. **Accion:** 1 accion concreta para la proxima semana, con primer paso.
4. Si hay regla: muestra el diff sobre el destino y **espera confirmacion** antes
   de aplicar. Append, nunca sobrescribir.

Reglas minimas: un tag Jarvis `{...}` por afirmacion no obvia; sin mezclar
`[...]`; friccion vista 1 vez → observacion. No inventes para rellenar. Si falta
fuente → `{VACIO_CRITICO}` y pregunta.
