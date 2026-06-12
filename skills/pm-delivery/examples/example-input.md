# Example Input — pm-delivery (risk-assessment route)

## User request
"We're migrating our orders service from a monolith to Firebase/Firestore before
the Q3 launch. The migration touches the payments path and a 5-table legacy
Postgres DB. The team is two engineers, one of whom is new. Give me a risk read
before we commit the timeline."

## Available artifacts
- `firestore.rules` (current draft) — line 12 allows writes to `/orders`
  without an auth check. [CONFIG]
- `migration-plan.md` — names 5 Postgres tables, no backup/restore step
  documented. [DOC]
- Team note: "Engineer B joined 3 weeks ago; on-call rotation is a single
  person." [DOC]

## Routing signal
Topic resolves to **risk-assessment** (the user asks for a "risk read"; no other
topic fits). Depth = **deep** (timeline commitment depends on it, so apply all 7
categories). [EXPLICIT]

## What the skill should do
Load only `references/risk-assessment.md`, walk all 7 categories, score
Severity × Likelihood, and name a mitigation for every High/Medium risk, with
evidence tags — without proposing implementation steps (phase separation).
