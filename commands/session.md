---
name: session
description: "Session lifecycle: /session <start|status|end|handoff> — bootstrap, state, cleanup, fork/resume decision"
argument-hint: "<action>"
---
# /session

Wrapper over `skills/session-workspace` router. `start` runs scripts/session-init.sh
(runtimes without hooks run it manually). `end` validates tasklog + timestamps.
`handoff` emits typed summary (resume vs fork vs fresh per session-lifecycle-management).
