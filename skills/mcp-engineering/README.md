# mcp-engineering

Configure MCP servers and design typed, machine-readable error contracts so that
clients and models can retry deterministically instead of guessing from prose.

## What it does

Three coupled deliverables:

1. **Scope decision + config** — choose `.mcp.json` (team, versioned) vs
   `~/.claude.json` (personal, out of repo), and emit an `mcpServers` block whose
   credentials are referenced as `${ENV_VAR}` with zero literals.
2. **Typed error contract** — every tool error exposes `isError`, `errorCategory`
   (`auth` / `rate_limit` / `transient` / `fatal`), `isRetryable`, and
   `retryAfterSeconds` when applicable. The model reads fields, never prose.
3. **Client-owned retry policy** — the retry loop lives in client code, bounded by
   `maxRetries`, honoring `retryAfterSeconds`. Backoff is never delegated to the
   model's judgement.

If a secret already leaked into version control, the deliverable also includes a
remediation plan: rotate the credential **and** purge history with
`git filter-repo` — a later `.gitignore` does not erase what is already committed.

## When to use

- Wiring an MCP server for a team and deciding the scope.
- A server returns prose errors (typical 429 / 500) and the model retries blindly.
- A literal token sits in a versioned file and must be rotated + purged.
- Deciding whether a capability should be an MCP server or is already covered by a
  built-in tool (Read / Grep / Bash). MCP only when no built-in applies.

**Anti-scope:** generic prose drafting, local `grep` searches, or any non-integration
task. If the user explicitly asks to keep a literal secret unexpanded, **reject** —
do not emit that config.

## How it routes / executes

`SKILL.md` is the contract. Deterministic validation runs offline against the JSON
policies in `assets/` via `scripts/validate_mcp_engineering.py`; the full smoke is
`scripts/check.sh`, which accepts valid fixtures and rejects invalid mutations.

| Phase | Role | Output |
|---|---|---|
| Orchestrate | `agents/lead.md` | scope decision, deliverable plan |
| Domain depth | `agents/specialist.md` | typed-error contract, scope/secret policy |
| Execution | `agents/support.md` | config block, retry loop, remediation steps |
| Validation | `agents/guardian.md` | gate checklist, deterministic-script result |

## References

- Domain knowledge: `knowledge/body-of-knowledge.md`
- Concept graph: `knowledge/knowledge-graph.json`
- Prompts: `prompts/primary.md`, `prompts/meta.md`,
  `prompts/variations/quick.md`, `prompts/variations/deep.md`
- Deliverable scaffold: `templates/output.md`
- Worked example: `examples/example-input.md`, `examples/example-output.md`
- Asset bundle: `assets/README.md`, `assets/manifest.json`
- Eval suite: `evals/evals.json`

## Evidence taxonomy

Every claim carries a tag: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`.
Never present green as proof of success; certify only against deterministic evidence.
