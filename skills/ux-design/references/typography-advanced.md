<!-- distilled from alfa skills/typography-advanced -->
<!-- > -->
# Typography Advanced
> "Method over hacks."
## TL;DR
Variable fonts, optical sizing, responsive type scales, vertical rhythm. Produce a tokenized type system that survives viewport and zoom changes without manual breakpoints. [EXPLICIT]

## Procedure
### Step 1: Discover
- Inventory typefaces, weights/axes, current scale, and rendering targets (web/print/app). [EXPLICIT]
- Capture constraints: brand fonts, license, language coverage (diacritics/CJK), min legible size, contrast floor. [EXPLICIT]
### Step 2: Analyze — decisions + trade-offs
- **Variable vs static**: ship variable font when 3+ weights/axes are used (one file, fewer requests); fall back to static subsets when `font-variation-settings` support or payload budget is tight. [INFERENCIA]
- **Optical sizing**: bind `opsz` to font-size via `font-optical-sizing: auto` so display sizes get tighter spacing and text sizes stay open. Pin `opsz` manually only when auto contradicts the brand. [EXPLICIT]
- **Fluid scale**: use `clamp(min, preferred-vw, max)` per step instead of breakpoint overrides — continuous, fewer rules, no jumps. Trade-off: harder to reason about exact px at a given width. [INFERENCIA]
- **Vertical rhythm**: set `line-height` unitless and a baseline grid (e.g. 4px); derive margins from the grid, not ad-hoc values. [EXPLICIT]
### Step 3: Execute
- Emit CSS custom properties as the single source of truth; reference them everywhere (no hard-coded px). Tag each token's rationale. [EXPLICIT]
### Step 4: Validate
- Verify acceptance criteria below across smallest/largest viewport and 200% zoom. [EXPLICIT]

## Worked Example
```css
:root {
  /* fluid step: 16px @320 → 19px @1280, ratio ~1.25 modular */
  --fs-body: clamp(1rem, 0.93rem + 0.36vw, 1.1875rem);
  --fs-h1:   clamp(2rem, 1.4rem + 3vw, 3.5rem);
  --lh-body: 1.5;            /* unitless → inherits cleanly */
  --baseline: 0.25rem;       /* 4px rhythm unit */
}
body { font-optical-sizing: auto; font-size: var(--fs-body); line-height: var(--lh-body); }
h1   { font-size: var(--fs-h1); line-height: 1.1; margin-block: calc(var(--baseline) * 6); }
```

## Quality Criteria / Acceptance
- [ ] Every size, line-height, and spacing value resolves from a token, not a literal. [EXPLICIT]
- [ ] Body text ≥16px effective at all viewports; line length 45–75ch. [EXPLICIT]
- [ ] No layout shift or clipping at 200% zoom (WCAG 1.4.4 reflow). [EXPLICIT]
- [ ] Variable-font axes have a static fallback declared. [EXPLICIT]
- [ ] Evidence tags applied; Constitution XIII/XIV-compliant. [EXPLICIT]

## Usage

Example invocations:

- "/typography-advanced" — Run the full typography advanced workflow
- "typography advanced on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and the target stylesheet. [EXPLICIT]
- Scope is screen/web type systems via CSS; print imposition and email-client type are out of scope. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final brand decisions. [EXPLICIT]

## Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request (print/email) | Redirect to appropriate skill or escalate |
| Brand font lacks a variable build | Use static weights; declare fallback, drop `opsz` axis |
| `clamp()`/variable-font unsupported | Ship static fallback rule first, enhance progressively |
| Non-Latin / missing glyphs | Verify subset coverage; add language fallback stack |
| Fluid min == max collapse | Ensure preferred term scales between bounds; recompute vw |
