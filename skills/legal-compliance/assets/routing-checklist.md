# Routing checklist — legal-compliance (pre-flight)

Run before executing any lane. All boxes must be checked or the lead stops and asks.

## Resolve topic
- [ ] Request matches exactly one lane:
  - clause / contract / MSA / indemnity / renewal → `contract-review`
  - posture vs named regulation (GDPR/SOX/PCI-DSS/HIPAA/ISO 27001/NIST CSF) → `compliance-assessment`
  - designing controls / policies / control library + evidence → `compliance-framework`
- [ ] If two lanes fit → ONE disambiguating question asked; route NOT guessed.

## Resolve depth
- [ ] `depth` set: `quick` (essentials) or `deep` (exhaustive, verify each step).

## Single-playbook discipline
- [ ] Only the routed `references/*.md` file is read.
- [ ] No second playbook loaded "for context."
- [ ] Multi-topic request → lanes sequenced, one playbook each.

## Critical-input check (stop-and-ask triggers)
- [ ] contract-review: executed copy + all exhibits/schedules present; governing law stated.
- [ ] compliance-assessment: applicable frameworks + framework versions known; control docs available.
- [ ] compliance-framework: framework version pinned; project artifacts accessible.

## Scope guardrails
- [ ] No net-new drafting, litigation strategy, certification issuance, or
      jurisdiction-specific enforceability — defer to counsel.
- [ ] Verbatim disclaimer slot reserved in the output template.
