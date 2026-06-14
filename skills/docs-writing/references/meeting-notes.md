<!-- distilled from alfa skills/meeting-notes -->
<!-- > -->
# Meeting Notes

> TL;DR — Transforms raw meeting input (transcript, rough notes, agenda) into structured
> minutes covering metadata, attendees, agenda items, discussion summaries, decisions log,
> and action items with assigned owners and deadlines. Outputs markdown and optionally a
> branded HTML document ready for distribution.

---

## When to Activate

| Signal | Example |
|--------|---------|
| Direct request | "Write up meeting notes from this transcript" |
| Minutes formatting | "Format these as meeting minutes" |
| Spanish variant | "Redacta el acta de la reunion de hoy" |
| Post-meeting context | "Here are my rough notes from the standup" |
| Action item extraction | "Pull out the action items from this meeting" |

Activate when the user provides meeting content (transcript, notes, agenda) and needs
structured documentation.

### Anti-Scope — Do NOT Activate

| Request | Route to | Why |
|---------|----------|-----|
| Meeting planning / agenda design | `workshop-facilitator` | Forward-looking, no source content |
| Retrospective facilitation | `retrospective-facilitation` | Needs sentiment/dynamics, not minutes |
| Board / governance minutes (legal record) | `board-minutes` | Statutory format, quorum, motions |
| Live transcription from audio/video | external tooling | This skill is text-in only [EXPLICIT] |
| Status report from project data | `status-report` | Not meeting-sourced |

Boundary test: if there is **no captured meeting content to structure**, this skill does not apply. [EXPLICIT]

---

## S1 — Input Processing & Metadata Extraction

### Accepted Input Formats

| Format | Processing |
|--------|-----------|
| Raw transcript | NLP extraction of speakers, topics, decisions |
| Bullet-point notes | Structure into agenda-aligned sections |
| Audio transcript paste | Clean filler words, attribute speakers |
| Agenda + outcomes | Map outcomes to each agenda item |
| Mixed / chaotic notes | Identify threads, group by topic |

### Metadata Block

Extract or ask for:

```markdown
## Meeting Metadata
- **Title**: [Meeting name]
- **Date**: [YYYY-MM-DD]
- **Time**: [HH:MM - HH:MM] [Timezone]
- **Location**: [Room / Video link]
- **Facilitator**: [Name]
- **Note-taker**: [Name or "AI-assisted"]
- **Attendees**: [Name (Role)] per person
- **Absent**: [Name (Role)] if applicable
```

If the user omits metadata fields, mark them `[NOT PROVIDED]` rather than guessing.

**Why never guess metadata**: a fabricated date or attendee makes the minutes an
unreliable record and erodes trust in every other section. Missing-but-flagged is
recoverable; wrong-but-confident is not. [INFERRED]

**Date/time normalization**: render dates as `YYYY-MM-DD` and times in 24h with an
explicit timezone. If the input gives a relative date ("yesterday", "last Tuesday")
and no anchor date exists, mark `[NOT PROVIDED]` — do not compute from the current
date, which may differ from when the meeting occurred. [INFERRED]

---

## S2 — Discussion Summary & Decision Log

### Discussion Summary Structure

For each agenda item:

```markdown
### [Agenda Item Title]

**Context**: Brief background (1-2 sentences).

**Discussion**:
- [Speaker] raised [point]. [Supporting detail].
- [Speaker] countered with [alternative view].
- Group consensus: [outcome summary].

**Status**: Resolved | Deferred | Escalated
```

Rules:
- Attribute statements to speakers when identifiable; mark ambiguous speakers `[SPEAKER UNCLEAR]`.
- Maintain neutral tone — report what was said, not what you infer was meant. "Carlos
  disagreed" (observed) is fine; "Carlos was frustrated" (interpreted intent) is not.
- Summarize, do not transcribe verbatim (respect copyright and brevity). Preserve at most
  short verbatim quotes where exact wording is load-bearing (e.g., a committed number).
- Flag unresolved disagreements explicitly — never paper over conflict with false "consensus".
- A discussion item is **not** a decision. If no choice was made, set Status, do not invent
  a Decision Log row.

### Decision Log

| ID | Decision | Rationale | Owner | Date |
|----|----------|-----------|-------|------|
| D1 | Adopt serverless for MVP | Cost reduction + faster iteration | CTO | 2026-03-27 |
| D2 | Delay mobile app to Q3 | Resource constraints | PM | 2026-03-27 |

Each decision gets a unique ID for traceability across future meetings. IDs are
session-scoped (`D1`, `D2`, …) and reset per meeting unless the user supplies a running
register; true cross-meeting tracking needs external tooling. [INFERRED]

