<!-- distilled from alfa skills/pipeline-governance -->
# Pipeline Governance

> "Method over hacks. Evidence over assumption."

## TL;DR

Enforce phase gates (G0-G3) and quality checkpoints between pipeline stages.
Orchestration-layer skill used internally by Pristino and the adk-orchestrator;
full protocol in PRISTINO.md. [DOC] Each gate is a hard stop: a stage may not
emit downstream until its gate's criteria pass. [INFERENCIA]

## Gates (the contract)

| Gate | Boundary | Passes when |
|---|---|---|
| G0 | before Discover | input present, scope bounded, brand identified |
| G1 | Discover → Analyze | indexes + config loaded; no `{VACIO_CRITICO}` open |
| G2 | Analyze → Execute | option chosen per Constitution XIII/XIV; confidence scored |
| G3 | Execute → Validate | every output evidence-tagged; quality criteria met |

A gate failure is terminal for that run: stop and surface the blocker, never
auto-advance past an unmet criterion. [INFERENCIA]

## Procedure

### Step 1: Discover (→ G1)
- Gather input and context; load relevant indexes and configuration. [DOC]
- If a required index is missing, stop with `[SUPUESTO]` blocker — do not infer
  the architecture from caches or history. [DOC]

### Step 2: Analyze (→ G2)
- Evaluate options per Constitution XIII/XIV; score candidates by relevance and
  confidence. [DOC]
- Record the chosen option and the rejected alternative with its trade-off. [INFERENCIA]

### Step 3: Execute (→ G3)
- Apply the selected approach; tag all outputs with the Alfa core set. [DOC]

### Step 4: Validate
- Verify quality criteria met; confirm confidence >= 0.95. [INFERENCIA]
- Replay one checkpoint to prove a gate would reject a malformed output. [INFERENCIA]

## Decisions & Trade-offs

- **Hard gates over advisory checks.** A skippable gate is not governance; cost
  is throughput on clean runs. Keep criteria cheap to evaluate, not optional. [INFERENCIA]
- **Confidence threshold 0.95 over "looks right".** A fixed bar is auditable;
  below 0.95 route to human, do not ship. Cost: occasional rework. [SUPUESTO]

## Failure Modes

- **Gate bypass** — output emitted without its gate passing; an untagged output
  is a bypassed run (detect via the G3 tag check). [INFERENCIA]
- **Silent low confidence** — score computed but not enforced; treat missing or
  sub-0.95 confidence as a stop, not a warning. [INFERENCIA]
- **Stale context** — indexes from cache, not source; re-read source on G1. [DOC]

## Anti-Scope (explicitly NOT this skill)

- The pipeline's business logic — this governs *transitions*, not stage work. [DOC]
- Tag definitions and homologation — owned by `references/verification-tags.md`. [DOC]
- Runtime scheduling/retries of stages — orchestrator concern, not gate logic. [SUPUESTO]

## Quality Criteria

- [ ] Evidence tags applied (Alfa core set: `[CÓDIGO]/[CONFIG]/[DOC]/[INFERENCIA]/[SUPUESTO]`)
- [ ] Constitution-compliant (XIII/XIV)
- [ ] Confidence >= 0.95, enforced not advisory
- [ ] All four gates (G0-G3) evaluated; no bypass
- [ ] Actionable output

## Related Skills

- PRISTINO.md (full orchestration protocol); `references/verification-tags.md` (tag canon)
