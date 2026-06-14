<!-- distilled from alfa skills/form-engineering -->
<!-- > -->
# Form Engineering

> "Forms are the gatekeepers of the web. Make them inviting, not intimidating." — Luke Wroblewski

## TL;DR

Implements robust web forms with layered validation (HTML5, client-side, server-side), multi-step wizards, file upload handling, and accessible error messaging for friction-free data capture. Use this skill when building complex forms, improving form conversion rates, or when form validation is inconsistent across the application. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify form requirements: fields, validation rules, submission endpoint
- Review existing form patterns in the codebase for consistency
- Gather UX requirements: inline validation timing, error message placement
- Check accessibility: labels, error associations, keyboard navigation
- Load reusable assets from `assets/`: `form-engineering-policy.json`, `error-message-patterns.json`, `optimistic-submit-template.ts`, and `upload-control-template.html` when designing implementation contracts.

### Step 2: Analyze
- Design validation layers — each is a distinct trust boundary, not a duplicate:
  1. **HTML5 native**: required, type, pattern, min/max. Free, but pattern messages are unstyleable and locale-bound; treat as a hint, never the guarantee. [INFERENCIA]
  2. **Client-side**: real-time validation with debounced feedback (250–400 ms on `input`, immediate on `blur`). UX layer only. [SUPUESTO]
  3. **Server-side**: authoritative. The only layer that may reject. Client rules MUST be a subset of server rules, never the reverse. [EXPLICIT]
- Plan multi-step form flow: step sequence, per-step persistence, back/forward navigation, and where partial state lives (memory vs storage — see Edge Cases).
- Design file upload: accepted MIME + extensions, max size, progress feedback, preview, retry, and the server storage boundary.
- Plan error handling: field-level (inline, beside input), form-level (summary at top, focus-linked), and server errors (network, 4xx/5xx, validation rejections) as three separate channels.
- Convert structured specs into a deterministic implementation contract with `scripts/compile-form-contract.py --spec <spec.json>` when the request includes enough field and submission detail.

**Decision: validation timing.** Validate on `blur` + on submit by default, not on every keystroke — keystroke validation flags errors before the user finishes typing and reads as hostile. Exception: show *positive* progress live for constrained fields (password strength, character count). Trade-off: `blur`-only delays feedback by one field, but eliminates false-error churn. [INFERENCIA]

### Step 3: Execute
- Build forms with proper HTML: label, fieldset/legend, input types, autocomplete attributes
- Implement real-time validation with meaningful error messages (not just "invalid")
- Create multi-step wizard with progress indicator and state preservation
- Implement file upload with drag-and-drop, preview, progress bar, and retry
- Set up optimistic submission: disable button, show loading, handle success/error
- Associate errors with inputs using aria-describedby and aria-invalid
- Implement autosave for long forms to prevent data loss
- Use the generated contract sections as the implementation checklist: validation parity, accessibility hooks, upload controls, optimistic submission, and telemetry.

### Step 4: Validate
- Verify all inputs have associated labels and error message connections
- Confirm server-side validation catches everything client-side does (and more)
- Test keyboard-only form completion (Tab, Enter, Escape)
- Check that error messages are specific and actionable ("Email must include @")
- Run `scripts/check.sh` after changing bundled assets, fixtures, or the deterministic compiler.

## Worked Example: actionable error copy

| Field state | Bad (rejected) | Good (acceptance bar) |
|---|---|---|
| Email missing `@` | "Invalid input" | "Email must include @, e.g. name@example.com" |
| Password too short | "Error" | "Use at least 12 characters" |
| Upload too large | "Upload failed" | "File is 14 MB; max is 10 MB. Try compressing it." |
| Server 500 on submit | (silent / spinner forever) | "We couldn't save this. Your entries are kept — retry?" + Retry button |

Rule: every error names the field, the rule, and the fix. Never blame ("You entered…"); state the constraint. [EXPLICIT]

## Quality Criteria

