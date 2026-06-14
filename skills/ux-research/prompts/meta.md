# Meta prompt — ux-research

Guidance for orchestrating the ux-research skill across its four agents and the
router contract. Use this when composing the run, not when executing a single
route.

## Orchestration spine
1. **Lead** resolves `topic` + `depth`, scopes the decision and segment, and
   selects exactly one route. Multi-route requests become **ordered sub-passes**
   (e.g. prototyping then user-testing), never one merged blob.
2. **Specialist** supplies method depth for the chosen route (sampling,
   instrument design, severity rubric, fidelity choice).
3. **Support** assembles the deliverable from `templates/output.md`, marshals and
   labels sources, runs the asset rubric / any `scripts/` checks.
4. **Guardian** gates: single route, evidence integrity, `[SUPUESTO]` pairing, no
   green-as-success, route-specific quality criteria, governance.

## Self-checks before returning
- Did I read **one and only one** playbook? Loading >1 is an automatic fail.
- Is the `topic` inside the enum? Inventing a topic outside it fails.
- Is each metric reported with n / response rate / margin of error (survey) or
  severity + verbatim evidence (testing)?
- Does the deliverable end with an explicit, owned next step?
- Is the tag family consistent and is every `[SUPUESTO]` paired with verification?

## Routing tie-breakers
- "Validate a design" with a built/clickable artifact → `user-testing`, not
  `prototyping`. "Validate a concept" with nothing built yet → `prototyping`.
- "Understand users" at depth → `user-research`; "size/segment a known attitude"
  → `survey-design`. When n you can reach < ~30/segment, do not survey.

## Failure modes to avoid
Persona sprawl, research theater, leading wording, happy-path-only journeys, n=1
conclusions, mean on an ordinal scale, mixing tag families. [INFERENCIA]
