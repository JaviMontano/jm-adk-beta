---
name: session-workspace
version: 1.0.0
description: "Router for agent session lifecycle: bootstrap, protocol, state/context-window management, compaction preservation, notifications, end-cleanup. Topics: context-window-management, notification-handler, pre-compact-context, session-end-cleanup, session-manager, session-protocol, session-start-bootstrap."
params:
  topic:
    enum: [context-window-management, notification-handler, pre-compact-context, session-end-cleanup, session-manager, session-protocol, session-start-bootstrap]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  context-window-management: references/context-window-management.md
  notification-handler: references/notification-handler.md
  pre-compact-context: references/pre-compact-context.md
  session-end-cleanup: references/session-end-cleanup.md
  session-manager: references/session-manager.md
  session-protocol: references/session-protocol.md
  session-start-bootstrap: references/session-start-bootstrap.md
---

# session-workspace

Router skill. Dispatch to EXACTLY ONE playbook; never load the cluster. [DOC]

## When to use
Any session-lifecycle moment: starting/resuming a session, persisting or
priming state, approaching the context limit, handling a notification, or
ending cleanly. If the task is content work (not lifecycle), this is the wrong
skill — anti-scope below. [INFERENCE]

## Routing (topic → playbook)
- **session-start-bootstrap** — cold start: load context, prime, announce stage.
- **session-protocol** — in-session rules of engagement / spine discipline.
- **session-manager** — read/write `.specify/context.json`: stages, artifacts. [CONFIG]
- **context-window-management** — budget tokens; decide trim vs. compact.
- **pre-compact-context** — snapshot state BEFORE compaction so nothing is lost.
- **notification-handler** — route/triage an inbound notification mid-session.
- **session-end-cleanup** — flush state, write handoff, leave a clean tree.
Pick by intent, not keyword overlap; ambiguous → ask one question, don't guess. [INFERENCE]

## Inputs / Outputs
- **In:** `topic` (required); `depth` (quick=essentials | deep=exhaustive + per-step verification). **Out:** whatever the routed playbook produces — this file emits no artifacts. [CONFIG]

## Spine & gates
Discover → Analyze → Execute → Validate. Enforce constitution v6.0.0, evidence
tags (Alfa set, see references/verification-tags.md), and the script-first rule
(prefer existing scripts over ad-hoc commands). [DOC]

## Acceptance criteria
- Exactly one route Read; no sibling playbooks loaded. [INFERENCE]
- `topic` resolved (or one clarifying question asked), `depth` honored.
- Output carries Alfa tags, one family, consistent spelling.
- Gate each dispatch with `assets/quality-rubric.json` + `assets/dispatch-checklist.md`. [CONFIG]

## Anti-scope
No multi-topic merges, no content authoring, no `.specify/context.json` writes
outside the **session-manager** route. If unsure which topic, ask — do not
fan out across playbooks. [ASSUMPTION]