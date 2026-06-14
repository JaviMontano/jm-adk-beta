<!-- distilled from alfa skills/accessibility-testing -->
<!-- > -->
# Accessibility Testing

> "The power of the web is in its universality. Access by everyone regardless of disability is an essential aspect." — Tim Berners-Lee

## TL;DR

Guides accessibility testing as an evidence-producing workflow: define scope, run automated checks where possible, execute manual keyboard and assistive-technology smoke tests, record contrast and motion results, and produce a pass/fail/not-verified report. Use for test plans, regression suites, QA reports, and retest evidence. Do not claim WCAG compliance without explicit target, scope, date, tested technologies, and evidence. [EXPLICIT]

**Anti-scope:** this skill tests and reports; it does not remediate, redesign, or set policy unless explicitly asked (see Related Skills). It produces evidence, not a conformance certificate. [EXPLICIT]

## Procedure

### Step 1: Discover
- Capture the accessibility target: WCAG version/level, routes, components, flows, browsers, viewports, auth state, and assistive technology pairings.
- Inventory dynamic states that must be opened before testing: menus, dialogs, tooltips, form errors, toasts, accordions, route changes, and live regions.
- Identify available tooling: axe-core, `@axe-core/playwright`, `jest-axe`, browser-rendered contrast checks, visual/focus evidence, CI, and manual test notes.
- Record known issues, exclusions, and suppressions with owner, issue ID, selector, rule ID, expiry, and re-enable criteria.
- If target level is unstated, assume WCAG 2.1 AA as the default reporting baseline and state it; do not silently test a stricter or looser bar. [SUPUESTO]

### Step 2: Analyze
- Map each test to an observable expectation, artifact, and status: `pass`, `fail`, `conditional`, or `not verified`.
- Separate automated evidence from manual evidence; a clean axe run is not a full accessibility or WCAG conformance claim. Rationale: automation covers roughly 30–40% of WCAG success criteria — order, meaning, and announced experience need a human. [INFERENCIA]
- Prioritize risks by user impact: blocker, high, medium, low, or observation.
- Choose manual scripts for focus order, focus trapping/restoration, keyboard activation, screen reader announcements, contrast, zoom/reflow, reduced motion, and dynamic content.

### Step 3: Execute
- Produce or run automated tests with route/component/state coverage; scan after interactions, not just first page load.
- Produce keyboard scripts covering Tab, Shift+Tab, Enter, Space, Escape, arrow keys where relevant, skip links, focus visibility, focus trap, and focus restoration.
- Produce screen reader smoke scripts with OS/browser/AT pairing, expected announcement, observed announcement, and pass/fail status. Pair AT with its supported browser (NVDA+Firefox/Chrome, VoiceOver+Safari, JAWS+Chrome); a mismatched pairing produces false failures and must be flagged, not reported as a defect. [INFERENCIA]
- Record contrast evidence for normal text, large text, non-text UI, placeholder, disabled, focus, hover, and error states, or mark gaps as `not verified`. Thresholds: 4.5:1 normal text, 3:1 large text (≥18.66px bold or ≥24px) and non-text UI/state indicators; disabled controls are exempt. [EXPLICIT]
- Create remediation tickets or backlog items only when remediation is requested; otherwise report issues with evidence and recommended owner.

### Step 4: Validate
- Every claim has a command, artifact, observation, or explicit `not verified` marker.
- Automated findings include command/tool version, route or component, state, rule ID, impact, selector, WCAG tags when available, and artifact path.
- Manual findings include script step, expected result, observed result, evidence, severity, and retest status.
- Final status avoids blanket "compliant" language unless the full conformance scope is documented and evidenced.

## Worked Example: one finding

```
ID:        A11Y-014
Type:      manual (keyboard)
Route:     /checkout  · state: payment dialog open
Script:    Tab to "Pay", press Esc
Expected:  dialog closes, focus returns to the trigger button
Observed:  dialog closes, focus lands on <body> (lost)
WCAG:      2.4.3 Focus Order (AA) · 2.1.2 No Keyboard Trap (A)
Severity:  high (keyboard users lose their place)
Evidence:  artifacts/a11y-014-focus.png, traces/checkout.zip
Status:    fail → retest pending
```

