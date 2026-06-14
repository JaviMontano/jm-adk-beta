<!-- distilled from alfa skills/file-watcher -->
<!-- > -->
# File Watcher
> "Method over hacks."
## TL;DR
Watch a path set, debounce events, and trigger validation (lint/format/test) on save without re-running on every keystroke. [DOC]

## Scope / Anti-scope
- In: local dev-loop reactions to file changes — lint-on-save, format, fast unit/affected tests, asset rebuilds. [DOC]
- Out: CI pipelines (use the runner's native triggers), production hot-reload, and cross-host sync (a watcher is single-host). [SUPUESTO] — verify by confirming the consumer runs the trigger in CI, not via this watcher.

## Procedure
### Step 1: Discover
- Resolve the watch root and an explicit ignore set (`.git`, `node_modules`, build output, the tool's own artifacts) to prevent self-trigger loops. [CONFIG]
### Step 2: Analyze
- Choose debounce window and event coalescing per Constitution XIII/XIV; pick native FS events over polling unless on a network mount. [INFERENCIA]
### Step 3: Execute
- Run the trigger command on the coalesced change set, tagging output with evidence tags. Serialize runs: never start a second run while one is in flight. [CÓDIGO]
### Step 4: Validate
- Confirm the run reacted to the real change set and that quality criteria below hold. [DOC]

## Decisions & trade-offs
- Debounce 200–400 ms: long enough to coalesce a multi-file save/format, short enough to feel instant. Lower → duplicate runs; higher → laggy feedback. [SUPUESTO] — tune against the editor's save-all latency.
- Native events vs polling: native is cheap and instant but misses some network/container FS changes; fall back to polling (~1 s interval) only when events are unreliable. [INFERENCIA]
- Latest-wins, not queue: while a run is active, collapse incoming events into one pending run rather than queuing each — avoids backlog storms on bulk edits (git checkout, find-replace). [INFERENCIA]

## Quality Criteria
- [ ] Evidence tags applied (Alfa core set, one per non-obvious claim) [DOC]
- [ ] Ignore set excludes VCS, deps, and the watcher's own output (no self-trigger loop) [CONFIG]
- [ ] Runs are debounced and serialized (no overlapping runs) [INFERENCIA]
- [ ] Trigger exit code surfaced; non-zero is visible, not swallowed [CÓDIGO]
- [ ] Constitution-compliant and actionable output

## Usage

Example invocations:

- "/file-watcher" — Run the full file watcher workflow
- "file watcher on this project" — Apply to current context

Minimal config shape (illustrative): [SUPUESTO]
```yaml
watch:   ["src/**", "tests/**"]
ignore:  [".git/**", "node_modules/**", "dist/**"]
debounce_ms: 300
on_change: "make lint test-affected"
```

## Assumptions & Limits
- Assumes a single-host, local filesystem the watcher can subscribe to. [SUPUESTO] — on containers/VMs verify event delivery before relying on native FS events.
- Assumes access to project artifacts (code, docs, configs). [DOC]
- English-language output unless otherwise specified. [DOC]
- Does not replace domain expert judgment for final decisions. [DOC]
- Not a build system: it triggers a command, it does not model a dependency graph — the `on_change` command owns incrementality. [INFERENCIA]

## Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Self-trigger loop (run writes into watched path) | Add output dir to ignore set; if unavoidable, gate on a content hash, not mtime [INFERENCIA] |
| Event storm (bulk edit, branch switch) | Debounce + latest-wins collapse; one run for the whole batch [INFERENCIA] |
| Missed events on network/container FS | Detect via heartbeat; fall back to polling [SUPUESTO] — confirm by diffing watched tree against last-seen state |
| Editor atomic save (write-temp-then-rename) | Watch the rename/move event, not just write, or the save is missed [INFERENCIA] |
| Trigger command hangs | Apply a timeout; kill and report rather than blocking all future runs [INFERENCIA] |
