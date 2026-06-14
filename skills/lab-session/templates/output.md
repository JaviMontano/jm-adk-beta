# Lab Session Scaffold — Run Report

> Deliverable scaffold for one `lab-session` run. The four canonical files are
> written under `<lab-root>/<slug>/`; this report is the console-facing summary.

## Session
- **Slug:** `<slug>`
- **Lab root:** `<lab-root>`
- **Topic:** <one-line objective>
- **Date:** `YYYY-MM-DD`

## Result
- **Created:** `<n>` — list of files written this run
- **Skipped (pre-existing):** `<m>` — list of files left byte-identical
- **Summary line:** `created=<n> skipped=<m>`

## Folder contents (must be exactly four)
- [ ] `notas.md`
- [ ] `hipotesis.md`
- [ ] `referencias.md`
- [ ] `decision.md`

## File starting states
| File | State after run |
|---|---|
| `notas.md` | dated stub entry (ISO date) |
| `hipotesis.md` | `<claim>` or `{HIPOTESIS_POR_DEFINIR}` |
| `referencias.md` | tagged skeleton (`[DOC]`/...) |
| `decision.md` | `{POR_CONFIRMAR}` |

## Validation gate
- [ ] Exactly four canonical files present
- [ ] No pre-existing file modified (mtime/bytes match snapshot)
- [ ] `hipotesis.md` falsifiable or explicit stub
- [ ] Every reference entry + non-obvious note carries one Alfa-core tag, one spelling
- [ ] `decision.md` is `{POR_CONFIRMAR}` (no pre-written verdict)
- [ ] Summary line reported
- [ ] Single-brand JM Labs; green not used as a success signal

## Notes / follow-ups
<free text — open questions, next probe, slug-collision flags>

---
Evidence tags: `[CODE]` / `[CONFIG]` / `[DOC]` / `[INFERENCE]` / `[ASSUMPTION]`
