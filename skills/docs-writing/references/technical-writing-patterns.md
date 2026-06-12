<!-- distilled from alfa skills/technical-writing-patterns -->
<!-- > -->
# Technical Writing Patterns
> "Method over hacks."
## TL;DR
Pick the right doc TYPE first (the #1 error is mixing them), then apply its fixed skeleton. Four types, four jobs — never blend them in one page. [EXPLICIT]

## Doc Types (Diátaxis) — choose ONE per page
| Type | Reader's question | Voice | Must NOT contain |
|------|-------------------|-------|------------------|
| Tutorial | "teach me by doing" | "we", imperative | options, edge cases, theory |
| How-to guide | "how do I do X?" | imperative, goal-named | onboarding, concept tangents |
| Reference | "what are the params?" | declarative, terse | opinions, narrative |
| Explanation | "why is it like this?" | discursive | step-by-step commands |
[EXPLICIT] Mixing types is the dominant failure mode: a tutorial that lists every flag overwhelms; a reference that tells a story is unsearchable.

## Procedure
### Step 1: Discover — classify the doc type
- Identify reader, their question, and the ONE type above. If two types fit, split into two pages. [EXPLICIT]
### Step 2: Analyze — apply the skeleton (evaluate options per Constitution XIII/XIV)
- **API endpoint**: signature → params table (name/type/required/default/desc) → minimal request → sample response → errors table (code/meaning/fix) → auth + rate limits.
- **How-to**: goal-named title ("Rotate an API key") → prerequisites → numbered steps (one action each) → verification step → rollback.
- **Tutorial**: promised end-state up front → linear happy path only → every command copy-pasteable → defer all "why" to Explanation.
### Step 3: Execute — write with evidence tags
- Lead with the answer; put context after (inverted pyramid). One idea per paragraph.
- Tag every behavioral claim with this file's convention `[EXPLICIT]` for stated facts vs inferred.
### Step 4: Validate — run the criteria below

## Quality Criteria
- [ ] Doc type is single and declared (Step 1)
- [ ] Constitution-compliant (XIII/XIV)
- [ ] Every code/command block is copy-paste runnable and version-pinned
- [ ] Params/errors shown as tables, not prose
- [ ] Evidence tags applied; no unsourced behavioral claims
- [ ] No second-person mood-shifts mid-page; tense/voice consistent
- [ ] Actionable: reader can act without leaving the page

## Anti-scope (this reference does NOT cover)
- Marketing/landing copy, changelogs (see docs-changelog), or ADRs. [EXPLICIT]
- Visual/diagram standards — out of scope; delegate to a diagramming skill.

## Usage

Example invocations:

- "/technical-writing-patterns" — Run the full technical writing patterns workflow
- "technical writing patterns on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- English output unless otherwise specified; one human-language per page [EXPLICIT]
- Does not replace domain-expert review for correctness of technical claims [EXPLICIT]
- Patterns are English/LTR-oriented; localized docs may need reordering [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Source code and docs disagree | Trust code; tag the doc claim and flag the drift |
| One page tries to be two doc types | Split into separate pages by type (Step 1) |
| Undocumented/private API behavior | State it's unverified; do not present as contract |
