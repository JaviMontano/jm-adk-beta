<!-- distilled from alfa skills/portfolio-sites -->
<!-- > -->
# Portfolio Sites

> "Your portfolio is your reputation made visible." — Unknown

## TL;DR

Builds portfolio and showcase sites — project galleries, case studies, tasteful scroll animation, working contact forms. Use for personal portfolios, agency showcases, creative-pro sites. [DOC]

## Scope & Anti-Scope

- IN: static/SSG/SPA portfolios, case-study pages, filterable galleries, contact capture, image/perf optimization. [DOC]
- OUT: CMS authoring backends, auth/paywalls, e-commerce, blog engines, multi-tenant dashboards — redirect to the matching skill. [SUPUESTO] Verify by checking whether the brief needs persisted user state; if yes, it is out of scope.

## Procedure

### Step 1: Discover
- Identify owner goal (job search, freelance leads, agency branding) — it sets the primary CTA and which sections lead. [INFERENCIA]
- Collect project assets (screenshots, descriptions, tech stacks, measurable outcomes).
- Capture brand elements (colors, type, tone) and accessibility floor (WCAG AA contrast). [DOC]
- Decide sections (about, projects, skills, testimonials, contact) and their order.

### Step 2: Analyze
- Pick gallery format (grid, carousel, filterable cards). Default: responsive grid + filter — predictable, indexable, low-risk. [SUPUESTO] Confirm against project count (<6 → single column; 6–30 → grid; >30 → add search/pagination).
- Lock case-study template: challenge → approach → solution → results.
- Choose animation strategy. Trade-off: CSS transitions (cheapest, ships least JS) > Framer Motion (React-native ergonomics, bundle cost) > GSAP (most control, heaviest, licensing for some plugins). Default to CSS unless choreography demands a library. [INFERENCIA]
- Plan hosting/domain (custom domain, SSL, CDN).

### Step 3: Execute
- Build responsive layout: hero, clear nav, semantic landmarks (`<header><nav><main><footer>`). [DOC]
- Implement gallery with category filtering and modal or dedicated detail pages. Prefer real routed pages over modals when content is SEO-relevant (case studies should be crawlable). [INFERENCIA]
- Write case-study pages with before/after visuals and quantified outcomes.
- Add scroll animation gated behind `prefers-reduced-motion`; ship the static layout as the no-JS baseline. [DOC]
- Build contact form with client + server validation, honeypot/turnstile spam guard, and email delivery (Formspree, Cloud Function). [DOC]
- Optimize images: lazy-load below the fold, responsive `srcset`/`sizes`, modern formats (AVIF/WebP with fallback), explicit `width`/`height` to reserve space. [DOC]

### Step 4: Validate
- Performance: LCP < 2.5s, CLS < 0.1 on a mid-tier mobile profile (Lighthouse mobile). [DOC]
- Verify every project link, image, and external URL resolves (no 404s, no mixed content).
- Check mobile layout — recruiters/clients often open on phones first. [INFERENCIA]
- Confirm the form delivers AND renders explicit success/error states; test the failure path (network down, validation reject), not just the happy path. [INFERENCIA]
- Run an axe/Lighthouse a11y pass: focus order, alt text, contrast, keyboard-only nav.

## Worked Example

Freelance designer, 8 projects, goal = inbound leads.
- Discover: CTA is "Hire me"; testimonials and contact lead. [SUPUESTO]
- Analyze: 8 projects → grid + tag filter; CSS-only fades (no choreography need). [INFERENCIA]
- Execute: routed `/work/<slug>` case studies for SEO; Formspree + Turnstile; AVIF hero with WebP fallback.
- Validate: mobile LCP 1.9s, CLS 0.02, axe clean, form failure path shows inline retry. [SUPUESTO] Numbers illustrative — re-measure on the real build.

## Quality Criteria

- [ ] Projects show measurable outcomes, not just screenshots.
- [ ] LCP < 2.5s and CLS < 0.1 on mobile with optimized media. [DOC]
- [ ] Animations run ~60fps and honor `prefers-reduced-motion`.
- [ ] Contact form works reliably with spam protection and a tested error path.
- [ ] Passes axe/Lighthouse a11y (focus, alt, contrast, keyboard).
- [ ] Every non-obvious claim carries one tag from the Alfa core family. [DOC]

## Failure Modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Layout jumps as images load | No reserved dimensions | Set explicit `width`/`height` or `aspect-ratio`. [DOC] |
| Form "sends" but nothing arrives | Silent provider error, no error UI | Surface server response; test failure path. [INFERENCIA] |
| Janky scroll on mobile | JS-driven scroll / heavy reflow | Use CSS transforms; throttle; respect reduced-motion. [DOC] |
| Case studies not indexed | Content trapped in modals/JS | Render as routed pages with real URLs. [INFERENCIA] |
| Looks generic to reviewers | Unmodified template | Customize type, spacing, color, copy. [DOC] |

## Anti-Patterns

- Over-animating — the portfolio becomes about effects, not the work.
- Screenshots without context (no problem statement, no result).
- Shipping a template untouched (reads as generic).
- Blocking first paint on hero video or web fonts (FOIT, slow LCP). [INFERENCIA]

## Related Skills

- `image-optimization` — critical for fast-loading galleries.
- `scroll-interaction` — tasteful scroll-driven animation.

## Usage

Example invocations:

- "/portfolio-sites" — Run the full portfolio sites workflow.
- "portfolio sites on this project" — Apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [DOC]
- English-language output unless otherwise specified. [DOC]
- Static/SSG/SPA only; needs an external service for form delivery and any dynamic backend. [SUPUESTO] Confirm a delivery endpoint exists before building the form.
- Does not replace domain-expert judgment for final decisions. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding. |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. |
| Out-of-scope request (CMS, auth, e-commerce) | Redirect to the appropriate skill or escalate. |
| No project outcomes available | Use qualitative impact; flag the gap, do not fabricate metrics. [SUPUESTO] |
| Single project | Drop the grid; use one long-form case study as the homepage. [INFERENCIA] |
