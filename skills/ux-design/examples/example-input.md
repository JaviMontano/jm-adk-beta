# Example Input — ux-design

## Request

"Critique this checkout payment screen. Our user goal is for a returning customer
to complete a card payment on mobile. Layout, top to bottom:

- A summary card showing order total ($128.40).
- A card-number field, then expiry and CVC on one row.
- A green 'Pay' button and, directly beside it at equal size and weight, a green
  'Cancel' button.
- On a failed payment we currently show: 'Error 402. Your transaction could not
  be processed.'
- The 'Pay' button has no loading or disabled state, so a slow network lets the
  user tap it twice.

Which decisions are open: button styling, error copy, and the loading state are
all still editable. The order-summary card is locked."

## Routing signal

Artifact = a screen; the verb is "critique"; a user goal is supplied → topic
resolves to `design-critique`, not `error-messaging` (the error copy is one item
inside a full-screen review, not the whole request). `depth=quick` (no request
for an exhaustive sweep).
