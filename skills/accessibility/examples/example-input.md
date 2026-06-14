# Example Input — accessibility (testing topic)

> A concrete request that exercises the router's `testing` path and the
> automated-first / manual-finality discipline.

**User request:**

"We just added a payment dialog to the `/checkout` route in our React app. Our CI
runs `@axe-core/playwright` and it's green, so I assumed we were fine — but a
keyboard user complained they get stuck after closing the dialog. Can you produce a
focused accessibility test report for the dialog flow? Target WCAG 2.1 AA. We have
VoiceOver on Safari available locally; no NVDA in CI."

**Implicit context the skill must extract:**
- Topic → `testing` (deliverable is verification evidence on existing UI, not a
  redesign and not a one-time governance scorecard).
- Target → `/checkout`, state: payment dialog open and on close.
- WCAG target → 2.1 AA (stated).
- Tooling → `@axe-core/playwright` in CI; VoiceOver + Safari available, no NVDA.
- Risk signal → "green CI" being read as "accessible"; reported focus-loss on dialog
  close points at 2.4.3 Focus Order and 2.1.2 No Keyboard Trap.
- Depth → deep (the user wants the dialog flow verified thoroughly).
