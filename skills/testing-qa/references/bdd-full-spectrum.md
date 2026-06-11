<!-- distilled from alfa skills/bdd-full-spectrum -->
<!-- > -->
# BDD Full-Spectrum Quality

> "If you can't express it as a Given/When/Then, you don't understand it well enough to build it."

## TL;DR

Generates Behavior-Driven Development scenarios that go beyond functional happy paths. Every feature gets Gherkin scenarios across all relevant quality angles: functional, accessibility, security, performance, SEO, offline, UI, backend, data, DevSecOps, and CI/CD. Step definitions are runner-agnostic — Playwright for browser tests, Vitest for code invariants, Firebase Emulator for security rules. Each scenario traces to a requirement (FR-XXX), success criterion (SC-XXX), and constitutional principle. [EXPLICIT]

## Procedure

### Step 1: Discover
- Read the feature specification (FR-XXX, SC-XXX)
- Identify which quality angles apply to this feature
- Review constitutional principles that govern the feature
- Check existing `.feature` files for coverage gaps

### Step 2: Analyze
- For each applicable angle, derive at least one Given/When/Then scenario
- **Coverage angles** (select all that apply):
  - `@functional` — Does the feature do what it should?
  - `@a11y` — Is it keyboard-navigable, screen-reader friendly, ARIA-correct?
  - `@security` — Are inputs sanitized? Rules enforced? No secrets exposed?
  - `@perf` — Does it meet Lighthouse budgets? Load within 2s on 3G?
  - `@seo` — Meta tags present? Structured data correct? Crawlable?
  - `@offline` — Degrades gracefully? Cached content displayed?
  - `@ui` — Design tokens used? No hardcoded colors/fonts?
  - `@backend` — Security rules pass? Data model validates?
  - `@data` — Schema enforced? Both languages present? Audit logged?
  - `@devsecops` — No secrets in client code? Rules tested pre-deploy?
  - `@cicd` — Gates block broken code? Tests run before merge?
- Map each scenario to its runner:
  - Browser-dependent → Playwright
  - Code structure invariants → Vitest/grep
  - Security rules → Firebase Emulator
  - Performance → Lighthouse CI

### Step 3: Execute
- Write `.feature` files with Gherkin syntax:
  ```gherkin
  @functional @TS-022
  Feature: Task creation
    Scenario: User creates a new task
      Given I am logged in as a team member
      When I enter "Buy groceries" in the task input
      And I click the "Add" button
      Then a task "Buy groceries" appears in the task list
      And the task has status "todo"

  @security @TS-024
  Feature: Input sanitization
    Scenario: HTML tags are stripped from task input
      Given I am logged in as a team member
      When I enter "<script>alert('xss')</script>Buy groceries" in the task input
      And I click the "Add" button
      Then the stored task title is "Buy groceries"
      And no script tags exist in the DOM
  ```
- Generate step definition stubs for the chosen runner
- Add traceability tags: `@TS-xxx` (requirement), `@SC-xxx` (success criterion), `@P-xxx` (principle)
- Hash-lock feature files after approval (changes require re-running testify phase)

### Step 4: Validate
- Every quality angle relevant to the feature has at least 1 scenario
- All scenarios have step definition stubs
- Runner assignment matches the test nature (not all forced through browser)
- Traceability tags link to existing requirements
- No ambiguous terms in scenarios (trigger Socratic debate if found)
- Feature file hash recorded for drift detection

## Quality Criteria

- [ ] All applicable quality angles have at least 1 scenario
- [ ] Scenarios use Given/When/Then syntax correctly
- [ ] Tags include angle (`@functional`), requirement (`@TS-xxx`), and principle (`@P-xxx`)
- [ ] Step definitions are runner-agnostic (runner chosen per nature of test)
- [ ] No ambiguous or untestable assertions
- [ ] Feature files hash-locked after approval
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Only writing `@functional` scenarios | Misses security, a11y, perf regressions | Cover all applicable angles |
| Forcing all tests through Playwright | Slow, flaky, wrong tool for code invariants | Match runner to test nature |
| Modifying feature files to pass | Weakens the spec to match broken code | Fix the code, not the spec |
| Skipping traceability tags | Orphaned tests lose their purpose | Every scenario traces to a requirement |
| Writing scenarios after code | Defeats BDD — tests should drive development | Write scenarios BEFORE code (ATDD) |

## Related Skills

- `test-strategy` — Overall test pyramid and automation architecture
- `e2e-testing` — Playwright-specific implementation of browser scenarios
- `unit-testing` — Vitest/Jest implementation of code invariant scenarios
- `security-testing` — Security-specific test patterns
- `socratic-debate` — Resolve ambiguous scenarios before implementation

## Usage

Example invocations:

- "/bdd-full-spectrum" — Run the full bdd full spectrum workflow
- "bdd full spectrum on this project" — Apply to current context


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
