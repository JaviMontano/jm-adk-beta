# Example output — message-batch-orchestration

Deliverable for the `examples/example-input.md` request (8000 support tickets,
overnight classification, cap 2).

## 1. Workload framing

- **Mode:** offline / latency-tolerant — gate passed (overnight backfill). [CONFIG]
- **Item count:** 8000
- **Business ID field → custom_id:** `ticket_id` [CÓDIGO]
- **Model:** claude-sonnet-4-5 [CONFIG]
- **max_tokens:** 512 · **max_retries (cap):** 2 [CONFIG]

## 2. Lifecycle executed

| Step | State | Notes |
|---|---|---|
| build_requests + uniqueness gate | pass | 8000 unique `ticket_id`, 0 duplicates |
| create + persist batch.id | msgbatch_01H... | checkpointed to `state.json` before poll |
| poll processing_status (backoff) | ended | 6 polls, backoff 2→30s |
| results() streamed | done | indexed by `custom_id` |
| fragment by result.type | done | 7960 succeeded, 40 failed |

## 3. Retry rounds

| Attempt | Sent | Succeeded | Failed (custom_id) |
|---|---|---|---|
| 1 | 8000 | 7960 | 40 (e.g. TK-104512, TK-107781, ...) — `expired`/`errored` |
| 2 | 40 | 38 | 2 (TK-104512, TK-107781) |

Cap reached: yes (2 retries used).

## 4. Results

- **Success map:** 7998 `custom_id → message` persisted to `succeeded.jsonl`. [CÓDIGO]
- **Unresolved custom_id (after cap):** `["TK-104512", "TK-107781"]` — returned
  for inspection, not silently dropped. [INFERENCIA]

## 5. Acceptance gate

- [x] Offline / latency-tolerant load confirmed
- [x] custom_id unique + stable from `ticket_id`; uniqueness validated before send
- [x] processing_status polled with backoff until `ended`
- [x] Results fragmented succeeded vs errored/expired/canceled
- [x] Retry selective + capped at 2; 2 unresolved IDs returned on exhaustion
- [x] No synchronous one-by-one loop on the offline path
- [x] Evidence report passes `scripts/check.sh`

## 6. Evidence

- Report path: `out/batch-report.json` (fields satisfy
  `assets/message-batch-orchestration-contract.json`).
- Validators run: `scripts/validate_message_batch_orchestration.py` (pass),
  `scripts/check.sh` (pass — valid fixture accepted, mutated fixture rejected).
- Evidence-tag family used: CÓDIGO / CONFIG / INFERENCIA (consistent set).
