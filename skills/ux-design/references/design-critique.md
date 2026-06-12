<!-- distilled from alfa skills/design-critique -->
<!-- > -->
# Design Critique
> "Method over hacks."
## TL;DR
Structured design review: heuristic evaluation, severity rating, and feedback framed as
observation → impact → suggestion. Critique the artifact, never the author. [EXPLICIT]
## Scope
In: a concrete artifact (screen, component, flow, copy, prototype) plus its user goal and
context. Out: a prioritized, evidence-tagged issue list with severities and fixes. [INFERENCIA]
Not: visual brand identity, code review, or product strategy — route to the sibling skill. [INFERENCIA]
## Procedure
### Step 1: Discover
- Capture the user goal, primary task, audience, device/context, and success metric. Without a
  goal, every critique is opinion — request it before proceeding. [EXPLICIT]
- Ask which decisions are still open vs. locked, so feedback lands where it can act. [INFERENCIA]
### Step 2: Analyze — heuristic pass
Walk the artifact against Nielsen's 10 heuristics, scoped to what's on screen: [EXPLICIT]
visibility of state · match to real world · user control/undo · consistency · error prevention ·
recognition over recall · flexibility · minimalist aesthetic · error recovery · help. [EXPLICIT]
For each finding record: location, heuristic violated, and the user consequence (not your taste). [INFERENCIA]
### Step 3: Execute — frame + rate
- Frame every item: **observation** (what, neutrally) → **impact** (cost to the user/task) →
  **suggestion** (one concrete direction, not a mandate). [EXPLICIT]
- Rate severity to force prioritization: **Blocker** (task fails) · **Major** (task succeeds but
  costly/confusing) · **Minor** (polish) · **Nit** (preference, optional). [INFERENCIA]
- Lead with strengths worth keeping, then order issues by severity, not reading order. [INFERENCIA]
### Step 4: Validate
- Each issue is goal-linked, severity-rated, and actionable; drop any item you cannot tie to user
  impact (that's preference, label it Nit or cut it). [EXPLICIT]
- Confirm severities are calibrated against each other, not inflated. [INFERENCIA]
## Severity rubric (worked example)
| Finding | Severity | Why |
|---------|----------|-----|
| Submit button has no loading/disabled state → double-submit | Blocker | Corrupts data; task fails [INFERENCIA] |
| Primary action and "Cancel" are equal weight | Major | Slows every user; misclick risk [INFERENCIA] |
| Inconsistent label casing across the form | Minor | Reads unpolished, task still completes [INFERENCIA] |
| Prefers 8px over 12px gutter | Nit | Pure preference; defer to owner [SUPUESTO] |
## Quality Criteria
- [ ] Evidence tags applied; every issue tied to user impact, not taste
- [ ] Constitution-compliant; critiques the artifact, not the person
- [ ] Each item severity-rated and ordered by severity
- [ ] Observation → impact → suggestion framing on every item
- [ ] At least one strength named before issues

## Usage

Example invocations:

- "/design-critique" — Run the full design critique workflow
- "design critique on this project" — Apply to current context

## Anti-scope

- Not a redesign: propose directions, do not produce the final solution unless asked. [EXPLICIT]
- Not code review or brand/visual-identity review — sibling skills own those. [INFERENCIA]
- Not a gate: critique informs the owner's decision; it does not approve or block ship. [SUPUESTO]

## Failure modes

- Bikeshedding: piling Nits while a Blocker hides — always severity-sort first. [INFERENCIA]
- Taste-as-fact: "I'd make it blue" with no user impact — cut or label Nit. [EXPLICIT]
- Author defensiveness: triggered by person-directed phrasing — keep it artifact-directed. [INFERENCIA]

## Assumptions & Limits

- Assumes the user goal and context are supplied or recoverable; otherwise stop and ask. [EXPLICIT]
- Heuristic eval surfaces likely issues, not measured ones — confirm Blockers with usability
  testing or analytics before treating them as proven. [SUPUESTO]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace usability testing or domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No stated user goal | Request it; critique without a goal is opinion, not review |
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Only positives requested | Still flag any Blocker — silent on task-breaking issues is malpractice |
| Out-of-scope request | Redirect to appropriate skill or escalate |
