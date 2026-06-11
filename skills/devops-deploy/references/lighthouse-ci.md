<!-- distilled from alfa skills/lighthouse-ci -->
<!-- > -->
# Lighthouse CI

> "What you don't measure, you can't improve. What you don't gate, you can't protect."

## TL;DR

Integrates Lighthouse audits into the CI pipeline using `@lhci/cli`. Defines performance budgets per page type, sets accessibility and SEO thresholds, and blocks merges when scores drop below targets. Enforces Constitution quality gate G2 (Lighthouse >= 90, Accessibility >= 95). Supports local development audits, PR checks, and production URL verification. [EXPLICIT]

## Procedure

### Step 1: Discover
- Check existing CI configuration (`.github/workflows/`)
- Review current Lighthouse scores for the project (if deployed)
- Identify page types: landing pages, app pages, admin pages
- Check for existing performance budgets or `web-vitals` integration

### Step 2: Analyze
- Define budgets per page type:
  - **Landing pages**: Performance >= 95, Accessibility >= 95, SEO >= 95
  - **App pages**: Performance >= 85, Accessibility >= 95, SEO >= 90
  - **Admin pages**: Performance >= 80, Accessibility >= 90
- Define Core Web Vitals targets:
  - FCP < 1.8s, LCP < 2.5s, CLS < 0.1, INP < 200ms
- Plan CI integration: run on PRs against staging, on deploy against production
- Determine assertion strategy: error (block merge) vs warn (notify)

### Step 3: Execute
- Install Lighthouse CI:
  ```bash
  npm install -D @lhci/cli
  ```
- Create `lighthouserc.js`:
  ```javascript
  module.exports = {
    ci: {
      collect: {
        url: ['http://localhost:5000/', 'http://localhost:5000/programs'],
        startServerCommand: 'npx serve public -p 5000',
        numberOfRuns: 3,
      },
      assert: {
        assertions: {
          'categories:performance': ['error', { minScore: 0.90 }],
          'categories:accessibility': ['error', { minScore: 0.95 }],
          'categories:best-practices': ['error', { minScore: 0.90 }],
          'categories:seo': ['warn', { minScore: 0.90 }],
          'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
          'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
          'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        },
      },
      upload: {
        target: 'temporary-public-storage',
      },
    },
  };
  ```
- Add to GitHub Actions:
  ```yaml
  - name: Lighthouse CI
    run: |
      npm install -g @lhci/cli
      lhci autorun
    env:
      LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
  ```
- For production verification post-deploy:
  ```bash
  lhci autorun --collect.url="https://yourdomain.com"
  ```

### Step 4: Validate
- CI runs Lighthouse on every PR (3 runs, median score)
- Budget violations block merge with clear error message
- Scores trend visible over time (temporary public storage or custom server)
- Production URLs meet budgets after deployment
- No false positives from Lighthouse variability (3-run median)

## Quality Criteria

- [ ] `lighthouserc.js` configured with project-specific budgets
- [ ] CI workflow runs Lighthouse on every PR
- [ ] Performance >= 90 enforced (Constitution G2)
- [ ] Accessibility >= 95 enforced (Constitution G2)
- [ ] Core Web Vitals thresholds set (FCP, LCP, CLS)
- [ ] 3 runs per URL for stable median scores
- [ ] Production URL audit runs post-deploy
- [ ] Results uploaded for trend tracking
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Single Lighthouse run | High variance, unreliable | Run 3+ times, use median |
| Warning-only assertions | Scores degrade without enforcement | Use `error` for critical thresholds |
| Only auditing homepage | Other pages may be slow | Audit representative pages per type |
| Ignoring CWV, only checking score | Score can be high with bad CWV | Set explicit CWV thresholds |
| Running only in CI | Developers discover issues late | Add `npm run lighthouse` for local runs |

## Related Skills

- `performance-testing` — Broader performance testing including load testing
- `build-optimization` — Reducing bundle size to meet budgets
- `github-actions-ci` — CI pipeline configuration
- `dual-layer-verification` — Security verification in the same CI pipeline

## Usage

Example invocations:

- "/lighthouse-ci" — Run the full lighthouse ci workflow
- "lighthouse ci on this project" — Apply to current context


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
