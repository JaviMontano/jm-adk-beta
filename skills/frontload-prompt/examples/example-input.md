# Example Input — frontload-prompt

Un usuario pega contexto crudo sin pedir nada explícito:

---

> Vengo del hilo con el equipo de soporte. El cliente Acme abrió 6 tickets esta
> semana, casi todos sobre que el export a PDF tarda más de 30 segundos y a veces
> se cae con timeout. El de infra dijo que el job corre síncrono en el request.
> Tengo el archivo `services/export/pdf_job.py` y el log de un timeout pegado más
> abajo. Lo necesito para el steering del jueves.
>
> ```
> [ERROR] 2026-06-10 14:22:01 ExportTimeout: pdf render exceeded 30s (req=8821)
>   at pdf_job.render (services/export/pdf_job.py:88)
> ```

---

Notas del input:
- Hay contexto (`{EXTRAIDO_HILO}`), un archivo referenciado (`{ADJUNTO}`) y un log.
- El **Purpose** no está dicho en una frase: ¿quiere un diagnóstico? ¿un plan de
  fix? ¿material para el steering? Es inferible pero ambiguo entre dos lecturas.
- La **fecha límite** (jueves, steering) y la **audiencia** (steering) sí están.
- Falta el **formato de salida** esperado.
