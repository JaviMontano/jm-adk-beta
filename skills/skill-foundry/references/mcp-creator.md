<!-- distilled from alfa skills/mcp-creator -->
<!-- Design deterministic MCP server configuration plans with transport, scope, auth, secret, preflight, validation, and rollback controls; validate offline before any live setup. -->
# MCP Creator

## Purpose

Design deterministic Model Context Protocol server configuration plans. The skill produces a validated plan for stdio or HTTP servers, scopes the config, prevents secret leakage, records preflight evidence, and defers live connectivity checks until the user explicitly approves setup. [DOC]

**Anti-scope** — this skill does NOT: spawn or connect to live servers, run OAuth flows, write to `~/.claude.json`/`.mcp.json`, or author the MCP server itself. It emits a *plan + config snippet* the user applies. Server authoring → `mcp-builder`/`build-mcp-server`. [INFERENCIA]

## Deterministic Contract

Use `assets/mcp-config-plan-contract.json` and validate plans with `scripts/validate_mcp_config_plan.py`. [CONFIG] A valid plan must include:

- `server.name` in kebab-case and `name_collision_checked=true`.
- `transport.type` of `stdio` or `http`; never `sse` (deprecated). [DOC]
- Stdio command/args or HTTPS URL according to transport.
- Scope decision: `local`, `project`, `user`, or `plugin`, with tracked-file risk called out.
- Auth policy with `secrets_hardcoded=false` and env-var placeholders for secrets.
- Preflight evidence for existing config review, collision check, and live validation deferral.
- Validation checks for assets, deterministic scripts, quality criteria, transport policy, scope policy, secret policy, preflight, rollback, and evidence.
- Offline validation flags: `offline=true`, `network_required=false`, `deterministic=true`.

**Validator contract** — `scripts/validate_mcp_config_plan.py` exits `0` on a conformant plan, non-zero with a field path on failure. It is offline and idempotent; re-running on an unchanged plan never mutates it. If the script is absent, treat the plan as **unvalidated** and stop — do not hand-wave conformance. [SUPUESTO] (verify: `ls scripts/validate_mcp_config_plan.py`)

## Assumptions & Limits

- **Assumes** the target service exists and is reachable; this skill configures the *connection*, not the server. [SUPUESTO]
- **Limit**: stdio servers run as child processes — they hold resources for the session lifetime. [DOC]
- **Limit**: SSE transport is deprecated — use HTTP for all new remote connections. [DOC]
- **Limit**: OAuth flows require a browser; headless/CI environments need pre-issued tokens in env. [DOC]
- **Limit**: env-var interpolation resolves at config *load*, not per-call — rotating a secret requires a session restart. [INFERENCIA]
- **Trade-off**: Local scope (default) = private but not shared; Project scope = shared but commits config to git. Choosing Project to "help the team" is the most common way secrets leak. [INFERENCIA]

### When NOT to use MCP

| Situation | Better alternative |
|---|---|
| One-off API call | Bash with curl |
| File system operations | Built-in Read/Write/Glob tools |
| Git operations | Built-in Bash with git |
| Static data reference | CLAUDE.md or skill reference files |
| You author the server code | `mcp-builder` / `build-mcp-server` |

Rule of thumb: reach for MCP only when you need a *stateful, multi-call tool surface* the model invokes repeatedly. A single shot is cheaper as Bash. [INFERENCIA]

## Usage

```
/mcp-creator my-database stdio        # local database server
/mcp-creator analytics-api http       # remote API
/mcp-creator project-tools            # interview mode
```

Parse `$1` as server name (kebab-case), `$2` as transport. If missing, ask:
1. What external system? (database, API, file service, custom tool)
2. Local process or remote endpoint?
3. Auth required? (API key, OAuth, none)

**Name normalization**: lowercase, spaces/underscores → hyphens, strip non-`[a-z0-9-]`. Reject empty or collision; do not silently rename past a collision. [INFERENCIA]

## Before Creating (preflight — record as evidence)

1. **Check existing**: `claude mcp list` to see configured servers. [DOC]
2. **Read project MCP**: `Read .mcp.json` if it exists.
3. **Verify no name collision**: names must be unique across ALL scopes (local/project/user/plugin), not just the active one. A collision is resolved by precedence, silently shadowing the loser. [INFERENCIA]

## Transport Types

### stdio (local processes — most common)

```json
{
  "mcpServers": {
    "{name}": {
      "type": "stdio",
      "command": "node",
      "args": ["./mcp-server/index.js"],
      "env": { "DATABASE_URL": "${DATABASE_URL}" }
    }
  }
}
```

**When**: server runs on the same machine — databases, local tools, custom scripts. [DOC]
**Lifecycle**: spawned on first tool use, killed on session end. [DOC]
**Pitfall**: relative `args` paths resolve against the launch cwd, not the config file — prefer `${CLAUDE_PLUGIN_ROOT}` or an absolute path. [INFERENCIA]

### HTTP (remote — recommended for cloud)

```json
{
  "mcpServers": {
    "{name}": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": { "Authorization": "Bearer ${API_TOKEN}" }
    }
  }
}
```

**When**: server is a remote endpoint. Stateless, no process management. [DOC]
**Pitfall**: non-HTTPS `url` is a secret-leak vector for the auth header — reject `http://` for any authenticated server. [INFERENCIA]

## Configuration Scopes

