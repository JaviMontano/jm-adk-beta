<!-- distilled from alfa skills/lighthouse-ci -->
<!-- > -->
# Lighthouse CI

> "What you don't measure, you can't improve. What you don't gate, you can't protect."

## TL;DR

Integrate Lighthouse audits into CI via `@lhci/cli`. Define performance budgets per page type, set accessibility/SEO thresholds, and block merges when scores drop below target. Enforces Constitution quality gate G2 (Performance >= 90, Accessibility >= 95). Covers local dev audits, PR checks, and post-deploy production verification. [DOC]

**Scope.** This skill configures and gates lab-data Lighthouse runs in CI. It does NOT: run RUM/field-data (use `web-vitals` in-app), load-test (use `performance-testing`), fix the underlying regressions (it only detects them), or audit pages behind auth without an explicit login step. [DOC]

## Procedure

### Step 1: Discover
- Inspect existing CI config (`.github/workflows/`) and any current `lighthouserc.*`.
- Pull current Lighthouse scores if the project is deployed (baseline before gating).
- Enumerate page types: landing, app, admin — each gets its own budget.
- Check for existing `web-vitals` integration so lab thresholds align with field reality.

### Step 2: Analyze
- Budgets per page type (rationale: app/admin trade speed for interactivity/data density, so demanding 95 there causes chronic false failures): [INFERENCIA]
  - **Landing**: Performance >= 95, Accessibility >= 95, SEO >= 95
  - **App**: Performance >= 85, Accessibility >= 95, SEO >= 90
  - **Admin**: Performance >= 80, Accessibility >= 90 (SEO N/A — noindex)
- Core Web Vitals targets (lab proxies): FCP < 1.8s, LCP < 2.5s, CLS < 0.1, TBT < 200ms.
  - **Caveat**: INP is a *field* metric — Lighthouse lab cannot measure it; gate INP via `web-vitals` RUM, gate TBT (its lab proxy) here. [DOC]
- Assertion strategy: `error` (block merge) for hard gates, `warn` (notify) for aspirational/noisy metrics. Decision below.
- Decide trigger surface: PRs against staging build + post-deploy against production URLs.

