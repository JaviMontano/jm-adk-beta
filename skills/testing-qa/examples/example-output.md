# Example Output — testing-qa

Worked deliverable for the `login → add card → place order` journey request.

## 1. Routing decision
- **Topic chosen:** `e2e-testing`
- **Depth:** `deep`
- **Why this route:** a multi-service *user journey* fails in production despite
  green units — the gap is integration through real UI, the cheapest layer that
  catches it is e2e, not unit. Not `performance-testing` (no load/latency framing)
  and not `bdd-full-spectrum` (no spec-first Gherkin requested). [INFERENCE]
- **Playbook Read:** `references/e2e-testing.md` (exactly one). [DOC]

## 2. Target under test
- **Artifact:** checkout SPA route flow `/login` → `/cart` → `/order/confirm`.
- **Environment:** `firebase emulators:start --only hosting,auth,firestore`;
  Playwright `baseURL` → emulator hosting. [CONFIG]

## 3. Discover
- Units green but journey breaks → classic missing-integration-seam signal; the
  bug lives in service composition, not pure logic. [INFERENCE]
- Critical path, business-unacceptable failure → qualifies for the small e2e set. [INFERENCE]

## 4. Analyze
- **Framework:** Playwright (multi-engine, native parallelism, network
  interception) over Cypress for a growing suite. [SUPUESTO]
- **Selectors:** `data-testid` only; no CSS/XPath. [DOC]
- **State seeding:** seed the test user via the Auth emulator REST API in
  `beforeEach` to reach the page faster — never to assert. [DOC]

## 5. Execute
```ts
// e2e/pages/CheckoutPage.ts  (Page Object — no assertions inside)
export class CheckoutPage {
  constructor(private page: Page) {}
  addCard = async (num: string) => {
    await this.page.getByTestId('card-number').fill(num);
    await this.page.getByTestId('save-card').click();
  };
  placeOrder = () => this.page.getByTestId('place-order').click();
}

// e2e/checkout.spec.ts
test('logs in, adds a card, and places an order', async ({ page }) => {
  const login = new LoginPage(page);
  const checkout = new CheckoutPage(page);
  await login.goto();
  await login.login('seed@test.dev', 'pw');      // user pre-seeded via Auth emulator
  await checkout.addCard('4242424242424242');
  await checkout.placeOrder();
  await expect(page.getByTestId('order-confirmation')).toBeVisible(); // auto-waits
});
```
CI: run against emulators, wait on the health endpoint (not a fixed sleep),
`npx playwright test --shard=$i/$n`, upload traces `if: failure()`. [CONFIG]

## 6. Validate (run before "done")
| Check | Command / evidence | Result | Status |
|-------|--------------------|--------|--------|
| Critical path covered | `npx playwright test checkout.spec.ts` | 1 passed | pass [CONFIG] |
| No flake | 3 consecutive CI runs | 3/3 green | pass [CONFIG] |
| POM enforced | grep for raw selectors in specs | 0 found | pass [CONFIG] |
| Gate blocks merge | force a failure, confirm CI red | merge blocked | pass [CONFIG] |

- Green is asserted only because the journey assertion is observable
  (`order-confirmation` visible) and the run output is attached, not from prose. [INFERENCE]

## 7. Quality criteria (from e2e-testing playbook)
- [x] Critical journey covered through real UI.
- [x] Zero raw selectors in specs (POM is the single chokepoint).
- [x] No flake — passes 3 consecutive CI runs; any 1/3 failure → quarantine.
- [x] Wall-clock < 5 min; traces on failure only.

## 8. Residual risk & handoff
- Third-party payment provider DOM is stubbed at the network boundary, not driven —
  provider-side outages are out of scope here. [INFERENCE]
- Owner for quarantine + 24h fix SLA on any future flake: checkout squad lead. [DOC]
