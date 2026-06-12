<!-- distilled from alfa skills/bdd-full-spectrum -->
<!-- > -->
# BDD Full-Spectrum Quality

> "If you can't express it as a Given/When/Then, you don't understand it well enough to build it."

## TL;DR

Generates Behavior-Driven Development scenarios that go beyond functional happy paths. Every feature gets Gherkin scenarios across all relevant quality angles: functional, accessibility, security, performance, SEO, offline, UI, backend, data, DevSecOps, and CI/CD. Step definitions are runner-agnostic — Playwright for browser tests, Vitest for code invariants, Firebase Emulator for security rules. Each scenario traces to a requirement (FR-XXX), success criterion (SC-XXX), and constitutional principle. [DOC]

**Scope.** Produces `.feature` files + step-definition stubs + a runner map + a traceability matrix. It does NOT implement step bodies, run the suite, or judge pass/fail — those belong to the runner-specific skills (see Related). [DOC]
**Anti-scope.** Not a substitute for exploratory/usability testing, load testing at scale, or pen-testing; those need dedicated tooling and human judgment. [INFERENCIA]

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
- Selection rule: an angle is in-scope if the feature touches its surface (UI render → `@a11y`+`@ui`; user input → `@security`; persisted write → `@data`+`@backend`). When unsure, include and tag `[SUPUESTO]` rather than silently drop. [INFERENCIA]
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

## Worked example: negative + boundary coverage

One angle, three scenarios — happy, negative, boundary. Happy-only is the #1 gap this skill exists to close. [INFERENCIA]

```gherkin
@functional @perf @TS-030 @SC-005
Feature: Task list rendering
  Scenario: List renders within budget               # happy
    Given 50 tasks exist
    When I open the task list
    Then all 50 tasks are visible
    And first contentful paint is under 1.5s

  Scenario: Empty state is shown                      # negative
    Given 0 tasks exist
    When I open the task list
    Then the empty-state illustration is visible
    And no error is logged

  Scenario: Large list virtualizes                    # boundary
    Given 10000 tasks exist
    When I open the task list
    Then at most 30 task rows exist in the DOM
    And scrolling stays above 50fps
```

## Decisions & trade-offs

| Decision | Why | Trade-off accepted |
|---|---|---|
| Runner-agnostic steps, per-nature mapping | Right tool per test; browser tests stay rare | Contributors learn 3 runners, not 1 [INFERENCIA] |
| Hash-lock features post-approval | Stops silently editing the spec to pass | Legit spec changes need an explicit re-run [DOC] |
| ATDD — scenarios before code | Spec drives design; tests can't be retrofitted to green | Slower start; needs a stable enough spec [INFERENCIA] |
| One angle tag + traceability per scenario | Filterable suites; orphan tests are impossible | Tag upkeep on every scenario [DOC] |

## Failure modes

| Symptom | Likely cause | Recovery |
|---|---|---|
| Flaky `@perf`/`@a11y` runs | Browser timing, shared CI runners | Pin budgets to p75, retry-once, quarantine — never weaken the assertion [SUPUESTO] |
| Hash mismatch on a locked feature | Spec edited outside testify phase | Re-run testify, re-approve, re-lock; do not hand-patch the hash [DOC] |
| Scenario passes but feature is wrong | Assertion too loose / restates the action | Assert observable outcome + side effect (e.g. DOM-absent, status set), not the click [INFERENCIA] |
| Step stub never implemented | Angle selected, runner not wired | Block merge on undefined steps; pending ≠ passing [INFERENCIA] |

## Quality Criteria

- [ ] All applicable quality angles have at least 1 scenario
- [ ] Each in-scope angle has happy + at least one negative/boundary scenario [INFERENCIA]
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
| Asserting the action, not the outcome | Passes while the feature is broken | Assert observable state + side effects |

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

- Assumes access to project artifacts (code, docs, configs) [SUPUESTO]
- Requires English-language output unless otherwise specified [SUPUESTO]
- Does not replace domain expert judgment for final decisions [DOC]
- Assumes FR/SC/P identifiers already exist; if absent, stop and request them rather than invent IDs [SUPUESTO]
- Hash-locking assumes an approval gate exists upstream; without it, drift detection is advisory only [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Feature touches no testable surface | Record "no scenarios — rationale" rather than fabricate coverage [INFERENCIA] |
| Angle applies but runner unavailable | Write the scenario, mark step `pending`, flag the missing runner [SUPUESTO] |
