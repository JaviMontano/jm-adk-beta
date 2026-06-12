# Example input — integrations

A concrete request a user brings to this skill.

> "We just launched Stripe Checkout for one-time purchases. The redirect back to
> our success page provisions the user, but we've had two cases where a customer
> was charged and never provisioned, and one where a user got the product twice.
> We're on Firebase (Cloud Functions + Firestore). Make fulfillment reliable. We
> already have the Stripe secret key and the webhook signing secret in Firebase
> secrets."

## Signals to extract
- Keywords: Stripe, Checkout, charged, provisioned, webhook → **topic =
  payment-integration** (the failure lives in webhook-driven fulfillment).
- Symptoms: lost provisioning (missed event) + double provisioning (non-idempotent
  handler) → the two failure modes the playbook targets.
- Depth: production incident with money on the line → **depth = deep**.
- Constraints: Firebase Cloud Functions + Firestore; secrets already exist (no
  `[VACIO_CRITICO]`).

## Expected routing
Resolve `topic = payment-integration`, `depth = deep`, read ONLY
`references/payment-integration.md`, and apply it — moving fulfillment off the
client redirect and onto a signature-verified, idempotent webhook handler.
