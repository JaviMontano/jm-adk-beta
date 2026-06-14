# Example output — subagent-orchestration

Plan for the 40-company careers enrichment task.

## 1. Fan-out justification

- **Verdict:** justified. [INFERENCIA]
- Each company is an independent unit; finder→extractor→ranker is sequential
  *within* a company but the 40 companies fan out in parallel, and ranking is a
  single reduce over independent extractions. [INFERENCIA]
- Not a single-pass task: 40 independent fetch+extract units exceed one summary. [DOC]

## 2. Hub contract

| Element | Specification |
|---|---|
| Coordinator model | Sonnet |
| Coordinator consumes | `last_message_only` from each spoke |
| Input queue | 40 company records |
| Aggregation shape | `{ ranked: [...], coverage_gaps: [...], result_type }` |
| `coverage_gaps` shape | `[{ company, failure_type, attempted_query, suggested_alternatives }]` |

## 3. Spokes

| Spoke | Subtask | tools | model | Isolation | Dispatch |
|---|---|---|---|---|---|
| finder | locate careers page URL | `WebFetch` | Haiku | `fresh_session` | `AgentDefinition` + `Task` |
| extractor | extract open eng roles | `WebFetch`, `Read`, `Grep` | Haiku | `fresh_session` | `AgentDefinition` + `Task` |
| ranker | rank by hiring velocity | `Read` | Sonnet | `fresh_session` | `AgentDefinition` + `Task` |

No spoke is granted a tool it does not call (finder gets only `WebFetch`). [CONFIG]

## 4. Error contract

- Typed failure: `{ failure_type, attempted_query, partial_results, suggested_alternatives }`. [CONFIG]
- A careers page reached but listing zero roles → `valid_empty`. [CONFIG]
- A careers page behind a login wall → `access_failure` (never `valid_empty`, never `success` + `[]`). [CONFIG]
- Local recovery: finder retries once, then proposes an alternative URL
  (e.g. `/jobs`, LinkedIn) before propagating. [DOC]

## 5. Aggregation policy

- Mode: degraded (continue-on-partial-failure) — matches the team's tolerance. [DOC]
- Company 17's careers page is login-walled: finder retries, proposes
  `linkedin.com/company/.../jobs`, still fails → records
  `{ company: "Acme", failure_type: "access_failure", attempted_query: "...", suggested_alternatives: [...] }`
  in `coverage_gaps`; the other 39 proceed and the ranker ranks them. [DOC]
- Result type: `partial_success` (39 ranked, 1 gap). [CONFIG]

## 6. Validation flags

- `offline = true`, `network_required = false`, `deterministic = true`. [CONFIG]
- Conforms to `assets/orchestration-contract.json`; `validate_orchestration_plan.py` exits 0. [CONFIG]

## 7. Acceptance gate

- [x] Fan-out justified · [x] 3 spokes, each `AgentDefinition` + `Task`, minimal tools, explicit model
- [x] `fresh_session` per spoke; coordinator `last_message_only`
- [x] Typed errors + local recovery + `coverage_gaps`
- [x] `valid_empty` ≠ `access_failure`; no swallowed errors · [x] flags `offline/deterministic=true`

## 8. Rationale

Haiku clears the finder/extractor bar (URL location and list extraction are
shallow); Sonnet handles the ranker's comparative judgment and the coordinator's
aggregation. The login-wall case is exactly why `access_failure` must stay
distinct from `valid_empty`: collapsing both to `[]` would have silently dropped
Acme from the denominator and inflated the ranking's apparent coverage. [INFERENCIA]
