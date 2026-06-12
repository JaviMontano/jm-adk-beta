# Routing + done checklist — docs-writing

Run this checklist on every `docs-writing` invocation. [CONFIG]

## Before writing (routing)

- [ ] Identified the deliverable noun in the request (changelog? API ref? memo?).
- [ ] Mapped it to exactly one `topic` enum value.
- [ ] If two topics were plausible, asked one disambiguating question — did not guess.
- [ ] If no topic matched, decided to write directly without routing.
- [ ] Read `references/<topic>.md` — only that one playbook.
- [ ] Set `depth` (`quick` internal / `deep` published-or-audited).

## While writing (spine)

- [ ] Discover: inventoried sources; logged each gap as `[SUPUESTO]` + its check.
- [ ] Analyze: recorded the trade-off accepted, not just the chosen approach.
- [ ] Execute: filled `templates/output.md`; realistic examples; secrets/PII redacted.
- [ ] Tagged every non-obvious claim with one family; picked the weaker tag when two fit.

## Before declaring done (validate)

- [ ] Ran the routed playbook's full Quality Criteria — none unchecked.
- [ ] Every `[SUPUESTO]` retired or carried with its verification step.
- [ ] No invented prices; no client PII; single brand; no green-as-success.
- [ ] Guardian verdict recorded (PASS, or BLOCK + failing gate + fix owner).
