# Example Input — brand-output

A real branded-output request that exercises routing, token resolution, and the
folio numbering contract.

## User request

> "Genera la cotizacion para el cliente Acme Corp por la migracion a la plataforma
> de pagos. El ultimo COT-2026 registrado es 007. Fecha de emision: 2026-06-12.
> Necesito el documento numerado y maquetado en HTML con los tokens de marca de
> negocio. Asunto: 'Migracion plataforma de pagos — Fase 1'."

## Supplied data

```json
{
  "type": "COT",
  "issue_date": "2026-06-12",
  "recipient": "Acme Corp",
  "subject": "Migracion plataforma de pagos — Fase 1",
  "body": "Propuesta de servicios para la migracion de la plataforma de pagos, Fase 1: descubrimiento y arquitectura objetivo."
}
```

## Context for the router
- Format named: **HTML**, numbered document → this is a **folio**.
- Brand: business/neutral tokens (no MetodologIA DS or MetodologIA named).
- `artifact_date` / issue date supplied: `2026-06-12` (use this, not the clock).
- Last correlative for `COT-2026`: `007`.
- depth: quick (request is unambiguous — one topic fits).

## Expected routing
One enum fits cleanly: a numbered, paginated business document →
`folio-generator`. No clarifying question needed. [INFERENCIA]
