---
name: session
description: "Session lifecycle: /session <start|status|end|handoff> — bootstrap, state, cleanup, fork/resume decision"
argument-hint: "<action>"
---
# /session

Thin wrapper over the `skills/session-workspace` router. [DOC] Dispatches `$1` to one action; no action → print this help.

| Action | Does | Acceptance |
|---|---|---|
| `start` | Runs `scripts/session-init.sh`. [CODE] | Workspace + tasklog scaffolded; exit 0. |
| `status` | Reports active session state from tasklog. [INFERENCE] | Prints session id, open tasks, last timestamp. |
| `end` | Validates tasklog entries + timestamps, then cleans up. [DOC] | Fails closed if a task lacks a close timestamp. |
| `handoff` | Emits typed summary: resume \| fork \| fresh, per `session-lifecycle-management`. [DOC] | Exactly one type emitted with rationale. |

- Hookless runtimes: run `session-init.sh` manually before `start`. [ASSUMPTION]
- Anti-scope: no git/PR ops, no cross-session merge — handoff only decides, never mutates prior sessions. [INFERENCE]
- Edge: unknown action → list valid actions, exit non-zero; never silently no-op. [ASSUMPTION]
