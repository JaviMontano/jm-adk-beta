# Example output — session-workspace

Dispatch decision produced for the input in `example-input.md`.

---

# Dispatch Decision — session-workspace

## 1. Request
- **Lifecycle moment:** Preserve in-flight fix state before imminent
  auto-compaction so the next session resumes without loss. [INFERENCE]
- **Repo / branch / brand:** `jm-adk-beta` @ `fix/auth-flake` · JM Labs [CONFIG]

## 2. Topic resolution
- **Resolved topic:** `pre-compact-context` [INFERENCE]
- **Discriminator applied:** the trigger is an *imminent compaction* on
  *unfinished* work — preserve-across-boundary, not session teardown. [DOC]
- **Rejected candidates:**
  - `session-end-cleanup` — excluded: the session is NOT finishing; the fix is
    mid-flight and must survive a compaction, not be closed out. [DOC]
  - `session-manager` — excluded: no request to write `.specify/context.json`
    stage; this is a rehydration packet, not a stage update. [CONFIG]
  - `context-window-management` — excluded: the user wants *preservation before
    compaction*, not a keep/compress/evict budget plan. [INFERENCE]
- **Clarifying question asked:** none — the "before it compacts" + "mid-fix"
  signals resolve to exactly one topic. [INFERENCE]

## 3. Depth
- **depth:** `deep` [CONFIG]
- **Effect:** exhaustive packet + per-step verification; warranted because an
  active blocker (CI red on `test_login_retry`) and PR #214 state must survive
  verbatim — a quick pass risks dropping a P0 item. [INFERENCE]

## 4. Route loaded
- **Single route Read:** `references/pre-compact-context.md` [CONFIG]
- **Siblings deliberately NOT loaded:** session-start-bootstrap, session-protocol,
  session-manager, context-window-management, notification-handler,
  session-end-cleanup. [CONFIG]
- **Playbook deterministic resources surfaced:** `assets/retention-policy.json`,
  `assets/output-contract.json`, `assets/compaction-risk-policy.json`,
  `scripts/check.sh`. [CONFIG]

## 5. Anti-scope check
- [x] No content authoring done by the router. [INFERENCE]
- [x] No `.specify/context.json` write outside the `session-manager` route. [CONFIG]
- [x] No multi-topic merge / fan-out. [INFERENCE]

## 6. Guardian decision
- **Decision:** `proceed` [DOC]
- **Rationale:** one route Read, topic unambiguous, `depth=deep` honored,
  anti-scope clean, tags single-family. [DOC]

## 7. Handoff
- **Next action (handed to the playbook):** build the rehydration packet —
  preserve verbatim P0 (objective "fix flaky auth test"; branch `fix/auth-flake`;
  PR #214 OPEN; CI red on `test_login_retry`); include the resume first-action and
  a Guardian gate that blocks compaction if any P0 item lacks a source. [DOC]
