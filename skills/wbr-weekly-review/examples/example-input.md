# Example input — wbr-weekly-review

Solicitud del operador para cerrar la semana de una estacion concreta.

---

> Cierra la semana **2026-W24** de la estacion **Jarvis-OS** (fecha de corte
> 2026-06-12).
>
> **Compromisos de la semana pasada (2026-W23):**
> 1. Mergear el refactor del router de cadencias.
> 2. Dejar el deploy de la API de bitacora en produccion.
> 3. Documentar la familia de tags Jarvis en references.
>
> **Senales de esta semana:**
> - Se mergearon 3 PRs del refactor del router (commits a1b2c3, d4e5f6, 7g8h9i).
> - El deploy de la API quedo a medias: el ambiente de QA no estaba aprovisionado,
>   asi que no paso de staging.
> - La migracion de datos de la bitacora vieja lleva **9 dias** en curso; espera
>   una decision de esquema que no ha llegado.
> - El doc de tags se escribio y mergeo (`references/verification-tags.md`).
> - El pipeline de CI volvio a fallar por flaky tests; es la tercera semana seguida.
>
> **Arrastres del WBR previo:**
> - "Definir politica de retencion de bitacora": abierto desde 2026-W22.
