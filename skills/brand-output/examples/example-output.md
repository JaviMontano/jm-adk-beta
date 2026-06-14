# Example Output — brand-output

Routing-and-delivery record for the `example-input.md` cotizacion request.

## 1. Request
- **Raw request:** numbered HTML cotizacion for Acme Corp, payments-platform migration.
- **Content/data source:** structured JSON (type/date/recipient/subject/body).
- **Target format:** HTML (numbered) → folio.
- **Brand system:** neutral business tokens (`assets/brand-tokens.json`).
- **artifact_date (caller-supplied):** 2026-06-12.
- **depth:** quick.

## 2. Routing decision
- **Chosen topic:** `folio-generator`.
- **Playbook loaded:** `references/folio-generator.md` (single playbook). [EXPLICIT]
- **Disambiguating signal:** request asks for a *numbered* document; numbering is
  the unique capability of `folio-generator`. [INFERENCIA]
- **Rejected candidates:** `brand-html`/`html-brand` — render branded HTML but do
  not own a correlative tracker.
- **Asked a clarifying question?** No — one enum fits.

## 3. Token resolution
- **Config source:** `assets/brand-tokens.json` (neutral business defaults).
- **Inherited keys:** none.
- **Brand-mix check:** single brand confirmed — yes.

## 4. Generation
- `scripts/next-folio-number.sh --dry-run --tracker .folio-tracker.json COT`
  → prints `COT-2026-008`, tracker intact. [CÓDIGO]
- User confirms → `scripts/next-folio-number.sh --apply --tracker .folio-tracker.json COT`
  → reserves `008`, tracker advances to `008`. [CÓDIGO]
- `scripts/render-folio-html.py --data cot.json`
  → HTML with header `COT-2026-008`, issue date 2026-06-12, recipient Acme Corp,
    subject line, body, footer "Documento generado — Folio COT-2026-008". [INFERENCIA]

## 5. Validation gate
- [x] Exactly one playbook loaded; topic matches the folio produced. [EXPLICIT]
- [x] Tokens only from `brand-tokens.json` + `folio-style.css`; no stray hex. [CONFIG]
- [x] Year `2026` came from the issue-date field, not the render clock. [CONFIG]
- [x] Script-first: number reserved via `--apply`, never hand-edited. [CÓDIGO]
- [x] `NNN` resets per `COT-2026`; `008` follows `007` with no gap. [DOC]
- [x] Evidence tags present; single Alfa family; no prices invented; no PII. [DOC]
- **check.sh:** pass.

## 6. Outcome
- **Status:** delivered — `COT-2026-008.html`, tracker reconciled.
- **Open findings / limitations:** distribution (Drive/Gmail) only on explicit
  user confirmation; number reserved before any send so a failed send re-tries
  without re-numbering. [INFERENCIA]
