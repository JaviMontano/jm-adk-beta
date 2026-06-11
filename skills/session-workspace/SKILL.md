---
name: session-workspace
description: "Agent session lifecycle: bootstrap, protocol, state management, context preservation/compaction, notifications, and clean handoff. Topics: context-window-management, notification-handler, pre-compact-context, session-end-cleanup, session-manager, session-protocol, session-start-bootstrap."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
