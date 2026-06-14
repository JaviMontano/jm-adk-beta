<!-- distilled from alfa skills/micro-interactions -->
<!-- > -->
# Micro Interactions
> "Method over hacks."
## TL;DR
Single-element feedback loops: button/control states, loading, success/error, hover, drag, toggles. Trigger → rules → feedback → mode. [EXPLICIT]
## Scope
In: state-level feedback on one control. Out: page transitions, choreographed multi-element sequences, full flows → see `motion-design.md`, `empty-states.md`. [EXPLICIT]

## Anatomy (apply to every interaction)
Trigger (user or system) → Rules (what happens) → Feedback (what the user perceives) → Loops/Modes (repeat, timeout, persistence). [DOC]

## State coverage (acceptance checklist)
Every interactive control MUST define: default, hover, focus-visible, active/pressed, loading, success, error, disabled, empty. Missing focus-visible or disabled is the most common defect. [INFERENCIA]
- [ ] All nine states designed and reachable by keyboard [EXPLICIT]
- [ ] Async actions show loading within 100ms and a terminal success/error [EXPLICIT]
- [ ] Feedback never relies on color alone (icon/text/shape too) [DOC]
- [ ] Reduced-motion variant defined for any movement [DOC]

## Timing (decision defaults, override with evidence)
| Interaction | Duration | Easing | Why |
|---|---|---|---|
| Hover / state tint | 100–150ms | ease-out | feels instant, not laggy [INFERENCIA] |
| Tap / press feedback | 50–100ms | ease-out | must register before next action [INFERENCIA] |
| Expand / reveal | 200–300ms | ease-in-out | shows spatial origin [INFERENCIA] |
| Loading → result | spinner after 400ms | — | avoid flash for fast responses [DOC] |
| Toast / success | 150ms in, 2–4s hold | ease-out | readable, auto-dismiss [SUPUESTO] |
Trade-off: <50ms reads as abrupt/janky; >400ms reads as sluggish. Tune per perceived weight, not uniformly. [INFERENCIA]

## Loading patterns (pick by expected wait)
- <300ms: no indicator — spinner would flash. [DOC]
- 300ms–1s: inline spinner or button-internal state, keep layout stable. [INFERENCIA]
- 1–10s: skeleton screen matching final layout (less jarring than spinner). [DOC]
- >10s or unknown: progress bar + cancel affordance + step text. [INFERENCIA]

## Failure modes to prevent
- Layout shift when a control swaps to loading/error (reserve space). [INFERENCIA]
- Double-submit: disable + show loading on first click. [INFERENCIA]
- Silent failure: every error state needs message + recovery action. [DOC]
- Optimistic UI without rollback: define the revert path before shipping. [SUPUESTO]
- Animation blocking input (control unusable mid-transition). [INFERENCIA]

## Accessibility (non-negotiable)
- focus-visible distinct from hover; never remove outlines without a replacement. [DOC]
- Announce async state changes via `aria-live`/`aria-busy`. [DOC]
- Honor `prefers-reduced-motion`: swap movement for opacity/instant change. [DOC]
- Hover-only feedback fails touch + keyboard — pair with focus/active. [INFERENCIA]

## Worked example: async submit button
Default → (click) disable + spinner replaces label within 100ms → on 200: checkmark 800ms then re-enable; on error: shake 150ms + inline message + re-enable for retry. Reduced-motion: skip shake, show message only. [EXPLICIT]

## Procedure
1. **Discover** — list every state the control can occupy; flag missing ones. [EXPLICIT]
2. **Analyze** — assign trigger/feedback/timing per tables; evaluate per Constitution XIII/XIV. [EXPLICIT]
3. **Execute** — implement with reduced-motion + aria; tag claims with evidence. [EXPLICIT]
4. **Validate** — run the state and a11y checklists; verify no layout shift. [EXPLICIT]

## Quality Criteria
- [ ] Nine states + timing + reduced-motion + aria covered
- [ ] Evidence tags applied; Constitution-compliant; actionable output

## Usage
- "/micro-interactions" — Run the full micro interactions workflow
- "micro interactions on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Durations are starting defaults, not brand tokens — reconcile with the design system. [SUPUESTO]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Slow/unknown network | Progress + cancel; never an indefinite spinner |
| Touch-only device | No hover-dependent feedback; use active/focus |
