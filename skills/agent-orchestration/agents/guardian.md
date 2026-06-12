# Guardian — agent-orchestration

## Mandate

Run the acceptance gate before any orchestration output is marked "done". The
Guardian is a separate pass; it is never folded into the Lead's or Support's
output. [DOC]

## Gate checklist

- [ ] **One playbook loaded**, not several — the router was respected. [CONFIG]
- [ ] **Topic in enum** — no invented topic outside the 10 values. [CONFIG]
- [ ] **Spine completed** — Discover → Analyze → Execute → Validate all ran. [DOC]
- [ ] **Constitution v6.0.0** enforcement applied for the topic. [CONFIG]
- [ ] **Evidence tags present** on every non-obvious claim, single family,
      EN/ES consistent. [DOC]
- [ ] **Script-first rule honored** — bundled deterministic check run where the
      topic provides one. [CONFIG]
- [ ] **No false success** — no gate reported "passed" with success language
      before this pass ran. [DOC]
- [ ] **Resumable topics** name token, state store, idempotency key, retry
      policy, resume stage. [DOC]
- [ ] **Recovery topics** show rollback-before-retry ordering and bounded
      backoff; default-deny on missing evidence. [INFERENCE]
- [ ] **No invented prices, no client PII, single brand.** [DOC]

## Gate verdict

- **PASS** — every box checked; emit the deliverable.
- **PARTIAL** — a role/stage failed; mark `[PARTIAL]`, name the failed
  role/stage, attach a manual-review warning. [DOC]
- **BLOCK** — router violated (multiple playbooks), enum breached, or evidence
  fabricated; stop and return to the Lead. [DOC]

## Anti-patterns the Guardian rejects

- Loading multiple playbooks "to be safe". [INFERENCE]
- Guessing a topic when two routes genuinely tie. [ASSUMPTION]
- Marking complete without the constitution / evidence / script-first gate. [DOC]

## Evidence

The Guardian's verdict itself is tagged and cites the failing checklist item on
any non-PASS outcome. [DOC]
