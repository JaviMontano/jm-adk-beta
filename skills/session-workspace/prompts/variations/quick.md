# Quick variation — fast dispatch (depth=quick)

Single-pass routing for an unambiguous lifecycle request. Essentials only.

1. Name the lifecycle moment in one line.
2. Pick the topic with the matching discriminator:
   - write/compute stage → `session-manager`
   - safe-to-start check → `session-start-bootstrap`
   - full cold-start init → `session-protocol`
   - token pressure → `context-window-management`
   - preserve before compaction → `pre-compact-context`
   - route an alert → `notification-handler`
   - close + handoff → `session-end-cleanup`
3. Read that ONE `references/<topic>.md` (path from `routes.json`); pass
   `depth=quick`.
4. Emit: `topic` + route path + Guardian `proceed` — each with an Alfa-core tag.

If two topics fit, do NOT use this variation — ask one clarifying question first.
No sibling routes, no content authoring, no `.specify` writes from the router. [DOC]
