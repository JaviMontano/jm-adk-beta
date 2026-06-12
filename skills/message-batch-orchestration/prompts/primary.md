# Primary prompt — message-batch-orchestration

You are orchestrating the Anthropic **Message Batches API** for an offline,
latency-tolerant workload. Build an orchestrator that processes the items as one
batch with a unique `custom_id` per request, fragments partial failures, and
retries only the failed items under a cap.

## Inputs to capture

- The list of items and the **stable business ID field** to use as `custom_id`.
- `model` (default the pinned `claude-sonnet-4-5` unless the user names another),
  `max_tokens`, and the prompt content per item.
- `max_retries` (the retry cap; must be > 0).
- Whether an evidence JSON report is required.

## Procedure

1. Confirm the load is **offline / latency-tolerant**. If it is interactive or
   streaming, stop and route away — this skill does not apply.
2. Build `requests`, validating `custom_id` uniqueness **before** sending; raise
   on any duplicate.
3. `create` the batch and persist `batch.id` immediately (crash-safe
   checkpoint).
4. Poll `processing_status` with backoff until `ended`.
5. Stream `results()`, indexing by `custom_id`.
6. Fragment by `result.type`: `succeeded` → persist to the `custom_id → message`
   map; `errored | expired | canceled` → collect for retry.
7. Retry only the failed `custom_id`s in a fresh batch, up to `max_retries`. On
   cap exhaustion, return the unresolved IDs.
8. If evidence is required, emit the JSON report and validate it with
   `scripts/check.sh`.

## Output

Return the deliverable using `templates/output.md`: the success map summary, the
unresolved `custom_id` list, attempt count, and the gate results. Tag every
claim with the skill taxonomy (`[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`).

## Refusals

Refuse and explain if asked to skip uniqueness validation, drop `custom_id`, or
disable fail isolation. Do not degrade the pattern.
