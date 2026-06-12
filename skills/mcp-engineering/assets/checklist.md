# Acceptance Checklist — mcp-engineering

Binary gate items consumed by `agents/guardian.md`. A deliverable certifies only when
every required item holds. Evidence tags noted per item.

- [ ] **Scope** resolved: team → `.mcp.json`, personal → `~/.claude.json`. [DOC]
- [ ] **Secrets** referenced as `${ENV_VAR}`; zero literals in versioned files. [CÓDIGO]
- [ ] **Typed error** exposes `isError`, `errorCategory`, `isRetryable`,
      `retryAfterSeconds` when applicable. [CÓDIGO]
- [ ] **Mapping** correct: `auth`=false, `rate_limit`=true, `transient`=true,
      `fatal`=false. [INFERENCIA]
- [ ] **Retry** loop client-owned and bounded by `maxRetries`, not in the model
      prompt. [CÓDIGO]
- [ ] **Leak** (if any): rotate credential + `git filter-repo`; `.gitignore`/`git rm`
      alone rejected. [DOC]
- [ ] **MCP vs built-in**: confirmed no built-in covers the capability. [INFERENCIA]
- [ ] **Evidence**: `scripts/check.sh` accepts valid fixtures, rejects mutations. [CÓDIGO]

Never present green as proof of success — certify only against deterministic evidence.
