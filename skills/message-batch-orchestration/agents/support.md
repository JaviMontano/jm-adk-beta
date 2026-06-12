# Support — message-batch-orchestration

## Mandate

Execute the batch lifecycle the Lead frames and the Specialist scopes: assemble
`requests`, create the batch, poll with backoff, stream results, fragment, retry
only the failed `custom_id`s under the cap, and persist the deliverable. [CÓDIGO]

## Execution steps

1. **Assemble requests.** For each item, set `custom_id` to the stable business
   ID and `params` to `{model, max_tokens, messages}`. Raise on a duplicate
   `custom_id` before sending (uniqueness gate). [CÓDIGO]
2. **Create + checkpoint.** Call `batches.create(requests=...)` and persist
   `batch.id` immediately so a crash can resume. [CÓDIGO]
3. **Poll.** Loop `retrieve(batch.id).processing_status` with backoff until
   `ended`; never treat a non-`ended` status as terminal. [CÓDIGO]
4. **Stream results.** Iterate `results(batch.id)`, indexing by `custom_id`. [CÓDIGO]
5. **Fragment.** `succeeded` → write to the `custom_id → message` map (e.g.
   JSONL); `errored | expired | canceled` → collect into the retry sub-batch. [CÓDIGO]
6. **Selective retry.** Rebuild `pending` from only the failed IDs and loop up to
   `max_retries`. On cap exhaustion, return the unresolved `custom_id` list — do
   not return an empty success as if complete. [CÓDIGO]
7. **Emit.** Produce the deliverable per `templates/output.md`; when evidence is
   required, write the JSON report and run `scripts/check.sh`. [CONFIG]

## Guardrails

- Allowed tools only: `Read`, `Grep`, `Glob`, `Bash`. [CONFIG]
- No synchronous `messages.create()` loop over offline items. [CÓDIGO]
- No `enumerate()`/index as `custom_id`. [CÓDIGO]
- No full-batch retry after a partial failure — fragment first. [CÓDIGO]

## Handoffs

- → **Guardian** with the success map, unresolved IDs, attempt count, and (if
  required) the evidence report path.

## Evidence

Tag each step `[CÓDIGO]`; tag config/model pins `[CONFIG]`. One family per
output. [DOC]
