# Email-Comms Routing Checklist

Run this before reading any playbook. It enforces the one-topic-per-run
discipline. [DOC]

## Step 1 — Classify the request

- [ ] Is it about mail **arriving / not in spam / DNS / provider / bounces**?
      → `email-sending`
- [ ] Is it **building new responsive HTML** (Firebase `mail` doc, inline CSS,
      ≤600px)? → `email-template-builder`
- [ ] Is it a **render bug / Outlook / MJML / dark mode / Gmail clip**?
      → `email-templates`
- [ ] Is it **standing up or diagnosing a newsletter** (open/click rates,
      subject, cadence)? → `newsletter-design`

## Step 2 — Resolve conflicts

- [ ] Maps to two topics? Run the **prerequisite first**:
      builder → templates → sending; newsletter-design → email-template-builder. [INFERENCE]
- [ ] Genuinely ambiguous? Ask **one** question — do not guess, do not tag as
      `[ASSUMPTION]`. [DOC]
- [ ] Out of scope (SMS / push / in-app messaging)? Redirect; don't invent a
      topic. [DOC]

## Step 3 — Guard the diagnosis

- [ ] Falling opens + steady CTOR ⇒ deliverability, not content
      (route to `email-sending`). [DOC]
- [ ] About to publish DMARC `p=reject` first? Stop — ramp from `none`. [DOC]
- [ ] Reaching for Lighthouse / flex / web fonts? Stop — web habits invalid in
      email. [INFERENCE]

## Step 4 — Commit

- [ ] Exactly ONE playbook selected from `routes:`.
- [ ] Depth set (`quick` / `deep`).
- [ ] Proceed to Discover → Analyze → Execute → Validate.
