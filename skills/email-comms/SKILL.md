---
name: email-comms
description: "Email systems and communication: transactional sending, templates, and newsletters. Topics: email-sending, email-template-builder, email-templates, newsletter-design."
params:
  topic:
    enum: [email-sending, email-template-builder, email-templates, newsletter-design]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  email-sending: references/email-sending.md
  email-template-builder: references/email-template-builder.md
  email-templates: references/email-templates.md
  newsletter-design: references/newsletter-design.md
---

# email-comms

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
