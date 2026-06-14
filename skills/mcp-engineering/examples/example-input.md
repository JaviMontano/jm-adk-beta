# Example Input — mcp-engineering

## Scenario

Our team runs a `billing` MCP server (a Node process at
`./servers/billing/index.js`). We want every teammate to inherit it from the repo,
so the credential must come from the `BILLING_API_KEY` environment variable — no
literal in the file.

The current server returns HTTP-style failures as plain prose
(`"Something went wrong, please try again"`) for 429 rate limits and 500 errors, so
the agent retries blindly: it hammers a `fatal` 500 and sometimes gives up on a
`transient` network blip.

## What we need

1. The versionable `.mcp.json` block with `${BILLING_API_KEY}` and zero literals.
2. A typed error contract covering `auth`, `rate_limit`, `transient`, `fatal` with
   `isRetryable` and `retryAfterSeconds`.
3. A client-owned retry loop bounded at `maxRetries = 3` that honors
   `retryAfterSeconds`.
4. Confirmation that, since no secret has leaked yet, no history purge is required —
   but tell us what to do if one ever does.

## Constraints

- Team-shared scope (not personal).
- Env-var name only; do not ask for or embed the key value.
- The retry decision must be readable from fields, not inferred from prose.
