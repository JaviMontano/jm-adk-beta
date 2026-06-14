<!-- distilled from alfa skills/e2e-testing -->
<!-- Cypress/Playwright E2E testing with page object model, CI integration, and visual assertions -->
# 081 — E2E Testing {Testing}

## Purpose
Validate complete user journeys through the application using Cypress or Playwright. Ensure critical paths work end-to-end against a Firebase test environment with real UI interactions. [DOC]

## Scope & Anti-Scope
- **In scope**: critical user journeys (auth, CRUD, payments, navigation, error states) exercised through real UI. [DOC]
- **Out of scope**: business-logic branches, validation rules, and pure functions — cover those in unit/integration, which are ~100x faster and non-flaky. E2E that re-tests logic is waste. [INFERENCIA]
- **Out of scope**: third-party domains (Stripe Checkout, OAuth provider pages) — stub at the network boundary; you cannot control their DOM or uptime. [INFERENCIA]

## Physics — 3 Immutable Laws

1. **Law of User Truth**: E2E tests simulate real user behavior — clicks, navigation, form fills. No direct API calls or DOM manipulation shortcuts (one exception: seeding state via API in `beforeEach` to reach the page under test faster — never to assert). [DOC]
2. **Law of Critical Path**: Only test critical journeys. E2E is expensive; every test is a flake-risk and CI-minute cost. If a unit test can catch the bug, it belongs in a unit test. [DOC]
3. **Law of Stability**: Use auto-waiting assertions, `data-testid` selectors, and retry logic. Banned: `cy.wait(5000)` / `page.waitForTimeout()`, CSS/XPath structural selectors, and asserting on text that is i18n-translated. [DOC]

## Framework Decision

| Pick | When | Trade-off accepted |
|------|------|--------------------|
| **Playwright** | multi-browser (WebKit/Firefox), parallel sharding, auto-wait, network interception | smaller plugin ecosystem than Cypress [INFERENCIA] |
| **Cypress** | best-in-class debugging DX, time-travel, component testing in same tool | Chromium-family only by default; parallelism needs paid Dashboard or custom sharding [INFERENCIA] |

Default to **Playwright** for new suites: native parallelism and cross-browser coverage matter more than Cypress DX once a suite exceeds ~20 tests. [SUPUESTO] — confirm against the team's existing tooling before standardizing.

## Protocol

### Phase 1 — Framework Setup
1. Pick framework per the table above. [DOC]
2. Configure `playwright.config.ts` / `cypress.config.ts` with `baseURL` → Firebase emulator hosting, plus `retries: 2` (CI) and a single global timeout. [DOC]
3. Create `e2e/pages/` with Page Object Model classes. [DOC]
4. Seed test users via the Auth emulator REST API in global setup; tear down Firestore between specs to keep tests independent. [DOC]

### Phase 2 — Test Authoring
1. Define Page Objects (`LoginPage`, `DashboardPage`, `SettingsPage`) encapsulating selectors + actions; no assertions inside POMs. [DOC]
2. Write scenarios as user stories: `should login and see dashboard`. One journey per test; no shared mutable state across tests. [DOC]
3. Select via `data-testid` exclusively. [DOC]
4. Add visual assertions: screenshot comparison at key states, with a tolerance threshold (see Gates). [DOC]

### Phase 3 — CI Pipeline
1. Run against `firebase emulators:start --only hosting,auth,firestore`; wait on the emulator health endpoint before launching tests (not a fixed sleep). [DOC]
2. Execute headless: `npx playwright test --shard=$i/$n` or `npx cypress run`. [DOC]
3. Generate HTML report + video/trace on failure only (full video on every run bloats artifacts). [DOC]
4. Upload artifacts via `actions/upload-artifact`, gated on `if: failure()`. [DOC]

## Worked Example — Page Object + test (Playwright)

```ts
// e2e/pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}
  goto = () => this.page.goto('/login');
  login = async (email: string, pw: string) => {
    await this.page.getByTestId('email').fill(email);
    await this.page.getByTestId('password').fill(pw);
    await this.page.getByTestId('submit').click();
  };
}
// e2e/auth.spec.ts
test('logs in and lands on dashboard', async ({ page }) => {
  const login = new LoginPage(page);
  await login.goto();
  await login.login('seed@test.dev', 'pw'); // user pre-seeded via Auth emulator
  await expect(page.getByTestId('dashboard-title')).toBeVisible(); // auto-waits
});
```
No raw selectors in the spec; assertion lives in the test, not the POM; auto-wait replaces explicit sleeps. [DOC]

## I/O

| Input | Output |
|-------|--------|
| User journey specification | E2E test file using Page Objects |
| UI components with `data-testid` | Page Object Model class |
| Firebase test environment | Test run against emulators |
| CI trigger | HTML report + failure videos/traces + screenshots |

## Quality Gates — 5 Checks

1. **All critical paths covered** — login, CRUD, navigation, error states. [DOC]
2. **POM enforced** — zero raw selectors in spec files (lint with a custom rule or grep gate). [DOC]
3. **`data-testid` on all interactive elements** — no CSS/XPath. [DOC]
4. **No flake** — suite passes 3 consecutive CI runs; any test failing 1/3 is quarantined, not retried into green. [DOC]
5. **Wall-clock < 5 min** — shard across N runners if exceeded; visual diff tolerance ≤ 0.1% pixels. [DOC]

## Edge Cases
- **Auth token expiration**: seed long-lived tokens or refresh mid-test via the Auth emulator. [DOC]
- **Network latency / failure paths**: use Playwright `route.fulfill()` (or Cypress `cy.intercept()`) to mock slow/500 endpoints — the only reliable way to test error states. [DOC]
- **Responsive**: run critical specs at mobile (375px) and desktop (1280px). [DOC]
- **File uploads**: Cypress `cy.fixture()` / Playwright `setInputFiles()`. [DOC]
- **Animations**: disable CSS transitions in test env to prevent screenshot-timing flake. [INFERENCIA]

## Failure Modes (and the fix)
- **Flaky on `data-testid` change**: testid renamed without updating POM → POM is the single chokepoint; one-line fix, no spec churn. That is the payoff of the POM law. [INFERENCIA]
- **Green locally, red in CI**: timing/viewport/seed-data differences → run the emulator + headless mode locally before blaming CI. [INFERENCIA]
- **Slow creep past 5 min**: tests doing logic verification through the UI → push those down to unit/integration. [INFERENCIA]
- **Screenshot diffs every run**: dynamic content (timestamps, avatars) in the frame → mask those regions or freeze the clock. [INFERENCIA]

## Self-Correction Triggers
- Flaky test (fails 1/3) → quarantine + fix within 24h. [DOC]
- Suite > 5 min → split into parallel shards. [DOC]
- New page without a Page Object → block PR until POM exists. [DOC]
- Visual regression > 0.1% pixel diff → review, then update baseline or fix. [DOC]

## Usage
- "/e2e-testing" — Run the full e2e testing workflow.
- "e2e testing on this project" — Apply to current context.

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [DOC]
- Assumes a runnable Firebase emulator suite; without it, this workflow stalls at Phase 1. [SUPUESTO] — verify `firebase.json` declares the emulator ports.
- English-language output unless otherwise specified. [DOC]
- Does not replace domain-expert judgment for final decisions. [DOC]
