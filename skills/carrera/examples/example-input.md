# Example input — carrera (topic: negociacion-oferta)

Operator request (Spanish candidate-side):

> Tengo dos ofertas y necesito decidir. ¿Cuál es aceptable?
>
> **Oferta A — MetodologIA (no, es un cliente externo):** 5000 USD/mes, remoto,
> no-exclusiva, compatible con reubicación. Evidencia: carta de oferta escrita.
> **Oferta B — Acme Corp:** 6500 USD/mes, híbrido, exclusiva, sin reubicación.
> Evidencia: correo del reclutador.
>
> Mis restricciones: `floor_usd = 4500`, requiero un stream paralelo (no
> exclusividad), reubicación es una meta. No inventes tasas de mercado ni
> ofertas que no existen.

Depth: `quick`.

Expected resolution:
- `topic` → `negociacion-oferta` (offer comparison, accept/reject decision).
- Required inputs present for both offers: name, USD amount, work mode,
  exclusivity, relocation flag, plus `floor_usd`. → scoreable, not blocked.
- Hard filters gate before PIVOTE; higher pay must not override a hard fail.
