# Batch Orchestration Deliverable — <workload name>

## 1. Workload framing

- **Mode:** offline / latency-tolerant — [confirm gate passed] [CONFIG]
- **Item count:** <n>
- **Business ID field → custom_id:** <field> [CÓDIGO]
- **Model:** claude-sonnet-4-5 (or user-named) [CONFIG]
- **max_tokens:** <n> · **max_retries (cap):** <n, > 0> [INFERENCIA]

## 2. Lifecycle executed

| Step | State | Notes |
|---|---|---|
| build_requests + uniqueness gate | pass/raised | duplicates: <list or none> |
| create + persist batch.id | <batch.id> | checkpointed before poll |
| poll processing_status (backoff) | ended | attempts: <n> |
| results() streamed | done | indexed by custom_id |
| fragment by result.type | done | succeeded / errored / expired / canceled |

## 3. Retry rounds

| Attempt | Sent | Succeeded | Failed (custom_id) |
|---|---|---|---|
| 1 | <n> | <n> | <list> |
| ... | | | |

Cap reached: <yes/no>.

## 4. Results

- **Success map:** `custom_id → message` — <count> persisted to <path/JSONL> [CÓDIGO]
- **Unresolved custom_id (after cap):** <list or empty> — returned for inspection [INFERENCIA]

## 5. Acceptance gate

- [ ] Offline / latency-tolerant load confirmed
- [ ] custom_id unique + stable from business ID; uniqueness validated before send
- [ ] processing_status polled with backoff until `ended`
- [ ] Results fragmented succeeded vs errored/expired/canceled
- [ ] Retry selective + capped; unresolved IDs returned on exhaustion
- [ ] No synchronous one-by-one loop on the offline path
- [ ] Evidence report passes `scripts/check.sh` (if required)

## 6. Evidence

- Report path: <path or n/a>
- Validators: `scripts/validate_message_batch_orchestration.py`, `scripts/check.sh`
- Evidence-tag family used: <one of CÓDIGO/CONFIG/DOC/INFERENCIA/SUPUESTO>
