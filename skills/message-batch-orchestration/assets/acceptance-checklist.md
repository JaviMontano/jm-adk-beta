# Acceptance checklist — message-batch-orchestration

Walk this pre-emit gate before returning a batch-orchestration deliverable. Every
box must be checked; any unchecked box blocks "done". [DOC]

- [ ] **Offline gate.** Load is offline / latency-tolerant; realtime/streaming
      was rejected, not orchestrated. [CONFIG]
- [ ] **custom_id source.** `custom_id` = stable business ID, not a loop index. [CÓDIGO]
- [ ] **Uniqueness gate.** Uniqueness validated before send; duplicates raise in
      `build_requests`. [CÓDIGO]
- [ ] **Checkpoint.** `batch.id` persisted before polling (crash-safe resume). [INFERENCIA]
- [ ] **Polling.** `processing_status` polled with backoff until `ended`; no
      assumed immediate completion. [CÓDIGO]
- [ ] **Fragmentation.** Results split `succeeded` vs `errored`/`expired`/`canceled`. [CÓDIGO]
- [ ] **Selective retry + cap.** Only failed IDs retried; cap > 0; unresolved IDs
      returned on exhaustion. [CÓDIGO]
- [ ] **No sync loop.** No one-by-one `messages.create()` on the offline path. [CÓDIGO]
- [ ] **Refusals honored.** Requests to skip uniqueness / drop `custom_id` /
      disable fail isolation were rejected. [CONFIG]
- [ ] **Evidence.** If required, JSON report passes `scripts/check.sh`; one
      evidence-tag family; no invented prices; no client PII; single brand. [CONFIG]
