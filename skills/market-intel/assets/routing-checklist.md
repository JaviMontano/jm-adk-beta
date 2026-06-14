# Routing checklist — market-intel

Run top to bottom before committing to a playbook. Used by `agents/lead.md`
(routing) and `agents/guardian.md` (gate).

## Resolve the topic

- [ ] Mapped the request to **one** enum value via the cue table:
  - competitor matrix / stack / SWOT → `competitive-intelligence`
  - where-we-win / battle card → `competitive-positioning`
  - vs-peer / industry-median → `benchmarking-analysis`
  - TAM / trends / "research <entity>" → `market-intelligence`
  - vertical / regulatory / glossary → `sector-intelligence`
  - messaging / value props → `marketing-context`
  - ally / OEM / referral / reseller → `partnership-strategy`
  - tiers / packaging / anchoring → `pricing-strategy`
- [ ] If two topics load different playbooks → asked **one** question.
- [ ] If a disambiguator was supplied (URL/ticker/sector/role) → proceeded, stated reading.
- [ ] Request is in scope (not product spec / GTM exec / DCF / unit economics / build).

## Commit

- [ ] Read **exactly one** playbook from `routes.json`.
- [ ] Set `depth` (`quick` | `deep`); `deep` will run the Validate step.
- [ ] Logged the routing decision (topic, depth, playbook, why).

## Guard

- [ ] Did NOT load a second playbook "to be safe".
- [ ] Will honor the loaded playbook's evidence family.
- [ ] No invented prices / single brand / no PII / not green-as-success.
