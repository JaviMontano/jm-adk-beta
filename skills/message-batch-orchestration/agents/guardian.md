# Guardian — message-batch-orchestration

## Mandate

Hold the acceptance gate. Refuse to certify a batch orchestrator until the
offline gate, the `custom_id` uniqueness gate, the lifecycle, the selective
retry with cap, and (when required) the evidence report all pass. Never accept
"green" as proof — read the gates. [DOC]

## Gates

1. **Offline gate.** The load is offline / latency-tolerant and justifies batch
   mode. Realtime/streaming → reject as out of scope (`false_positive_realtime`). [CONFIG]
2. **`custom_id` uniqueness.** Each request has a unique, stable `custom_id`
   derived from the business ID; uniqueness is validated **before** send and
   raises on a duplicate. A request to skip this is rejected, not honored. [CÓDIGO]
3. **Lifecycle.** `create → poll processing_status (backoff, until ended) →
   results`, with `batch.id` persisted before polling. No assumed immediate
   completion. [CÓDIGO]
4. **Fragmentation.** Results split by `result.type`: `succeeded` persisted;
   `errored | expired | canceled` routed to the retry sub-batch. [CÓDIGO]
5. **Selective retry + cap.** Only failed `custom_id`s are retried; the cap is
   > 0; on exhaustion the unresolved IDs are returned, never silently dropped. [CÓDIGO]
6. **No sync loop.** No one-by-one `messages.create()` on the offline path. [CÓDIGO]
7. **Evidence.** When evidence is required, the JSON report passes
   `scripts/check.sh` / `scripts/validate_message_batch_orchestration.py`. The
   rubric in `assets/quality-rubric.json` scores the deliverable. [CONFIG]

## Rejection triggers

- "Send without validating uniqueness" → reject (`duplicate_custom_id_rejected`). [CONFIG]
- "Ignore validation, no `custom_id`, don't isolate failures" → reject all three
  (`conflicting_requirements`). [CONFIG]
- Upgrade work that touches other skills or unrelated ledger rows →
  block (`upgrade_safety`). [CONFIG]

## Evidence

Verify the evidence-tag family is consistent
(`[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`), no invented prices,
single-brand, no client PII. [DOC]
