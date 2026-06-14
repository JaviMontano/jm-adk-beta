# Orchestration Plan — <task name>

## 1. Fan-out justification

- **Verdict:** justified | not-justified (route to `prompt-chaining-design` / single pass)
- **Independent subtasks:** <list, one line of independence argument each>
- Evidence: [DOC] / [INFERENCIA]

## 2. Hub contract

| Element | Specification |
|---|---|
| Coordinator model | <e.g. Sonnet> |
| Coordinator consumes | `last_message_only` |
| Input queue | <shape> |
| Aggregation shape | <fields> |
| `coverage_gaps` shape | `[{ unit, failure_type, attempted_query, suggested_alternatives }]` |

## 3. Spokes

| Spoke | Subtask | tools (minimal) | model | Isolation | Dispatch |
|---|---|---|---|---|---|
| <name> | <subtask> | <tools> | <tier> | `fresh_session` | `AgentDefinition` + `Task` |
| <name> | <subtask> | <tools> | <tier> | `fresh_session` | `AgentDefinition` + `Task` |

## 4. Error contract

- Typed failure fields: `failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`
- `valid_empty` (access ok, empty) ≠ `access_failure` (could not reach source)
- Local recovery before propagation: <retry cap / alternative-proposal policy>

## 5. Aggregation policy

- Mode: degraded (continue-on-partial-failure) | fail-fast (requested)
- On spoke failure: record `coverage_gaps` entry, continue siblings
- If fail-fast: skipped spokes recorded as <list>

## 6. Validation flags

- `offline = true`
- `network_required = false`
- `deterministic = true`
- Plan conforms to `assets/orchestration-contract.json` → `validate_orchestration_plan.py` exits 0

## 7. Acceptance gate (done = all true)

- [ ] Fan-out justified (no forced single-pass)
- [ ] 2+ spokes, each `AgentDefinition` + `Task`, minimal tools, explicit model
- [ ] `fresh_session` per spoke; coordinator `last_message_only`
- [ ] Typed errors + local recovery + `coverage_gaps`
- [ ] `valid_empty` ≠ `access_failure`; no swallowed errors
- [ ] Flags `offline/deterministic=true`

See `assets/checklist.md` for the legible mirror of this gate.

## 8. Rationale

<prose: why this decomposition, model/tool choices, and tolerance setting>
