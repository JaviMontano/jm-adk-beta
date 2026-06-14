<!-- distilled from alfa skills/accessibility-audit -->
<!-- WCAG 2.1 AA automated scanning with axe-core plus manual checklist for keyboard, screen reader, and contrast -->
# 082 — Accessibility Audit {Testing}

## Purpose
Audit digital interfaces against WCAG 2.1 AA using automated axe-core scanning plus structured manual checks for keyboard, screen reader behavior, color contrast, forms, focus management, dynamic content, and semantic structure. [EXPLICIT]
The default output is an evidence-backed accessibility audit report, not a code remediation patch. Code edits require an explicit remediation request. [EXPLICIT]

### Anti-scope (this skill does NOT)
- Auto-apply code fixes without an explicit remediation request. [EXPLICIT]
- Certify WCAG 2.1 **AAA**, EN 301 549 legal conformance, or VPAT/ACR sign-off — those need a named human accessibility owner. [EXPLICIT]
- Audit PDFs, native iOS/Android, or email HTML; axe-core targets DOM only. Out-of-scope targets return a gap report. [ASSUMPTION]
- Replace lived-experience testing with disabled users; automated + heuristic checks cover roughly 30–40% of WCAG SCs. [INFERENCE]

## Physics — 3 Immutable Laws

1. **Law of Universal Access**: If a sighted mouse user can do it, a keyboard-only or screen reader user must also be able to do it. No exceptions. [EXPLICIT]
2. **Law of Automated First, Manual Finality**: Automated scans find important issues but do not prove WCAG conformance. Run automation first, then manually verify the remaining criteria before making compliance claims. [EXPLICIT]
3. **Law of Evidence Before Compliance**: Do not claim "WCAG compliant" unless automated results, manual checks, scope, exceptions, and remediation status are documented. [EXPLICIT]

## Protocol

### Phase 0 — Scope and Evidence Setup
1. Identify audit target: URL, local app command, route list, component list, design artifact, or supplied HTML. [EXPLICIT]
2. Record environment: browser, viewport set, assistive technology used, auth/session state, and test date. [EXPLICIT]
3. If there is no runnable target, source artifact, or route/component list, return a gap report and do not claim compliance. [EXPLICIT]

### Phase 1 — Automated Scanning
1. Select the available runner: `axe-core`, `@axe-core/playwright`, `axe-playwright`, `cypress-axe`, `jest-axe`, or equivalent project-local tooling. [EXPLICIT]
2. Run scans against each route/component in scope and save machine-readable evidence when the environment permits. [EXPLICIT]
3. Report scan command, target, rule id, impact, affected selector, WCAG tags, and artifact path for every violation. [EXPLICIT]
4. Treat automated "no violations" as "no automated violations found", not as full WCAG compliance. [EXPLICIT]

### Phase 2 — Manual Checklist
1. **Keyboard navigation**: Verify tab order, visible focus, skip links, focus trap, return focus, escape behavior, and keyboard activation for custom controls. [EXPLICIT]
2. **Screen reader**: Verify page title, headings, landmarks, names/roles/values, form labels, error announcements, status updates, and modal announcements with VoiceOver, NVDA, or the available runner. [EXPLICIT]
3. **Contrast and visual states**: Verify 4.5:1 for normal text, 3:1 for large text, non-text contrast for UI controls/icons, focus indicator visibility, and color-not-alone signaling. [EXPLICIT]
4. **Responsive and motion**: Verify reflow at narrow widths, zoom behavior, orientation assumptions, `prefers-reduced-motion`, and pause/stop/hide controls for moving content. [EXPLICIT]

### Phase 3 — Remediation
1. Prioritize by user impact, WCAG level, blocker status, and recurrence across components; do not rely only on axe severity. [EXPLICIT]
2. Each remediation ticket must include target, selector/component, reproducer, WCAG criterion, user impact, expected behavior, evidence artifact, and acceptance check. [EXPLICIT]
3. If remediation is requested, make the smallest safe patch and rerun the relevant automated/manual checks. [EXPLICIT]
4. If remediation is not requested, produce owner-ready tickets and status: `pass`, `conditional`, `fail`, or `not verified`. [EXPLICIT]

**Decisions & trade-offs**
- **axe-core as default runner**: zero false positives by design, so it under-reports — it stays silent on the ~60% of SCs it cannot test (e.g. focus order, meaningful alt text). Trade-off accepted because a clean axe run is a trustworthy floor, not a ceiling. [INFERENCE]
- **Report-first, not patch-first**: a wrong remediation can mask a violation from axe while leaving the barrier (e.g. `aria-hidden` on a focusable control). Defaulting to evidence keeps the human owner in the decision loop. [EXPLICIT]
- **Impact-priority over axe severity**: axe `critical` on a hidden element outranks a `serious` on the primary CTA only by raw rule weight; user-blocker status reorders this. [EXPLICIT]

