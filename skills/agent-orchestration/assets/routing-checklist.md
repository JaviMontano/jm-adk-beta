# Routing checklist — agent-orchestration

Run top to bottom before emitting any dispatch packet. [DOC]

## Resolve
- [ ] Request mapped to exactly one of the 10 enum topics (narrowest match).
- [ ] If two routes genuinely tie → one clarifying question asked, not guessed.
- [ ] Topic is in the enum (no invented topic).
- [ ] Confirmed this is orchestration, not a single-agent / content / domain task.

## Load
- [ ] Exactly one `references/<topic>.md` loaded — not the cluster.
- [ ] `depth` set (quick default / deep on request).

## Run spine
- [ ] Discover: required inputs gathered; gaps marked `[OPEN]`, never auto-filled.
- [ ] Analyze: policy applied; chosen option + rejected trade-off recorded.
- [ ] Execute: deliverable shaped from `templates/output.md`; deterministic
      script run where available (script-first).
- [ ] Validate: Guardian checklist run.

## Gate
- [ ] Constitution v6.0.0 enforced.
- [ ] Evidence tags present, single core-set family, EN/ES consistent.
- [ ] No gate reported "passed" before the Guardian pass.
- [ ] Resumable/recovery topics carry state + ordering invariants.
- [ ] No invented prices, no client PII, single brand.

## Verdict
- [ ] PASS / PARTIAL / BLOCK emitted with the first failing item cited on non-PASS.
