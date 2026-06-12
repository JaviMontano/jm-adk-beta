# Security deliverable checklist

A deterministic pre-ship checklist the guardian walks for any `security` route.
Every box must be checked for the right reason before "done." [DOC]

## Routing
- [ ] One `topic` resolved, inside the enum.
- [ ] Exactly one playbook from `routes:` loaded (no cluster-load).
- [ ] Disambiguation noted, or "unambiguous."
- [ ] `depth` chosen (`quick`/`deep`); `deep` applied the playbook in full.

## Evidence & governance
- [ ] Every non-obvious claim tagged (Alfa core set, one spelling).
- [ ] No invented prices; no client PII; single-brand.
- [ ] No unresolved `{VACIO_CRITICO}`.

## Findings (audit / verification routes)
- [ ] Six scan categories executed in canonical order (audit-security).
- [ ] `SEC-NNN` ids ascending, gapless; `Summary` counts == `Findings`.
- [ ] Severity keyed on exploitable context; placeholders are INFO, not CRITICAL.
- [ ] Every CRITICAL/WARNING has a matching remediation entry.
- [ ] Live secrets redacted in prose (mask middle, keep prefix/suffix).

## Verification
- [ ] Static layer ran (the floor).
- [ ] Runtime layer ran against a prod-equivalent target, or recorded as
      skipped (not passed).
- [ ] Layer disagreements resolved via the protocol, not by muting a check.
- [ ] Validator exit codes captured verbatim; a zero exit treated as structure,
      not safety.

## Discipline
- [ ] No insecure output marked passing (no green-as-success).
- [ ] Targets unmodified; no offensive artifact produced.
- [ ] Explicit GO / NO-GO with a tagged rationale.
