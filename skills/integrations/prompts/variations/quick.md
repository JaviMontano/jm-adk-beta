# Quick variation — integrations (`depth: quick`)

Fast path for wiring one provider. Resolve the topic, read ONE playbook, and
cover the happy path plus the single failure that loses money or drops events.

## Steps
1. Resolve `topic` (payment / push / recaptcha / webhook) from keywords; ask
   only on real ambiguity.
2. Read the one matching playbook from `routes:`.
3. Implement the happy path:
   - **payment** — server-side Checkout Session + webhook-driven fulfillment.
   - **push** — contextual permission + token store + Admin SDK send.
   - **recaptcha** — `grecaptcha.execute` + server-side `siteverify`.
   - **webhook** — raw-body signature verify + fast `200` ack + async work.
4. Close the one critical failure:
   - payment/webhook → idempotency keyed on event ID (no double-fulfill).
   - recaptcha → reject client score; verify server-side only.
   - push → prune stale tokens on the not-registered error.
5. Run the minimal Validation gate: one playbook read, secrets server-side,
   signature/origin verified, money/event path idempotent.

## Keep it lean
No exhaustive lifecycle coverage. Tag claims; flag deferred `[SUPUESTO]` items
for a later `deep` pass. Stop on any missing secret (`[VACIO_CRITICO]`).
