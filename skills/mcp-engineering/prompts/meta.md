# Meta Prompt — mcp-engineering

Self-direction layer for the committee. Use before and during the primary flow to
keep scope, safety, and evidence discipline tight.

## Pre-flight reasoning

- **Is this even MCP?** If a built-in tool solves it, do not propose a server.
- **Who inherits?** This single question resolves scope (`.mcp.json` vs
  `~/.claude.json`).
- **Is there a secret in play?** Decide env-var expansion and, if already committed,
  the rotation + history-purge path.
- **Will the model have to guess retries?** If yes, the error contract is incomplete.

## During execution

- Prefer fields over prose: every error is consumed mechanically.
- Keep the retry loop client-owned and bounded; suspect any backoff that lives in a
  prompt.
- Treat shadowing (personal scope overriding repo scope) as a drift risk to document.

## Self-correction triggers

Stop and redo if you observe: a secret-shaped literal in a versioned file; an error
without `errorCategory`/`isRetryable`; backoff logic in prose; an MCP proposal that
skipped the built-in check; or a leak plan limited to `.gitignore` / `git rm`.

## Calibration

- Quick path (`variations/quick.md`): a single, well-specified ask.
- Deep path (`variations/deep.md`): multi-server, both scopes, or active leak.

## Governance

Harness voice; evidence tags on every claim; no invented prices; single-brand; no
client PII; never green-as-success.
