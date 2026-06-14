<!-- distilled from alfa skills/accessibility-design -->
<!-- > -->
# Accessibility Design

> "The power of the Web is in its universality. Access by everyone regardless of disability is an essential aspect." — Tim Berners-Lee

## TL;DR

Designs or implements accessible web UI behavior before or during feature
delivery. Output is component-level accessibility requirements: semantic
HTML/ARIA decisions, keyboard maps, focus rules, contrast/token requirements,
form/error behavior, and acceptance criteria. [EXPLICIT]

**Use this skill** when the deliverable is the accessible *design or build*.
**Route away** to `accessibility-audit` (discover/report violations on existing
UI) or `accessibility-testing` (author or run tests). This skill owns the
solution; those own findings and verification. [EXPLICIT]

**In scope:** native semantics, ARIA authoring practices, keyboard/focus models,
contrast/token specs, form and error UX, live regions, reduced motion, zoom,
forced colors. **Anti-scope:** full WCAG conformance audit, VPAT/ACR authoring,
legal/ADA sign-off, automated-scan setup, native iOS/Android a11y APIs, PDF/
document remediation — redirect or escalate these. [INFERENCIA]

**Target standard:** WCAG 2.1 AA unless the request names a different level.
State the assumed target in the output so a reviewer can challenge it. [SUPUESTO]

## Procedure

### Step 1: Discover
- Identify the feature, component, user journey, interaction states, target
  users, device constraints, and existing design-system tokens/components. [EXPLICIT]
- Capture required controls, content, validation states, dynamic updates,
  responsive behavior, motion behavior, and success/failure paths. [EXPLICIT]
- If the request is only to find violations, route to `accessibility-audit` or
  `accessibility-testing`. [EXPLICIT]
- **Failure mode:** designing a custom widget before checking whether a native
  element (`<details>`, `<dialog>`, `<select>`, `<input type>`) already covers
  it — re-deriving keyboard/ARIA you would get for free. Check native first. [INFERENCIA]

### Step 2: Analyze
- Choose native HTML semantics first: buttons, links, headings, labels,
  fieldsets, lists, tables, landmarks, and form controls before custom ARIA. [EXPLICIT]
- **Decision rule — native vs. ARIA:** prefer native (it ships role, state,
  focus, and keyboard with zero JS). Reach for an ARIA widget pattern *only*
  when no native element expresses the interaction (e.g. tabs, combobox,
  tree). Trade-off: native constrains styling (e.g. `<select>` option styling);
  accept that constraint unless a hard design requirement forces a custom
  widget, and if it does, you now own the full keyboard + ARIA contract. [INFERENCIA]
- For every custom component define: accessible **name**, **role**, **value/
  state**, **keyboard model**, **focus** entry/exit, **pointer** alternative,
  **screen-reader** announcement, and **disabled** behavior. Missing any one is
  an incomplete spec. [EXPLICIT]
- Map requirements to WCAG 2.1 AA / POUR and note acceptance criteria per
  state. [EXPLICIT]
- Identify design-token requirements for text contrast, non-text contrast,
  focus indicators, error/disabled states, hover/focus/active states, and
  color-not-the-only-signal. [EXPLICIT]

### Step 3: Execute
- Produce or update accessible implementation guidance, component specs, or code
  changes when explicitly requested. [EXPLICIT]
- Include keyboard interaction tables (see contracts below) for any in-scope
  pattern: dialog, tabs, accordion/disclosure, menu, combobox/listbox, toast/
  live region, forms, skip links. [EXPLICIT]
- Define focus management: initial focus, visible focus indicator, trap/
  containment when needed, return focus to trigger, route-change focus, and no
  focus stealing. [EXPLICIT]
- Define content: accessible names, labels, descriptions, alt text, error copy,
  status messages, plain language, and sensory-independent cues. [EXPLICIT]

### Step 4: Validate
- Verify the output includes: component behavior, semantic/ARIA decision log,
  keyboard map, focus plan, screen-reader expectations, contrast/token evidence
  (or an explicit *not-verified* status), and acceptance criteria. [EXPLICIT]
- Confirm ARIA is not redundant on native controls and that `aria-hidden` does
  not hide focusable or meaningful content. [EXPLICIT]
