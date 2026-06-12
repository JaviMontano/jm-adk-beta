<!-- distilled from alfa skills/hook-creator -->
<!-- This skill should be used when the user asks to "create a hook", -->
# Hook Creator

Create event-driven hooks — deterministic automation that fires at Claude Code lifecycle points. Hooks are NOT LLM judgment; they're programmatic control. [EXPLICIT]

## Assumptions & Limits

- **Assumes** the behavior should be deterministic and repeatable (for LLM-based judgment, use prompt/agent hook types) [EXPLICIT]
- **Limit**: Hooks run synchronously — long operations block Claude. Keep commands under 10s (configurable via `timeout`) [EXPLICIT]
- **Limit**: Exit code 2 (block) only works on PreToolUse, UserPromptSubmit, TeammateIdle, TaskCompleted. On any other event, exit 2 is treated as a non-blocking error (stderr -> log, action proceeds). [INFERENCIA]
- **Limit**: Multiple hooks on the same event+matcher run in **registration order, sequentially**; the first to exit 2 (on a blocking event) short-circuits the rest. Parallel execution is not guaranteed — never assume one hook sees another's side effects. [SUPUESTO]
- **Trade-off**: Command hooks are fast but brittle (shell parsing); prompt hooks are flexible but add latency (~2s per evaluation); agent hooks are most capable but cost the most tokens and time. [EXPLICIT]

### Anti-scope (out of scope for this skill)

- Authoring the *script* a command hook calls (write it separately; the hook only wires the trigger). [SUPUESTO]
- Secrets management beyond `allowedEnvVars` allow-listing — never inline tokens into `command`/`url`. [DOC]
- Retry/queue semantics: a failed hook does not auto-retry; build idempotency into the command. [INFERENCIA]

### When NOT to create a hook

| Situation | Better alternative | Why |
|---|---|---|
| Complex multi-file analysis | Agent (subagent) | Needs reasoning + tool turns, not a trigger |
| User-invoked workflow | Skill | Hooks fire on lifecycle events, not on demand |
| Always-on response style | Output style | Style is formatting, not an event reaction |
| Project-specific rules | CLAUDE.md | Static guidance, no execution needed |
| Cross-event state machine | Agent + persisted file | Hooks are stateless between fires |

## Usage

```
/hook-creator PostToolUse command    # auto-format on file save
/hook-creator PreToolUse             # interview mode — determine handler type
```

Parse `$1` as event name, `$2` as handler type (default: `command`). If missing, interview: [EXPLICIT]
1. What should happen automatically? (action description)
2. When? (before/after tool use, session start, on stop, etc.)
3. Should it block the action or just react? (blocking = exit 2)

## Before Creating

1. **Read existing hooks**: `Read .claude/settings.json` -> check `hooks` key. Also `Read ~/.claude/settings.json`
2. **Verify event name** against the supported list below
3. **Check for conflicts**: Multiple hooks on same event+matcher can interact unexpectedly

## Event Reference (16 events)

| Event | When | Can Block? | Matcher On | Stdin Fields |
|---|---|---|---|---|
| `PreToolUse` | Before tool executes | Yes | Tool name | tool_name, tool_input |
| `PostToolUse` | After tool succeeds | No | Tool name | tool_name, tool_input, tool_output |
| `PostToolUseFailure` | After tool fails | No | Tool name | tool_name, tool_input, error |
| `UserPromptSubmit` | Before processing user input | Yes | -- | user_prompt |
| `Stop` | Claude finishes responding | No | -- | stop_hook_active |
| `SessionStart` | Session begins/resumes | No | Source | source |
| `SessionEnd` | Session terminates | No | -- | -- |
| `Notification` | Notification sent | No | Type | type, message |
| `SubagentStart` | Subagent spawned | No | -- | agent_name |
| `SubagentStop` | Subagent finished | No | -- | agent_name |
| `PreCompact` | Before context compaction | No | -- | -- |
| `TeammateIdle` | Teammate going idle | Yes | -- | teammate_name |
| `TaskCompleted` | Task marked done | Yes | -- | task_id, task_description |
| `ConfigChange` | Config file changes | No | Source type | config_path |
| `WorktreeCreate` | Worktree created | No | -- | worktree_path |
| `WorktreeRemove` | Worktree removed | No | -- | worktree_path |

SessionStart source values: `startup`, `resume`, `clear`, `compact` [EXPLICIT]
Notification type values: `permission_prompt`, `idle_prompt` [EXPLICIT]

