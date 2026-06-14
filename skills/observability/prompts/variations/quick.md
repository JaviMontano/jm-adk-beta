# Quick variation — observability router

Use when `depth=quick`: deliver the essentials of the routed topic fast, without
exhaustive verification of every sub-step. Still enforce the invariants.

## Steps
1. Resolve the single `topic` by intent. If ambiguous or the target system is
   missing, ask one question and stop.
2. Load EXACTLY ONE playbook.
3. Produce only the load-bearing core of the deliverable:
   - **monitoring-setup**: the four golden signals per critical service, each
     bound to one SLI/SLO; cardinality + retention noted in one line.
   - **alerting-strategy**: the P1/P2 rules only, each with owner, threshold,
     `for:` window, and runbook; defer P3/P4 tuning.
   - **health-check-automation**: required checks with thresholds + dated
     evidence; compute the rollup; list unknowns.
   - **log-management**: the minimum log schema and ERROR/WARN discipline; flag
     PII risk.
   - **incident-response**: severity from the matrix, IC + Scribe, the next
     reversible mitigation.
4. Tag every non-obvious claim.
5. For the JSON topics, still run the validator — determinism is not optional even
   in quick mode. [CONFIG]

## Out of scope for quick
Full SLO catalog, exhaustive fatigue tuning, complete postmortem write-up. Note
each deferred item as a one-line `[SUPUESTO]` follow-up.
