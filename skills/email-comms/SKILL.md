---
name: email-comms
version: 1.0.0
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

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`. [DOC]

## When to use
Any email task: provider/transactional sending, building responsive HTML
templates, picking a template, or designing a newsletter. Not for in-app
messaging, push, or SMS — those route elsewhere. [INFERENCE]

## Topic selection
- **email-sending** — wiring a provider/extension to actually send mail. [DOC]
- **email-template-builder** — authoring new responsive HTML (table layout,
  inline CSS, 600px max-width). [CODE]
- **email-templates** — choosing/applying an existing template. [DOC]
- **newsletter-design** — layout/content for broadcast newsletters. [DOC]

If the request maps to two topics, run the prerequisite first
(builder → templates → sending). [INFERENCE]

## Procedure
1. Map request → one `topic` enum; if ambiguous, ask one question — do not guess. [DOC]
2. Read ONLY that route's playbook. Never load the whole cluster. [DOC]
3. Set `depth`: `quick` = essentials; `deep` = exhaustive, verify each step. [DOC]
4. Run the playbook spine: Discover → Analyze → Execute → Validate. [DOC]

## Guardrails
- Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first. [CONFIG]
- Tags use Alfa core EN ([DOC]/[INFERENCE]/[CODE]/[CONFIG]/[ASSUMPTION]); never
  mix the Jarvis `{…}` family. An unresolvable topic is stop-and-ask, not an [ASSUMPTION]. [DOC]

## Assets
Routing checklist and quality rubric live in `assets/` (see `assets/README.md`). [DOC]

## Anti-patterns
- Loading multiple playbooks "to be safe" — defeats the router. [INFERENCE]
- Inventing a topic outside the enum, or editing `routes:` to fit a request. [DOC]
- Marking done without the Validate step. [DOC]