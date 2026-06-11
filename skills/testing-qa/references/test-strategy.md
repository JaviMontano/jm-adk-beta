<!-- distilled from alfa skills/test-strategy -->
<!-- > -->
# Test Strategy

> "A test strategy is not about testing everything — it's about testing the right things." — Unknown

## TL;DR

Guides the design of a comprehensive testing strategy — defining test levels (unit, integration, e2e), choosing methodologies (TDD, BDD), setting coverage goals, and establishing testing culture. Use when starting a new project or restructuring testing practices for an existing codebase. [EXPLICIT]

## Procedure

### Step 1: Discover
- Assess current test coverage and test types in the codebase
- Identify the highest-risk areas (payment flows, auth, data integrity)
- Review CI/CD pipeline for existing test automation
- Check team testing skills and preferred frameworks

### Step 2: Analyze
- Design test pyramid proportions (70% unit, 20% integration, 10% e2e)
- Map critical user flows that require e2e coverage
- Define coverage thresholds (lines, branches, functions) per module
- Evaluate TDD vs test-after approach by module complexity
- For BDD, define scenarios across all quality angles (Constitution XV):
  `@functional`, `@a11y`, `@security`, `@perf`, `@seo`, `@offline`, `@ui`,
  `@backend`, `@data`, `@devsecops`, `@cicd`
- Use runner-agnostic Gherkin: match runner to test nature (Playwright for browser,
  Vitest for code invariants, Firebase Emulator for security rules)

### Step 3: Execute
- Document test strategy with scope, tools, and responsibilities
- Set up test runners: Vitest/Jest (unit), Testing Library (integration), Playwright (e2e)
- Create test templates and conventions (file naming, describe/it patterns)
- Configure coverage thresholds in CI (fail build below threshold)
- Establish test data management strategy (fixtures, factories, mocks)
- Define flaky test policy (quarantine, fix SLA, ownership)

### Step 4: Validate
- Review test pyramid balance — too many e2e tests indicate missing unit coverage
- Verify CI runs all test levels before merge
- Confirm coverage thresholds are enforced and trending upward
- Check that new PRs include tests for changed code (PR review checklist)

## Quality Criteria

- [ ] Test pyramid proportions documented and followed
- [ ] Coverage thresholds configured and enforced in CI
- [ ] Critical user flows have e2e test coverage
- [ ] Test data management strategy prevents flaky tests
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Relying solely on e2e tests (slow, expensive, flaky — ice cream cone anti-pattern)
- Setting coverage thresholds too high (incentivizes trivial tests)
- Not testing error paths and edge cases (only happy path coverage)

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

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
