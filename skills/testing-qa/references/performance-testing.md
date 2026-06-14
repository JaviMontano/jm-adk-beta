<!-- distilled from alfa skills/performance-testing -->
<!-- > -->
# Performance Testing

> "Performance is a feature — and the only one every user experiences." — Unknown

## TL;DR

Guides web performance measurement and optimization: Lighthouse CI in pipelines, bundle-size analysis, Core Web Vitals (LCP, INP, CLS) monitoring, and enforced performance budgets. Use when establishing baselines, debugging slow pages, or preventing regressions. [DOC]

## Scope

In scope: front-end load/render performance for web apps — lab (synthetic) + field (RUM) measurement, budget definition, CI enforcement, code splitting. [DOC]
Anti-scope (use another skill): back-end/API latency and throughput load testing (k6, Gatling, JMeter); database query tuning; native mobile app profiling; infra capacity planning. [INFERENCIA] Performance budgets here gate front-end delivery, not server SLOs. [SUPUESTO] → verify with the team's SLO owner before reusing thresholds.

## Procedure

### Step 1: Discover
- Run Lighthouse audit on key pages (home, listing, detail, checkout) — audit the deployed production build, not dev, since dev bundles are unminified and skip tree-shaking. [DOC]
- Read field data (real users) from Chrome UX Report (CrUX) or Search Console; lab and field diverge because lab uses one fixed device/network profile. [DOC]
- Analyze bundle with `source-map-explorer` or `webpack-bundle-analyzer`; requires source maps emitted at build. [CONFIG]
- Identify render-blocking resources and long tasks (>50ms) in the DevTools Performance tab. [DOC]

### Step 2: Analyze
- Set budgets (the "Good" CrUX thresholds, measured at p75): LCP < 2.5s, INP < 200ms, CLS < 0.1. [DOC] Rationale: Google ranks and reports CWV at the 75th percentile, so a passing median can still fail real users. [DOC]
- Add a secondary lab budget so CI fails before field data degrades: Lighthouse performance score >= 90, total JS transfer <= a per-project byte cap. [SUPUESTO] → set the cap from the current bundle baseline, not a guessed number.
- Rank the top 3 bottlenecks from Lighthouse diagnostics by estimated savings (ms), not by count of warnings. [INFERENCIA]
- Evaluate bundle splitting (route-based first, then component lazy-load). Trade-off: more chunks cut initial JS but add request overhead and risk waterfall stalls on slow links — split by route boundary, not per-component, unless a component is both heavy and below the fold. [INFERENCIA]
- Decide SSR/SSG vs CSR. SSG wins for static, cacheable content (fastest LCP, no server cost per request); SSR wins when content is per-request dynamic; CSR is acceptable only for low-traffic, auth-gated app shells. [INFERENCIA] Trade-off: SSR shifts cost to TTFB and server load, and can worsen INP via hydration. [DOC]

### Step 3: Execute
- Set up Lighthouse CI in CI (e.g. GitHub Actions) with budget assertions that fail the build on breach. [CONFIG]
- Track bundle size with `bundlesize` or `size-limit`; fail the PR when a chunk exceeds its cap. [CONFIG]
- Implement code splitting via dynamic `import()` at route-level chunks. [CODE]
- Add the `web-vitals` library for RUM, sending LCP/INP/CLS to an analytics sink in production. [CODE]
- Optimize render-blocking CSS/JS: `defer`/`async` scripts, inline critical CSS, lazy-load the rest. [DOC]
- Use WebPageTest for waterfall analysis on key pages when CI numbers regress but the cause is unclear. [DOC]

### Step 4: Validate
- Lighthouse CI passes with scores at/above budget thresholds. [CONFIG]
- Bundle size stays within limits across PRs (no silent creep). [CONFIG]
- CWV meet "Good" at p75 in field data (CrUX/RUM), not just in lab. [DOC]
- No regressions between releases — compare against the previous tagged release, not against an arbitrary local run. [INFERENCIA]

## Worked example: Lighthouse CI budget gate

`lighthouserc` assertion block (conceptual): [CONFIG]
```
assertions:
  categories:performance: ["error", { minScore: 0.9 }]
  largest-contentful-paint: ["error", { maxNumericValue: 2500 }]
  cumulative-layout-shift: ["error", { maxNumericValue: 0.1 }]
  total-byte-weight: ["warn",  { maxNumericValue: <project cap> }]
```
`error` blocks the merge; `warn` surfaces creep without blocking. Run against 3+ runs per URL and use the median to damp variance. [DOC]

## Quality Criteria

- [ ] Lighthouse CI runs on every PR with budget assertions that block on breach
- [ ] Bundle size tracked and enforced with per-chunk caps derived from baseline
- [ ] CWV monitored in production via RUM (field), reported at p75
- [ ] Budgets documented, version-controlled, and enforced in CI
- [ ] INP measured (not legacy FID) — INP replaced FID as a Core Web Vital in 2024 [DOC]
- [ ] Evidence tags applied to all non-obvious claims

## Anti-Patterns & Failure Modes

- Testing performance only in dev mode — production builds minify, tree-shake, and compress; dev numbers mislead. [DOC]
- Measuring only lab data — lab cannot see real device/network diversity; a green Lighthouse score with failing CrUX is the classic false pass. [INFERENCIA]
- Setting budgets but only as `warn` — an unenforced budget is documentation, not a gate. [INFERENCIA]
- Reporting at the median (p50) — hides the slow tail that CrUX ranks on (p75). [DOC]
- Over-splitting bundles — too many tiny chunks add request overhead and can regress LCP on high-latency links. [INFERENCIA]
- Optimizing by warning count instead of estimated ms savings — burns effort on cosmetic wins. [INFERENCIA]
- Flaky CI from single-run measurement — synthetic runs vary; without median-of-N the gate produces false failures. [DOC]

## Related Skills

- `build-optimization` — bundle optimization directly drives load metrics
- `image-optimization` — images are often the largest contributor to page weight and LCP

## Usage

Example invocations:

- "/performance-testing" — Run the full performance testing workflow
- "performance testing on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, build config, deployed URL). [SUPUESTO] → if no deployed/production build exists, baseline against a production-mode local build, never dev.
- Requires a source-map-emitting build for bundle analysis; without it, size attribution is unavailable. [CONFIG]
- Field data (CrUX) requires sufficient real-user traffic; low-traffic or pre-launch sites have no CrUX dataset — fall back to lab + a private RUM sink. [INFERENCIA]
- English-language output unless otherwise specified. [SUPUESTO]
- Does not replace domain-expert judgment for final release decisions. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements (e.g. tight budget vs heavy feature) | Flag conflict explicitly, propose phased budget or scope cut |
| Out-of-scope request (API/load/DB perf) | Redirect to a back-end load-testing skill or escalate |
| No CrUX/field data (low traffic, pre-launch) | Use lab + private RUM; flag that field validation is deferred |
| No source maps available | Report bundle size only at chunk granularity; flag attribution gap |
| CI numbers flaky | Switch to median-of-N runs per URL before tightening thresholds |
