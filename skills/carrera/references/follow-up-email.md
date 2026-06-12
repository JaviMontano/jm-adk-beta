<!-- distilled from alfa skills/follow-up-email -->
<!-- > -->
# Follow-Up Email Generator

Generates personalized follow-up emails after meetings or events. Extracts action items from meeting notes and sends individualized messages to each responsible party with only their relevant tasks, deadlines, and context. [EXPLICIT]

**Scope.** One meeting → N recipient drafts, one recipient per render. [EXPLICIT]
**Anti-scope** (out of this skill): scheduling the meeting, summarizing for non-attendees, sending newsletters/bulk mail, threading replies into an existing conversation, or any send without explicit approval. [INFERENCIA]

## When to Activate

This skill activates when the user: [EXPLICIT]
- Requests follow-up emails after a meeting or event
- Wants to distribute action items to attendees
- Says "seguimiento", "follow up", "send action items", "meeting recap"
- Provides meeting notes and asks to notify participants
- Needs reminders created for upcoming deadlines from a meeting

**Do NOT activate** for: a single recipient with no action items (use a plain reply), real-time meeting transcription, or "draft an email" requests unrelated to meeting action items. [INFERENCIA]

## Inputs & Assumptions

| Input | Required | Default if absent |
|-------|----------|-------------------|
| Meeting notes (text/file/link) | yes | `{VACIO_CRITICO}` — stop, ask [SUPUESTO] |
| Attendee emails | per-recipient | flag + skip that person [EXPLICIT] |
| Deadlines per task | no | flag, ask user; never invent a date [EXPLICIT] |
| Tone / language | no | from `email-copy-tokens.json` [CONFIG] |
| Send vs draft | no | draft-first (token default) [CONFIG] |

Assumptions made explicit: notes are in one language per meeting unless mixed-language is detected; "first name" is derivable from the attendee record; one email address per attendee. [SUPUESTO] Verify mixed-language and duplicate-name cases with the user before rendering. [SUPUESTO]

## Execution Flow

### Step 1: Extract Action Items from Meeting Notes

Parse the meeting notes (provided as text, file, or document link) to identify: [EXPLICIT]

1. **Meeting metadata**: title, date, location, duration
2. **Attendees**: name, email, role/title (if available)
3. **Action items**: task description, assignee, deadline, priority, context
4. **Decisions made**: key agreements that provide context for action items
5. **Next meeting**: date/time if scheduled

**Parsing rules:** [EXPLICIT]
- Patterns: `ACTION:`, `TODO:`, `- [ ]`, `@name will...`, `name se encarga de...`
- Associate deadlines with tasks: "para el viernes", "by Friday", "deadline: 2026-04-10"
- Ambiguous assignee → flag for user confirmation before sending
- Group items by person for individualized emails

**Edge cases (decide, don't guess):** [INFERENCIA]
- Task with two assignees → emit to both, mark "shared with <name>"; do not silently pick one.
- Relative deadline ("next Friday") → resolve against meeting date, echo the absolute date back for confirmation. [SUPUESTO]
- Assignee named but not in attendee list → flag as `{POR_CONFIRMAR}`; no email until address is supplied.
- Unassigned action item → never drop it; surface in the summary as "owner needed".
- Duplicate/near-identical tasks → dedup before grouping so a person is not emailed the same item twice.

### Step 2: Generate Personalized Emails Per Person

For each attendee with action items: [EXPLICIT]

1. Use the `templates/follow-up-action-items.md` template
2. Use `assets/email-copy-tokens.json` for default subject, sign-off, tone, and draft-first policy
3. Use `scripts/render-follow-up-email.py --data <meeting.json> --recipient <email>` when the meeting notes have been normalized into JSON
4. Include ONLY that person's action items (never leak others' tasks)
5. Add relevant context from meeting decisions that affect their tasks
6. Include next steps that apply to everyone
7. Set appropriate tone: professional but warm, action-oriented

**Personalization rules:** [EXPLICIT]
- Address by first name
- Reference their specific contributions from the meeting
- Order action items by deadline (earliest first); undated items sort last
- Flag high-priority items with bold formatting
- Include meeting title and date for reference

**Failure modes to guard against:** [INFERENCIA]
- Privacy leak: another person's name/task in the body or in shared-context decisions — strip cross-references that name unrelated owners.
- Template-token left unrendered (`{{name}}`) — fail the render rather than send a literal placeholder. [SUPUESTO]
- Empty body after filtering (all items reassigned) — skip the recipient, do not send a hollow email.

### Step 3: Optionally Create Calendar Reminders

When deadlines are identified: [EXPLICIT]

1. Ask user if they want calendar events created for deadlines
2. Use `mcp__workspace-mcp__manage_event` to create reminders
3. Set reminder 24h before each deadline
4. Include action item description in event body
5. Invite the responsible person

