# Example Output — ux-design (design-critique)

**Topic (route):** design-critique · **Depth:** quick · **User goal:** returning
customer completes a card payment on mobile. [EXPLICIT]

> One playbook Read: `references/design-critique.md`. No other reference loaded.

## Strengths worth keeping

- The order-summary card surfaces the total ($128.40) before the payment fields,
  matching the user's real-world expectation of confirming the amount before
  paying (heuristic: match to real world). Keep it. [EXPLICIT]

## Issues — ordered by severity

| # | Location | Heuristic | Observation → Impact → Suggestion | Severity |
|---|----------|-----------|-----------------------------------|----------|
| 1 | Pay button | Error prevention | No loading/disabled state → a slow network lets the user tap 'Pay' twice → on success this double-submits and can double-charge → disable the button and show a spinner on first tap until the request resolves. | Blocker [SUPUESTO] |
| 2 | Pay / Cancel pair | Aesthetic + match to real world | Both buttons are green, equal size and weight → the destructive 'Cancel' competes visually with the primary action, inviting misclicks that abandon a near-complete payment → make 'Pay' the sole filled primary (note: filled success affordance must NOT be green — green is decorative-only; use the brand primary), demote 'Cancel' to a text/ghost button. | Major |
| 3 | Failure message | Help users recover from errors | 'Error 402. Your transaction could not be processed.' exposes a raw status code and gives no next step → the user does not know whether to retry, edit the card, or use another method → rewrite blameless + actionable, e.g. "We couldn't authorize this card. Check the number and expiry, or try a different card." | Major |
| 4 | Expiry / CVC row | Recognition over recall | Two fields share one row with no inline format hint → on a narrow mobile viewport the user guesses the expiry format → add placeholder/format hints (MM/YY, 3-digit CVC) and an input mode that triggers the numeric keypad. | Minor |

## Validation gate

- [x] Exactly one playbook Read (`design-critique`).
- [x] Strengths named before issues; each issue tied to the stated user goal.
- [x] Observation → impact → suggestion framing on every item; severities calibrated.
- [x] Blocker marked `[SUPUESTO]` — double-charge risk to be confirmed with a
  real network-throttle test before treated as proven.
- [x] No green-as-success: the fix explicitly rejects a green primary affordance.
- [x] No `{VACIO_CRITICO}` left; no invented metrics; single brand. [EXPLICIT]
