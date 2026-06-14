# Routing checklist — ai-architecture

Run this before handing off any ai-architecture deliverable. [CONFIG]

## Resolve
- [ ] Request is AI/LLM-system shaped (else do not route here). [INFERENCIA]
- [ ] Exactly one `topic` chosen, present in the enum. [DOC]
- [ ] Chosen by intent, not keyword match. [INFERENCIA]
- [ ] If two topics fit equally, asked exactly one clarifying question. [SUPUESTO]
- [ ] If none fit, stopped and reported the gap — no force-fit. [SUPUESTO]

## Dispatch
- [ ] Read exactly one `references/<topic>.md`. [DOC]
- [ ] Did NOT bulk-load the cluster "to compare". [DOC]
- [ ] `depth` set and honored (quick=essentials / deep=exhaustive). [INFERENCIA]

## Validate
- [ ] Output uses ONE evidence-tag family (Alfa core). [CONFIG]
- [ ] Playbook's own gate satisfied and named. [DOC]
- [ ] Output is the playbook's artifact, not an inline answer. [DOC]
- [ ] Deterministic/script checks (if any) ran offline. [CÓDIGO]

## Govern
- [ ] No invented prices. [SUPUESTO]
- [ ] No client PII. [SUPUESTO]
- [ ] Single brand. [SUPUESTO]
