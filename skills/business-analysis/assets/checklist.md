# Acceptance checklist — business-analysis

Run this gate before declaring any `business-analysis` deliverable done. Mirrors the
acceptance section in `SKILL.md` and the universal block of `assets/quality-rubric.json`.
Block with named fixes if any box is unchecked. [DOC]

## Routing
- [ ] Resolved exactly one `topic`; loaded exactly one playbook from `routes.json`.
- [ ] Topic matches the dominant signal in the request (no needless clarifying question,
      no guessing through a real tie).
- [ ] `depth` (`quick`/`deep`) stated.

## Evidence discipline
- [ ] Every non-obvious claim carries one tag from a single family, spelled consistently.
- [ ] Every `[ASSUMPTION]` has a paired verification step.
- [ ] Evidence-tag summary present; if `[ASSUMPTION]` >30%, WARNING banner + gap list shown.

## Governance
- [ ] No phase leakage: no target architecture, API contracts, schemas, sprint plans, or
      pricing.
- [ ] Effort is FTE-time, never currency.
- [ ] Feasibility/scenario integration points scored for Firebase/Google/Hostinger lens;
      off-stack justified or marked infeasible.
- [ ] No score or dashboard framed as "success."
- [ ] Single brand; no client PII.

## Topic quality criteria
- [ ] The chosen topic's criteria in `assets/quality-rubric.json` (`topic_specific`) all
      pass — e.g. resolved gateways for process-modeling, reconciled integration matrix for
      flow-mapping, no orphans for requirements, decision rule applied for feasibility,
      locked weights for scenario, first-≤3 barrier for change-readiness.

## Output shape
- [ ] Deliverable follows `templates/output.md` (routing record → spine → recommendation →
      gate → evidence summary).
