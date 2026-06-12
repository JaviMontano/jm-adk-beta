<!-- distilled from alfa skills/retrospective-facilitation -->
<!-- > -->
# Retrospective Facilitation
> "Method over hacks."
## TL;DR
Facilitate sprint retros, blameless postmortems, and action-item tracking that survives to next sprint. Output = ranked, owned, dated actions — not a vent log. [EXPLICIT]
## Procedure
### Step 1: Discover
- Pull sprint signals before the session: velocity delta, carryover, incident/escalation count, prior retro's open actions. [EXPLICIT]
- Pick a format to fit the trigger: Start/Stop/Continue (default), 4Ls (Liked/Learned/Lacked/Longed-for, low-trust teams), Mad/Sad/Glad (morale), 5-Whys (single incident postmortem). [EXPLICIT]
### Step 2: Analyze
- Set the prime directive aloud: focus on system/process, never persons — blameless. [EXPLICIT]
- Cluster raw notes into themes; dot-vote to rank; spend depth on top 2-3 only. Evaluate options per Constitution XIII/XIV. [EXPLICIT]
- For incidents, drive each thread to a root cause (5-Whys), not the first plausible stop. [EXPLICIT]
### Step 3: Execute
- Convert each chosen theme into a SMART action: owner + due date + done-definition. Cap at 3-5 — more guarantees zero. [EXPLICIT]
- Carry forward unfinished prior actions explicitly; do not silently drop them. Tag each claim with evidence tags. [EXPLICIT]
### Step 4: Validate
- Verify every action has an owner and date; verify prior-retro actions were reviewed. [EXPLICIT]
## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output — every item owned + dated + measurable
- [ ] Blameless framing held; no individual named as a fault
- [ ] Action count <= 5; prior open actions reconciled

## Usage

Example invocations:

- "/retrospective-facilitation" — Run the full retrospective facilitation workflow
- "retrospective facilitation on this project" — Apply to current context

Worked example (Start/Stop/Continue → action):
- Signal: 2 stories carried over, 1 prod hotfix. Theme (dot-voted #1): "PRs sit >1 day." Root cause (5-Whys): no review SLA. Action: "Adopt 4h first-review SLA; @lead adds to DoD by 2026-06-18." [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) and prior-retro actions [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Not for live incident response — runs after stabilization, on the postmortem [EXPLICIT]
- Anti-scope: no individual performance review, no HR/disciplinary output [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Blame surfaces / naming an individual | Reframe to the system/process; restate prime directive |
| No prior actions completed | Surface as the top theme; diagnose why before adding new actions |
| >5 candidate actions | Dot-vote; defer the rest to backlog, don't commit them |
| Same theme recurs across retros | Escalate as systemic; a retro action alone is insufficient |
