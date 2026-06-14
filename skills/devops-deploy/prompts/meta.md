# Meta Prompt — devops-deploy

Reasoning controller for the router. Use to decide HOW to route and validate
before producing any artifact.

## Routing self-check
- Did I map to exactly ONE topic in the enum? If two seem to apply, which is the
  *primary* deliverable the user asked for? If still tied → ask.
- Am I about to load more than one playbook "to be safe"? Stop — that defeats the
  router.
- Mid-task, has the real need shifted to a different topic? If so, re-route and
  re-read.

## Depth self-check
- `quick`: essentials only — the minimum viable artifact + gate.
- `deep`: apply the playbook exhaustively, verify each step, enumerate edge cases
  and failure modes.

## Evidence & governance self-check
- Is every factual claim tagged? Are assumptions explicitly `[SUPUESTO]`?
- Did I avoid embedding secret values, invented prices, and client PII?
- Single brand only; harness voice; constitution v6.0.0.

## Done-ness self-check (the trap)
- Am I treating a green build as proof of correct behavior? That is FALSE.
  Require behavior evidence: smoke test, monitoring window, or explicit gate.
- Does my handoff list the operator prerequisites that a local plan cannot prove?

## When to escalate to a sibling skill
If the request needs infra provisioning, DNS cutover, secret rotation, or cloud
OIDC trust-role setup, name it as a prerequisite and hand it off — do not absorb
it into this router.
