# Quick variation — message-batch-orchestration

Minimal offline batch orchestrator. No evidence report.

## Steps

1. Confirm offline / latency-tolerant. If realtime → stop, route away.
2. `build_requests(items)`: `custom_id = business ID`; raise on duplicate.
3. `batches.create(requests=...)`; persist `batch.id`.
4. Poll `processing_status` with backoff until `ended`.
5. Stream `results()`; `succeeded` → success map; `errored|expired|canceled` → failed list.
6. Retry only `failed` up to `max_retries`; return success map + unresolved IDs.

## Defaults

- `model = claude-sonnet-4-5` (unless the user names another).
- `max_retries = 2` if unspecified (cap must be > 0).

## Output

One paragraph + the success/unresolved counts, per `templates/output.md`.
Evidence tags from one family. Do not skip the uniqueness gate even in quick
mode.
