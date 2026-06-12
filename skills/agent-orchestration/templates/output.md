# Orchestration Dispatch Packet

## Request Classification
- Raw request:
- Resolved `topic`: <one of the 10 enum values>
- Runner-up topic (if any) and why the chosen topic wins:
- `depth`: quick | deep
- Evidence: [CONFIG]

## Playbook Loaded
- Playbook: `references/<topic>.md` (exactly one)
- Required inputs gathered / `[OPEN]` gaps:
- Evidence: [DOC]

## Analysis (policy applied)
- Policy invoked (confidence band / decision-table row / model tier / checkpoint
  policy):
- Option chosen and trade-off rejected:
- Evidence: [DOC] / [INFERENCE]

## Execution / Deliverable
- Deliverable produced (triad packet, route decision, workflow plan, recovery
  plan, monitor report, etc.):
- Deterministic script run (script-first) and result:
- Resume/recovery state (token, stateStore, idempotencyKey, retryPolicy,
  resumeFrom — only for resumable/recovery topics):
- Evidence: [CODE] / [CONFIG]

## Validation Gate (Guardian)
- [ ] One playbook loaded
- [ ] Topic in enum
- [ ] Spine completed (Discover → Analyze → Execute → Validate)
- [ ] Constitution v6.0.0 enforced
- [ ] Evidence tags present, single family, EN/ES consistent
- [ ] Script-first honored
- [ ] No false "passed" before this gate
- Verdict: PASS | PARTIAL | BLOCK
- Evidence: [DOC]

## Risks & Assumptions
- [ASSUMPTION] ...
- Residual risk / manual-review warning (if PARTIAL):
