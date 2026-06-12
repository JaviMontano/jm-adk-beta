# Body of Knowledge — mcp-engineering

Domain knowledge for configuring MCP servers and designing typed error contracts.
Evidence tags on every claim.

## 1. Scope: where a server is declared

Two configuration locations with different inheritance: [DOC]

- **`.mcp.json`** at the repo root — versioned, shared. Every teammate who checks out
  the repo inherits the server. Use for capabilities the whole team needs.
- **`~/.claude.json`** in the user home — personal, never committed. Use for
  capabilities only one developer needs (personal API keys, experiments).

**Decision rule:** ask *who must inherit this server?* Team → `.mcp.json`. Just me →
`~/.claude.json`. [DOC]

**Shadowing:** when the same server name exists in both, the personal
`~/.claude.json` overrides the repo `.mcp.json`. Document which wins to avoid silent
configuration drift. [SUPUESTO]

## 2. Secrets: env-var expansion, never literals

Credentials are referenced by `${ENV_VAR}` expansion; the literal value lives only
in the process environment, never in a file. [CÓDIGO]

- Detect literals by shape: `sk-...`, `ghp_...`, long base64 blobs.
- A missing env-var at runtime must **fail loud at startup**, not silently run with
  an empty credential. [INFERENCIA]
- A literal already committed is leaked the moment it lands. Removing it later does
  not un-leak it.

## 3. Leak remediation: rotate + purge history

If a secret reached version control: [DOC]

1. **Rotate** the credential at the provider — the committed value must become
   worthless.
2. **Purge history** with `git filter-repo` (or BFG) to rewrite every commit that
   contained it.
3. `.gitignore` and `git rm` are **insufficient**: they stop future commits but the
   value still lives in historical objects and any clone/fork.

## 4. Typed error contract

Each tool error must be machine-readable, not prose. Required fields: [CÓDIGO]

- `isError: boolean` — authoritative success/failure flag.
- `errorCategory: "auth" | "rate_limit" | "transient" | "fatal"`.
- `isRetryable: boolean` — whether retrying can plausibly succeed.
- `retryAfterSeconds: number | null` — server hint when present.

**Why typed:** the model reads fields and the client decides. A prose error
(`"Something went wrong, please try again"`) forces the model to guess, which means
retrying a `fatal` or abandoning a `transient`. [INFERENCIA]

## 5. Error → retryability mapping (default policy)

The client may harden this but must not relax it. [INFERENCIA]

| `errorCategory` | `isRetryable` | `retryAfterSeconds` | Decision rule |
|---|---|---|---|
| `auth` | `false` | n/a | Bad credential; retry never helps; escalate to rotation. |
| `rate_limit` | `true` | server-provided | Honor `Retry-After`; bounded backoff if absent. |
| `transient` | `true` | `null` → default 1s | Temporary failure; bounded retry. |
| `fatal` | `false` | n/a | Contract/logic error; retry amplifies harm. |

## 6. Client-owned retry loop

The retry policy lives in client code, never in the model's judgement or the prompt.
[CÓDIGO]

- Decide via `isRetryable`; honor `retryAfterSeconds`; fall back to bounded
  exponential backoff.
- Every loop has a hard ceiling (`maxRetries`). Without it, a persistent `transient`
  hangs the agent indefinitely.

## 7. MCP vs built-in

Add an MCP server only when no built-in tool (Read, Grep, Glob, Bash) covers the
capability. A built-in is cheaper, already trusted, and needs no config. [INFERENCIA]

## 8. Standards & references

- Model Context Protocol — tool result schema, `isError` semantics. [DOC]
- HTTP retry semantics — `Retry-After` header for 429 / 503. [DOC]
- `git filter-repo` — supported history-rewrite tool for secret purging. [DOC]

## 9. Decision rules summary

1. Who inherits? → scope.
2. Any literal secret? → `${ENV_VAR}` + (if committed) rotate + `filter-repo`.
3. Does the error carry `errorCategory` + `isRetryable`? → else invalid contract.
4. Is backoff in the client and bounded? → else move it and add `maxRetries`.
5. Does a built-in already solve it? → then no MCP server.
