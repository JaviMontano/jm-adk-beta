<!-- distilled from alfa skills/performance-testing -->
<!-- > -->
# Performance Testing

> "Performance is a feature — and the only one every user experiences." — Unknown

## TL;DR

Guides web performance measurement and optimization — running Lighthouse CI in pipelines, analyzing bundle sizes, monitoring Core Web Vitals (LCP, INP, CLS), and setting performance budgets. Use when establishing performance baselines, debugging slow pages, or preventing performance regressions. [EXPLICIT]

## Procedure

### Step 1: Discover
- Run Lighthouse audit on key pages (home, listing, detail, checkout)
- Check current Core Web Vitals from Chrome UX Report or Search Console
- Analyze bundle size with `source-map-explorer` or `webpack-bundle-analyzer`
- Identify render-blocking resources and long tasks in DevTools Performance tab

### Step 2: Analyze
- Set performance budgets: LCP < 2.5s, INP < 200ms, CLS < 0.1
- Identify the top 3 performance bottlenecks from Lighthouse diagnostics
- Evaluate bundle splitting opportunities (route-based, component lazy loading)
- Determine if SSR/SSG would improve initial load performance

### Step 3: Execute
- Set up Lighthouse CI in GitHub Actions with performance budget assertions
- Configure bundle size tracking (bundlesize, size-limit) in CI
- Implement code splitting with dynamic `import()` for route-level chunks
- Add `web-vitals` library for real-user monitoring (RUM) in production
- Optimize render-blocking CSS and JavaScript (defer, async, critical CSS)
- Set up WebPageTest for detailed waterfall analysis on key pages

### Step 4: Validate
- Lighthouse CI passes with scores above budget thresholds
- Bundle size stays within defined limits across PRs
- Core Web Vitals meet "Good" thresholds for 75th percentile of users
- No performance regressions detected between releases

## Quality Criteria

- [ ] Lighthouse CI runs on every PR with budget assertions
- [ ] Bundle size tracked and enforced with size limits
- [ ] Core Web Vitals monitored in production with RUM data
- [ ] Performance budgets documented and enforced in CI
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Only testing performance in development mode (production builds differ significantly)
- Measuring only lab data without real-user monitoring
- Setting performance budgets but not enforcing them in CI

## Related Skills

- `build-optimization` — bundle optimization directly impacts performance metrics
- `image-optimization` — images are the largest contributor to page weight

## Usage

Example invocations:

- "/performance-testing" — Run the full performance testing workflow
- "performance testing on this project" — Apply to current context


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
