# Quick Variation: email-comms

`depth=quick`. Resolve the topic and deliver the essential path only. [DOC]

## Use when

The user wants a fast, correct answer — not the full render/deliverability
matrix. E.g. "which SPF record do I publish for SendGrid?" or "give me a
single-column responsive table shell."

## Compressed procedure

1. Map request → one topic (routing table in `prompts/primary.md`). Ask one
   question only if genuinely ambiguous. [INFERENCE]
2. Read that one playbook; pull the TL;DR + the directly relevant Execute steps.
3. Deliver the minimal artifact + the 2–3 must-pass Validate checks for that
   topic:
   - email-sending → SPF/DKIM/DMARC present + suppression + one-click unsub. [DOC]
   - email-template-builder → ≤600px table, inline CSS, alt on images. [DOC]
   - email-templates → renders in Gmail+Outlook, legible images-off. [DOC]
   - newsletter-design → one CTA, subject+preheader pair, UTMs. [DOC]
4. Tag each claim (Alfa core EN). Flag anything skipped for `deep`. [DOC]

## Do not

Run the full Litmus matrix or DMARC ramp planning in quick mode — note them as
deferred to `deep`. [INFERENCE]
