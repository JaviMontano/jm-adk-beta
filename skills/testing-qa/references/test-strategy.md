<!-- distilled from alfa skills/test-strategy -->
<!-- > -->
# Test Strategy

> "A test strategy is not about testing everything — it's about testing the right things." — Unknown

## TL;DR

Guides the design of a comprehensive testing strategy — defining test levels (unit, integration, e2e), choosing methodologies (TDD, BDD), setting coverage goals, and establishing testing culture. Use when starting a new project or restructuring testing practices for an existing codebase. [EXPLICIT]

## Scope & Anti-Scope

- **In scope:** test-level mix, coverage policy, runner selection, test-data strategy, flaky-test governance, CI gating. [DOC]
- **Out of scope:** writing the tests themselves (see `unit-testing`/`e2e-testing`), release/deploy strategy, security pentest execution, load/perf tuning beyond budget definition. [INFERENCIA]
- **Strategy ≠ plan.** This produces the *policy*; per-sprint test plans inherit from it. [INFERENCIA]

## Procedure

### Step 1: Discover
- Assess current test coverage and test types in the codebase. [CONFIG]
- Identify highest-risk areas (payment flows, auth, data integrity) — risk drives where effort concentrates, not uniform coverage. [INFERENCIA]
- Review CI/CD pipeline for existing test automation and gate points. [CONFIG]
- Check team testing skills and preferred frameworks (a strategy the team cannot run is theater). [INFERENCIA]

### Step 2: Analyze
- Design test pyramid proportions (~70% unit, ~20% integration, ~10% e2e) as a *default*, not a quota — invert toward integration for thin-logic/IO-heavy services. [INFERENCIA]
- Map critical user flows that require e2e coverage; cap the e2e set at the few flows whose failure is unacceptable. [INFERENCIA]
- Define coverage thresholds (lines, branches, functions) per module; weight by risk, not a single global number. [DOC]
- Evaluate TDD vs test-after by module complexity and stability of requirements. [INFERENCIA]
- For BDD, define scenarios across all quality angles (Constitution XV):
  `@functional`, `@a11y`, `@security`, `@perf`, `@seo`, `@offline`, `@ui`,
  `@backend`, `@data`, `@devsecops`, `@cicd`. [DOC]
- Use runner-agnostic Gherkin: match runner to test nature (Playwright for browser,
  Vitest for code invariants, Firebase Emulator for security rules). [DOC]

### Step 3: Execute
- Document the strategy with scope, tools, owners, and CI gate definitions. [DOC]
- Set up runners: Vitest/Jest (unit), Testing Library (integration), Playwright (e2e). [CONFIG]
- Create test templates and conventions (file naming, `describe`/`it` patterns). [CONFIG]
- Configure coverage thresholds in CI (fail build below threshold). [CONFIG]
- Establish test-data management (fixtures, factories, mocks; isolated per test). [DOC]
- Define flaky-test policy: quarantine lane, fix SLA, named owner, auto-revert on N consecutive flakes. [DOC]

### Step 4: Validate
- Review pyramid balance — an e2e-heavy shape signals missing unit coverage (ice-cream-cone). [INFERENCIA]
- Verify CI runs all levels before merge and that gates actually block (test the gate). [CONFIG]
- Confirm thresholds are enforced and trending upward, not gamed downward. [INFERENCIA]
- Check that new PRs include tests for changed code (PR review checklist). [DOC]

## Decisions & Trade-offs

| Decision | Choose when | Trade-off accepted | Tag |
|----------|-------------|--------------------|-----|
| TDD | Requirements stable, logic-dense, regression-prone | Slower initial velocity for design pressure + safety net | [INFERENCIA] |
| Test-after | Exploratory/UI spikes, churning requirements | Risk of untested branches; backfill debt | [INFERENCIA] |
| Pyramid (unit-heavy) | Rich domain logic | Fewer integration seams exercised | [INFERENCIA] |
| Trophy (integration-heavy) | Thin glue over IO/DB/APIs | Slower suite, more infra in CI | [INFERENCIA] |
| Global coverage % | Small uniform codebase | Incentivizes trivial tests on low-risk code | [SUPUESTO] |
| Per-module risk-weighted % | Mixed-criticality monorepo | More policy to maintain | [INFERENCIA] |

## Worked Example

Fintech app, payments + marketing site in one repo. [SUPUESTO]
- `payments/`: branches ≥ 90%, TDD, e2e on checkout + refund only.
- `marketing/`: lines ≥ 50%, test-after, zero e2e (visual regression instead).
- CI gate: block merge if any module drops below its floor; flaky test → quarantine + 48h fix SLA.
- Result: ~140 unit, ~30 integration, 6 e2e — effort follows risk, not file count. [INFERENCIA]

## Quality Criteria

- [ ] Test pyramid proportions documented, risk-justified, and followed.
- [ ] Coverage thresholds configured per-module and enforced in CI.
- [ ] Critical user flows have e2e coverage; e2e set is deliberately small.
- [ ] Test-data strategy keeps tests isolated and deterministic.
- [ ] Flaky-test policy has owner + SLA, not just a label.
- [ ] Every non-obvious claim carries one evidence tag from a single family.

## Acceptance Criteria

- A reader can determine, for any module, its target level mix and coverage floor. [DOC]
- CI fails (not warns) when a floor is breached; the gate is verified to block. [CONFIG]
- The e2e list maps 1:1 to flows whose failure is business-critical. [INFERENCIA]
- Strategy names the owner for flaky triage and the quarantine mechanism. [DOC]

## Failure Modes

| Failure mode | Symptom | Mitigation |
|--------------|---------|------------|
| Ice-cream cone | Slow, flaky e2e-heavy suite | Push assertions down to unit/integration |
| Coverage theater | High % but bugs ship | Mutation testing; assert behavior, not lines |
| Green-but-empty | Tests with no assertions pass | Lint for assertion presence; review PR tests |
| Flake normalization | Reruns until green | Quarantine + SLA; block on repeat flakes |
| Frozen pyramid | Default 70/20/10 applied blindly | Re-derive mix per service nature |

## Anti-Patterns

- Relying solely on e2e tests (slow, expensive, flaky — ice-cream-cone). [INFERENCIA]
- Setting coverage thresholds too high (incentivizes trivial tests). [INFERENCIA]
- Testing only the happy path (error paths and edge cases go uncovered). [INFERENCIA]
- Treating green CI as success when assertions are weak or absent. [DOC]

## Related Skills

- `unit-testing` — Implementation of unit test layer
- `e2e-testing` — Implementation of end-to-end test layer
- `bdd-full-spectrum` — Multi-angle Gherkin scenarios (Constitution XV)
- `lighthouse-ci` — Performance budgets in CI (G2 gate)

## Usage

Example invocations:

- "/test-strategy" — Run the full test strategy workflow
- "test strategy on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Default pyramid ratios are heuristics, not targets — always re-derive per service. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Legacy codebase, ~0% coverage | Set a ratchet (no-decrease) floor; raise gradually, don't block all merges |
| No CI available | Define local pre-commit gate; flag CI as a prerequisite [SUPUESTO] |