- [ ] Every input has a visible (not placeholder-only) label and accessible error association via `aria-describedby` + `aria-invalid`
- [ ] Client validation rules are a strict subset of server rules; server independently rejects everything client does, plus authz/uniqueness/business rules [EXPLICIT]
- [ ] Error messages name field + rule + fix; no generic "invalid"
- [ ] Multi-step forms preserve state on back navigation AND survive accidental reload (autosave) for long flows
- [ ] Submit is idempotent: double-click or retry cannot create duplicate records (disable + request token/key)
- [ ] Focus moves to the first error (or error summary) on failed submit; summary is keyboard-reachable
- [ ] Evidence tags applied to all non-obvious claims, one tag per claim, single family
- [ ] `assets/manifest.json` declares every reusable form engineering asset
- [ ] `scripts/compile-form-contract.py` rejects specs without validation parity, accessible errors, upload limits, or optimistic submit behavior
- [ ] File upload fields include accepted MIME/extensions, max size, preview/progress, retry, and server storage boundary

## Failure Modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Trusting client validation | Malformed/malicious data reaches DB | Server re-validates every field authoritatively [EXPLICIT] |
| Duplicate submission | Two records from one user intent | Disable on submit + idempotency key; re-enable only on confirmed failure |
| Lost input on error | Server error clears the form | Never reset on failure; repopulate from last-known state |
| Silent network failure | Spinner hangs forever | Timeout + explicit error channel + Retry; never leave button disabled with no feedback |
| Placeholder-as-label | Label vanishes on focus; screen readers skip it | Persistent `<label>`; placeholder is example text only |
| Validation race | Stale async result overwrites newer one | Tag requests; ignore responses older than the latest field edit [INFERENCIA] |

## Anti-Patterns

- Client-only validation without server-side verification
- Generic error messages ("Invalid input") that don't help users fix the issue
- Clearing the entire form on submission error, losing user input
- Placeholder text used as the only label (disappears on input, fails a11y)
- Disabling the submit button until the form is "valid" — hides what is wrong and traps keyboard users [INFERENCIA]

## Related Skills

- `accessibility-design` — accessible form patterns and error handling
- `html-semantic` — proper form markup and native validation
- `angular-development` — Angular reactive forms implementation
- `form-builder` — semantic form rendering from JSON schema

## Usage

Example invocations:

- "/form-engineering" — Run the full form engineering workflow
- "form engineering on this project" — Apply to current context

## Deterministic Script Contract

- Runtime script: `scripts/compile-form-contract.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill form-engineering`
- Default behavior: render the contract to stdout; write files only when `--output` is explicit.
- Safety boundary: malformed specs fail nonzero instead of producing partial form guidance.

## Assets Contract

- Output assets live in `assets/`.
- `assets/manifest.json` lists every reusable asset and where it is used.
- `assets/form-engineering-policy.json` defines required validation, accessibility, upload, and submission sections.
- `assets/error-message-patterns.json` provides deterministic copy patterns for field and form-level errors.
- `assets/optimistic-submit-template.ts` provides an implementation skeleton for pending, success, failure, and retry state.
- `assets/upload-control-template.html` provides the accessible file upload control baseline.


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified; form *copy* should follow the product locale, not this skill's output language [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: this skill designs the form layer (markup, validation, upload, submit, a11y). It does NOT define server schema, auth, rate-limiting, or storage backends — those are owned by API/security skills and are referenced as boundaries, not implemented here. [SUPUESTO]
- Does not cover CAPTCHA/anti-bot or payment-card capture (PCI scope) — escalate to a dedicated control. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal spec | Request field list + submission endpoint before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| User navigates back mid-wizard | Restore prior step's values; never re-blank completed steps |
| Reload / tab close on long form | Autosave to `sessionStorage` (per-tab) or `localStorage` (cross-session) keyed by form id; clear on success [INFERENCIA] |
| Upload exceeds size or wrong MIME | Reject client-side with specific copy AND re-check server-side; show which file and the limit |
| Slow / dropped network on submit | Optimistic pending → timeout → error channel + Retry; keep all input |
| Duplicate/idempotent resubmit | Disable + idempotency key so retries don't create duplicates |
| Async validity still pending at submit | Block submit until resolved or fail safe; never submit on stale "valid" |
