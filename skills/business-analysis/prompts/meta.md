# Meta prompt — business-analysis (self-check)

Use this to audit your own routing and output before handing back to the user. It encodes
the failure modes this cluster is most prone to.

## Routing self-check
- Did I resolve to **exactly one** topic? If I loaded more than one playbook, stop — I
  defeated the router.
- Was the topic genuinely ambiguous, or did I ask a needless clarifying question on a
  dominant signal?
- Is the request actually in-cluster, or is it asking for target architecture / API
  contracts / sprint plans / pricing (out of scope, redirect)?

## Evidence self-check
- Does every non-obvious claim carry exactly one tag from one family with consistent
  spelling?
- Is every `[ASSUMPTION]` paired with a concrete verification step?
- Is the `[ASSUMPTION]` ratio >30%? If so, is the WARNING banner present with the gap list?

## Method self-check (topic-dependent)
- feasibility/scenario: Did I apply the decision rule rather than eyeballing the mean? Did
  I lock weights before scoring? Is the stack lens applied?
- change-readiness: Is the barrier the *first* ADKAR dimension ≤3 in order — not the lowest
  or the average?
- flow-mapping: Does every cross-context arrow have a matrix row and vice versa? Are there
  8–12 flows, each with an alt/error path?
- requirements: Do AC include negative + boundary cases? Any orphan requirements or
  objectives in the traceability matrix?
- process-modeling: Is every gateway branch and end event resolved? Is PCE reported against
  a baseline?

## Tone / governance self-check
- No pricing anywhere; effort is FTE-time.
- No score or dashboard presented as "success."
- Single brand, no client PII.
- Output matches `templates/output.md` structure.
