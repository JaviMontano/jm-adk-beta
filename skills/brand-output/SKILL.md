---
name: brand-output
description: "Branded output generation: HTML, DOCX, XLSX, folios, templates (Sofka DS tokens in references/brand). Topics: brand-docx, brand-html, brand-xlsx, branded-html-output, folio-generator, html-brand, presentation-design, xlsx-template-creator."
params:
  topic:
    enum: [brand-docx, brand-html, brand-xlsx, branded-html-output, folio-generator, html-brand, presentation-design, xlsx-template-creator]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  brand-docx: references/brand-docx.md
  brand-html: references/brand-html.md
  brand-xlsx: references/brand-xlsx.md
  branded-html-output: references/branded-html-output.md
  folio-generator: references/folio-generator.md
  html-brand: references/html-brand.md
  presentation-design: references/presentation-design.md
  xlsx-template-creator: references/xlsx-template-creator.md
---

# brand-output

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
