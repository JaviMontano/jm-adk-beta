# Deep variation — message-batch-orchestration

Full offline batch orchestrator with checkpointing, edge-case handling, and an
evidence report.

## Steps (beyond quick)

1. Run the full lifecycle as in `prompts/variations/quick.md`.
2. **Checkpoint.** Persist `batch.id` before polling and persist successes
   incrementally (e.g. JSONL) so a crash resumes via `retrieve`/`results`.
3. **Edge cases.**
   - Partial `expired`/`canceled` → same retry sub-batch under the cap.
   - Source duplicates → fail in `build_requests`; dedup upstream or request a
     tie-break rule.
   - Crash during poll → resume from persisted `batch.id`, do not recreate.
   - All items fail on the last attempt → return the unresolved `custom_id`
     list, never empty-success-as-complete.
4. **Evidence report.** Emit the JSON report whose fields satisfy
   `assets/message-batch-orchestration-contract.json`; validate offline with
   `scripts/validate_message_batch_orchestration.py` and run the full smoke
   `scripts/check.sh` (accepts valid fixtures, rejects invalid mutations).
5. **Rubric.** Score the deliverable against `assets/quality-rubric.json` and
   walk `assets/acceptance-checklist.md` before declaring done.

## Output

Full deliverable per `templates/output.md`, including the gate table and the
evidence report path. Evidence tags from one family; no invented prices.
