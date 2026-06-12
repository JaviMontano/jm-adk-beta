<!-- distilled from alfa skills/microcopy-writing -->
<!-- > -->
# Microcopy Writing
> "Method over hacks."
## TL;DR
Write the small UI text that drives action: button labels, tooltips, empty states, confirmation dialogs, placeholders, error/success messages, inline validation. Optimize for clarity → action → reassurance, in that order. [EXPLICIT]
## Scope & Anti-Scope
- IN: in-product strings tied to a UI surface or interaction. [EXPLICIT]
- OUT: marketing/landing copy, long-form docs, legal/consent text (route to legal), localization/translation (write source EN; flag string for i18n). [EXPLICIT]
## Procedure
### Step 1: Discover
- Gather the surface, user goal at that moment, what just happened / happens next, and the system constraint (char limit, RTL, screen-reader path). [EXPLICIT]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV against the principles below; choose the verb-led option that needs the least re-reading. [EXPLICIT]
### Step 3: Execute
- Write the string + an empty/error/loading variant; attach evidence tags. [EXPLICIT]
### Step 4: Validate
- Verify against Quality Criteria; read aloud; confirm it works truncated and via screen reader. [EXPLICIT]
## Principles
- Lead with a verb that names the outcome ("Save changes", not "OK" / "Submit"). [EXPLICIT]
- Front-load the keyword; users scan first 1–2 words. [EXPLICIT]
- One idea per string; if it needs "and", split it. [EXPLICIT]
- Match the user's words, not the system's (avoid "invalid token", "null"). [EXPLICIT]
- Be specific over polite: "Choose a file under 5 MB" beats "An error occurred". [EXPLICIT]
- Voice = brand-consistent; tone shifts by stakes (calm on destructive, light on success). [EXPLICIT]
## Surface Patterns
| Surface | Pattern | Soft char budget |
|---------|---------|------------------|
| Button / primary CTA | Verb + object; never "Yes/No" alone | ≤ 25 |
| Confirmation dialog | Title = the action; body = consequence + reversibility; buttons restate verbs | title ≤ 40 |
| Empty state | What it is + the one action to fill it | body ≤ 90 |
| Placeholder | Example input, NOT the label (it vanishes on focus) | ≤ 30 |
| Tooltip | Why/what, not restate the label | ≤ 60 |
| Inline validation | What's wrong + how to fix, present tense | ≤ 80 |
| Success toast | Confirm + (optional) next/undo | ≤ 60 |
## Error Message Anatomy
Cause (plain) + Fix (actionable) + optional Reassurance. No blame, no codes user can't act on, no dead ends. [EXPLICIT]
- Bad: "Error 422: validation failed." → Good: "That email's already in use. Try signing in instead." [EXPLICIT]
## Worked Examples
- Destructive confirm: Title "Delete 3 projects?" / Body "This can't be undone." / Buttons "Delete" + "Cancel" (never "OK"). [EXPLICIT]
- Empty state: "No invoices yet. Create your first to start tracking payments." + [Create invoice]. [EXPLICIT]
- Loading vs blank: show "Loading invoices…", never an empty table that reads as "none". [EXPLICIT]
## Quality Criteria
- [ ] Verb-led, keyword front-loaded, one idea per string [EXPLICIT]
- [ ] Errors name a fix, not just a failure [EXPLICIT]
- [ ] Reads correctly when truncated and via screen reader (no icon-only meaning) [EXPLICIT]
- [ ] Empty / error / loading variants all written [EXPLICIT]
- [ ] Evidence tags applied; Constitution-compliant; actionable output [EXPLICIT]
## Accessibility & Edge Cases
- Don't encode meaning in color/icon alone; the words must stand alone. [EXPLICIT]
- Pair every destructive label with an aria-friendly consequence in the body. [EXPLICIT]
- Assume strings expand ~30% under localization; never tune to pixel-tight EN. [EXPLICIT]

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No char limit given | Apply soft budgets above; flag the assumption |
| String will be localized | Write source EN, avoid idioms, flag for i18n |
## Usage
Example invocations:
- "/microcopy-writing" — Run the full microcopy writing workflow
- "microcopy writing on this project" — Apply to current context
## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- English-language source output unless otherwise specified [EXPLICIT]
- Char budgets are defaults, not hard platform limits — verify per design system [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
