---
name: brand-output
version: 1.0.0
description: "Branded output generation: HTML/CSS/JS, DOCX, XLSX, PDF, vector art, folios, templates (MetodologIA DS tokens in references/brand). Topics: brand-art, brand-docx, brand-html, brand-pdf, brand-xlsx, branded-html-output, folio-generator, html-brand, presentation-design, xlsx-template-creator."
params:
  topic:
    enum: [brand-art, brand-docx, brand-html, brand-pdf, brand-xlsx, branded-html-output, folio-generator, html-brand, presentation-design, xlsx-template-creator]
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

Router skill for **branded deliverable generation** with MetodologIA DS tokens. Resolve
`topic`, then Read EXACTLY ONE playbook from `routes:` — never load the cluster. [EXPLICIT]

## When to use
Any request to produce a branded artifact: HTML pages/folios, DOCX, XLSX, slides,
or reusable templates. **Not** for raw content authoring (no brand) or non-MetodologIA
output — route those elsewhere. [INFERENCE]

## Inputs / Outputs
- **In:** `topic` (one of the 8 enums), `depth`, the source content/data, target format.
- **Out:** one branded file using `references/brand` tokens; provenance-tagged where
  claims aren't reproducible from the prompt. [CONFIG]

## Routing
1. Infer `topic` from the request; ask only if genuinely ambiguous (≥2 enums fit equally). [EXPLICIT]
2. Read that single playbook. `deep` → apply exhaustively, verify each step; `quick` → essentials. [EXPLICIT]
3. Format-vs-topic disambiguation:
   - HTML: `brand-html` (general) · `html-brand` (token-heavy/deep) · `branded-html-output` (lightweight) · `folio-generator` (paginated folios). [INFERENCE]
   - Slides → `presentation-design`. DOCX → `brand-docx`. XLSX → `brand-xlsx` (one-off) vs `xlsx-template-creator` (reusable template). [INFERENCE]

Spine: Discover → Analyze → Execute → Validate.

Router aids in `assets/` — `assets/routing-checklist.md` and `assets/quality-rubric.json` (see `assets/README.md`). [CONFIG]

## Validation gate (done = all true)
- Exactly one playbook loaded; topic matches the artifact actually produced. [EXPLICIT]
- MetodologIA DS tokens applied from `references/brand`; no hardcoded brand values. [CONFIG]
- Constitution v6.0.0 enforcement + script-first rule honored (generate via script, not hand-edits). [EXPLICIT]
- Evidence tags present on non-obvious claims; family not mixed (kit set: `[EXPLICIT]`/`[INFERENCE]`/`[ASSUMPTION]`/`[CONFIG]`/`[DOC]`). [DOC]

## Anti-patterns
- Loading multiple playbooks "to compare" — pick one, re-route only if wrong. [EXPLICIT]
- Mixing brands in one output, or inventing tokens/prices. [EXPLICIT]
- Skipping the script-first rule by hand-crafting the file. [ASSUMPTION]
