# Quick variation — market-intel (depth=quick)

Fast routed pass. Essentials only — no exhaustive Validate sweep.

1. Infer the topic in one read of the request (cue table in `prompts/primary.md`).
   Do not ask unless two playbooks genuinely contend.
2. Read the one matching playbook from `routes.json`.
3. Run a lightweight spine: Discover (just the inputs needed) → Analyze (the
   playbook's core artifact only) → Execute (emit).
4. Apply evidence tags to every non-obvious claim; downgrade unsourced figures.

Quick-tier scope by topic (deliver the headline artifact, defer the rest):
- `competitive-intelligence` → feature matrix + 1-line SWOT, top 3 competitors.
- `competitive-positioning` → positioning statement + 3-axis matrix vs status quo.
- `benchmarking-analysis` → top gap, normalized, with source + date.
- `market-intelligence` → entity classification + 5-bullet exec summary.
- `sector-intelligence` → sub-segment + 3-row regulatory matrix + glossary stub.
- `marketing-context` → positioning statement + 1 primary value prop.
- `partnership-strategy` → fit-score table for the named candidates only.
- `pricing-strategy` → tier skeleton + anchor recommendation (ranges only).

Hard rules still apply: no invented prices, single brand, no PII, no
green-as-success. State the chosen topic and that this is a quick pass.
