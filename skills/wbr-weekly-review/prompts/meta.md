# Prompt — Meta (wbr-weekly-review self-check)

Usa este prompt para auto-criticar un acta WBR antes de declararla hecha. Recorre
el gate como guardian, no como redactor: tu salida es un veredicto con fallas
concretas, no una nueva version del acta.

## Preguntas de control

1. **Estructura.** ¿Estan las seis secciones y el encabezado lleva periodo ISO +
   alcance + fecha de corte?
2. **Lente unico.** ¿Algun item aparece en dos lentes? ¿Algun "ya casi" colado en
   avances? Si si → falla clasificacion.
3. **Estancado accionable.** ¿Cada estancado tiene dueno y proximo paso *fechado*?
   ¿Hay algun "se revisara" sin fecha?
4. **Cumplimiento honesto.** ¿Cada compromiso previo esta marcado cumplido /
   parcial / no-cumplido? ¿Se omitio algun fallido?
5. **Friccion.** ¿Cada friccion esta clasificada recurrente vs puntual? ¿Las
   recurrentes (≥2 semanas) escalan a accion?
6. **Compromisos.** ¿Son ≤5 y cada uno con criterio de hecho? ¿Salen de
   estancado+friccion o son deseos nuevos?
7. **Arrastres.** ¿Los arrastres ≥3 semanas estan marcados `{POR_CONFIRMAR}` y
   escalados a bloqueo?
8. **Evidencia y tags.** ¿Cada avance tiene `{DOC}`/`{ADJUNTO}`? ¿Una sola familia
   de tags `{...}`? ¿Algun `[...]` colado?
9. **Subreporte.** ¿Esta todo verde y nada estancado? Si si → sospechar y preguntar
   que NO se movio.

## Veredicto
Devuelve `pass` o `bloqueado` + lista de fallas del gate con su seccion. No hay
aprobacion parcial. {DOC}
