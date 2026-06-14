<!-- distilled from alfa skills/google-calendar-mcp -->
<!-- > -->
# Google Calendar MCP

## TL;DR

Use this skill to safely query Google Calendar agendas, check availability, and create, edit, or cancel events through the local `workspace-mcp` server. Always read first, choose the narrowest Calendar scope, preserve timezone evidence, and require human confirmation before any mutating MCP call. Use `scripts/compile-google-calendar-mcp.py` when a structured offline plan is useful. [EXPLICIT]

**In scope:** agenda reads, free/busy checks, single + recurring event create/edit/cancel, Google Meet attach, out-of-office, read-back verification. **Out of scope (anti-scope):** silent mutations, bulk deletes without per-event confirmation, calendar sharing/ACL changes, cross-account access, sending mail (delegate to `gmail-mcp`), reminder automation (delegate to `notification-service`). [INFERENCE]

## Prerequisites

- Google Workspace MCP server configured (see `docs/google-workspace-mcp-setup.md`) [DOC]
- Google Calendar API enabled in Google Cloud Console [DOC]
- OAuth2 credentials authenticated; the granted scopes must already cover the operation — the MCP cannot widen scope at call time. If a needed scope is absent, stop and ask the user to re-consent. [INFERENCE]
- Environment variable `GOOGLE_WORKSPACE_CREDENTIALS_PATH` set for local `workspace-mcp` [CONFIG]

## Procedure

### Step 1: Discover Read-Only Context
- Verify the user intent: agenda query, availability check, create, edit, cancel, or out-of-office.
- Prefer read-only MCP calls first: `mcp__workspace-mcp__list_calendars` and `mcp__workspace-mcp__get_events`.
- Capture the calendar id, event id, date window, timezone, attendees, and whether Google Meet is requested.
- For agenda searches, use bounded `timeMin`/`timeMax`, `singleEvents=true`, and `orderBy=startTime` when available. With `singleEvents=true`, recurring series expand into instances; the instance id (`<eventId>_<timestamp>`) — not the series id — is what you edit/cancel. [INFERENCE]
- Resolve relative dates ("tomorrow", "next Tuesday") against the user's timezone, not the host/account default, then echo the absolute date back for confirmation. [ASSUMPTION]

### Step 2: Select Minimum Scope
- Availability-only checks use `https://www.googleapis.com/auth/calendar.freebusy`.
- Agenda/event reads use `https://www.googleapis.com/auth/calendar.events.readonly`.
- Create, edit, or cancel operations use `https://www.googleapis.com/auth/calendar.events`.
- App-owned secondary calendar workflows may use `https://www.googleapis.com/auth/calendar.app.created`.
- Avoid broad `calendar` unless the local MCP configuration already has it and a narrower scope is impossible.
- **Decision — scope vs. friction:** narrowest scope is the default because over-broad consent is the highest-impact, hardest-to-revoke risk; the trade-off is occasional re-consent prompts, which is acceptable for a confirmation-gated tool. [INFERENCE]

### Step 3: Build the Safe Operation
- Use `assets/` as the deterministic policy source:
  - `assets/scope-policy.json` for scope selection.
  - `assets/calendar-event-payload-policy.json` for event fields, timezone, attendees, and notifications.
  - `assets/conference-data-policy.json` for Google Meet and `requestId` handling.
  - `assets/confirmation-policy.json` for human-confirmation gates.
- For structured work, run `scripts/compile-google-calendar-mcp.py --input <operation.json> --output <plan.md>`. [CODE]
- The compiler renders a plan only; it never calls Calendar or MCP. [EXPLICIT]
- **Timezone rule:** always send `start`/`end` as RFC3339 with explicit offset AND a `timeZone` IANA field (e.g. `America/Bogota`); the offset alone is ambiguous across DST transitions, and the IANA name is what Calendar uses for recurrence math. [INFERENCE]
- All-day events use date-only `start.date`/`end.date` where `end.date` is exclusive (the day after the last day). [DOC]

### Step 4: Confirm Before Mutation
- Before `mcp__workspace-mcp__manage_event` or `mcp__workspace-mcp__manage_out_of_office`, show the user the exact operation: summary, calendar id, date/time, timezone, attendees, `sendUpdates`, Meet request, and target event id when editing/cancelling.
- Do not create, edit, cancel, add attendees, or send invitations until the user confirms.
- If Google Meet is requested, require `conferenceDataVersion=1` and a fresh `conferenceData.createRequest.requestId` for the new conference request.
- **Edit semantics:** `manage_event` updates replace the fields you send. For attendees, send the FULL intended list (omitting an attendee removes them); to keep existing attendees while adding one, read the current list first and append. [INFERENCE]
- **Recurring edits:** confirm the user's intent — this instance, this-and-following, or the whole series — before mutating; the three map to different ids/payloads and are not reversible by a single undo. [INFERENCE]

