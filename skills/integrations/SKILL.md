---
name: integrations
version: 1.0.0
description: "Third-party service integration router: routes to one playbook for payment-integration, push-notifications, recaptcha-integration, or webhook-handling. Use when wiring an external provider (Stripe/PayPal, FCM/APNs, reCAPTCHA, inbound webhooks)."
params:
  topic:
    enum: [payment-integration, push-notifications, recaptcha-integration, webhook-handling]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  payment-integration: references/payment-integration.md
  push-notifications: references/push-notifications.md
  recaptcha-integration: references/recaptcha-integration.md
  webhook-handling: references/webhook-handling.md
---

# integrations

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`.
Never load the cluster — one route per invocation keeps context lean. [INFERENCIA]

**Inputs:** `topic` (required, from enum), `depth` (`quick`|`deep`). **Output:**
resolved playbook applied with Alfa-core tags (`[CÓDIGO]` `[CONFIG]` `[DOC]`
`[INFERENCIA]` `[SUPUESTO]`); never mix tag families. [CONFIG]

## Resolve topic
- Stripe/PayPal/checkout/charge/refund → `payment-integration`.
- FCM/APNs/device token/notification → `push-notifications`.
- reCAPTCHA/bot-check/score/sitekey → `recaptcha-integration`.
- Inbound event/callback URL/provider POST → `webhook-handling`.
- Two topics → run sequentially, one playbook each; ambiguous → ask, never
  guess across the security boundary. [SUPUESTO]

## Depth & spine
- `quick` → happy path + the one failure mode that loses money or drops events.
- `deep` → apply the playbook exhaustively, verifying at each step. [DOC]
- Spine: Discover → Analyze → Execute → Validate. Gates: constitution v6.0.0 +
  evidence tags + script-first. [CONFIG]

## Validation gate (done = all true)
- Exactly one playbook was read; `topic` ∈ enum. [CONFIG]
- Secrets/keys never inlined — referenced from config/env. [CÓDIGO]
- Signature/origin verification present (webhook HMAC, captcha server verify,
  payment-event auth) before trusting any external payload. [DOC]
- Idempotency on money/event paths; retries are safe to replay. [INFERENCIA]

## Assets
Run-before-done routing/gate checklist and quality rubric: `assets/` (see
`assets/README.md`). [CONFIG]

## Anti-patterns
- Loading multiple playbooks "for context" — defeats the router. [INFERENCIA]
- Trusting client-side captcha scores or unverified webhook bodies. [DOC]
- Hardcoded provider secrets — `[VACIO_CRITICO]`: stop and ask. [SUPUESTO]