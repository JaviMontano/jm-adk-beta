# Body of Knowledge — message-batch-orchestration

Domain reference for orchestrating the Anthropic **Message Batches API** on
offline, latency-tolerant workloads.

## Key concepts

- **Message Batches API.** Asynchronous endpoint that processes many
  `messages.create`-shaped requests in one batch, decoupled from any live
  request. At volume it cuts cost ~50% vs. synchronous calls. [DOC]
- **`custom_id`.** A caller-assigned identifier attached to each request and
  echoed on each result. It is the correlation key between input and output and
  the dedup key across retries. Must be **unique** within a batch and **stable**
  across attempts. [DOC]
- **`processing_status`.** Batch-level lifecycle field. Non-`ended` values are
  non-terminal; the batch is only safe to read once it reaches `ended`. [CÓDIGO]
- **`result.type`.** Per-request outcome: `succeeded`, `errored`, `expired`,
  `canceled`. Only `succeeded` carries a usable `message`; the other three are
  reintegrable failures. [CÓDIGO]
- **Selective retry.** Re-running only the failed `custom_id`s in a fresh batch,
  never the whole lot. [DOC]
- **Retry cap.** Upper bound (`max_retries`) on retry rounds; mandatory and > 0
  to bound recurring `expired`/`errored`. [INFERENCIA]
- **Checkpoint.** Persisted `batch.id` (and success map) that lets the
  orchestrator resume after a crash via `retrieve`/`results`. [INFERENCIA]

## Lifecycle (canonical)

`create → poll processing_status (backoff, until ended) → results() → fragment by
result.type → selective retry under cap`. [CÓDIGO]

## Decision rules

1. **`custom_id` = business ID, not loop index.** The index breaks correlation
   when `items` are reordered between attempts; the business ID is idempotent. [INFERENCIA]
2. **Persist `batch.id` before polling.** Enables crash-safe resume; avoids
   recreating (and re-billing) the batch. [INFERENCIA]
3. **Cap > 0 is mandatory.** Without it, recurring failures loop forever. [INFERENCIA]
4. **Backoff, not busy-wait.** Saves `retrieve` calls on long batches. [INFERENCIA]
5. **Fragment before retry.** Persist successes first; retry only the failed
   sub-set. [CÓDIGO]
6. **Reject degraded patterns.** Skipping uniqueness, dropping `custom_id`, or
   disabling fail isolation → refuse; do not silently comply. [CONFIG]

## Standards and gates

- **Offline gate.** Activate only on offline / latency-tolerant loads
  (classification, enrichment, evals, backfills). Realtime/streaming → out of
  scope. [CONFIG]
- **Uniqueness gate.** Validate `custom_id` uniqueness before send; raise on
  duplicate. [CÓDIGO]
- **Evidence gate.** When evidence is required, the JSON report passes
  `scripts/check.sh`; offline JSON validates with
  `scripts/validate_message_batch_orchestration.py`. [CONFIG]
- **Model pin.** `claude-sonnet-4-5` unless the user names another. [CONFIG]

## Edge cases

- **Partial `expired`/`canceled`.** Treat as reintegrable failures; same retry
  cap. [CÓDIGO]
- **Source duplicates.** Fail in `build_requests`; dedup upstream or ask for a
  tie-break rule. [CÓDIGO]
- **Crash during poll.** Resume from persisted `batch.id`; do not recreate. [INFERENCIA]
- **All items fail on the last attempt.** Return the unresolved `custom_id`
  list; never return empty success as complete. [INFERENCIA]

## Anti-patterns

- Synchronous `messages.create()` loop over offline items. [CÓDIGO]
- `enumerate()`/index as `custom_id`. [CÓDIGO]
- Full-batch retry after a partial failure. [CÓDIGO]
- Treating a non-`ended` `processing_status` as terminal. [CÓDIGO]
- Retry without a cap. [INFERENCIA]
