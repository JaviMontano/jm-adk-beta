<!-- distilled from alfa skills/scheduled-functions -->
<!-- > -->
# Scheduled Functions

> "Automate what repeats — schedule what must happen on time." — Unknown

## TL;DR

Guides implementation of scheduled Cloud Functions using Firebase's `onSchedule` with cron patterns — covering batch data processing, cleanup tasks, report generation, and reliable execution with error handling and monitoring. Use when you need periodic server-side tasks that run automatically. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify tasks that need periodic execution (cleanup, reports, sync, reminders)
- Check existing scheduled functions and their cron patterns
- Review data volumes for batch processing capacity planning
- Determine timezone requirements for schedule timing

### Step 2: Analyze
- Define cron schedule for each task (Cloud Scheduler syntax)
- Plan batch processing strategy for large datasets (pagination, chunking)
- Design idempotency for safe re-execution on failures
- Evaluate timeout limits (Cloud Functions v2: up to 60 minutes)

### Step 3: Execute
- Create scheduled function with `onSchedule` and cron expression
- Implement batch processing with Firestore pagination (process N documents per run)
- Add execution logging: start time, records processed, errors, duration
- Handle timeouts gracefully (checkpoint progress, resume on next run)
- Set up error alerting via Cloud Monitoring
- Use `runWith({ timeoutSeconds, memory })` for resource-intensive tasks
- Implement distributed locks if concurrent execution must be prevented

### Step 4: Validate
- Test function manually before scheduling (`firebase functions:shell`)
- Verify cron expression fires at expected times (use crontab.guru)
- Confirm batch processing handles edge cases (empty collections, errors mid-batch)
- Check Cloud Scheduler dashboard for execution history and errors

## Quality Criteria

- [ ] Cron schedule documented with human-readable explanation
- [ ] Batch processing handles large datasets without timeout
- [ ] Function is idempotent — safe to re-run without side effects
- [ ] Execution results logged for monitoring and debugging
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Running expensive queries without pagination (timeout on large collections)
- Not handling function timeout (data left in inconsistent state)
- Scheduling functions too frequently without checking if previous run completed

## Related Skills

- `cloud-functions` — scheduled functions are a specialized Cloud Function trigger
- `firebase-extensions` — some extensions include scheduled processing

## Usage

Example invocations:

- "/scheduled-functions" — Run the full scheduled functions workflow
- "scheduled functions on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
