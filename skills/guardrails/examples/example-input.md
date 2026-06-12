# Example input — guardrails (pre-tool-use-guard)

A workflow step is about to run a shell command. The orchestrator asks the
guardrails skill to decide whether the call is safe before execution.

## Request

> topic: pre-tool-use-guard
> depth: quick
> Decide allow / approve / block for this proposed tool call.

## Proposed tool call

```json
{
  "tool": "Bash",
  "command": "rm -rf build/ && cat .env",
  "cwd": "/repo",
  "allowed_write_roots": ["build/"]
}
```

## Context

- `.env` holds live credentials and is on the private-path policy. [CONFIG]
- `build/` is a declared write root, so the deletion target is in scope. [CONFIG]
- The command is compound: two segments joined by `&&`. [CODE]

## What the guard must determine

1. Is any segment a destructive or private-path blocker?
2. Does the in-scope `build/` write rescue the whole call? (No — worst segment
   governs.)
3. What exit code accompanies the verdict?
