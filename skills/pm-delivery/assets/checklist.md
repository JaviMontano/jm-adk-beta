# Acceptance Checklist — pm-delivery

Reusable gate the guardian role walks before emitting `dod=pass`. Each item
requires cited evidence, not a self-assertion. [EXPLICIT]

## Routing
- [ ] Topic is one of the 11 enums; none invented or renamed.
- [ ] Exactly one playbook from `routes.json` was loaded (no merge/pre-read).
- [ ] If two topics fit, one disambiguating question was asked.

## Method
- [ ] All four spine phases ran: Discover → Analyze → Execute → Validate.
- [ ] Output matches the loaded playbook's template/schema.

## Evidence
- [ ] Every non-trivial claim tagged EXPLICIT / INFERENCE / ASSUMPTION.
- [ ] Evidence-tag summary included.
- [ ] WARNING banner present if ASSUMPTION share > 30%.

## Cost discipline
- [ ] No currency, rate, or price anywhere.
- [ ] Cost/budget/capacity in FTE-months with optimistic/expected/pessimistic
      bands where the topic calls for an estimate.

## Topic-specific completeness
- [ ] risk-assessment: all 7 categories addressed or N/A-with-reason; every
      High/Medium has a named mitigation.
- [ ] okr-design: 2–5 outcome KRs, each baseline→target→due+owner.
- [ ] stakeholder-mapping: power/interest grid + RACI.

## Governance
- [ ] Constitution v6.0.0 + script-first satisfied.
- [ ] No implementation detail in an analysis deliverable (phase separation).
- [ ] Single brand; no client PII.
- [ ] No gate reported as passed without evidence.