**Worked example — custom dropdown**
`<div class="select">` with click-only open. axe: **0 violations** (no rule covers it). Manual keyboard: Tab reaches it but Enter/Space/Arrow do nothing → SC 2.1.1 (A) **fail**. Manual SR: announced as "group", no role/state → SC 4.1.2 (A) **fail**. Verdict: **fail** despite clean automation — illustrates Law 2. Ticket: add `role="combobox"`, `aria-expanded`, `tabindex="0"`, key handlers; reproducer = "Tab to control, press Enter"; acceptance = SR announces role+expanded state. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| React/HTML component | axe-core violation report (JSON/HTML) |
| Route list | Full-site automated scan results |
| Manual audit checklist | Completed checklist with pass/fail per criterion |
| Violation report | Remediation tickets with WCAG reference |

## Quality Gates — 5 Checks

1. **Zero unresolved WCAG 2.1 AA failures** in scope, or each exception has owner, rationale, expiry, and risk acceptance. [EXPLICIT]
2. **Automated evidence present**: command/tool, target, rule id, impact, selector, WCAG tags, and report artifact are recorded when runnable. [EXPLICIT]
3. **Manual evidence present**: keyboard, screen reader, contrast, forms/errors, focus, dynamic content, motion, and responsive checks are pass/fail/not-verified with notes. [EXPLICIT]
4. **No unsupported compliance claim**: final status is `pass`, `conditional`, `fail`, or `not verified`; "compliant" requires all in-scope checks passing or documented exceptions. [EXPLICIT]
5. **Owner-ready remediation**: every finding has severity, WCAG criterion, user impact, reproducer, expected behavior, and acceptance check. [EXPLICIT]

## Edge Cases

- **Dynamic content**: Use `aria-live="polite"` for async updates (toasts, loaders).
- **Modals**: Trap focus inside modal. Return focus to trigger on close.
- **Custom components**: `<div>` buttons need `role="button"`, `tabindex="0"`, `onKeyDown` for Enter/Space.
- **SVG icons**: Add `aria-hidden="true"` for decorative. `role="img"` + `aria-label` for meaningful.
- **ARIA overuse**: Prefer native HTML before adding ARIA. Remove redundant or misleading roles.
- **Clean axe report with manual failure**: Overall status remains `fail` or `conditional`; automation cannot override manual blockers.
- **Auth/SPA routes**: axe scans the rendered DOM only — scan *after* login and after each client-side route change, not just the initial HTML, or post-auth content is silently skipped. [EXPLICIT]
- **Iframes / shadow DOM / canvas**: cross-origin iframes and `<canvas>` games are opaque to axe; flag as `not verified` and route to manual or SR testing rather than reporting a false pass. [INFERENCE]
- **Data tables**: require `<th scope>`, `<caption>`, and programmatic header association — visual alignment alone fails SC 1.3.1. [EXPLICIT]
- **Disabled vs aria-disabled**: native `disabled` removes the control from the tab order (SR users may miss it); `aria-disabled="true"` keeps it focusable and announceable. Choose per intent. [EXPLICIT]

## Failure Modes (and the guard)

- **False sense of security**: shipping on "axe: 0 violations" alone. Guard: Quality Gate 4 forbids a `pass` without manual evidence. [EXPLICIT]
- **Flaky contrast checks**: gradient/image backgrounds and opacity defeat automated contrast math. Guard: sample the worst-case pixel manually; record the measured ratio, not the tool's "unable to determine". [EXPLICIT]
- **Focus-trap regressions**: a modal that traps focus but never returns it to the trigger passes the open test, fails on close. Guard: test open *and* close in the same pass (Phase 2.1). [EXPLICIT]
- **Tag drift**: introducing a foreign provenance taxonomy. Guard: this doc uses `[EXPLICIT]` plus canon `[INFERENCE]`/`[ASSUMPTION]` only; see `references/verification-tags.md`. [EXPLICIT]

## Self-Correction Triggers

- axe violation count increases between releases → block deploy, remediate.
- Screen reader test skipped → flag in PR review checklist.
- New component lacks a11y test → component review blocks approval.
- Contrast check fails on new theme → update design tokens before merge.

## Usage

Example invocations:

- "/accessibility-audit" — Run the full accessibility audit workflow
- "accessibility audit on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- If no runnable target or artifact is available, produce a gap report with required inputs instead of an audit verdict. [EXPLICIT]

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
