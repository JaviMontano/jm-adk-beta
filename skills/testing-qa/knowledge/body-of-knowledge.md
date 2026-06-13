# testing-qa — Body of Knowledge

Domain knowledge for routing and executing software testing work across the six
testing-qa disciplines. [DOC]

## Core concepts

### Test levels and shapes
- **Test pyramid** — many fast unit tests, fewer integration, fewest e2e
  (~70/20/10 as a *default*, never a quota). Inverting it produces the
  **ice-cream cone**: a slow, flaky, e2e-heavy suite that signals missing unit
  coverage. [INFERENCE]
- **Testing trophy** — integration-heavy shape that fits thin glue services over
  IO/DB/APIs, where unit tests have little logic to assert. [INFERENCE]
- **Cheapest-layer rule** — push every assertion to the cheapest layer that can
  catch its bug. An e2e test that re-tests business logic is waste; a unit test is
  ~100x faster and non-flaky. [INFERENCE]

### Methodologies
- **TDD (red-green-refactor)** — write a failing test that fails for the *right*
  reason, write minimal code to pass, refactor green. Fits stable, logic-dense,
  regression-prone modules; trades initial velocity for design pressure + a safety
  net. [DOC]
- **Test-after** — fits exploratory/UI spikes and churning requirements; risks
  untested branches and backfill debt. [INFERENCE]
- **BDD / ATDD** — Given/When/Then scenarios written *before* code, traced to a
  requirement (FR-XXX), success criterion (SC-XXX), and principle (P-XXX). Spec
  drives design; tests cannot be retrofitted to green. [DOC]

### Coverage
- Measure on the **diff**, not the whole repo, so legacy gaps do not mask new
  misses; enforce per-module **risk-weighted floors**, not one global number. [CONFIG]
- A global coverage % incentivizes trivial tests on low-risk code; high coverage
  with weak assertions is **coverage theater** — verify with mutation testing on
  critical modules. [INFERENCE]

### Browser engines
- Test by **engine**, not brand: Blink (Chrome/Edge/Opera/Brave), Gecko (Firefox),
  WebKit (Safari macOS+iOS). iOS browsers are forced to WebKit, so Safari covers
  them. Testing four brands but two engines wastes budget. [EXPLICIT]
- **Feature detection** (and `@supports`) over UA sniffing, which breaks silently
  on each new release. Autoprefixer is driven by `browserslist` so the two never
  drift. [EXPLICIT]

### Web performance
- **Core Web Vitals**: LCP < 2.5s, INP < 200ms (INP replaced FID in 2024),
  CLS < 0.1 — all measured at **p75** because CrUX ranks at the 75th percentile,
  so a passing median can still fail real users. [DOC]
- **Lab vs field** — lab (Lighthouse, one device/network) and field (CrUX/RUM)
  diverge; a green lab score with failing CrUX is the classic false pass. [INFERENCE]

## Standards and references
- **Constitution v6.0.0** — enforcement gates, Article XV quality angles for BDD
  (`@functional`, `@a11y`, `@security`, `@perf`, `@seo`, `@offline`, `@ui`,
  `@backend`, `@data`, `@devsecops`, `@cicd`). [DOC]
- **Evidence taxonomy** — Alfa core set, EN spelling per
  `references/verification-tags.md`: `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`,
  `[SUPUESTO]`, `[EXPLICIT]`. One tag per claim, single family. [DOC]
- **CrUX p75 thresholds** — the "Good" bucket Google reports and ranks on. [DOC]
- **Runners** — Vitest/Jest (unit), Testing Library (integration), Playwright /
  Cypress (e2e), Firebase Emulator (security rules), Lighthouse CI (budgets). [CONFIG]

## Decision rules
1. **Routing** — single named dimension → that topic; "where to invest / what to
   test" → `test-strategy`; spec-first browser scenarios → `bdd-full-spectrum`;
   load/latency → `performance-testing`; "increase coverage" with no type →
   `unit-testing`. Read exactly one playbook. [DOC]
2. **Thresholds** — derive from a baseline or recognized standard (CrUX p75, ≥80%
   diff coverage), never a guessed number; tag derived caps `[SUPUESTO]`. [SUPUESTO]
3. **Flake** — quarantine + named owner + fix SLA; never retry a flaky test into
   green. Flake is a correctness failure. [DOC]
4. **Gate** — CI must *fail* (not warn) on a floor/budget breach, and the gate
   itself must be verified to block. Green ≠ success without evidence. [CONFIG]

## Anti-patterns (cross-cutting)
- Reading 2+ playbooks "to compare" instead of routing to one. [INFERENCE]
- Re-testing logic through the UI (e2e) or routing a flow test through unit. [INFERENCE]
- Treating green CI as success when assertions are weak/absent. [DOC]
- UA sniffing instead of feature detection; testing Chromium only. [EXPLICIT]
- Reporting performance at p50, or budgets set only as `warn`. [INFERENCE]
