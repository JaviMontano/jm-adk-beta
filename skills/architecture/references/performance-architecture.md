<!-- distilled from alfa skills/performance-architecture -->
<!-- > -->
# Performance Architecture

> "Performance is a feature." — Jeff Atwood

## TL;DR

Designs web performance optimization strategies targeting Core Web Vitals (LCP, INP, CLS) through lazy loading, code splitting, image optimization, and bundle analysis. Use when Core Web Vitals are poor, page loads are unacceptable, or when setting performance budgets for new projects. [DOC]

**Scope.** Front-end delivery performance: render path, bundle, assets, runtime responsiveness. [DOC]
**Anti-scope (use the linked skill instead):** backend/DB latency, API p99, infra autoscaling, `caching-strategy` (CDN/origin), `pwa-architecture` (offline). Flag and redirect; do not solve here. [INFERENCIA]

## Procedure

### Step 1: Discover
- Measure field Core Web Vitals first (CrUX/RUM), then lab — field is the target, lab is the diagnostic. [INFERENCIA]
- Run Lighthouse and WebPageTest; capture the network waterfall for render-blocking resources.
- Analyze bundle with webpack-bundle-analyzer (or framework equivalent: `@next/bundle-analyzer`, `vite-bundle-visualizer`). [CONFIG]

### Step 2: Analyze
- Identify the LCP element and its full loading path (server TTFB → resource discovery → download → render).
- Find INP bottlenecks: long tasks (>50ms), heavy event handlers, layout thrashing, hydration cost.
- Locate CLS sources: images/embeds without dimensions, dynamic insertion above-fold, late web-font swaps.
- Triage the JS bundle: large deps, dead code, duplicate copies (mismatched semver), unused polyfills.
- Prioritize by impact ÷ effort; fix the LCP path before micro-optimizations. [INFERENCIA]

### Step 3: Execute
- Code splitting: route-based first, then component-level lazy loading for below-fold/interaction-gated UI.
- Images: AVIF/WebP with fallback, responsive `srcset`/`sizes`, explicit width/height, lazy-load below-fold, eager-load the LCP image.
- Reduce render-blocking: inline critical CSS, defer non-critical CSS/JS, `async`/`defer` scripts.
- Resource hints: `preconnect` to critical origins, `preload` the LCP image/font, `prefetch` next-route chunks. Cap preloads — over-preloading steals bandwidth from the LCP resource. [INFERENCIA]
- Fonts: `font-display: swap` (or `optional` to avoid CLS), subset, self-host + preload the critical face.
- Enforce performance budgets in CI (bundle-size ceilings, Lighthouse-CI thresholds) — fail the build, don't warn. [CONFIG]

### Step 4: Validate
- Verify field CWV pass "good": LCP < 2.5s, INP < 200ms, CLS < 0.1 (p75). [DOC]
- Confirm budgets block merges in the CI pipeline, not just report.
- Test on real mid-tier devices with throttled CPU/network — never trust the dev machine. [INFERENCIA]
- Monitor RUM after release; lab gains that don't show in field data are not done. [INFERENCIA]

## Worked example

React/Vite SPA, LCP 4.8s on 4G. Waterfall shows a 320KB main chunk blocking a hero image discovered late. Fixes: route-split the bundle (320KB → 90KB initial), `preload` the hero as AVIF with width/height, self-host + preload the heading font with `font-display: optional`. Result: LCP 2.1s, CLS 0.18 → 0.02, INP unchanged (no heavy handlers). Budget added: initial JS ≤ 120KB gzip, Lighthouse-CI LCP assert. [INFERENCIA]

## Quality Criteria

- [ ] Field CWV meet "good" at p75 (not just lab).
- [ ] Performance budgets defined and **build-blocking** in CI.
- [ ] Images: modern format, responsive `srcset`, explicit dimensions, correct eager/lazy split.
- [ ] JS code-split; non-critical routes/components lazy-loaded.
- [ ] LCP resource preloaded; preloads capped to avoid bandwidth contention.
- [ ] Evidence tags applied to all non-obvious claims (Alfa set). [DOC]

## Anti-Patterns

- Optimizing Lighthouse lab scores while ignoring field data — lab ≠ user experience. [INFERENCIA]
- Premature optimization before measuring the actual LCP/INP/CLS driver.
- Shipping the entire UI framework for a page that needs a static form.
- Lazy-loading the LCP image — defers the one resource that defines LCP. [INFERENCIA]
- Preloading everything — bandwidth contention regresses the LCP element. [INFERENCIA]

## Failure modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Lab/field divergence | Lighthouse green, RUM red | Anchor on CrUX p75; treat lab as diagnostic only |
| Budget bypass | Bundle grows silently | CI assertion blocks merge, not warn-only |
| Hydration INP | Good LCP, poor INP | Reduce client JS, defer/island hydration |
| Font CLS | Layout shift on swap | `font-display: optional` + preload + reserved metrics |
| Duplicate deps | Bundle bloat, no dead code found | Dedupe lockfile; check for mismatched semver copies |

## Related Skills

- `pwa-architecture` — service-worker caching improves repeat-load performance.
- `caching-strategy` — browser/CDN caching reduces server round trips.
- `seo-architecture` — Core Web Vitals influence search ranking.

## Usage

- "/performance-architecture" — run the full workflow.
- "performance architecture on this project" — apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). If absent, stop at Discover and request them. [SUPUESTO]
- English-language output unless otherwise specified. [SUPUESTO]
- CWV thresholds and `bundle-analyzer` tooling assume web targets; native/desktop are out of scope. [SUPUESTO]
- Does not replace domain-expert judgment for final delivery decisions. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements (e.g. rich media vs. budget) | Flag conflict, propose a measured trade-off |
| Out-of-scope request (backend/infra latency) | Redirect to the appropriate skill or escalate |
| No field data available yet | Use lab as proxy, label `[SUPUESTO]`, schedule RUM before sign-off |
