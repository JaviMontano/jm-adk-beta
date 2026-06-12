<!-- distilled from alfa skills/iconography -->
<!-- > -->
# Iconography
> "Method over hacks."

## TL;DR
Build and audit icon systems: grid + stroke consistency, SVG optimization, accessibility, stable naming. [DOC]

## Scope
- In: icon set design tokens, SVG hygiene, a11y semantics, naming/handoff. [DOC]
- Out (anti-scope): full brand identity, illustration, motion design, raster/photo assets — redirect to the relevant skill. [SUPUESTO]

## Procedure
### Step 1: Discover
- Inventory existing icons, target sizes, framework (inline SVG, sprite, icon font), and a11y requirements. [DOC]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV against the System Rules below. Flag inconsistencies (mixed grids, mixed stroke widths). [DOC]
### Step 3: Execute
- Normalize to one grid/stroke, optimize SVGs, apply naming + a11y, emit evidence tags. [DOC]
### Step 4: Validate
- Run Acceptance Criteria; report residual gaps as `[SUPUESTO]` with a verification step. [DOC]

## System Rules
- One grid (commonly 24×24, 2px padding live area) and one stroke width per set; mixing reads as broken. [SUPUESTO]
- Optical sizing over mathematical: hand-tune small sizes (16px) rather than scaling the 24px master down. [INFERENCIA]
- Decide rendering by need, with trade-offs: [INFERENCIA]
  - Inline SVG — per-icon styling/animation, no extra request; cost: markup weight if repeated.
  - SVG sprite (`<use>`) — dedup + cacheable; cost: harder per-instance theming, build step.
  - Icon font — legacy/broad support; cost: a11y traps, no multicolor, blurry rendering — avoid for new work.
- SVG hygiene: strip editor metadata, flatten transforms, set `fill="currentColor"` so CSS `color` themes the icon, keep one `viewBox`, drop hardcoded width/height in markup. [DOC]

## Accessibility
- Decorative icon (text label present): `aria-hidden="true"`, no `role`. [DOC]
- Standalone icon (icon-only button): give the control an `aria-label`; mark the SVG `aria-hidden`. [DOC]
- Meaningful standalone graphic: `role="img"` + `<title>` as first child. [DOC]
- Never rely on color alone to convey state (e.g. error vs success) — pair with shape or label (WCAG 1.4.1). [DOC]
- Target size: interactive icon hit area ≥ 24×24 CSS px even when the glyph is smaller (WCAG 2.5.8). [DOC]

## Naming & Handoff
- Kebab-case, semantic-then-variant: `arrow-left`, `chevron-down`, `status-error`; avoid visual-only names like `red-circle`. [SUPUESTO]
- One concept = one canonical name; aliases documented, not duplicated as separate files. [INFERENCIA]

## Worked Example
Input: 30 SVGs exported from design tool, two stroke widths (1.5px and 2px), inline hex fills.
Action: snap all to 24×24 grid, normalize to 2px stroke, replace `fill="#111"` with `fill="currentColor"`, optimize (≈40% bytes saved via metadata strip), rename to kebab semantic, wrap icon-only buttons with `aria-label`.
Output: single themeable set + `[SUPUESTO]` note that 16px variants still need optical hinting. [INFERENCIA]

## Quality Criteria
- [ ] Single grid + single stroke width across the set [DOC]
- [ ] All SVGs use `currentColor`; no editor metadata; one `viewBox` [DOC]
- [ ] A11y pattern applied per icon role (decorative / labeled / meaningful) [DOC]
- [ ] Semantic kebab-case names, no duplicates [DOC]
- [ ] Evidence tags applied; Constitution-compliant; actionable output [DOC]

## Usage
Example invocations:
- "/iconography" — Run the full iconography workflow
- "iconography on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and source SVGs. [SUPUESTO]
- English-language output unless otherwise specified. [SUPUESTO]
- Does not replace domain expert judgment for final visual decisions. [SUPUESTO]
- Color-token mapping depends on an existing design-system palette; if absent, flag `[SUPUESTO]` and request it. [INFERENCIA]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request (illustration, motion) | Redirect to appropriate skill or escalate |
| Multicolor / duotone icon needed | Inline SVG with layered paths; rule out icon-font path |
| Mixed grids in existing set | Re-snap to one grid; list icons that changed bounds |
| RTL-sensitive icon (arrows, chevrons) | Mark for mirroring; do not mirror logos/clocks |
