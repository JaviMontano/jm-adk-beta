<!-- distilled from alfa skills/notification-handler -->
<!-- > -->
# Notification Handler
> "Method over hacks."
## TL;DR
System notification management for a session: emit progress updates, route alerts by severity, dedupe noise, and degrade gracefully when no notifier channel exists. [EXPLICIT]

## Procedure
### Step 1: Discover
- Gather context: what events fire (task done, error, long-run milestone, user-input-needed), available channels (stdout, OS notifier, log file, webhook), and the caller's verbosity preference. [EXPLICIT]
- If no channel is configured, default to stdout + session log; never fail the session for a missing notifier. [ASSUMPTION]

### Step 2: Analyze (classify + route)
- Assign each event a severity and route it (Constitution XIII/XIV — least-surprise, evidence-first). [EXPLICIT]

| Severity | Trigger example | Default route | User-facing? |
|----------|-----------------|---------------|--------------|
| `info` | step complete, milestone | session log only | no (batched) |
| `progress` | long-run % update | inline stdout, throttled | yes |
| `warn` | recoverable issue, retry | stdout + log | yes |
| `error` | task failed, aborting | stdout + log + OS notifier | yes (immediate) |
| `action` | user input required | OS notifier + block | yes (immediate) |

### Step 3: Execute
- Emit with an evidence tag and a stable `event_id` so downstream dedupe works. [EXPLICIT]
- Throttle `progress` to >=1 update / 2s; coalesce `info` into an end-of-step digest. [ASSUMPTION]
- Worked example: a 200-file scan emits one `progress` line per 2s, one `info` digest at end ("198 ok, 2 skipped"), and a single `warn` per skipped file — not 200 lines. [EXPLICIT]

### Step 4: Validate
- Verify every `error`/`action` reached a user-visible channel; if the OS notifier failed, confirm the stdout fallback fired. [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Severity assigned + routed per table
- [ ] `error`/`action` delivered to a user-visible channel (fallback verified)
- [ ] Noise throttled/deduped; no flooding
- [ ] Constitution-compliant; actionable output

## Usage

Example invocations:

- "/notification-handler" — Run the full notification handler workflow
- "notification handler on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Out of scope: delivery guarantees, retry queues, or persistence across crashes — best-effort, in-session only. [EXPLICIT]
- Out of scope: emitting secrets/PII in notification bodies; redact before routing. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No notifier channel configured | Fall back to stdout + session log; warn once, continue [ASSUMPTION] |
| OS notifier API fails mid-run | Catch, log `warn`, deliver via stdout fallback; never abort the session [EXPLICIT] |
| Duplicate event re-fired | Suppress by `event_id`; emit only on state change [EXPLICIT] |
| High-frequency progress | Throttle to the cadence above; coalesce into a digest [ASSUMPTION] |
| Notification body contains secrets/PII | Redact before routing; if unredactable, drop body and route metadata only [EXPLICIT] |

## Failure Modes
- Flooding: unthrottled `progress`/`info` buries `error`/`action`. Mitigation: severity gates + coalescing. [EXPLICIT]
- Silent loss: `error` sent only to a failed channel. Mitigation: Step 4 fallback verification. [EXPLICIT]
- Leakage: raw payload routed to an external webhook. Mitigation: redact-before-route limit. [EXPLICIT]
