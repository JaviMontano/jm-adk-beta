# Example input — product-analytics

A product manager sends this request:

> "Last sprint we changed the signup form from a single long page to a two-step
> wizard. We split traffic 50/50 by `user_id`. Conversion on the new flow looks
> a bit higher in the dashboard after 4 days — can we ship it? Baseline signup
> completion is about 12%, we get roughly 6,000 signups-started per day, and the
> smallest lift worth shipping for is +1 percentage point. We care about not
> hurting day-1 retention."

Context the skill can use:
- Randomization unit: `user_id`.
- Primary candidate metric: signup completion rate.
- Guardrail of concern: day-1 retention.
- Observed: "a bit higher" after 4 days (no significance stated).
- Baseline 12%, ~6,000 signups-started/day, MDE = +1pp absolute.

Expected routing: `ab-testing` (the question is "did the change work / can we
ship"), `depth=deep` (a ship decision with a guardrail). The "a bit higher after
4 days" framing is a peeking trap the skill must catch.
