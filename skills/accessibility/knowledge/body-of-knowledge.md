# Accessibility — Body of Knowledge

Domain reference for the `accessibility` router. Grounds the four playbooks
(audit, design, testing, writing) in shared WCAG concepts, standards, and decision
rules. [DOC]

## 1. The standard
- **WCAG 2.1 AA** is the default target for every topic unless the request names a
  different level; state the assumed target so a reviewer can challenge it. [EXPLICIT]
- **POUR principles** — Perceivable, Operable, Understandable, Robust — organize the
  success criteria each finding maps to. [DOC]
- Out of this skill's scope: AAA conformance, EN 301 549 legal sign-off, VPAT/ACR
  authoring — those require a named human accessibility owner. [EXPLICIT]

## 2. Three immutable laws (from the audit playbook)
1. **Universal Access** — if a sighted mouse user can do it, a keyboard-only or
   screen-reader user must be able to do it too. [EXPLICIT]
2. **Automated First, Manual Finality** — run automation first, then manually verify
   the remaining criteria before any conformance claim. [EXPLICIT]
3. **Evidence Before Compliance** — never claim "WCAG compliant" without documented
   automated results, manual checks, scope, exceptions, and remediation status. [EXPLICIT]

## 3. Key success criteria seen across playbooks
| SC | Level | Concern |
|----|-------|---------|
| 1.1.1 Non-text Content | A | Alt text treatment by image job |
| 1.3.1 Info & Relationships | A | Semantic structure, table headers |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 text / 3:1 large text |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI controls, focus, icons |
| 2.1.1 Keyboard | A | Operable without a pointer |
| 2.1.2 No Keyboard Trap | A | Focus can leave every component |
| 2.4.3 Focus Order | AA | Logical order, return focus |
| 2.4.7 Focus Visible | AA | Never `outline:none` unreplaced |
| 4.1.2 Name, Role, Value | A | ARIA/native semantics for controls |

## 4. Coverage reality
Automated tooling (axe-core) detects roughly **30–40%** of WCAG success criteria and
is designed for ~zero false positives, so it under-reports. Order, meaning, and the
announced experience need a human. A clean scan is a trustworthy floor, never a
ceiling. [INFERENCE]

## 5. Core decision rules
- **Native before ARIA.** Prefer native HTML (ships role, state, focus, keyboard for
  free). Reach for an ARIA widget pattern only when no native element expresses the
  interaction; if forced into a custom widget, you own the full keyboard + ARIA
  contract. [INFERENCIA]
- **Report-first, not patch-first.** A wrong remediation can mask a violation from
  axe while leaving the barrier (e.g. `aria-hidden` on a focusable control). Default
  to evidence; keep the human owner in the loop. [EXPLICIT]
- **Impact-priority over tool severity.** User-blocker status reorders raw axe rule
  weight. [EXPLICIT]
- **`not verified` over assumed pass.** Untested is not passing; an assumed pass is a
  latent false claim. [EXPLICIT]
- **Browser-rendered contrast over static tokens.** Overlays, opacity, and gradients
  change the ratio a user actually sees; themed tokens are checked per theme. [INFERENCIA]
- **Pick alt treatment by the image's job**, not its content: decorative → empty alt;
  informative → one idea; functional → the action; complex → short alt + adjacent
  long description from supplied data only; text-in-image → transcribe verbatim. [DOC]

## 6. Keyboard contracts (quick reference)
- Dialog: `Esc` closes, `Tab`/`Shift+Tab` cycle within, trap focus, return to trigger.
- Tabs: `←`/`→` move, `Home`/`End` jump, roving tabindex (one tab stop).
- Menu button: `↓` opens + first item, `Esc` closes, return focus to button.
- Combobox: `↓`/`↑` move options, `Enter` selects, `aria-activedescendant` tracks.
- Toast/live region: must not steal focus; `aria-live="polite"`, `assertive` only for errors.
- Skip link: revealed on first `Tab`, `Enter` moves focus to the target landmark.

## 7. Status vocabulary
Every result is exactly one of `pass`, `conditional`, `fail`, `not verified`. No
pass-by-silence; "green CI" gates a subset, it does not certify conformance. [EXPLICIT]

## 8. Evidence taxonomy
Audit/testing playbooks use `[EXPLICIT]` plus canon `[INFERENCE]`/`[ASSUMPTION]`;
the router and design/writing use the Alfa-core family
`[CODE]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`. One tag per claim, one
family per document — no tag drift. [EXPLICIT]
