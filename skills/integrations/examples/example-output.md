# Example output — integrations

Worked deliverable for the `example-input.md` Stripe fulfillment incident.

## 1. Routing decision
- **Resolved topic:** payment-integration
- **Depth:** deep
- **Playbook read:** references/payment-integration.md  _(only this one)_
- **Provider:** Stripe (Checkout, one-time purchases)
- **Routing rationale:** "Stripe / Checkout / charged / provisioned / webhook"
  keywords; failure is in webhook-driven fulfillment. [INFERENCIA]

## 2. Discover
- Current flow: client redirect to success page provisions the user. [CÓDIGO]
- Two incidents: (a) charged-but-not-provisioned = missed/ignored event;
  (b) double provisioning = non-idempotent handler. [INFERENCIA]
- Stripe secret + webhook signing secret already in Firebase secrets — no
  `[VACIO_CRITICO]`. [CONFIG]

## 3. Analyze
- **Decision:** make signature-verified webhooks the source of truth; the client
  redirect becomes a UX hint only. [DOC]
- Events to subscribe: `checkout.session.completed` (one-time fulfillment),
  plus `charge.refunded` / `charge.dispute.created` for reversals. [DOC]
- **The one critical failure:** duplicate fulfillment under Stripe's retry —
  closed by idempotency keyed on `event.id`. [DOC]

## 4. Execute
| Step | What was wired | Evidence |
|------|----------------|----------|
| Endpoint | Cloud Function HTTP trigger over the **raw** body | [CÓDIGO] |
| Verify | `stripe.webhooks.constructEvent(rawBody, sig, endpointSecret)`; bad sig → 400 | [DOC] |
| Idempotency | atomic insert of `event.id` in Firestore; duplicate → ack 200, no re-fulfill | [INFERENCIA] |
| Fulfillment | provision on `checkout.session.completed`; move provisioning off the client redirect | [CÓDIGO] |
| Reconcile | scheduled sweep over recent `invoice.paid`/sessions to catch any missed event | [INFERENCIA] |
| Secrets | read from Firebase secrets; never inlined or client-side | [CÓDIGO] |

## 5. Validation gate
- [x] Exactly one playbook read; `topic = payment-integration`. [CONFIG]
- [x] Stripe secret + signing secret referenced from Firebase secrets. [CÓDIGO]
- [x] Signature verified against raw body before any field is trusted. [DOC]
- [x] Idempotent on `event.id`; replay shows no double-fulfillment
      (verified via `stripe trigger checkout.session.completed`). [DOC]
- [x] No PAN touches our servers (hosted Checkout, SAQ-A scope). [DOC]
- [x] Evidence tags applied; no mixed families.

## 6. Open items
- `[SUPUESTO]` Confirm event names + test-card numbers against current Stripe
  docs before release.
- `[SUPUESTO]` Decide dispute/chargeback access-revocation policy.

## 7. Gate result
**gate = pass** — fulfillment is webhook-driven, signature-verified, and
idempotent; both reported incidents are closed.
