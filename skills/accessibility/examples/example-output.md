# Example Output — accessibility (testing topic)

> Response to `examples/example-input.md`. Single playbook loaded: `references/testing.md`.

## 1. Routing & scope
- **Topic:** testing (verification evidence on existing UI)
- **Target:** `/checkout`, states: payment dialog open and on close
- **WCAG target:** 2.1 AA
- **Depth:** deep
- **Environment:** Chromium (Playwright), 1280×800; VoiceOver + Safari 17 (macOS);
  no NVDA available — NVDA coverage `not verified`. Date: 2026-06-12.

## 2. Summary verdict
- **Status:** fail
- **Rationale:** axe is clean in scanned states, but a manual keyboard test
  reproduces focus loss on dialog close. A clean scan does not override a manual
  blocker. [EXPLICIT]
- **Coverage note:** automated covers ~30–40% of SCs; the blocker here is in the
  manual remainder. [INFERENCE]

## 3. Automated evidence
| Route/Component | State | Tool + version | Rule id | Impact | Selector | WCAG tags | Artifact |
|---|---|---|---|---|---|---|---|
| /checkout payment dialog | dialog open | @axe-core/playwright 4.x | (none) | — | `[role=dialog]` | — | artifacts/axe-checkout-dialog.json |

Reported as "0 axe violations in scanned states", never "accessible". [CODE]

## 4. Manual findings
| ID | Type | WCAG SC (level) | Expected | Observed | Severity | Evidence | Status |
|---|---|---|---|---|---|---|---|
| A11Y-014 | keyboard | 2.4.3 Focus Order (AA); 2.1.2 No Keyboard Trap (A) | On `Esc`, dialog closes and focus returns to the trigger button | Dialog closes; focus lands on `<body>` (lost) | high | artifacts/a11y-014-focus.png, traces/checkout.zip | fail → retest pending |
| A11Y-015 | screen reader | 4.1.2 Name, Role, Value (A) | VoiceOver announces "Payment, dialog" on open | Announced "Payment" with no dialog role | medium | VO+Safari notes | conditional |

## 5. Findings detail
- **A11Y-014 — focus not restored on close**
  - **WCAG:** 2.4.3 Focus Order (AA); 2.1.2 No Keyboard Trap (A)
  - **User impact:** keyboard users lose their place after closing the dialog and
    must tab from the top of the page. [EXPLICIT]
  - **Reproducer:** Tab to "Pay", open dialog, press `Esc`.
  - **Expected:** focus returns to the element that opened the dialog.
  - **Fix / acceptance check:** store the trigger ref on open; on close call
    `trigger.focus()`. Acceptance: after `Esc`, focus is on the "Pay" trigger.
  - **Evidence:** traces/checkout.zip
  - **Tag:** [EXPLICIT]

## 6. Suppressions / exceptions
None.

## 7. Gate checklist
- [x] Exactly one playbook loaded (testing); topic matches intent
- [x] Every finding cites a WCAG SC + concrete fix
- [x] Automated + manual evidence present; NVDA marked `not verified`
- [x] Status is fail (no green-as-success despite clean axe)
- [x] One evidence tag per claim
- [x] No invented prices, no client PII, single-brand
