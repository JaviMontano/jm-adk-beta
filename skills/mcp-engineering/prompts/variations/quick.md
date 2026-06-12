# Quick Variation — mcp-engineering

For a single, well-specified MCP ask. Skip the committee ceremony; deliver fast,
still safe.

## Use when

- One server, one scope already known.
- Env-var name(s) provided.
- No active secret leak.

## Five-step quick path

1. **Scope:** team → `.mcp.json`, personal → `~/.claude.json`. One line of rationale.
2. **Config:** emit the `mcpServers` block with `${ENV_VAR}` — zero literals.
3. **Error contract:** the typed `toolError(category, retryAfter?)` returning
   `isError`, `errorCategory`, `isRetryable`, `retryAfterSeconds`.
4. **Retry loop:** bounded client loop honoring `retryAfterSeconds`, `maxRetries`.
5. **Gate:** run the acceptance checklist; if JSON, pass `scripts/check.sh`.

## Hard stops

- Literal secret requested → refuse.
- Error missing `errorCategory`/`isRetryable` → invalid, do not certify.

Tag every claim. Never green-as-success.
