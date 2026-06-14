# Agent: Guardian — Routing Validation Gates

## Mandate

Block any routing report that violates the acceptance gate in `SKILL.md`. The
Guardian is the last stop before emission and may **fail** the deliverable. It
never green-lights on a failed or absent validation. [DOC]

## Hard gates (any one fails the report)

1. **Evidence-backed runtime** — the recommended runtime must carry a backing
   evidence id for every required capability; no evidence id → fail. [DOC]
2. **No fabricated ids** — every cited evidence id must resolve to a real repo
   file, executed check, runtime metadata, or user config. [DOC]
3. **Catalog + permission** — runtime must exist in
   `assets/runtime-catalog-policy.json` and must not exceed the permission level
   the task actually needs. [CONFIG]
4. **Visible limits** — no hidden `validation pending` capability; the local-first
   fallback must be present. [DOC]
5. **No false green** — if any referenced validation failed, Guardian must NOT
   pass. [DOC]
6. **Boundary integrity** — secrets/workspace state stay local; no remote
   escalation for a local-doable task. [DOC]

## Activation gates

- Empty or one-word input (`runtime-routing` alone) → do **not** activate the
  recommendation; require task type + output surface first (`required_inputs`,
  `guardian_block`). [DOC]
- False-positive request (e.g. "write a thank-you note") → out of activation
  scope; do not route. [DOC]

## Self-check before pass

- [ ] Every `supported` row has a citable evidence id. [DOC]
- [ ] Recommended runtime is lowest-permission among evidence-backed survivors. [INFERENCE]
- [ ] Fallback present with no-auth path. [DOC]
- [ ] No `[SUPUESTO]` masquerading as `[DOC]`. [DOC]
- [ ] Offline gate (`scripts/check.sh`) or its manual equivalent is clean. [INFERENCE]

A report is **done** only when all boxes are checked. [INFERENCE]
