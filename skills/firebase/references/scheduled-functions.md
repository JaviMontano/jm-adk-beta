<!-- distilled from alfa skills/scheduled-functions -->
<!-- > -->
# Scheduled Functions

> "Automate what repeats — schedule what must happen on time." — Unknown

## TL;DR

Implement scheduled Cloud Functions via Firebase `onSchedule` (cron) for batch processing, cleanup, report generation, and sync — with idempotency, checkpointing, and monitoring. Use for periodic server-side tasks that must run unattended. [EXPLICIT]

## Scope & Anti-Scope

- **In scope**: time-triggered functions (`onSchedule`), Cloud Scheduler cron, batch/chunked Firestore jobs, retry/idempotency, alerting. [DOC]
- **Out of scope**: event-triggered functions (`onDocumentWritten`, Pub/Sub, HTTP) — use `cloud-functions`; client-initiated long jobs (use Cloud Run/Tasks); sub-minute cadence (Scheduler minimum is 1 min — use a self-rescheduling Task queue instead). [SUPUESTO] Verify cadence floor against current Cloud Scheduler quotas.

## Procedure

### Step 1: Discover
- Identify periodic tasks (cleanup, reports, sync, reminders) and their business SLA (must-run-by time). [INFERENCIA]
- Inventory existing scheduled functions + cron patterns to avoid overlap/thundering-herd at common boundaries (midnight UTC). [INFERENCIA]
- Size data volumes → decide single-pass vs. paginated batch. [DOC]
- Capture timezone: `onSchedule` defaults to UTC unless `timeZone` is set. [SUPUESTO] Confirm against deployment config.

### Step 2: Analyze
- Define cron per task (Cloud Scheduler / unix-cron syntax). [DOC]
- Plan pagination/chunking for large datasets (cursor by doc ID or `orderBy` + `startAfter`). [DOC]
- Design idempotency: derive a deterministic run/window key so re-execution is a no-op (see Worked Example). [INFERENCIA]
- Budget timeout: Cloud Functions v2 allows up to 60 min; default is 60 s — set explicitly. [SUPUESTO] Verify max against current Firebase Functions v2 docs.

### Step 3: Execute
- Create the function with `onSchedule` + cron expression and explicit `timeZone`. [DOC]
- Paginate Firestore (process N docs/run); persist a cursor so the next run resumes. [DOC]
- Log per run: start time, records processed, errors, duration, cursor reached. [DOC]
- Handle timeout: checkpoint progress, exit cleanly, resume next invocation — never leave partial writes uncommitted. [INFERENCIA]
- Configure resources via v2 options: `{ timeoutSeconds, memory, retryCount }`. [SUPUESTO] (v1 used `runWith(...)`; confirm SDK major version before copying syntax.)
- Add a distributed lock (Firestore transaction on a `locks/{job}` doc with TTL) only if overlap is unsafe. [INFERENCIA]
- Alert on failure via Cloud Monitoring (log-based metric → alert policy). [DOC]

### Step 4: Validate
- Dry-run locally before deploy: `firebase functions:shell` (or emulator). [DOC]
- Verify the cron fires when expected (crontab.guru); confirm timezone matches intent. [DOC]
- Exercise edge cases: empty collection, error mid-batch, slow run hitting timeout. [INFERENCIA]
- After deploy, inspect Cloud Scheduler + function logs for the first real execution. [DOC]

## Worked Example (idempotent daily cleanup)

```js
const { onSchedule } = require("firebase-functions/v2/scheduler");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");

exports.cleanupStale = onSchedule(
  { schedule: "every day 03:00", timeZone: "America/Bogota",
    timeoutSeconds: 540, memory: "512MiB", retryCount: 1 },
  async (event) => {
    const db = getFirestore();
    const runId = event.scheduleTime.slice(0, 10);          // window key → idempotent
    const guard = db.doc(`jobRuns/cleanup_${runId}`);
    if ((await guard.get()).exists) return;                 // already ran this window
    const cutoff = Date.now() - 30 * 864e5;
    let processed = 0, last = null;
    for (;;) {                                              // paginate, resumable
      let q = db.collection("sessions").where("ts", "<", cutoff).orderBy("ts").limit(500);
      if (last) q = q.startAfter(last);
      const snap = await q.get();
      if (snap.empty) break;
      const batch = db.batch();
      snap.docs.forEach((d) => batch.delete(d.ref));
      await batch.commit();
      processed += snap.size; last = snap.docs.at(-1);
    }
    await guard.set({ processed, at: FieldValue.serverTimestamp() });
    console.log(JSON.stringify({ runId, processed }));      // structured log → metric
  }
);
```
[CÓDIGO] Pattern is illustrative; verify SDK import paths against the installed `firebase-functions` version. [SUPUESTO]

## Quality Criteria

- [ ] Cron + timezone documented with human-readable explanation. [DOC]
- [ ] Batch processing handles large datasets without timeout (paginated + resumable). [DOC]
- [ ] Function is idempotent — re-run within the same window is a no-op. [DOC]
- [ ] Execution results logged structurally for monitoring/debugging. [DOC]
- [ ] Failure alert wired to Cloud Monitoring. [DOC]
- [ ] Evidence tags applied to all non-obvious claims. [DOC]

## Failure Modes

| Mode | Symptom | Mitigation |
|------|---------|------------|
| Timeout mid-batch | Partial deletes/writes, inconsistent state | Checkpoint cursor; commit per chunk, not at end. [INFERENCIA] |
| Overlapping runs | Double-processing, lock contention | Distributed lock or idempotent window key. [INFERENCIA] |
| Silent failure | No data, no alert | Log-based metric + alert policy; assert non-empty result. [DOC] |
| Wrong timezone | Fires at unexpected local hour | Set `timeZone` explicitly; never rely on UTC default. [SUPUESTO] |
| Retry storms | Repeated failing runs amplify load | Cap `retryCount`; make handler idempotent so retries are safe. [INFERENCIA] |

## Anti-Patterns

- Unpaginated queries over large collections → timeout. [INFERENCIA]
- Ignoring timeout → data left inconsistent. [DOC]
- Over-frequent scheduling without checking prior-run completion → overlap. [DOC]
- Non-deterministic side effects → retries corrupt state. [INFERENCIA]

## Related Skills

- `cloud-functions` — scheduled functions are a specialized Cloud Function trigger. [DOC]
- `firebase-extensions` — some extensions include scheduled processing. [DOC]

## Usage

- "/scheduled-functions" — run the full scheduled functions workflow.
- "scheduled functions on this project" — apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Assumes Cloud Functions **v2** + Cloud Scheduler enabled on the project. [SUPUESTO] Confirm via `firebase` config / GCP console.
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Empty target collection | Exit clean, log `processed: 0`, no error |
| Error mid-batch | Commit completed chunks, surface error, resume from cursor |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
