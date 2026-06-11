<!-- distilled from alfa skills/performance-architecture -->
<!-- > -->
# Performance Architecture

> "Performance is a feature." — Jeff Atwood

## TL;DR

Designs web performance optimization strategies targeting Core Web Vitals (LCP, INP, CLS) through lazy loading, code splitting, image optimization, and bundle analysis. Use this skill when Core Web Vitals scores are poor, page load times are unacceptable, or when building performance budgets for new projects. [EXPLICIT]

## Procedure

### Step 1: Discover
- Measure current Core Web Vitals: LCP, INP (Interaction to Next Paint), CLS
- Run Lighthouse and WebPageTest for detailed performance audit
- Analyze bundle size with webpack-bundle-analyzer or similar
- Review network waterfall for render-blocking resources

### Step 2: Analyze
- Identify LCP element and optimize its loading path
- Find INP bottlenecks: long tasks, heavy event handlers, layout thrashing
- Locate CLS sources: images without dimensions, dynamic content insertion, font loading
- Analyze JavaScript bundle: identify large dependencies, dead code, duplicates
- Prioritize optimizations by impact vs. effort

### Step 3: Execute
- Implement code splitting: route-based and component-based lazy loading
- Optimize images: modern formats (WebP, AVIF), responsive srcset, lazy loading
- Reduce render-blocking: defer non-critical CSS/JS, inline critical CSS
- Set up performance budgets in CI (bundle size limits, Lighthouse thresholds)
- Implement resource hints: preload, prefetch, preconnect for critical resources
- Optimize fonts: font-display: swap, subset, preload critical fonts

### Step 4: Validate
- Verify Core Web Vitals pass "good" thresholds (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- Confirm performance budgets are enforced in CI pipeline
- Test on real devices with throttled connections (not just fast dev machines)
- Monitor RUM (Real User Monitoring) data for field performance

## Quality Criteria

- [ ] Core Web Vitals meet "good" thresholds in field data
- [ ] Performance budgets are defined and enforced in CI
- [ ] Images use modern formats with responsive srcset
- [ ] JavaScript is code-split with lazy loading for non-critical routes
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Optimizing for Lighthouse lab scores while ignoring field data
- Premature optimization without measuring what actually matters
- Loading entire UI framework for a page that needs a simple form

## Related Skills

- `pwa-architecture` — service worker caching improves load performance
- `caching-strategy` — browser and CDN caching reduce server round trips
- `seo-architecture` — Core Web Vitals impact search ranking

## Usage

Example invocations:

- "/performance-architecture" — Run the full performance architecture workflow
- "performance architecture on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