**Event-selection decision rule**: pick the event by *when the side effect must land*, not by what data you want. Format-on-save -> `PostToolUse` (the write already happened). Veto a write -> `PreToolUse` (only place a block reverses it). React to a user's message before Claude reasons -> `UserPromptSubmit`. Notify a human -> `Notification` or `Stop`. Re-seed context after compaction -> `SessionStart` matcher `compact`. [INFERENCIA]

## Handler Types

### Command (fast, deterministic)
```json
{
  "type": "command",
  "command": "npx prettier --write $CLAUDE_TOOL_ARG_file_path",
  "matcher": "Edit|Write",
  "timeout": 10000
}
```
**Stdin**: JSON with event data. **Exit 0**: proceed (stdout -> context). **Exit 2**: block (stderr -> Claude). **Other**: proceed (stderr -> log).
**Choose when**: the decision is a pure function of the stdin payload (path, tool name, regex match) — no judgment, no codebase read. **Worked example** — block writes outside `src/`: `echo "$CLAUDE_TOOL_INPUT" | jq -er '.file_path | startswith("src/")' || (echo 'Writes restricted to src/' >&2; exit 2)`. The `-e` flag makes `jq` exit non-zero on `false`, driving the `||`. **Env injection**: `$CLAUDE_TOOL_ARG_<field>` expands a top-level `tool_input` field; for nested/array fields, parse stdin with `jq` instead. **Failure mode**: an unset `$CLAUDE_TOOL_ARG_*` expands to empty string, silently passing a blank arg downstream — guard with `[ -n "$VAR" ]`. [INFERENCIA]

### Prompt (LLM judgment, single-turn)
```json
{
  "type": "prompt",
  "prompt": "Evaluate if the task is truly complete. Check all requirements are met.",
  "matcher": null
}
```
Returns `{"ok": true/false, "reason": "..."}`. Uses Haiku by default. Good for subjective quality checks. [EXPLICIT]
**Choose when**: the gate is subjective ("is this complete/safe/on-tone") but a single pass with no tool access suffices. **Failure mode**: a vague prompt yields inconsistent verdicts — anchor it to enumerable criteria ("each of: tests named, edge cases listed, no TODO left"). `ok:false` on a blocking event blocks; on a non-blocking event it only surfaces `reason` as context. [INFERENCIA]

### Agent (multi-turn verification)
```json
{
  "type": "agent",
  "prompt": "Read the changed files and verify they pass the test suite. Run tests if needed.",
  "timeout": 60000
}
```
Full subagent with tool access. 60s default timeout, max 50 tool turns. Use when verification needs codebase state. [EXPLICIT]
**Choose when**: the verdict requires reading files or running commands (e.g. "do tests actually pass"). **Failure mode**: hitting the 50-turn or timeout cap returns an indeterminate result — treat indeterminate as non-blocking and log it, never as silent pass. Scope the prompt tightly (name the files/commands) so the agent does not wander and burn turns. [INFERENCIA]

### HTTP (webhook)
```json
{
  "type": "http",
  "url": "https://hooks.example.com/events",
  "headers": { "Authorization": "Bearer ${API_TOKEN}" },
  "allowedEnvVars": ["API_TOKEN"]
}
```
POST event data to endpoint. Cannot be added via `/hooks` menu — requires direct JSON editing. [EXPLICIT]
**Choose when**: an external system (CI, alerting, audit log) must hear about the event; the response is not used to block. **Security**: only env vars listed in `allowedEnvVars` are interpolated into `headers`/`url`; everything else is stripped — this is the boundary that keeps unrelated secrets out of the request. **Failure mode**: a slow/unreachable endpoint blocks Claude until `timeout`; set a low `timeout` and treat the webhook as fire-and-forget, never as a blocking gate. [INFERENCIA]

## Matcher Patterns

Matchers are **regex** applied to the event's matcher field: [EXPLICIT]

| Pattern | Matches | Use Case |
|---|---|---|
| `Edit\|Write` | Edit OR Write | Format-on-save |
| `Bash` | Only Bash | Command auditing |
| `mcp__.*` | Any MCP tool | MCP monitoring |
| `Edit` | Exactly Edit | Targeted formatting |
| `startup` | Session start (not resume) | First-run setup |
| `compact` | After compaction | Re-inject critical context |

## Configuration Scopes

