# Ejemplo — Entrada (dbr-daily-plan)

Mensaje del usuario al inicio de la jornada:

> Buenos dias, dame el plan del dia (DBR). Esto es lo que tengo:
>
> **Backlog/agenda de hoy:**
> - Terminar la propuesta tecnica para el cliente Andes (vence manana 10am).
> - Reunion de equipo 10:00–11:00 (fija).
> - Reunion 1:1 con Marta 15:00–15:30 (fija).
> - Revisar el PR #482 que lleva 3 dias bloqueando a Dev.
> - Responder el hilo de soporte de Beta Corp (lleva 2 dias).
> - Investigar el bug intermitente de login (sin deadline claro).
> - Actualizar la documentacion del onboarding (hace tiempo que quiero).
> - Llamar al proveedor de hosting por la factura.
>
> **Restriccion:** tengo el dia 9:00–18:00 pero con las 2 reuniones y comida me
> quedan unas **5 horas reales de foco**. Hoy ando con energia media.
>
> **Continuidad de ayer:** ayer dejé el borrador de la propuesta Andes al 60% y el
> PR #482 ya estaba pendiente de mi review.

Notas de origen:
- Continuidad de ayer ⇒ `{EXTRAIDO_HILO}`.
- "5 horas reales" lo da el usuario; la reparticion fina la estimara el plan
  ⇒ `{AUTOCOMPLETADO}` donde se infiera.
