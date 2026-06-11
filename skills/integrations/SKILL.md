---
name: integrations
description: "Third-party service integration: payments, webhooks, push notifications, and captcha. Topics: payment-integration, push-notifications, recaptcha-integration, webhook-handling."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