| Scope | File | Shared? | Precedence |
|---|---|---|---|
| Personal | `~/.claude/settings.json` | No | All projects |
| Project shared | `.claude/settings.json` | Yes (git) | This project |
| Project local | `.claude/settings.local.json` | No | This project |
| Plugin | `hooks/hooks.json` | With plugin | Plugin scope |
| Skill/Agent | Frontmatter `hooks:` | With skill | Skill scope |

## Battle-Tested Patterns

### Auto-format on save
```json
{ "PostToolUse": [{ "type": "command", "command": "npx prettier --write $CLAUDE_TOOL_ARG_file_path", "matcher": "Edit|Write" }] }
```

### Block edits to lock files
```json
{ "PreToolUse": [{ "type": "command", "command": "echo $CLAUDE_TOOL_INPUT | jq -r '.file_path' | grep -qE '(package-lock|yarn\\.lock|\\.lock)' && (echo 'Lock files are auto-generated' >&2; exit 2) || exit 0", "matcher": "Edit|Write" }] }
```

### macOS notification on idle
```json
{ "Notification": [{ "type": "command", "command": "osascript -e 'display notification \"Claude needs attention\" with title \"Claude Code\"'", "matcher": "permission_prompt|idle_prompt" }] }
```

### Re-inject context after compaction
```json
{ "SessionStart": [{ "type": "command", "command": "cat .claude/critical-context.md", "matcher": "compact" }] }
```

### Quality gate before task completion
```json
{ "TaskCompleted": [{ "type": "prompt", "prompt": "Verify all acceptance criteria are met. Check that tests pass and no regressions were introduced." }] }
```

## Gotchas & Debugging

| Problem | Cause | Fix |
|---|---|---|
| Stop hook infinite loop | Hook triggers Claude, which triggers Stop again | Check `stop_hook_active` field — if true, exit 0 immediately |
| JSON parse error in stdout | Shell profile `echo` statements pollute output | Guard with `if [[ $- == *i* ]]` |
| Hook doesn't fire | Wrong event name or matcher miss | Debug with `claude --debug` or Ctrl+O verbose mode |
| Hook blocks unexpectedly | Exit code 2 from unexpected path | Test command standalone: `echo '{}' \| your-command` |
| Timeout kills hook | Operation too slow | Increase `timeout` or make command async |

## Validation Gate

- [ ] Event name is one of the 16 supported events
- [ ] Handler type is valid (command, prompt, agent, http)
- [ ] If blocking (exit 2): event supports blocking (PreToolUse, UserPromptSubmit, TeammateIdle, TaskCompleted)
- [ ] Matcher regex is valid (test with `echo "ToolName" | grep -qE 'pattern'`)
- [ ] Command handles JSON stdin correctly (not expecting positional args)
- [ ] No infinite loop risk in Stop hooks (checks stop_hook_active)
- [ ] Timeout appropriate for operation complexity
- [ ] Saved to correct scope file
- [ ] Tested standalone before deployment: `echo '{"tool_name":"Edit"}' | your-command`

## Acceptance Criteria (hook is "done")

- Fires on exactly the intended event+matcher and no broader (verified by triggering an adjacent tool that should NOT match). [EXPLICIT]
- Blocking hooks reverse the action on exit 2 *and* return a human-readable reason on stderr; non-blocking hooks never depend on exit 2 to take effect. [INFERENCIA]
- Idempotent: re-firing on identical input produces identical state (no duplicated appends, no double-format). [SUPUESTO]
- Worst-case latency (slow path / timeout) is bounded and acceptable for the event's frequency. [INFERENCIA]
- Secrets reach the hook only via `allowedEnvVars`; none are inlined. [DOC]
- Stop/SubagentStop hooks cannot self-trigger (guard on `stop_hook_active`). [EXPLICIT]

## Failure Modes (hook-specific)

| Failure | Symptom | Mitigation |
|---|---|---|
| Over-broad matcher | Fires on unrelated tools | Tighten regex; anchor with exact name, not substring |
| Silent empty arg | Command runs with blank `$CLAUDE_TOOL_ARG_*` | Guard `[ -n "$VAR" ]`; prefer `jq` for nested fields |
| Indeterminate prompt/agent | Timeout/turn-cap returns no clear verdict | Treat indeterminate as non-blocking + log; never silent pass |
| Webhook stalls session | Claude hangs to `timeout` | Low `timeout`, fire-and-forget, never blocking |
| Profile noise in stdout | JSON parse error consuming hook output | Guard interactive-only output: `[[ $- == *i* ]]` |

---
**Author:** Javier Montano | **Last updated:** June 11, 2026