### Step 3: Execute
- Install:
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
        startServerReadyPattern: 'Accepting connections', // avoid race: wait for server
        numberOfRuns: 3,
        settings: { preset: 'desktop' }, // pin form-factor; mobile is default & stricter
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
          'total-blocking-time': ['error', { maxNumericValue: 200 }],
        },
      },
      upload: { target: 'temporary-public-storage' },
    },
  };
  ```
- GitHub Actions step (pin the version — `@lhci/cli` ships breaking minors): [DOC]
  ```yaml
  - name: Lighthouse CI
    run: |
      npm install -g @lhci/cli@0.14.x
      lhci autorun
    env:
      LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
  ```
- Post-deploy production verification (no server boot — audit the live URL):
  ```bash
  lhci autorun --collect.url="https://yourdomain.com" --collect.startServerCommand=""
  ```
- Local developer audit (catch regressions before pushing):
  ```json
  // package.json
  { "scripts": { "lighthouse": "lhci autorun" } }
  ```

### Step 4: Validate
- CI runs on every PR: 3 runs per URL, median reported.
- Budget violations block merge with a per-assertion error message.
- Score trend visible over time (temporary public storage link, or a self-hosted LHCI server for retention).
- Production URLs meet budgets post-deploy.
- No false positives from Lighthouse variance (3-run median absorbs single-run noise).

## Key decisions & trade-offs

| Decision | Choice | Trade-off / why | Tag |
|---|---|---|---|
| Assertion level for category scores | `error` | Blocks regressions, but flaky infra can red a good PR — pair with 3-run median + pinned form-factor | [DOC] |
| SEO assertion | `warn` | SEO score is config-driven and rarely regresses from code; erroring adds noise without protecting a real gate | [INFERENCIA] |
| `numberOfRuns` | 3 | Higher cuts variance further but is linear in CI minutes; 3 is the documented variance/cost knee | [DOC] |
| Upload target | `temporary-public-storage` | Zero-setup, 7-day public retention; switch to a self-hosted LHCI server when you need history or privacy | [DOC] |
| Form-factor | pinned `desktop` (or `mobile`) | Mixing presets makes scores incomparable across runs; pin one per URL set | [INFERENCIA] |
| INP gate | `web-vitals` RUM, not here | Lighthouse lab cannot synthesize real interactions; TBT is the only honest lab proxy | [DOC] |

## Quality Criteria

- [ ] `lighthouserc.js` configured with project-specific, per-page-type budgets.
- [ ] CI workflow runs Lighthouse on every PR with a pinned `@lhci/cli` version.
- [ ] Performance >= 90 and Accessibility >= 95 enforced as `error` (Constitution G2).
- [ ] CWV lab thresholds set (FCP, LCP, CLS, TBT); INP delegated to RUM.
- [ ] `numberOfRuns: 3` and a pinned form-factor for stable, comparable medians.
- [ ] `startServerReadyPattern` set so audits never race a not-ready server.
- [ ] Production URL audit runs post-deploy.
- [ ] Results uploaded for trend tracking.
- [ ] Evidence tags applied to all non-obvious claims (single family, per `references/verification-tags.md`).

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| `NO_FCP` / blank audit | Audit started before server ready | Set `startServerReadyPattern`; verify `startServerCommand` actually serves the built assets |
| Scores swing ±10 between runs | CI runner CPU contention / single run | Keep `numberOfRuns: 3`; if still noisy, pin throttling or use a dedicated runner |
| PR comment never appears | Missing/invalid `LHCI_GITHUB_APP_TOKEN` | Install the LHCI GitHub App and set the secret; without it autorun still gates but stays silent |
| Accessibility stuck < 95 from one rule | Single axe violation tanks the category | Read the assertion output for the failing audit id; fix the element, don't lower the gate |
| Prod audit fails but staging passed | CDN/cache/cold-start or different bundle | Audit prod twice; compare bundle hashes; warm the route before the gating run |
| `lhci` exits 0 but nothing asserted | `url` array empty or wrong base path | Confirm collected URLs in the run log match the served routes |

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|---|---|---|
| Single Lighthouse run | High variance, unreliable verdict | Run 3+, use median |
| Warning-only on critical thresholds | Scores degrade unenforced | `error` for hard gates |
| Auditing only the homepage | Other page types may be slow | Audit one representative URL per page type |
| Checking score, ignoring CWV | Score can be high with bad LCP/CLS | Set explicit CWV thresholds |
| CI-only, no local script | Devs discover failures late, in PR | Add `npm run lighthouse` |
| Unpinned `@lhci/cli` | Minor bumps silently change scoring | Pin to a known version |
| Lowering the gate to make CI green | Hides the regression you built the gate to catch | Fix the page or document an explicit, reviewed exception |

## Edge Cases

| Scenario | Handling |
|---|---|
| Page behind auth | Add a Puppeteer login script via `collect.puppeteerScript`; without it the audit measures the login screen, not the app |
| SPA client-side route | Audit the rendered route URL directly, or script navigation; a bare base URL may audit an empty shell |
| Dynamic/AB-tested content | Pin a deterministic variant via cookie/flag in the puppeteer script so runs are comparable |
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to `performance-testing` / `web-vitals` or escalate |

## Assumptions & Limits

- Lighthouse lab data approximates, but does not equal, real-user field data; treat it as a regression tripwire, not ground truth. [DOC]
- Assumes access to project artifacts (code, built assets, CI config). [SUPUESTO]
- Assumes a buildable, servable target on the CI runner (or a reachable prod URL). [SUPUESTO]
- English-language output unless otherwise specified. [DOC]
- Does not replace domain-expert judgment for accepting a scored exception. [DOC]

## Related Skills

- `performance-testing` — Broader performance/load testing
- `build-optimization` — Bundle-size reduction to meet budgets
- `github-actions-ci` — CI pipeline configuration
- `dual-layer-verification` — Security verification in the same CI pipeline

## Usage

- "/lighthouse-ci" — Run the full Lighthouse CI workflow
- "lighthouse ci on this project" — Apply to current context
