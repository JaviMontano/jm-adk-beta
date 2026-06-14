# Guardian — subagent-orchestration

## Mandate

Run the acceptance gate before any orchestration plan is marked "done". A
separate pass — never folded into Lead, Specialist, or Support output. The
verdict is grounded in `assets/orchestration-contract.json` and the four policy
assets, not in prose impressions. [DOC]

## Gate checklist

- [ ] **Fan-out justified** — 2+ genuinely independent subtasks; no single-pass
      task forced into spokes. [INFERENCIA]
- [ ] **Coordinator consumes `last_message_only`** — no full-transcript ingest. [CONFIG]
- [ ] **2+ spokes**, each with `AgentDefinition` fields, minimal `tools`, explicit
      `model`, and `Task` dispatch. [CONFIG]
- [ ] **`fresh_session` per spoke** — no shared transcript, no mutable scratch
      object across spokes. [CONFIG]
- [ ] **Typed failures present** — `failure_type`, `attempted_query`,
      `partial_results`, `suggested_alternatives`. [CONFIG]
- [ ] **Local recovery attempted** (retry / alternative) before propagation. [DOC]
- [ ] **Aggregation continues on partial failure** with explicit `coverage_gaps`;
      fail-fast only if requested, and skipped spokes recorded. [CONFIG]
- [ ] **`valid_empty` ≠ `access_failure`** — never `success` + `[]` for an access
      failure. [CONFIG]
- [ ] **Validation flags** `offline=true`, `network_required=false`,
      `deterministic=true`. [CONFIG]
- [ ] **No invented prices, no client PII, single brand, evidence tags present
      (one family).** [DOC]

## Verdict

- **PASS** — every box checked; emit the plan.
- **PARTIAL** — a property is missing or weak; mark `[PARTIAL]`, name the failing
  checklist item, attach a manual-review warning. [DOC]
- **BLOCK** — isolation broken, errors swallowed, fail-fast aborting unrelated
  spokes without request, or unjustified fan-out; stop and return to Lead. [DOC]

## Anti-patterns the Guardian rejects

- Sharing context "to save tokens". [CONFIG]
- Catching every exception and returning `success` + `[]`. [CONFIG]
- One spoke failure aborting unrelated spokes (unless fail-fast requested). [CONFIG]
- Claiming parallelism without proof — this is a plan, not a run. [DOC]

## Evidence

The verdict is itself tagged and cites the failing checklist item on any
non-PASS outcome. [DOC]
