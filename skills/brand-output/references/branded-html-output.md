<!-- distilled from alfa skills/branded-html-output -->
<!-- > -->
# Branded Html Output

> "Method over hacks. Evidence over assumption."

## TL;DR

Generate HTML using the MetodologIA brand design system. Source of truth: `references/brand/design-tokens.json` (palette, type, effects) + `references/brand/html-template.html` (structure, slots). Render: navy surface, gold accents, Poppins headings, Trebuchet MS body, glassmorphism, print-ready. Every visual value comes from a token; every claim carries an evidence tag. [DOC]

Tag family for this kit-facing doc: **Alfa core** — `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Never mix with the Jarvis set. Canon: `references/verification-tags.md`. [DOC]

## Procedure

### Step 1: Discover
- Gather requirements from user input; restate scope back before building. [DOC]
- Read existing context and reference materials.
- Load `references/brand/design-tokens.json`. If absent or unparseable → stop and ask; do not invent colors/fonts (`[SUPUESTO]` is not a substitute for the token file). [INFERENCIA]

### Step 2: Analyze
- Structure content into sections that map to template slots.
- Identify data sources (web search, provided docs, codebase) and tag each accordingly. [DOC]
- Confirm output is HTML via brand template (not ad-hoc markup). [DOC]

### Step 3: Execute
- Populate `references/brand/html-template.html`.
- Apply tokens, not literals: navy surface `#122562`, gold accent `#FFD700`, Poppins headings, Trebuchet MS body (Montserrat fallback), JetBrains Mono for code, glassmorphism via `effects`. [CONFIG]
- Replace exactly four template variables: `{{TITLE}}`, `{{SUBTITLE}}`, `{{CONTENT}}`, `{{DATE}}`. Unreplaced `{{...}}` tokens are a hard fail. [CONFIG]

### Step 4: Validate
- Renders with brand aesthetic (Neo-Swiss clean, high contrast, generous whitespace). [CONFIG]
- Content accurate and evidence-tagged; no `[WEB]`-style claim without citation. [DOC]
- Zero raw hex in body markup — colors flow from CSS variables bound to tokens. [INFERENCIA]
- Print layout works (A4/Letter, no clipped content, backgrounds preserved). [DOC]
- No leftover `{{...}}` placeholders; all four slots filled. [CONFIG]

## Quality Criteria

- [ ] Uses MetodologIA brand template (navy `#122562` + gold `#FFD700` + glassmorphism). [CONFIG]
- [ ] All non-obvious content evidence-tagged, one Alfa tag per claim. [DOC]
- [ ] Print-friendly (page breaks sane, colors retained). [DOC]
- [ ] No raw hex in markup — CSS variables only, sourced from tokens. [INFERENCIA]
- [ ] Poppins headings, Trebuchet MS body (Montserrat fallback), JetBrains Mono code. [CONFIG]
- [ ] Every `{{TITLE}}`/`{{SUBTITLE}}`/`{{CONTENT}}`/`{{DATE}}` replaced. [CONFIG]

## Acceptance Criteria (output is "done" when)

- File opens standalone in a browser with fonts + glassmorphism intact (web fonts imported, not assumed installed). [INFERENCIA]
- Diff of rendered HEX values ⊆ `palette` / `paletteExclusive` in tokens. [CONFIG]
- Print preview shows no overflow, no white-on-white, no orphaned headings. [DOC]
- A reviewer can trace each claim to a tag and each color to a token name. [DOC]

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Raw hex colors in HTML | Breaks brand consistency, drifts from tokens | Use CSS variables bound to `design-tokens.json` |
| Generic white background | Not MetodologIA aesthetic | Navy surface `#122562` (token, not literal) |
| Missing evidence tags | Claims without basis | Tag every non-obvious claim, one Alfa tag |
| Hardcoding a color from memory | Tokens are versioned; memory drifts (e.g. navy is `#122562`, not `#0A122A`) | Read the token each run |
| Mixing tag families | Two taxonomies break scannability | Alfa core only in this kit doc |
| Shipping with `{{...}}` left in | Visible template leakage to reader | Fail validation; fill all four slots |
| Assuming fonts are installed | Renders in fallback, off-brand | Keep the `@import` from token `import` URLs |

## Failure Modes

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Token file missing/corrupt | No palette to bind | Stop, request file; never fabricate colors [INFERENCIA] |
| Web font blocked offline | Body renders in fallback | Accept Montserrat fallback for body; flag for reviewer [SUPUESTO] |
| Content exceeds one page | Print clipping | Add page-break rules; re-run print check [DOC] |
| Tokens version bump | Stale colors in output | Re-read tokens (currently `2.0.0`), rebind [CONFIG] |

## Related Skills

- branded-html-output — Base skill for all HTML generation
- guardrails-management — Check user guardrails before generating

## Usage

Example invocations:

- "/branded-html-output" — Run the full branded html output workflow
- "branded html output on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [SUPUESTO]
- Requires English-language output unless otherwise specified. [SUPUESTO]
- Does not replace domain expert judgment for final decisions. [DOC]
- Out of scope: PDF/DOCX/XLSX generation (see sibling refs), live data fetch, or editing the token file itself. [INFERENCIA]
- Token file is canonical over this doc: if a literal here ever disagrees with `design-tokens.json`, the token wins. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Token literal vs. doc mismatch | Trust `design-tokens.json`; treat doc literal as stale [INFERENCIA] |
| Long-form content (multi-page) | Apply print page-break rules; verify in print preview [DOC] |
| Code-heavy output | JetBrains Mono on code blocks, not body font [CONFIG] |
