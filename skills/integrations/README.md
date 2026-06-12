# integrations — skill overview

Router skill for wiring third-party services into an application. It resolves a
single `topic` and loads EXACTLY ONE playbook, keeping context lean and the
security boundary explicit. One invocation = one provider integration.

## What it does

Routes a third-party integration request to one of four hardened playbooks and
applies it with Alfa-core evidence tags (`[CÓDIGO]` `[CONFIG]` `[DOC]`
`[INFERENCIA]` `[SUPUESTO]`):

| Topic | Covers | Route |
|-------|--------|-------|
| `payment-integration` | Stripe/PayPal Checkout, subscriptions, refunds, webhook-driven fulfillment, PCI SAQ-A scope | `references/payment-integration.md` |
| `push-notifications` | FCM + Web Push/VAPID, permission timing, token lifecycle, topic/segment targeting, preferences | `references/push-notifications.md` |
| `recaptcha-integration` | reCAPTCHA v3 score + App Check, server-side `siteverify`, graduated fallback | `references/recaptcha-integration.md` |
| `webhook-handling` | Inbound signature verification, idempotency, fast-ack + async, replay defense | `references/webhook-handling.md` |

## When to use

Invoke when you must connect to an external provider: accept money, send a push,
score a bot-risk signal, or react to inbound provider events. Use it the moment
secrets, signatures, or money/event idempotency enter the design — these are the
failure modes the playbooks are built to close.

Do NOT use for: outbound webhooks you emit, in-app messaging, SMS/email
channels, marketplace payouts, or edge WAF/DDoS — those are out of scope and
flagged in each playbook's Anti-Scope.

## How it routes and executes

1. Resolve `topic` from the request (keywords below); ask only on genuine
   ambiguity — never guess across the security boundary. [SUPUESTO]
2. Pick `depth`: `quick` (happy path + the one money/event-losing failure) or
   `deep` (apply the playbook exhaustively, verifying each step). [CONFIG]
3. Read ONE playbook from `routes:`. Never load the cluster. [INFERENCIA]
4. Apply along the spine Discover → Analyze → Execute → Validate, then clear the
   Validation gate before declaring done.

Topic keywords: Stripe/PayPal/charge/refund → payments · FCM/APNs/device-token →
push · reCAPTCHA/score/sitekey → recaptcha · inbound callback/provider POST →
webhooks.

## References

- `references/payment-integration.md` — payment flows + fulfillment.
- `references/push-notifications.md` — FCM/Web Push delivery.
- `references/recaptcha-integration.md` — bot-risk scoring + App Check.
- `references/webhook-handling.md` — inbound event verification.
- `routes.json` — machine-readable topic → playbook map.

## Companion bundle

- `knowledge/` — body of knowledge + concept graph for the integration domain.
- `agents/` — lead, specialist, support, guardian role contracts.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — the integration deliverable scaffold.
- `evals/evals.json` — scenario suite for routing + gate coverage.
- `examples/` — a worked Stripe-webhook fulfillment example.
- `assets/` — quality rubric + routing checklist (see `assets/README.md`).