A clean automated counterpart, for contrast: `axe-core 4.x, @axe-core/playwright, /checkout, dialog open, 0 violations, artifacts/axe-checkout.json` — reported as "0 axe violations in scanned states", never as "accessible". [CODE]

## Quality Criteria

- [ ] Scope and environment are explicit: target, routes/components/states, browser, viewport, assistive technology, date, and tool versions.
- [ ] Automated evidence is scoped and reproducible; single body scans and unopened dynamic states are rejected as insufficient proof.
- [ ] Keyboard evidence covers forward/reverse tab order, activation keys, escape paths, focus visibility, traps, restoration, and route-change focus.
- [ ] Screen reader evidence is labeled as smoke, regression, or full manual test and includes expected vs observed announcements, plus the AT+browser pairing used.
- [ ] Contrast and reduced-motion results are recorded with the ratio and threshold applied, or each gap is marked `not verified` with next action.
- [ ] Suppressions have issue ID, owner, expiry, selector, rule ID, reason, and re-enable criteria.
- [ ] No WCAG conformance claim is made without scope, target level, tested technologies, date, and evidence.
- [ ] Every status is one of `pass` / `fail` / `conditional` / `not verified`; no implicit pass-by-silence.
- [ ] Evidence tags applied to all claims.

## Decisions & Trade-offs

- **`not verified` over assumed pass.** Untested ≠ passing. Marking a gap explicitly is honest and cheap; an assumed pass is a latent false claim that surfaces in audit or litigation. [EXPLICIT]
- **Smoke first, full manual on risk.** Full AT passes are expensive; gate them on user-impact (auth flows, payments, primary nav) and label coverage depth so readers do not over-read a smoke run. [INFERENCIA]
- **Browser-rendered contrast over static design tokens.** Test computed colors in the real DOM — overlays, opacity, and gradients change the actual ratio a user sees. [INFERENCIA]

## Anti-Patterns

- Treating automated tools as complete proof of accessibility or WCAG conformance
- Adding ARIA attributes to elements that already have native semantics
- Using `outline: none` without providing alternative focus indicators
- Scanning only the initial DOM while ignoring opened menus, dialogs, form errors, and live updates
- Broadly excluding selectors from axe without owner, expiry, and re-enable criteria
- Mixing testing with remediation without explicit user approval
- Reporting "green CI" as "accessible"; CI gates a subset, it does not certify conformance

## Failure Modes

| Failure | Symptom | Guard |
|---------|---------|-------|
| False pass | Axe clean but dialogs/menus never opened | Scan after every interaction; assert state was reached |
| False fail | Defect from wrong AT+browser pairing or stale build | Record pairing + build SHA; reproduce before filing |
| Flaky focus tests | Pass/fail varies with timing | Wait on focus/visibility, not fixed delays |
| Suppression rot | Old axe exclusions hide real regressions | Every suppression carries an expiry and re-enable criteria |
| Scope creep into fixing | Test run mutates the product | Stop at evidence unless remediation is explicitly approved |

## Related Skills

- `accessibility-audit` — use for broader governance, policy, and compliance audit scope
- `accessibility-design` — use for designing accessible interaction patterns and UI changes
- `modal-dialog-patterns` — focus management is critical for modal accessibility
- `navigation-patterns` — navigation is the most common a11y failure area

## Usage

Example invocations:

- "/accessibility-testing" — Run the full accessibility testing workflow
- "accessibility testing on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Automated tooling detects a minority of WCAG criteria; manual evidence is required for a conformance position, not optional [INFERENCIA]
- Cannot certify experience for AT versions/devices not in the tested pairings; out-of-scope pairings are `not verified`, not pass [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Auth-gated routes untestable | Mark `not verified`, name the credential/state blocker as next action |
| Third-party/iframe widget fails | Report with evidence; flag ownership boundary, do not file against host app |
| No AT available in environment | Deliver automated + keyboard evidence; label AT coverage `not verified` |

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
