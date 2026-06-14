<!-- distilled from alfa skills/error-messaging -->
<!-- > -->
# Error Messaging
> "Method over hacks."
## TL;DR
Taxonomy, tone, and actionability rules for user-facing error messages: classify the error, write in plain calm language, state cause + recovery, never blame the user. [EXPLICIT]

## Anti-scope
- Not log/telemetry strings for engineers (different audience: terse, codes OK). [EXPLICIT]
- Not exception-handling architecture or retry logic — message copy only. [EXPLICIT]
- Not localization mechanics — but every string MUST be translatable (no concatenation). [EXPLICIT]

## Taxonomy (classify first; tone follows from class)
| Class | Cause | Default tone | Primary action |
|-------|-------|--------------|----------------|
| User-input | Bad/invalid value | Neutral, instructive | Tell exactly what to fix |
| State/precondition | Action not allowed now | Explanatory | Offer the unblocking step |
| System/transient | Timeout, 5xx, network | Reassuring, no blame | Retry / auto-recover |
| Permission/auth | Lacks access | Direct, non-accusatory | Path to request access |
| Catastrophic | Data loss risk | Calm, serious | Safe exit + support ref |

## Message formula
`[What happened] + [Why, if useful] + [What to do next]`. Lead with the action when space is tight. [EXPLICIT]
- One idea per message. Match severity to UI weight (inline < toast < blocking dialog). [EXPLICIT]
- Give an error reference/code ONLY for system/catastrophic classes (support handoff). [INFERENCIA]

## Tone rules
- No blame ("you entered" → "this field needs"), no jargon, no raw stack traces, no "Error 0x...". [EXPLICIT]
- Never end with a dead end — always one next step or escape. [EXPLICIT]
- No false reassurance; if data was lost, say so plainly. [EXPLICIT]

## Worked examples
| Bad | Good | Why |
|-----|------|-----|
| "Invalid input." | "Email needs an @ — e.g. name@site.com." | Names field + shows fix |
| "Error 500." | "We couldn't save. Trying again… (ref 8F2A)" | No blame, recovery, ref |
| "Access denied." | "You need editor access. Request it from the owner." | Gives a path |
| "Operation failed." | "Can't delete a project with open tasks. Close them first." | States precondition |

## Procedure
### Step 1: Discover
- Inventory error states from code/flows; tag each with a taxonomy class. [EXPLICIT]
### Step 2: Analyze
- Score each message vs the formula + tone rules per Constitution XIII/XIV. [EXPLICIT]
### Step 3: Execute
- Rewrite as translatable strings (no concatenation, no embedded markup) with evidence tags. [EXPLICIT]
### Step 4: Validate
- Verify every message has a next step and matches its class's severity weight. [EXPLICIT]

## Quality Criteria
- [ ] Every error classified by taxonomy
- [ ] Each message gives a concrete next step (no dead ends)
- [ ] No blame, jargon, or raw codes in user-facing copy
- [ ] Severity matches UI weight (inline/toast/dialog)
- [ ] Strings translatable; evidence tags applied; Constitution-compliant

## Usage

Example invocations:

- "/error-messaging" — Run the full error messaging workflow
- "error messaging on this project" — Apply to current context

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
| Unknown/unanticipated system error | Generic calm message + reference code + support path [INFERENCIA] |
| Error during error display | Fail safe to a static fallback string; never loop [INFERENCIA] |