Reminders are opt-in and idempotent: re-running must not create duplicate events for the same task+deadline — match on (assignee, task, date) before creating. [INFERENCIA]

### Step 4: Send or Draft for Review

Default behavior: **draft first, send after user approval.** [EXPLICIT]

1. Use `mcp__workspace-mcp__draft_gmail_message` to create drafts
2. Present summary: who gets what, how many items per person
3. On user approval, use `mcp__workspace-mcp__send_gmail_message` to send
4. Log sent emails with timestamps

**Safety rules:** [EXPLICIT]
- NEVER auto-send without explicit user confirmation
- Show preview of each email before sending
- Allow user to edit individual emails before sending
- If no email address found for an attendee, flag and skip
- Partial send is acceptable: send approved drafts, hold flagged ones; report both sets. [INFERENCIA]

## Acceptance Criteria

A run is complete only when ALL hold: [INFERENCIA]
- Every extracted action item appears in exactly one recipient email (or the "owner needed" list) — count in == count out.
- No recipient's body references another owner's task. (Privacy test must pass.)
- Each dated item shows an absolute date; no relative dates survive in output.
- No email sent without a recorded user-approval timestamp.
- Every rendered draft passes template-token completeness (zero `{{...}}` literals).
- Skipped attendees are reported with the reason (no email / zero items).

## Quality Criteria

| Criterion | Requirement |
|-----------|-------------|
| Completeness | Every action item from notes appears in exactly one email |
| Accuracy | Correct assignee for each task, correct deadlines |
| Privacy | No person sees another person's action items |
| Tone | Professional, warm, actionable — not robotic |
| Timing | Follow-up sent within 24h of meeting (best practice) |
| Template | Uses branded template consistently |
| Confirmation | User approves before any email is sent |
| Assets | `assets/manifest.json` declares every reusable output asset |
| Determinism | Scripted rendering is one-recipient-at-a-time and privacy tested |

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| Sending all action items to everyone | Personalize: each person gets only their items |
| Auto-sending without review | Always draft first, send after approval |
| Vague action items ("handle the thing") | Preserve original specificity from notes; flag vague items |
| Missing deadlines | If no deadline specified, flag and ask user |
| Generic greeting ("Dear team member") | Use attendee's actual first name |
| Ignoring meeting context | Include relevant decisions that affect each task |
| Sending to people with no action items | Skip attendees with zero items (or send optional summary-only) |
| Inventing a deadline to satisfy ordering | Leave undated, sort last, ask user |
| Re-running creates duplicate calendar events | Match on (assignee, task, date) before create |

## Agent Composition

| Agent | Role |
|-------|------|
| Lead | Parses meeting notes, extracts action items, generates email content |
| Support | Formats emails, applies templates, handles calendar event creation |
| Guardian | Validates completeness (all items assigned), privacy (no cross-leak), tone |
| Specialist | Email deliverability, personalization optimization, multi-language support |

## Example Input

```
Meeting: Q2 Planning - April 1, 2026
Attendees: Ana (ana@company.com), Carlos (carlos@company.com), Maria (maria@company.com)

Decisions:
- Budget approved for new marketing campaign
- Launch date set for May 15

Action items:
- Ana: Prepare campaign brief by April 8
- Carlos: Set up analytics dashboard by April 10
- Carlos: Review vendor proposals by April 5
- Maria: Schedule kickoff with design team by April 4
- Maria: Draft social media calendar by April 12
```

## Example Output

Three personalized emails, each containing only the recipient's items, with meeting context and next steps. Worked detail for Carlos (demonstrates deadline ordering + privacy): [INFERENCIA]

```
Subject: Q2 Planning follow-up — your 2 action items
Hi Carlos,
Thanks for joining Q2 Planning (April 1). Your items, soonest first:
1. Review vendor proposals — due April 5
2. Set up analytics dashboard — due April 10
Context: budget for the new campaign is approved; launch is May 15, so the
dashboard should be live before then.
Next step for everyone: confirm the May 15 launch date works.
```

Note Carlos's email names neither Ana nor Maria and excludes their tasks (privacy), and April 5 precedes April 10 (ordering). [INFERENCIA]

## Deterministic Script Contract

- Runtime script: `scripts/render-follow-up-email.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill follow-up-email`
- Default behavior: render to stdout; write files only with `--output`.
- Safety boundary: scripts render drafts only; they never send email.
- One recipient per invocation — the privacy guarantee is structural, not a runtime filter. [SUPUESTO]

## Assets Contract

- Output assets live in `assets/`.
- `assets/manifest.json` lists every asset and where it is used.
- `assets/email-style.css` styles HTML previews.
- `assets/email-copy-tokens.json` carries subject, sign-off, tone, and draft-first policy defaults.
