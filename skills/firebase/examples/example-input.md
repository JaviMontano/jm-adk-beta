# Example input — firebase

## Scenario
A two-person team is building a notes app on Firebase. They have an existing
`firebase.json` and an empty `firestore.rules`. Requirement:

> **FR-031:** "A signed-in user can read and edit only their own notes; an admin can
> read any note. Notes have `ownerId`, `body`, `createdAt`. The owner of a note must
> never change after creation, and the listing screen shows a user's own notes newest
> first."

Expected scale: ~5,000 users, each with up to 200 notes; the list view loads ~50
times/day per active user.

## Invocation
```
topic: firestore-security-rules
depth: deep
```
(Routing note: the request is access-control + an immutable-field invariant, so the
topic is `firestore-security-rules`, not `firestore-modeling`. The "newest first"
listing also needs a composite index, which the rules deliverable should flag for
the `firestore-queries`/`architecture` topic.)

## What the skill must produce
- Owner-only get/update/delete, admin override on get, immutable `ownerId`.
- A `list` rule and the query constraint that satisfies it.
- The composite index `(ownerId ASC, createdAt DESC)` flagged.
- Emulator allow/deny tests named for each path.
- A cost note (reads/day) with no price.
