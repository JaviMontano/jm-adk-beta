# Meta Prompt — pm-delivery

Use this to reason about HOW to route and self-check the pm-delivery run, not to
produce the deliverable itself.

## Routing self-check
- Did I pick exactly ONE topic from the 11-enum? If the request blends topics
  (e.g. "estimate the budget and the risks"), split it or ask which to run
  first — do not load two playbooks at once.
- Common confusions to disambiguate explicitly:
  - cost-estimation vs. budget-management → estimating effort vs. allocating a
    baseline.
  - capacity-planning vs. team-topology → who is available vs. how teams are
    shaped.
  - okr-design vs. product-roadmapping → goals/outcomes vs. sequenced delivery.

## Execution self-check
- Did I read only the one playbook, or did I summarize from memory? If from
  memory, restart and actually read it.
- Did I run all four spine phases? Discover and Validate are the usual casualties.
- For cost-bearing topics: did any price, rate, or currency slip in? Strip it and
  re-express as FTE-months.

## Evidence self-check
- Is every non-trivial claim tagged? Untagged claims block the deliverable.
- What fraction is `[ASSUMPTION]`? If >30%, banner it and recommend discovery.

## Governance self-check
- Constitution v6.0.0, script-first, single brand, no client PII — all honored?
- Am I about to claim a gate passed without showing the evidence? If so, stop.
