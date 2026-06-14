<!-- distilled from alfa skills/empty-states -->
<!-- > -->
# Empty States
> "Method over hacks."
## TL;DR
Design the zero-data UI: what a screen shows when there is nothing to show. Three distinct types — **first-use** (never had data), **user-cleared** (emptied it), **error/blocked** (data exists but unreachable) — each needs different copy and CTA. An empty state is the highest-leverage onboarding surface, not a blank canvas. [EXPLICIT]

## When each type fires
| Type | Trigger | Goal | Primary CTA |
|------|---------|------|-------------|
| First-use | New account/feature, no records yet | Teach value + first action | "Create your first X" |
| User-cleared | Search/filter returns 0, inbox zero, deleted all | Confirm + offer next move | "Clear filters" / "Add X" |
| Error/blocked | Load failed, no permission, offline | Explain + recover | "Retry" / "Request access" |

## Procedure
### Step 1: Classify
- Identify which of the 3 types applies; a screen may have several (filtered-to-zero ≠ first-use). [EXPLICIT]
### Step 2: Write the message
- One-line headline (what + why empty), one-line subtext (what to do). Plain language, no dead-ends. [EXPLICIT]
### Step 3: Choose CTA + illustration
- Exactly one primary action; optional secondary (docs, sample data). Illustration is optional and must not delay the CTA. [EXPLICIT]
### Step 4: Validate
- Verify against quality criteria below; test with real zero-data accounts, not seeded demos. [EXPLICIT]

## Worked example
Projects list, first-use:
- Headline: "No projects yet"
- Subtext: "Projects group your work and let you invite teammates."
- Primary CTA: "Create project" · Secondary: "Import from CSV"
- Anti-pattern avoided: showing a spinner-like blank, or "Error: no data found" for a normal empty list. [EXPLICIT]

## Quality Criteria
- [ ] Empty-state type correctly classified (first-use vs cleared vs error)
- [ ] Headline + subtext present; no raw "0 results" with no guidance
- [ ] Exactly one primary CTA, reachable in one tap/click
- [ ] Error states offer a recovery path (retry/permission/contact), never a dead-end
- [ ] Tested on a true zero-data account; loading state distinguishable from empty state
- [ ] Evidence tags applied; accessible (CTA is a real focusable control, illustration has alt/aria-hidden)

## Usage

Example invocations:

- "/empty-states" — Run the full empty states workflow
- "empty states on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Covers screen-level zero-data UI only; full onboarding flows → see first-use-onboarding.md / onboarding-ux.md [EXPLICIT]
- Copy guidance defers to microcopy-writing.md for tone/voice; this file owns structure + CTA logic [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Loading vs empty ambiguity | Show skeleton while loading; only render empty state after fetch resolves [EXPLICIT] |
| Search/filter returns 0 | Treat as user-cleared, not first-use; offer "clear filters", keep query visible [EXPLICIT] |
| Error masquerading as empty | If fetch failed, show error state with retry — never imply the user has no data [EXPLICIT] |
| Partial permission | Show what's visible + inline note on what's gated and how to request access [EXPLICIT] |
