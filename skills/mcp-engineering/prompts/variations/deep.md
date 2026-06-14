# Deep Variation — mcp-engineering

For multi-server setups, dual-scope configurations, or an active secret leak. Run the
full committee.

## Use when

- Multiple servers, or the same server across both scopes (shadowing).
- A literal secret already reached version control.
- The error taxonomy must be designed from scratch and justified.

## Full path

1. **Lead — scope gate.** Confirm MCP is warranted; rule out built-ins per server.
2. **Specialist — policy design.**
   - Resolve scope per server; document shadowing when a name exists in both.
   - Define the error → retryability mapping for all four categories.
   - Encode edge cases: `rate_limit` without `Retry-After`; `isError` + useful
     `content`; missing env-var fails loud.
3. **Support — emit artifacts.** Config blocks, typed error function, client retry
   loop with `maxRetries`, and — if leaked — the rotation + `git filter-repo` plan.
4. **Guardian — gate + scripts.** Run the acceptance checklist and
   `scripts/check.sh`; the smoke must accept valid fixtures and reject mutations.

## Leak remediation detail

1. Rotate the credential at the provider.
2. Rewrite history (`git filter-repo`) across all affected commits.
3. State that `.gitignore` / `git rm` alone does not purge history.

## Governance

Harness voice; evidence tags; no invented prices; single-brand; no client PII; never
green-as-success.
