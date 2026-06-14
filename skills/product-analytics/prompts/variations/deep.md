# Deep variation — product-analytics

Thorough path: `depth=deep`. Run the resolved playbook in full with per-step
verification and a validity-threat sweep.

1. Resolve the single topic; record why the other near-fit routes were rejected.
2. Read the one matching playbook; run all four spine phases:
   - **Discover** — inventory evidence (events, tables, specs, code); mark every
     unknown `not verified`; never invent metrics, volumes, or owners.
   - **Analyze** — define formulas/denominators/method BEFORE interpreting; pick
     the statistical method up front so it can't be method-shopped after data.
   - **Execute** — produce the full artifact via `templates/output.md`.
   - **Validate** — run the route's acceptance + quality criteria.
3. Validity-threat sweep relevant to the route:
   - ab-testing: peeking, SRM, novelty, seasonality, overlapping experiments.
   - funnel: denominator drift, identity reset, late data, Simpson's paradox.
   - cohort: survivorship, shifting "active" definition, immature late cells.
   - real-time: late/out-of-order events, backpressure, threshold flapping.
4. Decision rule (where applicable) covers win, loss, inconclusive, guardrail
   breach, and instrumentation failure — all set before launch.
5. Gate: one playbook, evidence tags on every claim, no fabricated numbers, no
   premature significance, no client PII. Deliver the explicit gap report for
   anything unverified.