- Provide a test matrix: automated checks, keyboard, screen-reader smoke,
  contrast/non-text contrast, reduced motion, 200% zoom/reflow, forced colors. [EXPLICIT]

## Keyboard contracts (reference)

Specify these when the pattern is in scope. `Esc`, `Tab`, and arrow semantics
are the usual gaps. [DOC]

| Pattern | Required keys | Focus rule |
|---|---|---|
| Dialog (modal) | `Esc` closes; `Tab`/`Shift+Tab` cycle within | Trap focus; return to trigger on close |
| Tabs | `←`/`→` move tabs; `Home`/`End` jump; `Tab` exits to panel | Roving tabindex; one tab stop for the tablist |
| Accordion / disclosure | `Enter`/`Space` toggles | Focus stays on the header after toggle |
| Menu (button) | `↓` opens + first item; `↑`/`↓` move; `Esc` closes | Return focus to the menu button on close |
| Combobox / listbox | `↓`/`↑` move options; `Enter` selects; `Esc` collapses | Focus stays in the input; `aria-activedescendant` tracks |
| Toast / live region | none (must not steal focus) | `aria-live="polite"`; `assertive` only for errors |
| Skip link | `Tab` reveals as first focusable; `Enter` jumps | Move focus to the target landmark |

## Worked example — custom "copy" icon button

Bad: `<div class="icon" onclick="copy()">📋</div>` — not focusable, no name, no
key support, emoji read literally. [INFERENCIA]

Good spec: `<button type="button" aria-label="Copy to clipboard">` with the
glyph as `aria-hidden="true"`; native `<button>` supplies role, `Tab` stop,
and `Enter`/`Space`. On success, announce via a `role="status"` live region
("Copied"). Visible focus ring ≥3:1 against the adjacent background; the icon's
foreground ≥3:1 (non-text contrast). [EXPLICIT]
Acceptance: reachable by `Tab`; activates on `Enter` and `Space`; SR reads
"Copy to clipboard, button"; success announced once, not on every render. [EXPLICIT]

## Quality Criteria

- [ ] All interactive elements are keyboard accessible
- [ ] Native HTML used before ARIA; every ARIA use has a clear purpose
- [ ] Name, role, value/state, and description specified for custom controls
- [ ] Color contrast meets WCAG AA ratios for text and non-text UI states
- [ ] Forms have visible labels, programmatic labels, error messages, descriptions, recovery flow
- [ ] Focus order, visibility, return, and route-change focus are specified
- [ ] Reduced motion, zoom/reflow, and sensory-independent cues addressed
- [ ] Acceptance criteria and validation matrix included

## Anti-Patterns

- ARIA overuse: roles on already-semantic elements (`role="button"` on a `<button>`)
- Visible focus removal (`outline: none`) without replacement
- Color as the only means of conveying information
- `aria-label` that hides or contradicts visible text
- Focusable content inside `aria-hidden="true"`
- Custom widgets without a keyboard interaction model
- `aria-live` region injected *after* its content exists (SR misses the change) — render the empty region first, then populate [INFERENCIA]
- Placeholder used as the only label (disappears on input, low contrast) [INFERENCIA]

## Related Skills

- `html-semantic` — semantic HTML is the foundation of accessibility
- `form-engineering` — accessible form patterns and validation
- `responsive-design` — responsive and accessible design overlap significantly
- `accessibility-audit` — use when the primary output is an audit report
- `accessibility-testing` — use when the primary output is test automation or manual test execution

## Usage

Example invocations:

- "/accessibility-design" — Run the full accessibility design workflow
- "accessibility design on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]
- If contrast ratios, runtime behavior, or assistive-technology output cannot be
  verified, mark them *not verified* and state the evidence needed (e.g. run a
  contrast checker on the resolved token values, smoke-test with NVDA/VoiceOver). [EXPLICIT]
- Contrast specs assume token values resolve to fixed colors; themed/dynamic
  tokens must be checked per theme, not once. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Design mandates a non-native widget | Accept it, but own the full keyboard + ARIA contract; flag the added test surface |
| Contrast unverifiable (dynamic theming) | Mark not-verified; require per-theme check before sign-off |
| Third-party/embedded component | Treat its a11y as unverified; spec a wrapper or document the gap |

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
