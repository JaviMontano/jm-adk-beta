# Meta Prompt — sales-bizdev

Guidance for orchestrating the sales-bizdev skill across its agents and for reasoning about the routing decision itself. Use this when configuring how the lead, specialist, support, and guardian collaborate.

## Orchestration contract

1. **Lead** classifies → loads one route → sequences the spine → submits to guardian.
2. **Specialist** owns domain depth (scoring, hypotheses, persuasion, proof selection).
3. **Support** produces ship-ready artifacts (scripts, CSVs, tables, rendered docs).
4. **Guardian** runs the blocking Validation Gate; green is never assumed.

## How to reason about the route

The single most common failure is loading the wrong topic or loading two "to be safe." Force a deliverable-type classification before anything else:

- "Who should I contact / build me a list" → a *list* artifact → `client-prospecting`.
- "Qualify these inbound signups / build a capture funnel" → a *scoring/handoff* artifact → `lead-generation`.
- "Research this one company before my call" → a *brief* artifact → `client-dossier`.
- "Write the messages to reach them" → a *sequence* artifact → `b2b-outreach`.
- "Get the CFO to say yes" → a *decision narrative* → `executive-pitch`.
- "Respond to this RFP" → a *proposal document* → `proposal-writing`.
- "Make me a battle card / one-pager" → a *collateral asset* → `sales-collateral`.

If the request names a channel ("LinkedIn", "email", "deck"), strip the channel and ask: what artifact is the user actually asking me to produce?

## Evidence-family selection

- Kit-facing default: Alfa-core `[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`.
- If the loaded playbook is `b2b-outreach`, `client-prospecting`, or `client-dossier`, match its `[EXPLICIT]`/`[INFERRED]`/`[OPEN]` convention for that deliverable.
- Never mix families in a single output. Pick the weaker tag when two could apply.

## Governance invariants (non-negotiable, every output)

- No invented prices → FTE-months + disclaimer.
- Single brand → identify first, never mix.
- No green-as-success → state confidence, don't style it.
- No client PII → public professional context only.
- Every hypothesis is labeled and carries a validation step.

## When to escalate to a human

- A price/rate is explicitly demanded and FTE-month structure won't satisfy the buyer.
- Legal/compliance sign-off is required (contract terms, consent law, SLAs).
- A request needs private personal data — decline that element, deliver the rest.
