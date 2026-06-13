<!-- distilled from brand-output; MetodologIA Design System -->
# Brand Art — vector illustration & graphic generator

Produce brand-compliant **vector art** (SVG) on the MetodologIA Design System: hero
graphics, spot illustrations, icons, diagrams, social/share images. Output is editable,
scalable SVG (rasterize to PNG only at the end if a format demands it). [DOC]

## When to use
A deliverable needs an *illustration or graphic asset* — not a document. Hero image for a
landing/proposal, section spot art, an icon set, a diagram, an OG/share card. For
text-first documents use `html-brand`/`brand-pdf`/`brand-docx`. [DOC]

## Brand visual language [CONFIG]
- **Aesthetic**: flat vibrant vector, Swiss grid, generous whitespace, **faceless human
  figures**, soft geometric shapes, soft shadows + discreet micro-gradients. No realism,
  no photographic texture. (See `references/brand/design-tokens.json` → `illustration`.)
- **Palette** (exclusive): blue-dark `#0A122A`, gold `#FFD700`, cyan `#00FFFF`, blue-light
  `#1E3A5F`, gray `#B0C4DE`, white. Gold/cyan = accents; blue-dark = ground.
- **Type in art**: Poppins for any display text baked into the SVG. [CONFIG]
- **No green-as-success**: never use green to mean status/OK; it is not in the brand set.

## Procedure
1. Pick canvas + intent: hero (16:9 / 1200×630 OG), spot (1:1), icon (24/48px grid),
   diagram (fluid). State dimensions. [DOC]
2. Author SVG with brand tokens as CSS variables in `<defs><style>`; compose flat shapes +
   one or two micro-gradients (`linearGradient` gold→transparent). Keep figures faceless.
   [CODE]
3. Accessibility: `<title>` + `<desc>` per SVG; sufficient contrast; do not encode meaning
   in color alone. [CONFIG]
4. Optimize: strip editor cruft, round coords, keep it hand-editable; only rasterize to PNG
   (e.g. for email/OG) as a final, separate step. [CODE]

## Acceptance
- [ ] Only brand palette + derived tints; zero green-as-success. [CONFIG]
- [ ] Faceless figures; flat vector; soft shadows/micro-gradients; Swiss grid + whitespace. [DOC]
- [ ] Valid standalone SVG with `<title>`/`<desc>`; scales crisp at all sizes. [DOC]
- [ ] Display text (if any) in Poppins; high contrast. [CONFIG]

## Edge cases
- **Brand-color-only contrast fail** (e.g. cyan text on white): darken to blue-dark or add
  a blue-dark backing shape; never introduce an off-brand color to fix contrast. [INFERENCE]
- **Raster required** (PNG/JPG): render from the SVG at 2× for crispness; keep the SVG as
  the editable source of truth. [DOC]
- **Complex diagram:** prefer `mermaid` + brand theming over hand-SVG when the graph is the
  point; reserve hand-SVG for illustrative/hero art. [INFERENCE]

## Anti-scope
Not for documents (`brand-pdf`/`brand-docx`/`html-brand`), not for data tables
(`brand-xlsx`). One brand — MetodologIA only. No stock photos / no realistic rendering. [DOC]

## Related
`html-brand` (embeds the art), `presentation-design` (slide visuals), `brand-pdf` (print). [DOC]
