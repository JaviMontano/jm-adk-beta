# Meta Prompt: email-comms

Guidance for reasoning about HOW to run the email-comms router, not the email
task itself. [DOC]

## Self-check before answering

1. **Did I pick exactly one topic?** If I'm about to read two playbooks "to be
   safe," stop — that defeats the router. Sequence prerequisites instead. [DOC]
2. **Is the topic actually resolvable?** If the request could be sending OR
   templates with no signal, ask ONE question. An unresolvable topic is
   stop-and-ask, never an `[ASSUMPTION]`. [DOC]
3. **Am I confusing problem spaces?** Deliverability (does it arrive),
   render (does it display), and content (does it engage) fail independently.
   Falling opens with steady CTOR is deliverability, not bad copy. [DOC]

## Failure-mode heuristics

- Reaching for Lighthouse / flexbox / web fonts ⇒ I've slipped into web habits;
  email render engines reject them. [INFERENCE]
- Publishing DMARC `p=reject` before SPF/DKIM align ⇒ I'll silently drop
  legitimate mail. Ramp from `none`. [DOC]
- Optimizing open rate in isolation ⇒ Apple MPP inflates it; judge by CTOR. [DOC]
- Editing `routes:` to fit a request ⇒ invent nothing outside the enum. [DOC]

## Evidence discipline

Every claim gets an Alfa core EN tag. Mark vendor thresholds (dedicated-IP
volume, warm-up schedule) `[ASSUMPTION]` until confirmed against current docs.
Never mix the Jarvis `{…}` tag family. [DOC]

## Calibration of depth

`quick` answers the essential path; `deep` verifies each step and runs the full
render/deliverability matrix. Escalate to `deep` for production sends. [INFERENCE]
