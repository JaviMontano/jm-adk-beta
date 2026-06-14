# MCP Engineering Report — billing

> Evidence-tagged. Green is not certified until `scripts/check.sh` accepts the JSON.

## 1. Scope decision

- **Who inherits this server:** team (every teammate via the repo)
- **Resolved location:** `.mcp.json` (versioned at repo root) [DOC]
- **Rationale:** the whole team needs `billing`, so it is shared and versioned, not
  personal. [DOC]
- **Shadowing note:** if a dev also defines `billing` in `~/.claude.json`, the
  personal entry wins; document this to avoid drift. [SUPUESTO]

## 2. Configuration block

```jsonc
{
  "mcpServers": {
    "billing": {
      "command": "node",
      "args": ["./servers/billing/index.js"],
      "env": { "BILLING_API_KEY": "${BILLING_API_KEY}" }
    }
  }
}
```

- Literal-secret scan: PASS — zero literals; credential resolved from environment. [CÓDIGO]
- Missing `BILLING_API_KEY` at runtime must fail loud at startup, not run empty. [INFERENCIA]

## 3. Typed error contract

| `errorCategory` | `isRetryable` | `retryAfterSeconds` | Notes |
|---|---|---|---|
| `auth` | `false` | n/a | Bad credential → escalate to rotation, never retry. |
| `rate_limit` | `true` | from `Retry-After` | 429: honor the header; backoff if absent. |
| `transient` | `true` | `null` → 1s default | Network/500 blip: bounded retry. |
| `fatal` | `false` | n/a | Contract/logic error: retry amplifies harm. |

```ts
type ErrorCategory = "auth" | "rate_limit" | "transient" | "fatal";

function toolError(category: ErrorCategory, retryAfter?: number) {
  return {
    isError: true,
    errorCategory: category,
    isRetryable: category === "rate_limit" || category === "transient",
    retryAfterSeconds: retryAfter ?? null
  };
}
```

The original 500 was mislabeled: a true server contract error is `fatal`
(not retryable); a transient network 500 is `transient`. The server must classify,
not the model. [CÓDIGO]

## 4. Client-owned retry policy

```ts
async function callTool(req: Req, maxRetries = 3) {
  for (let attempt = 0; ; attempt++) {
    const res = await invoke(req);
    if (!res.isError || !res.isRetryable || attempt >= maxRetries) return res;
    await sleep((res.retryAfterSeconds ?? 2 ** attempt) * 1000); // bounded, client-owned
  }
}
```

- `maxRetries = 3`; honors `retryAfterSeconds`; exponential fallback. [CÓDIGO]
- Loop lives in client code, never in the model prompt. [CÓDIGO]

## 5. Leak remediation (if applicable)

No secret has leaked: the key was always an env-var. **If one ever does:** [DOC]

- [ ] Rotate `BILLING_API_KEY` at the provider.
- [ ] Purge history with `git filter-repo` across all affected commits.
- [ ] Note that `.gitignore` / `git rm` alone does not purge history.

## 6. MCP vs built-in justification

- Built-in considered: none — billing requires an external API call no built-in
  covers.
- Verdict: MCP warranted. [INFERENCIA]

## 7. Acceptance gate

- [x] Correct scope (`.mcp.json`, team) [DOC]
- [x] `${ENV}` credential, zero literals [CÓDIGO]
- [x] `errorCategory` + `isRetryable` on every error [CÓDIGO]
- [x] Client retry bounded by `maxRetries = 3` [CÓDIGO]
- [x] Leak path documented (rotate + `filter-repo`) [DOC]
- [ ] `scripts/check.sh` to be run as the certifying evidence [CÓDIGO]

## 8. Evidence

Run `scripts/check.sh` against this report's JSON; certify only when it accepts the
valid fixture and rejects mutated ones. [CÓDIGO]
