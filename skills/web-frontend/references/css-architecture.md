<!-- distilled from alfa skills/css-architecture -->
<!-- CSS methodology selection (BEM/utility-first). Custom properties system. Container queries. CSS layers. Dark mode. [EXPLICIT] -->
# css-architecture {Frontend} (v1.1)
> **"Ship pixels that perform, accessible by default."**
## Purpose
CSS methodology selection (BEM/utility-first). Custom properties system. Container queries. CSS layers. Dark mode. [EXPLICIT]
**When to use:** Frontend development within the Firebase/Google/Hostinger stack.
**Anti-scope:** Not for design-token *authoring* (see `design-tokens.md`), backend/data modeling, or framework choice (assumes stack is already fixed). [INFERENCIA]
## Core Principles
1. **Law of Semantics:** HTML first, CSS second, JS third. Semantic markup is non-negotiable. [EXPLICIT]
2. **Law of Performance:** Lighthouse > 90. Lazy load images. Code-split routes. Critical CSS inline. [EXPLICIT]
3. **Law of Accessibility:** WCAG 2.1 AA minimum. Keyboard navigable. Screen reader tested. ARIA where needed. [EXPLICIT]
## Architecture Decisions (decide once, justify, then move)
| Decision | Default | When to deviate | Trade-off |
|----------|---------|-----------------|-----------|
| Methodology | Utility-first (Tailwind) for app UI | BEM when shipping a shared component lib consumed outside the build | Utility = fast/low-specificity but verbose markup; BEM = readable classes but specificity creep [INFERENCIA] |
| Layering | `@layer reset, tokens, base, components, utilities` | Skip only on <3-file projects | Explicit layers kill specificity wars; cost is one-time setup [INFERENCIA] |
| Responsiveness | Container queries (`@container`) for reusable components | Media queries for page-level/viewport concerns (nav, grid) | Container queries make components context-agnostic; ~96% browser support, gate critical paths [SUPUESTO] |
| Theming | CSS custom properties on `:root` + `[data-theme]` | CSS-in-JS only if runtime theming is dynamic per-user | Custom props = zero-JS theme swap; CSS-in-JS adds bundle + runtime cost [INFERENCIA] |
| Dark mode | `prefers-color-scheme` + manual `[data-theme]` override | Forced single theme by brand mandate | Respect OS pref AND allow toggle; storing choice in `localStorage` avoids flash [INFERENCIA] |
## Core Process
### Phase 1: Structure
1. Define page/component structure with semantic HTML5. [EXPLICIT]
2. Apply design tokens from `.agent/.shared/design-tokens.md` as custom properties; never hardcode hex/px that a token covers. [EXPLICIT]
3. Configure responsive breakpoints (mobile-first); declare `@layer` order before any rule. [EXPLICIT]
### Phase 2: Build
1. Implement with framework (React/Angular) or vanilla HTML/CSS/JS. [EXPLICIT]
2. Integrate Firebase services (Auth, Firestore listeners, Storage). [EXPLICIT]
3. Add loading/error/empty states for every async operation; reserve layout space to avoid CLS. [EXPLICIT]
### Phase 3: Validate
1. Run Lighthouse audit (> 90 on all categories). [EXPLICIT]
2. Run accessibility audit (axe-core); zero serious/critical violations. [EXPLICIT]
3. Test on mobile, tablet, desktop breakpoints + forced dark mode + 200% zoom. [EXPLICIT]
## Worked Example: token-driven dark-mode button
```css
@layer tokens {
  :root { --btn-bg: #2563eb; --btn-fg: #fff; --space-2: .5rem; }
  [data-theme="dark"] { --btn-bg: #3b82f6; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) { --btn-bg: #3b82f6; }
  }
}
@layer components {
  .btn { background: var(--btn-bg); color: var(--btn-fg); padding: var(--space-2) 1rem; }
  .btn:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; } /* a11y */
}
```
Result: OS-pref dark mode that a `[data-theme]` toggle can override, no `!important`, focus visible. [INFERENCIA]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Requirements/spec | Text/File | Yes | What to build |
| Design tokens | File | If themed | `design-tokens.md`; absent → request before styling |
| Output | Type | Description |
|--------|------|-------------|
| Source files | HTML/CSS/JS/TSX | Production-ready code |
## Validation Gate (acceptance criteria — all must pass)
- [ ] Semantic HTML5 structure (no div-soup for interactive elements)
- [ ] Responsive on all breakpoints, mobile-first, no horizontal scroll at 320px
- [ ] Lighthouse > 90 (Perf, A11y, Best-Practices, SEO)
- [ ] WCAG 2.1 AA: contrast ≥ 4.5:1 text, visible focus, keyboard-reachable
- [ ] Dark mode renders with no flash-of-wrong-theme (FOUC) and correct contrast
- [ ] `@layer` order declared; zero `!important` in component layer
- [ ] Firebase integration working with loading/error/empty states
## 5. Self-Correction Triggers
> [!WARNING]
> IF div soup without semantic elements THEN refactor to semantic HTML5.
> IF Lighthouse < 90 THEN optimize before shipping.
> IF `!important` appears in components THEN reorder `@layer` instead.
> IF specificity war emerges THEN move rules into the correct layer, do not raise selectors.
> IF dark-mode flash on load THEN inline a blocking script that sets `[data-theme]` before first paint.
## Failure Modes (anticipate)
| Failure | Cause | Mitigation |
|---------|-------|------------|
| Theme flash (FOUC) | Theme set after hydration | Set `[data-theme]` in inline `<head>` script pre-paint [INFERENCIA] |
| Layout shift (CLS) | Async content w/o reserved space | Skeletons + fixed aspect-ratio boxes [INFERENCIA] |
| Specificity creep | Nested overrides / `!important` | Enforce `@layer` order; lint with stylelint [INFERENCIA] |
| Container queries unsupported | Old browser | Feature-query `@supports (container-type: inline-size)` fallback to media queries [SUPUESTO] |
## Usage
Example invocations:
- "/css-architecture" — Run the full css architecture workflow
- "css architecture on this project" — Apply to current context
## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes target browsers support CSS custom properties, `@layer`, and `@container`; otherwise apply documented fallbacks [SUPUESTO]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No design tokens provided | Request `design-tokens.md` before styling; do not invent palette |
| Brand forbids dark mode | Lock `[data-theme="light"]`, skip `prefers-color-scheme` |
