# firebase — pre-deploy checklist

Run this before declaring any firebase deliverable "done". Tied to the gates in
`assets/quality-rubric.json`.

## Routing
- [ ] Exactly one `topic` resolved; one `references/*.md` playbook read.
- [ ] If ambiguous, asked one question — did not load two routes.

## Firestore & Rules
- [ ] Schema designed for read patterns (denormalized, not SQL-normalized).
- [ ] Every collection AND subcollection has an explicit rule; deny-by-default.
- [ ] Writes validate `request.resource.data.keys()` and types.
- [ ] Immutable fields asserted equal across `resource.data` / `request.resource.data`.
- [ ] `list` rules satisfiable by the real client query.
- [ ] Composite indexes defined for every compound / ordered query.

## Functions
- [ ] Every trigger handler idempotent (processed-marker).
- [ ] No trigger write-loop (self / changed-field guard).
- [ ] Region colocated with Firestore; memory/concurrency right-sized.

## Test & deploy
- [ ] Emulator unit tests cover allow AND deny per path (rules-unit-testing SDK).
- [ ] Deploy via dry-run / preview channel before prod — emulator pass alone is not enough.

## Cost & governance
- [ ] List queries bounded (`limit()` + cursor); persistence enabled; no orphan listeners.
- [ ] Billing alerts at 50/80/100% (+ hard-cap on non-prod).
- [ ] No price quoted — usage / FTE-months estimate with disclaimer.
- [ ] No AWS/Azure/Docker/K8s; single brand; no client PII; every claim evidence-tagged.
