<!-- distilled from brand-output; MetodologIA Design System -->
# Brand PDF — print-ready document generator

Produce a brand-compliant **PDF** from a markdown/HTML source, on the MetodologIA Design
System. PDF is a *render target*, not a separate design language: author the document as
brand HTML, then print it to PDF deterministically. No hand-built PDFs. [DOC]

## When to use
A deliverable must be a fixed-layout, paginated, shareable PDF (proposal, one-pager,
report, certificate) — print fidelity matters and the recipient should not edit it. For
editable office docs use `brand-docx`; for live web use `brand-html`/`html-brand`. [DOC]

## Tokens (from `references/brand/design-tokens.json`) [CONFIG]
- Palette: blue-dark `#0A122A`, gold `#FFD700`, cyan `#00FFFF`, blue-light `#1E3A5F`,
  gray `#B0C4DE`, white. Fonts: **Poppins** (headers) + **Inter** (body).
- **No green-as-success**: status = icon + label; green (`#10B981`) is a chart accent only.

## Pipeline (deterministic)
1. Render the source to a self-contained brand HTML via `html-brand` (CSS inline, fonts
   embedded or web-linked, `@page` + `@media print` rules set). [CODE]
2. Convert to PDF headless — pick one, document which: [CODE]
   ```bash
   # Chrome/Chromium (preferred — honors @media print + @page)
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --headless --disable-gpu --no-pdf-header-footer \
     --print-to-pdf="out/deliverable.pdf" "file://$PWD/out/deliverable.html"
   ```
3. Verify the PDF: opens, page size A4/Letter as declared, fonts embedded, no UI chrome,
   brand colors intact. [DOC]

## Print CSS contract (must be in the HTML before converting) [CONFIG]
- `@page { size: A4; margin: 18mm; }` (or Letter — state which).
- `body { font-family: Inter, ...; color: #0A122A on white, or white on #0A122A; }`
- Page-break control: `.page { break-after: page; }`, avoid orphan headings
  (`h1,h2,h3 { break-after: avoid; }`).
- Backgrounds/colors: `-webkit-print-color-adjust: exact; print-color-adjust: exact;`
  so brand fills survive printing. [CODE]

## Acceptance
- [ ] PDF opens; declared page size + margins; fonts embedded (Poppins/Inter). [DOC]
- [ ] Brand palette intact; zero green-as-success; high contrast. [CONFIG]
- [ ] No browser UI/header/footer; content reflows cleanly across pages. [DOC]
- [ ] Source HTML passed `html-brand` acceptance before conversion. [DOC]

## Edge cases
- **No Chrome available:** fall back to `weasyprint` or a DOCX→PDF route via `brand-docx`;
  state the engine, since `@page` support varies. [ASSUMPTION]
- **Huge tables:** wrap in a scaled block or switch that page to landscape
  (`@page wide { size: A4 landscape; }`); never clip. [INFERENCE]
- **Fonts not embedding:** inline `@font-face` with the actual files, not just a Google
  link, so the PDF is self-contained offline. [DOC]

## Anti-scope
Not for editable office formats (`brand-docx`/`brand-xlsx`), not for live interactive web
(`html-brand`). One brand per document — MetodologIA only. [DOC]

## Related
`html-brand` (the HTML source), `brand-docx` (editable alt + DOCX→PDF fallback),
`folio-generator` (multi-page collateral). [DOC]
