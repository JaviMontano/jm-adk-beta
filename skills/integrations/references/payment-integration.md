<!-- distilled from alfa skills/payment-integration -->
<!-- > -->
# Payment Integration

> "Payment flows must be the most tested, most reliable, most boring code in your system." — Unknown

## TL;DR

Guides payment integration with Stripe and PayPal — Checkout sessions, subscription management, webhook-driven fulfillment, refund handling, and PCI compliance. Use when adding payment processing, subscription billing, or one-time purchases to your application. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify payment types: one-time, recurring subscription, usage-based (metered)
- Check Stripe/PayPal account setup, API key configuration, and whether the account is in a region Stripe supports for payouts [SUPUESTO] — verify in Dashboard before committing
- Review product/price catalog requirements (currencies, billing intervals, tiers)
- Determine tax (Stripe Tax vs manual), currency, and regional payment method requirements

### Step 2: Analyze
- Choose integration approach (decision below): Stripe Checkout (hosted) vs Stripe Elements (embedded)
- Plan subscription lifecycle: `trialing` → `active` → `past_due` → `canceled`/`unpaid`
- Design webhook-driven fulfillment — never trust client-side payment confirmation [DOC]
- Evaluate SCA / 3D Secure (Strong Customer Authentication) requirements for EU/UK [DOC]

### Step 3: Execute
- Create Stripe products and prices via API or Dashboard
- Implement Checkout Session creation server-side (Cloud Function / backend endpoint)
- Set up webhook endpoint for: `checkout.session.completed`, `invoice.paid`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted` [DOC]
- **Verify webhook signature** with `stripe.webhooks.constructEvent(body, sig, endpointSecret)` using the *raw* request body — parsed JSON breaks signature validation [DOC]
- **Idempotency**: store processed `event.id`; on replay, ack 200 without re-fulfilling. Fulfillment must be idempotent because Stripe retries until it gets a 2xx [DOC]
- Build subscription management: upgrade, downgrade, cancel, resume (set proration_behavior explicitly)
- Handle payment failures with dunning: rely on Stripe Smart Retries + `invoice.payment_failed` notifications; gate access on subscription status, not on last charge
- Implement refund processing via admin interface (full + partial; record reason)
- Store `customer`/`subscription` IDs in Firestore linked to user documents; treat Stripe as source of truth for status [INFERENCIA]
- Use Stripe test mode and test card numbers for development

### Step 4: Validate
- Test full purchase flow with Stripe test cards: success `4242…`, decline `4000…0002`, 3DS-required `4000…3155` [DOC]
- Verify webhook processes all subscribed events and is idempotent under replay
- Confirm subscription lifecycle transitions (trial end, payment failure → past_due, cancellation, resume)
- Confirm no raw card data (PAN) touches your servers — keeps you in PCI SAQ-A scope [DOC]
- Replay a webhook via `stripe trigger` / CLI to confirm no double-fulfillment [CONFIG]

## Decisions & Trade-offs

| Decision | Choose | When / Trade-off |
|----------|--------|------------------|
| Checkout (hosted) vs Elements (embedded) | **Checkout** by default | Hosted page = lowest PCI scope (SAQ-A), SCA/wallets handled for you, less UI control. Elements only when brand-controlled in-page checkout is required and you accept more frontend + compliance work. [INFERENCIA] |
| Sync strategy | **Webhooks as source of truth** | Polling/client callbacks miss async events (delayed 3DS, bank declines, disputes). Webhooks are authoritative; client redirect is a UX hint only. [DOC] |
| Plan change proration | **Explicit `proration_behavior`** | `create_prorations` for fair mid-cycle billing; `none` for simpler UX. Defaulting silently surprises customers on the next invoice. [INFERENCIA] |
| Stripe vs PayPal | Stripe for cards/subscriptions; add PayPal as an extra method | PayPal subscription webhooks and refund APIs differ — do not assume Stripe semantics carry over. [SUPUESTO] |

## Quality Criteria

- [ ] Payment confirmation driven by webhooks, not client-side callbacks
- [ ] Webhook signature verified against raw body; bad signatures rejected with 400
- [ ] Webhook handler idempotent (dedup on `event.id`); replays do not re-fulfill
- [ ] Stripe secret keys stored as Firebase secrets / env, never in client code
- [ ] Subscription status synced Stripe → Firestore via webhooks (Stripe authoritative)
- [ ] All Stripe test scenarios covered (success, decline, 3D Secure, disputes)
- [ ] Access gated on subscription status, not on a single charge result
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Confirming payment on the client side without webhook verification (users can skip payment)
- Exposing Stripe secret key in frontend code
- Building custom card input forms instead of using Stripe Elements (PCI scope increase)
- Parsing the webhook body to JSON before signature check — silently fails validation
- Returning 5xx/timeout from the webhook on a downstream error — Stripe retries the *same* event, causing duplicate fulfillment if the handler isn't idempotent

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|-----------|
| Duplicate fulfillment | User charged once, provisioned twice | Idempotent handler keyed on `event.id` |
| Lost webhook | Paid user not provisioned | Reconcile via scheduled `invoice.paid` sweep; never rely solely on client redirect [INFERENCIA] |
| Out-of-order events | `subscription.updated` arrives after `deleted` | Re-fetch object from API on receipt; trust latest API state, not payload order [INFERENCIA] |
| Webhook secret rotation | All events 400 | Support both old+new endpoint secrets during rotation window [SUPUESTO] |
| Dispute/chargeback | Silent revenue loss | Subscribe to `charge.dispute.created`; revoke access per policy |

## Related Skills

- `webhook-handling` — Stripe webhooks drive the payment fulfillment flow
- `ecommerce-frontend` — checkout UI that triggers payment processing

## Usage

Example invocations:

- "/payment-integration" — Run the full payment integration workflow
- "payment integration on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: does not cover marketplace/Connect payouts, in-app purchase (Apple/Google) billing, or crypto rails — those need dedicated flows [SUPUESTO]
- Card-number specifics and event names reflect Stripe's documented test set; confirm against current Stripe docs before shipping [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Trial with no card on file | Decide gate-at-signup vs gate-at-trial-end; handle `trial_will_end` |
| Currency/region mismatch | Validate supported currency per price before session creation |