**Decision vs Action distinction** (common failure): a Decision is a *choice made*
("adopt serverless"); an Action is *work to do* ("draft the proposal"). One decision
often spawns several actions. Do not collapse them into one row.

---

## S3 — Action Items & Follow-up

### Action Item Format

| ID | Action | Owner | Due Date | Priority | Status |
|----|--------|-------|----------|----------|--------|
| A1 | Draft serverless architecture proposal | Maria R. | 2026-04-03 | High | Open |
| A2 | Schedule user testing sessions | Carlos P. | 2026-04-10 | Medium | Open |
| A3 | Review vendor contracts | Legal team | 2026-04-07 | High | Open |

Rules:
- Every action item must have an **owner** (person, not team, when possible). A team owner
  diffuses accountability; flag `[OWNER NEEDED]` rather than assigning to "the team".
- Every action item must have a **due date** (if not stated, suggest one and mark `[SUGGESTED]`).
  A `[SUGGESTED]` date is a prompt for the owner to confirm, not a commitment on their behalf.
- Phrase actions as imperative verb + object ("Draft the RFC"), not status ("RFC in progress").
- Priority levels: High, Medium, Low. Default to Medium if unstated; do not invent urgency.
- Status on creation is always "Open".
- Actions without clear owners are flagged: `[OWNER NEEDED]`.
- One action = one owner = one verb. Split "Maria and Carlos review and deploy" into separate
  rows so each owner has an unambiguous commitment.

### Follow-up Section

```markdown
## Next Meeting
- **Date**: [Next meeting date or cadence]
- **Carry-over items**: [List deferred agenda items]
- **Pre-read**: [Documents to review before next meeting]
```

---

## S4 — Output Formatting & Distribution

### Markdown Output (Default)

Clean markdown file following the structure:
1. Metadata block
2. Attendees table
3. Agenda items with discussion summaries
4. Decision log table
5. Action items table
6. Follow-up / next meeting

Filename convention: `YYYY-MM-DD_meeting-title.md`

### Branded HTML Output (Optional)

When the user requests HTML output or distribution-ready format:

- **Brand tokens**: navy #122562 background header, gold #FFD700 accent on decision badges,
  blue #137DC5 for links and action item highlights.
- **Typography**: Poppins 600 for section headings, Inter 400 for body.
- **Layout**: dark header with meeting title and date, light body for readability,
  action items in a highlighted card section.
- **Print styles**: clean black-on-white with visible table borders.
- **Self-contained**: single HTML file, no external dependencies beyond Google Fonts.
- **Offline fallback**: if Google Fonts cannot load, the page must degrade to system fonts
  (`font-family: Inter, system-ui, sans-serif`) without breaking layout. [INFERRED]
- **Markdown is the source of truth**: HTML is a rendering of the same content. Never let the
  two diverge — regenerate HTML from the markdown, do not hand-edit both. [INFERRED]

### Distribution Checklist

- [ ] Review for sensitive information before sharing externally.
- [ ] Confirm all attendee names are spelled correctly.
- [ ] Verify action item owners have been notified.
- [ ] Attach to calendar invite for the next meeting.

---

## Trade-off Matrix

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Detail level | Verbatim transcript | Executive summary | Summary with key quotes |
| Attribution | Name every speaker | Anonymize discussion | Attribute when relevant |
| Format | Markdown only | Markdown + HTML | Both — markdown for archive, HTML for distribution |
| Action item dates | Only stated dates | Suggest dates for undated items | Suggest with [SUGGESTED] tag |
| Language | Single language | Bilingual ES/EN | Match meeting language; bilingual if mixed |

---

## Assumptions & Limits

- Assumes the user provides accurate input; the skill does not verify claims made in meetings. [EXPLICIT]
- Does not record, transcribe, or access audio/video — works from provided text only. [EXPLICIT]
- Speaker attribution accuracy depends on input quality; ambiguous speakers are marked
  `[SPEAKER UNCLEAR]`. [INFERRED]
- Does not send emails, calendar invites, or notifications to attendees. [EXPLICIT]
- Decision IDs and action item IDs are session-scoped; cross-meeting tracking requires
  external tooling. [INFERRED]

---

## Edge Cases

1. **Transcript with no clear agenda** — Infer topic clusters from discussion flow; present
   as "Discussion Topics" rather than "Agenda Items" and note that no formal agenda was provided.
2. **Meeting with no decisions or action items** — Explicitly state "No decisions were recorded"
   and "No action items were identified" rather than omitting the sections.
3. **Highly technical meeting with jargon** — Preserve technical terms exactly as stated;
   add a glossary section at the end if 5+ specialized terms appear.
