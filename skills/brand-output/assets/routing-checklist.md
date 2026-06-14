# Routing Checklist — brand-output

Run top-to-bottom before delivering any branded artifact. Stop at the first
failure; do not mark green by default. [CONFIG]

## Discover
- [ ] Content/data present? If not → stop `{VACIO_CRITICO}`, ask. [EXPLICIT]
- [ ] Target format identified (HTML / DOCX / XLSX / spec / slides / folio).
- [ ] Brand identified: MetodologIA DS · MetodologIA · fallback config.
- [ ] `artifact_date` captured from the caller (never inferred). [INFERENCIA]

## Route (pick exactly one)
- [ ] HTML general → `brand-html`
- [ ] HTML MetodologIA DS (orange/Poppins/Inter) → `html-brand`
- [ ] HTML MetodologIA (navy/gold/glassmorphism) → `branded-html-output`
- [ ] Numbered/paginated document → `folio-generator`
- [ ] Word `.docx` → `brand-docx`
- [ ] Finished `.xlsx` workbook → `brand-xlsx`
- [ ] Reusable spec, no binary → `xlsx-template-creator`
- [ ] Slide deck → `presentation-design`
- [ ] If ≥2 fit equally → ask ONE disambiguating question. [EXPLICIT]

## Execute
- [ ] Read that single playbook only. [EXPLICIT]
- [ ] Resolve tokens via the documented search order; merge partials, tag
      inherited keys `[SUPUESTO]`. [INFERENCIA]
- [ ] Generate via the playbook's deterministic script (folio: `--dry-run` then
      `--apply`). Never hand-edit. [CÓDIGO]

## Validate
- [ ] One playbook loaded; topic matches artifact. [EXPLICIT]
- [ ] No hardcoded brand values outside `:root`/token files; single brand. [CONFIG]
- [ ] Determinism honored (no clock/remote/random). [INFERENCIA]
- [ ] Format-specific gate passed; `check.sh`/compiler clean. [CÓDIGO]
- [ ] Evidence tags present, single Alfa family; no invented prices; no PII. [DOC]
