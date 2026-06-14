# Meta Prompt — ux-design

Use this to reason about *how* the ux-design router should behave, not to produce
a deliverable.

## Routing reflection

- Did the request name a clear artifact (screen, component, copy, flow) and a
  user goal? If the goal is missing and the topic is `design-critique`, stop and
  ask — critique without a goal is opinion. [EXPLICIT]
- Is the topic genuinely ambiguous, or am I about to ask a needless question?
  Ask only on a true tie between two enums. [EXPLICIT]
- Am I tempted to read a second playbook "for context"? That is the primary
  anti-pattern — read exactly one. [EXPLICIT]

## Quality reflection

- Are my severities calibrated against each other, or inflated? A page of Majors
  with a hidden Blocker is a calibration failure. [INFERENCIA]
- Have I tied every finding to user impact? Items with no impact are Nits or are
  cut. [EXPLICIT]
- Did I mark heuristic Blockers `[SUPUESTO]` until confirmed by testing? [SUPUESTO]
- Did I avoid green-as-success and any invented metric? [EXPLICIT]

## Escalation reflection

- If no enum fits, name the gap and the nearest sibling skill (brand identity,
  frontend code-gen, product strategy) rather than force-fitting a route. [INFERENCIA]
- If the routed playbook turns out wrong mid-flow, re-resolve `topic` exactly once.
  [INFERENCIA]