| Scope | Storage | Precedence | Use When |
|---|---|---|---|
| Local | `~/.claude.json` | Highest | Personal, current project |
| Project | `.mcp.json` (git tracked) | Medium | Team-shared servers |
| User | `~/.claude.json` | Lowest | Personal, all projects |
| Plugin | Plugin's `.mcp.json` | Plugin scope | Bundled with plugin |

**Decision logic**: whole team needs it → Project; only you, here → Local; you, everywhere → User; ships with a plugin → Plugin. [DOC]
**Precedence consequence**: a Local entry shadows a Project entry of the same name with no warning. When debugging a "wrong server," check Local first. [INFERENCIA]

## Environment Variables

Use `${VAR}` in command, args, env, url, headers:

```json
{
  "env": {
    "API_KEY": "${MY_API_KEY}",
    "DB_URL": "${DATABASE_URL:-sqlite:///fallback.db}",
    "HOME_DIR": "${HOME}"
  }
}
```

- `${VAR}` — required, fails to load if missing.
- `${VAR:-default}` — optional with fallback.

**Security rule**: NEVER hardcode secrets — always env vars. A literal token in any field (including `url`/`headers`) fails the secret policy check. [DOC]
**Worked example — what NOT to do**: `"Authorization": "Bearer sk-abc123..."` committed via Project scope = credential in git history. Fix: `"Bearer ${API_TOKEN}"` + Local scope, or set the secret in the shell env. [INFERENCIA]

## Common Server Patterns

### PostgreSQL
```json
{
  "mcpServers": {
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    }
  }
}
```

### Filesystem (sandboxed)
```json
{
  "mcpServers": {
    "files": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${PROJECT_DATA_DIR}"]
    }
  }
}
```
Scope the served dir as tightly as possible — the path arg IS the security boundary. [INFERENCIA]

### Custom API with OAuth
```bash
claude mcp add --transport http my-api https://api.example.com/mcp \
  --client-id "${CLIENT_ID}" \
  --client-secret "${CLIENT_SECRET}" \
  --callback-port 3000
```
Then authenticate via `/mcp` in session. Callback port must be free and not firewalled. [DOC]

### Plugin-bundled server
```json
{
  "mcpServers": {
    "my-tool": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/tool.js"]
    }
  }
}
```
`${CLAUDE_PLUGIN_ROOT}` keeps the path portable across install locations. [DOC]

## CLI Quick Reference

```bash
claude mcp add --transport stdio my-db -- node server.js   # Add stdio
claude mcp add --transport http my-api https://url.com      # Add HTTP
claude mcp list                                             # List all
claude mcp remove my-db                                     # Remove (rollback)
```

**Flag order matters**: `--transport`, `--env`, `--scope` go BEFORE the server name. `--` separates name from command/args; everything after `--` is the spawned command, not a flag. [DOC]
**Rollback**: `claude mcp remove {name}` is the one-step undo; pair every `add` in a plan with its removal command as the documented rollback. [INFERENCIA]

## Output Token Limits

| Threshold | Behavior |
|---|---|
| 10,000 tokens | Warning logged |
| 25,000 tokens | Default max (truncated) |
| Custom | `MAX_MCP_OUTPUT_TOKENS=50000` env var |

## MCP Tool Search (auto-discovery)

When MCP tools exceed 10% of context window, Claude auto-enables tool search — loading tool definitions on demand instead of all at once. Control with `ENABLE_TOOL_SEARCH`: `auto` (default), `true`, `false`. [DOC]

## Failure Modes & Edge Cases

| Symptom | Cause | Action |
|---|---|---|
| Server crashes mid-session | Process exit / unhandled error | Claude retries once, then reports. Add a health check in the server. [DOC] |
| "Wrong server" responds | Name shadowed by higher-precedence scope | Inspect Local before Project/User. [INFERENCIA] |
| Tool output silently cut | Exceeds `MAX_MCP_OUTPUT_TOKENS` | Paginate server-side; raise the env var only if justified. [DOC] |
| Config loads but tools absent | Missing/empty env var → load failure | Confirm every `${VAR}` is set in the launch environment. [INFERENCIA] |
| `command not found` on stdio | Binary not on PATH | `which {command}`; use absolute path or `npx -y`. [INFERENCIA] |
| Auth header leaked in git | Literal secret + Project scope | Rotate the secret, move to env + Local scope. [INFERENCIA] |
| Port conflict | Two servers bind the same listener | stdio servers don't share ports unless they bind one explicitly; isolate. [INFERENCIA] |
| Multiple servers, same API | Intentional — distinct auth/rate-limit contexts | Valid; name them by context, not by API. [DOC] |

## Validation Gate (acceptance criteria)

- [ ] Server name is kebab-case and unique across ALL scopes.
- [ ] Transport is `stdio` or `http` (never `sse`).
- [ ] stdio: command resolves (`which {command}`) and is executable.
- [ ] http: URL is valid and `https://` (reject `http://` when auth is present).
- [ ] All secrets use `${ENV_VAR}` syntax; zero literals in any field.
- [ ] Config targets the correct scope; Project scope contains no secrets.
- [ ] Rollback command (`claude mcp remove {name}`) is recorded in the plan.
- [ ] Every `${VAR}` referenced is set in the target environment.
- [ ] Plan passes `scripts/validate_mcp_config_plan.py` (exit 0) with offline flags set.
- [ ] Live connectivity check deferred until the user approves setup.

---
**Author:** Javier Montaño | **Last updated:** 2026-06-11