### Step 5: Validate Result
- After a real MCP mutation, read back the event and verify `id`, `htmlLink`, start/end, timezone, attendees, and `hangoutLink` or `conferenceData` when Meet was requested.
- Report tool errors as recoverable execution errors when possible; do not hide failed or partial operations.
- Keep evidence tags on claims: `[CODE]`, `[DOC]`, `[INFERENCE]`, or `[ASSUMPTION]`.
- If Meet was requested but `conferenceData.status` is `pending`, re-read once after a short delay before declaring the link unavailable — conference provisioning is asynchronous. [INFERENCE]

## Failure Modes & Recovery

| Symptom | Likely cause | Recovery |
| --- | --- | --- |
| `403 insufficientPermissions` | granted scope narrower than operation | stop; ask user to re-consent at the needed scope (Step 2) [INFERENCE] |
| `404 notFound` on edit/cancel | wrong id (series vs. instance), or wrong calendar id | re-read with `singleEvents=true`, use the instance id [INFERENCE] |
| `409`/duplicate Meet | reused `requestId` | generate a fresh `requestId` per conference request [DOC] |
| `429`/`rateLimitExceeded` | quota/burst | back off and retry the read; never auto-retry a mutation without re-confirmation [INFERENCE] |
| Event created at wrong hour | offset sent without IANA `timeZone`, or DST boundary | resend with both offset and `timeZone`; verify on read-back [INFERENCE] |
| Attendee silently dropped | partial attendee list sent on edit | re-read, append to full list, re-confirm [INFERENCE] |
| Invite not received | `sendUpdates` not set to `all` | confirm notification policy before re-sending [INFERENCE] |

## Quality Criteria

- [ ] Read-only-first check completed before mutation.
- [ ] Minimum Calendar scope selected for the operation.
- [ ] Timed events include RFC3339 date-times with offsets AND IANA `timeZone` names.
- [ ] Attendee emails and `sendUpdates` policy are explicit before invitations.
- [ ] Edit payloads carry the full attendee list (no accidental removals).
- [ ] Recurring-edit target (instance / following / series) confirmed.
- [ ] Google Meet requests include `conferenceDataVersion=1` and a fresh `conferenceData.createRequest.requestId`.
- [ ] Human confirmation captured before create/edit/cancel/out-of-office mutation.
- [ ] Result is verified with a read-back when a real MCP mutation occurs.
- [ ] Evidence tags on all claims.

## Anti-Patterns

- Creating events without confirming date/time with user
- Deleting events without explicit confirmation
- Sending calendar invites without user review
- Scheduling over existing events without checking availability
- Calling mutating MCP tools from scripts or fixtures
- Using account default timezone when the request contains a concrete locale or timezone
- Reusing a Meet `requestId` for a different conference request
- Requesting broad Calendar scopes when a narrow scope satisfies the task
- Sending a partial attendee list on edit (silently drops omitted attendees)
- Editing one recurring instance when the user meant the series (or vice versa)
- Auto-retrying a failed mutation without fresh user confirmation

## Worked Example — "Schedule 45 min with Ana next Tuesday 3 PM, with Meet"

1. Read: `list_calendars` → pick primary; `get_events` over that Tuesday to confirm 15:00–15:45 `America/Bogota` is free. [CODE]
2. Scope: `calendar.events` (create). [INFERENCE]
3. Build payload: `summary`, `start={dateTime:"2026-06-16T15:00:00-05:00", timeZone:"America/Bogota"}`, `end=...15:45...`, `attendees:[{email:"ana@…"}]`, `sendUpdates:"all"`, `conferenceDataVersion:1`, `conferenceData.createRequest.requestId=<new-uuid>`. [INFERENCE]
4. Confirm: show the full block; wait for explicit yes.
5. Mutate `manage_event`; read back → verify `id`, `htmlLink`, times, `hangoutLink`. If `conferenceData.status=pending`, re-read once. [INFERENCE]

## Related Skills

- `gmail-mcp` — send email follow-ups after scheduling
- `google-workspace-apis` — programmatic Calendar API patterns
- `notification-service` — automated reminders

## Usage

- `/google-calendar-mcp` — interactive calendar management.
- "What meetings do I have tomorrow?"
- "Check whether I am free Friday from 2 to 3 PM America/Bogota."
- "Schedule a 45-minute meeting with Ana next Tuesday at 3 PM with Google Meet."
- "Move the portfolio review to Wednesday and keep the same attendees."
- "Cancel the standup on Friday after I confirm the event id."

## Assumptions & Limits

- Requires authenticated Google Workspace MCP server [EXPLICIT]
- Cannot access calendars from non-authenticated accounts [EXPLICIT]
- Cannot widen OAuth scope at call time; missing scope requires user re-consent [INFERENCE]
- Scripts compile offline plans and never call Google Calendar or MCP [EXPLICIT]
- A generated Google Meet conference may be asynchronous and should be read back after mutation [EXPLICIT]
- The skill does not bypass user confirmation for mutating operations [EXPLICIT]
- Does not manage calendar ACLs/sharing or send standalone email — delegate to the related skills [INFERENCE]
