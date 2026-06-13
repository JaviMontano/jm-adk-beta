# Body of Knowledge — session-workspace

Domain knowledge for routing the **agent session lifecycle**. This skill is a
dispatcher: it owns the decision of *which* lifecycle playbook runs, never the
lifecycle work. The seven playbooks below are the domain. [DOC]

## 1. Key concepts

### The session lifecycle (seven moments)
A session passes through distinct moments, each with one owning playbook:

| Moment | Playbook | Core artifact |
|---|---|---|
| Cold start / safe-state check | `session-start-bootstrap` | start packet + `PROCEED/PAUSE/BLOCK` |
| Full init (load→recover→close→next) | `session-protocol` | 4-step protocol report |
| Stage/state tracking | `session-manager` | `.specify/context.json` |
| Token-budget pressure | `context-window-management` | keep/compress/evict plan |
| Snapshot before compaction | `pre-compact-context` | rehydration packet |
| Inbound alert/progress | `notification-handler` | routed, deduped event |
| Clean teardown | `session-end-cleanup` | closeout + handoff |

### Single-route dispatch
The router Reads exactly one `references/<topic>.md`. Loading siblings is the
primary defect class this skill prevents — it wastes context and blurs ownership. [DOC]

### Feature stage chain (owned by session-manager)
`specified → planned → testified → tasks-ready → implementing → complete`.
Stage = the **highest** row whose evidence is present AND every lower row's
evidence is also present (unbroken chain). A higher artifact over a gap does not
advance the stage; it raises a drift `[OPEN]`. Linear/no-skip is deliberate: a
missing artifact maps to exactly one named stage, and `false complete` is worse
than understatement. [DOC]

### Context priority tiers
Two playbooks classify context by retention:
- **context-window-management**: P0 (active instructions/repo state/blockers) ·
  P1 (active task files/edits/skill contract) · P2 (supporting docs) · P3
  (historical/redundant). Compress before evict; **never evict P0**. Ties → higher
  (lower-numbered) tier. [DOC]
- **pre-compact-context**: P0 (hard rules/objective/blockers/next action) · P1
  (impl details/paths/decisions) · P2 (summarizable background) · DROP
  (chatter/disproven). [DOC]

### Notification severity ladder
`info` (log only) · `progress` (throttled stdout, ≥1/2s) · `warn` (stdout+log) ·
`error` (stdout+log+OS notifier) · `action` (OS notifier + block). Dedupe by
stable `event_id`; coalesce `info` into an end-of-step digest. [DOC]

## 2. Standards and invariants

- **Spine**: Discover → Analyze → Execute → Validate, every playbook.
- **Constitution v6.0.0** governance; script-first rule (prefer existing
  `scripts/check.sh` over ad-hoc commands). [DOC]
- **Evidence taxonomy (Alfa core)**: `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]`
  `[ASSUMPTION]` plus closeout-local `[OPEN]`. One tag per claim, weakest
  applicable, one family — never mix the Jarvis `{...}` family. [DOC]
- **Guardian decision** is mandatory output of every lifecycle playbook
  (`PROCEED/PASS/proceed` vs. `PAUSE/BLOCKED/blocked/needs-confirmation/PARTIAL`).
  Green is never the default; an unknown is `[OPEN]`. [DOC]
- **Deterministic gate**: each playbook ships `assets/*.json` policies and a
  `scripts/check.sh` that validates JSON fixtures offline. Asset beats prose on
  conflict. [CONFIG]
- **Write boundary**: only `session-manager` writes `.specify/context.json`,
  `.specify/score-history.json`, `.specify/decisions/DL-NNN.md`. All other
  playbooks are read-only over project state. [CONFIG]

## 3. Decision rules (routing)

1. Intent mentions *writing* `.specify/context.json` or computing feature stage →
   `session-manager` (only writer). [CONFIG]
2. Intent is "is it safe to start writing?" → `session-start-bootstrap`. [INFERENCE]
3. Intent is "run the full cold-start sequence incl. closing old tasks" →
   `session-protocol`. [INFERENCE]
4. Intent mentions token limit / "what to keep before a big task" →
   `context-window-management`. [DOC]
5. Intent is "preserve before compaction/`/clear`/handoff to fresh thread" →
   `pre-compact-context`. [DOC]
6. Intent is routing an alert / suppressing notification noise →
   `notification-handler`. [DOC]
7. Intent is "close the session / write the handoff" → `session-end-cleanup`. [DOC]
8. Two topics fit → ask one clarifying question; never fan out across playbooks. [INFERENCE]

## 4. Anti-patterns

- Loading the whole `references/` cluster "to be safe" — defeats the router. [DOC]
- Keyword-matching `session` to a playbook (e.g. a login-session question) —
  route by *lifecycle intent*, not the word. [INFERENCE]
- Writing `.specify/context.json` from any route except `session-manager`. [CONFIG]
- Emitting a Guardian `proceed/PASS` while a critical field is `[OPEN]`. [DOC]
- Advancing the feature stage more than one step in a single pass. [DOC]
- Echoing secrets/PII into a notification body or rehydration packet. [DOC]
