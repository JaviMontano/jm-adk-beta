# Testing-QA Deliverable — {{topic}}

> Routed discipline and depth for this request. One playbook, one spine. [DOC]

## 1. Routing decision
- **Topic chosen:** {{test-strategy | unit-testing | e2e-testing | bdd-full-spectrum | cross-browser-testing | performance-testing}}
- **Depth:** {{quick | deep}}
- **Why this route (disambiguation applied):** <one line; e.g. "load/latency framing → performance-testing"> [INFERENCE]
- **Playbook Read:** `references/{{topic}}.md` (exactly one) [DOC]

## 2. Target under test
- **Artifact:** <repo path / route list / component / deployed URL / feature spec FR-/SC- IDs>
- **Environment:** <Firebase emulator / deployed build / browser matrix> [CONFIG]
- **If no runnable target:** <gap report — do not test a hypothetical> [INFERENCE]

## 3. Discover
- Current state: <coverage snapshot / pyramid shape / CrUX availability / engine support> [CONFIG]
- Highest-risk surface: <payments / auth / data integrity / critical journey> [INFERENCE]

## 4. Analyze
- Level mix / quality angles / engine matrix / budgets: <the design, risk-justified> [INFERENCE]
- Runner & thresholds: <Vitest|Jest | Playwright|Cypress | Lighthouse CI; threshold + source> [CONFIG]
- Thresholds derived from: <baseline / CrUX p75 / ≥80% diff> (no guessed numbers) [SUPUESTO]

## 5. Execute
- Artifacts produced: <config blocks / mocks / POMs / .feature files / CI assertions>
- Commands to run: <`vitest run --coverage` | `npx playwright test` | Lighthouse CI | `npx browserslist`> [CONFIG]

## 6. Validate (run before "done")
| Check | Command / evidence | Result | Status |
|-------|--------------------|--------|--------|
| <decisive check 1> | <command + output pointer> | <numbers> | pass / fail / not-verified |
| <decisive check 2> | <command + output pointer> | <numbers> | pass / fail / not-verified |

- Gate verified to BLOCK on breach (not warn): <yes/no> [CONFIG]
- Green-as-success rejected if assertions weak/absent or lab-green-but-field-fails. [INFERENCE]

## 7. Quality criteria (from the routed playbook)
- [ ] <criterion 1 specific to {{topic}}>
- [ ] <criterion 2 specific to {{topic}}>
- [ ] Every non-obvious claim carries one evidence tag from a single family.

## 8. Residual risk & handoff
- Out-of-scope / deferred: <e.g. server SLO load testing, field validation deferred> [INFERENCE]
- Owner for flaky triage / next action: <named owner> [DOC]
