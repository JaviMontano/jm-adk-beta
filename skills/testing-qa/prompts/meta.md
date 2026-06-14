# Meta Prompt — testing-qa (self-check)

Run this reasoning gate before emitting any testing-qa deliverable.

## Routing integrity
- Did I resolve exactly ONE `topic`, and Read exactly ONE playbook? If I read two
  "to compare", I broke the router contract — pick one and re-run.
- Did the disambiguation rules actually fire, or did I default silently? If two
  enums fit equally, I must have asked once.
- Is the request even a testing task? Build/deploy/lint → route elsewhere.

## Boundary integrity
- Am I re-testing logic through e2e, or routing a flow test through unit? Reroute
  to the cheapest layer that catches the bug.
- Is the ask actually out of scope (server SLO load testing, pen-testing, native
  mobile profiling)? Name it and redirect — do not fake coverage.

## Evidence and gate integrity
- Does every non-obvious claim carry exactly one tag from a single family?
- Is any threshold I cited derived from a baseline/standard (CrUX p75, ≥80% diff),
  not guessed? Derived caps tagged `[SUPUESTO]`?
- Did the Validate step actually RUN, with script output behind it? A "done" on an
  unrun Validate step is a hard fail.
- Am I about to call green = success? Check for weak/absent assertions, gamed
  coverage, lab-green-but-field-failing, or a flaky test retried into green.

## Governance
- Constitution v6.0.0 enforcement respected; no invented prices; no client PII;
  single brand. If any check fails, fix it before output, not after.
