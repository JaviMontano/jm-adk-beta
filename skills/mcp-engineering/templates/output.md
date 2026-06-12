# MCP Engineering Report — <server-name>

> Tag every claim: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`.
> Never present green as proof of success.

## 1. Scope decision

- **Who inherits this server:** <team | personal>
- **Resolved location:** `<.mcp.json | ~/.claude.json>`
- **Rationale:** <one line> [DOC]
- **Shadowing note (if same server in both scopes):** <which wins> [SUPUESTO]

## 2. Configuration block

```jsonc
{
  "mcpServers": {
    "<server-name>": {
      "command": "<command>",
      "args": [<args>],
      "env": { "<ENV_VAR>": "${<ENV_VAR>}" }
    }
  }
}
```

- Literal-secret scan: <PASS — zero literals | FAIL — found ...> [CÓDIGO]

## 3. Typed error contract

| `errorCategory` | `isRetryable` | `retryAfterSeconds` | Notes |
|---|---|---|---|
| `auth` | `false` | n/a | |
| `rate_limit` | `true` | server-provided | |
| `transient` | `true` | `null` → default 1s | |
| `fatal` | `false` | n/a | |

```ts
function toolError(category, retryAfter) {
  return {
    isError: true,
    errorCategory: category,
    isRetryable: category === "rate_limit" || category === "transient",
    retryAfterSeconds: retryAfter ?? null
  };
}
```

## 4. Client-owned retry policy

- `maxRetries`: <n>
- Honors `retryAfterSeconds`: <yes>
- Backoff fallback: bounded exponential
- Loop location: client code (not the model prompt) [CÓDIGO]

## 5. Leak remediation (if applicable)

- [ ] Credential rotated at provider [DOC]
- [ ] History purged via `git filter-repo` [DOC]
- [ ] Confirmed `.gitignore` / `git rm` alone is insufficient [DOC]

## 6. MCP vs built-in justification

- Built-in considered: <Read | Grep | Bash | none applies>
- Verdict: <MCP warranted because ... | revert to built-in> [INFERENCIA]

## 7. Acceptance gate

- [ ] Correct scope [DOC]
- [ ] `${ENV}` credentials, zero literals [CÓDIGO]
- [ ] `errorCategory` + `isRetryable` on every error [CÓDIGO]
- [ ] Client retry bounded by `maxRetries` [CÓDIGO]
- [ ] Leak: rotate + `filter-repo` if applicable [DOC]
- [ ] `scripts/check.sh` accepts deliverable when evidence required [CÓDIGO]

## 8. Evidence

- Deterministic check command + result: `<scripts/check.sh output>` [CÓDIGO]
