# Deep Prompt — accessibility (depth=deep)

Exhaustive path: apply the routed playbook fully with verification at each step.

1. **Route** to one topic and load only its playbook. If the request genuinely spans
   two (e.g. design then testing), run them as ordered sub-passes.
2. **Scope precisely.** Record target, every in-scope route/component/state, browser,
   viewport, auth/session state, assistive-technology pairings, tool versions, and
   test date. Inventory dynamic states to open before testing: menus, dialogs,
   tooltips, form errors, toasts, accordions, route changes, live regions.
3. **Automated, then manual.**
   - Run axe-core against each route/component **and after each interaction/route
     change**, saving machine-readable artifacts.
   - Manual keyboard: tab order both directions, activation keys, Esc paths, skip
     links, focus visibility, focus trap, focus restoration, route-change focus.
   - Screen-reader smoke with a valid AT+browser pairing; record expected vs observed
     announcement.
   - Contrast on computed DOM colors for normal/large text, non-text UI, placeholder,
     disabled, focus, hover, error; record ratio + threshold or `not verified`.
   - Reduced motion, 200% zoom/reflow, forced colors.
4. **Map & prioritize.** Each finding → WCAG criterion + level, user impact
   (blocker/high/medium/low), reproducer, expected behavior, evidence artifact, and
   acceptance check. Prioritize by user impact, not raw tool severity.
5. **Validate against the playbook's Quality Criteria** and the guardian gate. Every
   claim carries one evidence tag; suppressions carry owner, expiry, re-enable
   criteria. Status: `pass` / `conditional` / `fail` / `not verified` — never
   green-as-success, never an unbacked "WCAG compliant".
