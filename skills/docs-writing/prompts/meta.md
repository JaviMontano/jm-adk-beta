# Meta prompt — docs-writing

Reasoning scaffold for operating the `docs-writing` router well. Use this to decide HOW
to route and validate, not to write the deliverable itself.

## Routing reasoning

- Read the request for the deliverable NOUN (a changelog? an API reference? a memo?) —
  that noun is the strongest routing signal. Verbs ("draft", "document") are weaker.
- If the request names a transformation (release diff → notes) the *output* type wins
  the route, not the input.
- Hold the one-route rule as a hard constraint: if you feel pulled toward two playbooks,
  that is the signal to ask one disambiguating question, not to merge them.

## Depth reasoning

- Choose `deep` when the artifact will be published, audited, or read by an external
  audience; `quick` for internal drafts and quick turnarounds.
- `deep` adds verification per step (lint the spec, replay an example, re-review a doc),
  not just more prose.

## Evidence reasoning

- Tag a claim only when it is non-obvious; self-evident lines stay clean to control
  density.
- When two tags fit, choose the weaker (e.g. `[INFERENCIA]` over `[DOC]`) — under-claim
  rather than over-claim provenance.
- Treat every `[SUPUESTO]` as a debt: it must carry the step that retires it.

## Self-check before declaring done

1. Did I read exactly one playbook? 
2. Did the spine reach Validate?
3. Is the tag family single and consistent?
4. Is every `[SUPUESTO]` paired with a check?
5. Any invented price, PII, or second brand? If yes → BLOCK and fix.
