# Routing checklist — kata

Run top to bottom before and after applying a kata.

## Before applying

- [ ] Request mapped to exactly one `routes:` key. [DOC]
- [ ] If two keys plausibly fit, both presented and user asked. [DOC]
- [ ] `depth` set (`quick` or `deep`). [DOC]
- [ ] Only `references/<topic>.md` opened — no second playbook. [INFERENCIA]
- [ ] Playbook precondition/assumptions confirmed to hold for this request. [INFERENCIA]

## After applying

- [ ] Output follows the playbook's structure, not improvised prose. [DOC]
- [ ] Correct pattern instantiated; anti-pattern removed. [CÓDIGO]
- [ ] Relevant edge cases from the playbook addressed. [DOC]
- [ ] Out-of-scope concerns deferred to named neighboring katas. [DOC]
- [ ] Every acceptance criterion in the playbook met (checklist filled). [DOC]
- [ ] One Alfa-core tag per non-obvious claim; no mixed families. [DOC]
- [ ] Every `[SUPUESTO]` paired with a verification step. [DOC]
- [ ] Script-first honored; no invented prices; no client PII; single brand. [DOC]

## Re-route trigger

- [ ] If evidence contradicted the chosen topic, STOP, named the mismatch, and
      re-resolved `topic` instead of force-fitting. [INFERENCIA]
