# Example input — ux-research

## Request (as received)
> "Our B2B invoicing app loses people at the payment step. The funnel shows a
> 38% drop right at 'submit payment', but nobody knows why. We're about to start
> a redesign. Help us understand what's actually going wrong for the people doing
> this job before we commit engineering time."

## Attached context
- Funnel analytics export: confirmed 38% drop at the `payment-submit` event,
  last 90 days.
- 6 scheduled interview slots with AP (accounts-payable) clerks across 3 customer
  accounts.
- No prior persona work; team has been arguing from anecdote.

## Parameters resolved by the router
- `topic = user-research` — the question is *why* users abandon (generative), not
  *how many* (already known from analytics) and not *can they complete a built
  flow* (the redesign isn't built yet). [INFERENCIA]
- `depth = deep` — feeds a build commitment, so apply the playbook exhaustively. [DOC]

## Decision this must inform
Whether the redesign prioritizes fixing the **payment-submit** experience, and
which specific friction to target first. [DOC]