4. **Multilingual meeting (mixed ES/EN)** — Write notes in the dominant language; include
   key terms in both languages where they first appear: "sprint planning (planificacion de sprint)".
5. **Conflicting accounts of the same outcome** — If two attendees state different versions of
   what was decided, record both as a flagged disagreement; do not silently pick one.
6. **Sensitive / off-the-record content** — If the input contains compensation, legal exposure,
   PII, or "do not minute this" asides, exclude from the shared record and note `[REDACTED — see
   facilitator]` rather than copying it verbatim. [EXPLICIT]
7. **Decision reversed later in the same meeting** — Keep the final decision in the log; note the
   reversal in the discussion ("initially agreed X, reversed to Y after …") for traceability.
8. **Action with a dependency but no owner for the dependency** — Record the action, then add a
   `[BLOCKED — depends on …]` note so the gap is visible, not buried.
9. **Empty or near-empty input** — If content is too thin to structure (e.g., one vague line),
   ask for the transcript/notes rather than fabricating sections. [EXPLICIT]

---

## Good vs Bad Example

### Good

```markdown
### API Migration Timeline

**Context**: Team needs to migrate from REST v2 to GraphQL before Q3 launch.

**Discussion**:
- Maria proposed a phased migration starting with read-only endpoints.
- Carlos raised concerns about client SDK compatibility.
- Group agreed on a 3-phase approach with a compatibility layer.

**Status**: Resolved

| ID | Decision | Owner | Date |
|----|----------|-------|------|
| D1 | Phased migration with compatibility layer | Maria R. | 2026-03-27 |

| ID | Action | Owner | Due Date | Priority | Status |
|----|--------|-------|----------|----------|--------|
| A1 | Draft migration RFC | Maria R. | 2026-04-03 | High | Open |
| A2 | Audit client SDK dependencies | Carlos P. | 2026-04-01 | High | Open |
```

Why it works: clear context, attributed discussion, linked decision and actions, dates assigned.

### Bad

```markdown
## Meeting Notes

We talked about the API migration. Some people think we should do GraphQL.
There was some disagreement. We decided to move forward.

TODO: someone should write something up about this.
```

Why it fails: no attribution, no decision detail, vague action item with no owner or date.

---

## Failure Modes

| Failure | Symptom | Prevention |
|---------|---------|-----------|
| Hallucinated metadata | Date/attendee not in source | Mark `[NOT PROVIDED]`; never infer from current date |
| Decision/action conflation | A choice lands only in the action table | Apply the Decision-vs-Action test (S2/S3) |
| Orphan action | Action with no owner or no date | Flag `[OWNER NEEDED]` / `[SUGGESTED]`; do not assign blame |
| Editorializing | "Was frustrated", "obviously wrong" | Report observed words only; strip inferred intent |
| False consensus | "Group agreed" over an unresolved split | Flag disagreement; set Status Deferred/Escalated |
| Verbatim dump | Notes mirror the raw transcript length | Summarize; quote only load-bearing wording |
| Section omission | Empty Decisions/Actions silently dropped | State "No decisions recorded" explicitly (Edge Case 2) |
| HTML/markdown drift | Two outputs disagree | Regenerate HTML from markdown source of truth |
| Leaked sensitive content | PII/comp/legal in shared file | Redact per Edge Case 6 before distribution |

---

## Validation Gate

Before delivering the final meeting notes, confirm every item:

- [ ] Metadata block includes date, time, attendees, and facilitator (or marked [NOT PROVIDED])
- [ ] Each agenda/discussion item has context, discussion summary, and status
- [ ] Decision log uses unique IDs with rationale and owner columns
- [ ] Every action item has an assigned owner (person name, not team)
- [ ] Every action item has a due date (actual or [SUGGESTED])
- [ ] Speaker attribution is present where identifiable
- [ ] No editorializing or interpreting speaker intent
- [ ] Unresolved items are explicitly marked as Deferred or Escalated
- [ ] HTML output (if requested) uses brand colors #122562, #FFD700, #137DC5 and degrades to system fonts offline
- [ ] Follow-up section includes next meeting date and carry-over items
- [ ] No hallucinated metadata — every field is from source or explicitly flagged
- [ ] Sensitive/off-the-record content redacted before any external share (Edge Case 6)
- [ ] Decisions and actions are distinct rows (no conflation)

If any box cannot be checked, deliver with the gap **visibly flagged** rather than silently
filled — a flagged hole is fixable; a confident fabrication is not. [INFERRED]

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/minutes-template.md` | Standard meeting minutes markdown template |
| `references/action-item-patterns.md` | Action item writing patterns with examples |
| `references/html-minutes-template.html` | Branded HTML template for distribution |
| `references/decision-log-schema.md` | Decision log format and cross-meeting tracking |
