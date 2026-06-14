<!-- distilled from alfa skills/landing-page-builder -->
<!-- High-conversion landing page. Hero, features, testimonials, pricing, CTA, footer sections. SEO optimized. Hostinger deploy. [EXPLICIT] -->
# landing-page-builder {Frontend} (v1.1)
> **"Ship pixels that perform, accessible by default."**
## Purpose
High-conversion landing page. Hero, features, testimonials, pricing, CTA, footer sections. SEO optimized. Hostinger deploy. [EXPLICIT]
**When to use:** Frontend development within the Firebase/Google/Hostinger stack. [EXPLICIT]
**Anti-scope (do NOT use for):** backend/API logic, multi-page app routing, CMS authoring, A/B-test infra, paid-ads landers requiring tag managers — route to the owning skill. [INFERENCIA]
## Core Principles
1. **Law of Semantics:** HTML first, CSS second, JS third. Semantic markup is non-negotiable. [EXPLICIT]
2. **Law of Performance:** Lighthouse > 90. Lazy load images. Code-split routes. Critical CSS inline. [EXPLICIT]
3. **Law of Accessibility:** WCAG 2.1 AA minimum. Keyboard navigable. Screen reader tested. ARIA where needed. [EXPLICIT]
4. **Law of Conversion:** one primary CTA per viewport; above-the-fold hero states value in <5s read; trust signals (testimonials/logos) precede pricing. [INFERENCIA]
## Core Process
### Phase 1: Structure
1. Define page/component structure with semantic HTML5 (`<header><main><section><article><footer>`, single `<h1>`). [EXPLICIT]
2. Apply design tokens from `.agent/.shared/design-tokens.md`. If absent → derive a minimal token set, flag for review, do not hardcode hex inline. [EXPLICIT]
3. Configure responsive breakpoints (mobile-first): base ≤480, sm 481–768, md 769–1024, lg ≥1025. [EXPLICIT]
### Phase 2: Build
1. Implement with framework (React/Angular) or vanilla HTML/CSS/JS. **Decision:** vanilla when page is static + SEO-critical (smaller bundle, faster LCP); framework when interactivity/state is required. Trade-off: framework adds hydration cost vs. vanilla adds manual DOM wiring. [INFERENCIA]
2. Integrate Firebase services (Auth, Firestore listeners, Storage). Lazy-init SDK after first paint to protect LCP. [EXPLICIT]
3. Add loading/error/empty states for every async operation; never leave a blank frame. [EXPLICIT]
### Phase 3: Validate
1. Run Lighthouse audit (> 90 on all four categories: Perf, A11y, Best-Practices, SEO). [EXPLICIT]
2. Run accessibility audit (axe-core) — zero critical/serious violations. [EXPLICIT]
3. Test on mobile, tablet, desktop breakpoints + keyboard-only + one screen reader pass. [EXPLICIT]
4. Verify deploy artifact: built assets fingerprinted, sitemap.xml + robots.txt present before Hostinger upload. [INFERENCIA]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Requirements/spec | Text/File | Yes | What to build (sections, copy, brand) |
| Design tokens | File | No | `.agent/.shared/design-tokens.md`; derived if missing |
| Assets (images/logos) | Files | No | Pre-optimized; else compressed during build |
| Output | Type | Description |
|--------|------|-------------|
| Source files | HTML/CSS/JS/TSX | Production-ready, fingerprinted code |
| SEO artifacts | XML/TXT | sitemap.xml, robots.txt, meta/OG tags |
| Audit report | Text | Lighthouse + axe scores vs. gate |
## Validation Gate (all required — ship blocked if any fail)
- [ ] Semantic HTML5 structure; exactly one `<h1>` [EXPLICIT]
- [ ] Responsive on all breakpoints, no horizontal scroll [EXPLICIT]
- [ ] Lighthouse > 90 on all four categories [EXPLICIT]
- [ ] WCAG 2.1 AA: axe zero critical/serious; visible focus; alt text on all images [EXPLICIT]
- [ ] Firebase integration working; async paths have loading/error/empty states [EXPLICIT]
- [ ] SEO: unique title + meta description, OG tags, sitemap + robots present [INFERENCIA]
## 5. Self-Correction Triggers
> [!WARNING]
> IF div soup without semantic elements THEN refactor to semantic HTML5. [EXPLICIT]
> IF Lighthouse < 90 THEN optimize before shipping (LCP image, unused JS/CSS, font display). [EXPLICIT]
> IF axe reports critical/serious THEN fix before deploy; never waive A11y for deadline. [INFERENCIA]
> IF design-tokens.md missing THEN derive + flag; never inline raw hex. [INFERENCIA]
> IF >1 `<h1>` or skipped heading levels THEN restructure outline. [INFERENCIA]

## Failure Modes (symptom → likely cause → fix)
| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Low LCP / Perf <90 | Unoptimized hero image, render-blocking CSS | Compress + `loading="eager"` on hero only, inline critical CSS, defer rest [INFERENCIA] |
| CLS jank | Images without width/height, late-loading fonts | Set intrinsic dimensions, `font-display: swap` [INFERENCIA] |
| Firebase blocks paint | SDK loaded in head, synchronous | Lazy-init after first paint [EXPLICIT] |
| Keyboard trap / no focus ring | Custom controls missing ARIA + focus styles | Add roles, `tabindex`, visible `:focus-visible` [INFERENCIA] |
| Pages not indexed | Missing meta/sitemap/robots | Generate SEO artifacts in Phase 3 [INFERENCIA] |

## Worked Example
Spec: "SaaS pricing lander, 3 tiers, hero + 4 features + 2 testimonials + FAQ + CTA, static."
1. **Structure:** `<header>` nav → `<main>`: hero `<section>` (single `<h1>`, primary CTA) → features `<section>` (4 `<article>`) → testimonials → pricing (3 `<article>`) → FAQ (`<details>`) → CTA → `<footer>`. [INFERENCIA]
2. **Decision:** vanilla HTML/CSS (static, SEO-critical) → smallest bundle, best LCP. [INFERENCIA]
3. **Build:** mobile-first CSS, hero image `<picture>` AVIF+fallback, lazy-load below-fold images, critical CSS inline. [INFERENCIA]
4. **Validate:** Lighthouse 96/100/100/100, axe clean, keyboard pass, sitemap+robots emitted → gate passes → Hostinger deploy. [INFERENCIA]

## Usage
Example invocations:
- "/landing-page-builder" — Run the full landing page builder workflow
- "landing page builder on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Targets static/low-interactivity landers; complex SPA routing is out of scope [INFERENCIA]
- Hostinger is the assumed deploy target; other hosts need adapted artifact/upload steps [INFERENCIA]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Missing design tokens | Derive minimal set, flag for review, never inline hex |
| Brand/copy absent | Use neutral placeholders, mark `TODO:` for owner |
| Asset-heavy (>10 images) | Enforce compression + lazy-load to protect LCP |
