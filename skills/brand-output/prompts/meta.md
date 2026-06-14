# Meta Prompt — brand-output

Use this to reason about the routing itself before committing to a topic.

## Self-check before routing
- **Format certainty.** Did the user name a format (HTML/DOCX/XLSX/slides/folio)?
  If implicit, what signal disambiguates it? Record the signal as `[INFERENCIA]`.
- **Brand certainty.** MetodologIA DS, MetodologIA, or fallback config? If two brands
  are plausible, ask — never guess between brands. [EXPLICIT]
- **Binary vs spec.** XLSX request: does the user want a finished workbook
  (`brand-xlsx`) or a reusable, diffable spec (`xlsx-template-creator`)?
- **Numbering.** Does the document need a unique correlative? → `folio-generator`.

## Tie-break heuristics
- HTML + "MetodologIA" / orange / Poppins → `html-brand`.
- HTML + navy/gold/glassmorphism/MetodologIA → `branded-html-output`.
- HTML + generic/external brand config → `brand-html`.
- "template" + spreadsheet → `xlsx-template-creator`; "report"/"dashboard" + xlsx
  → `brand-xlsx`.

## Anti-patterns to catch in yourself
- Loading two playbooks "to compare" — pick one, re-route only on proof it's wrong.
- Letting the render clock set the folio year instead of the issue-date field.
- Reporting the gate green without verifying each box.

## Escalate when
The request needs SPA/routing/multi-page, e-signature, accounting, or non-DS
output — decline the out-of-scope part and route the in-scope subset only. [CONFIG]
