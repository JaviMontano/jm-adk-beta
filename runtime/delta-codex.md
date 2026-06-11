## Codex delta

- No hooks, no native skill discovery: skills table inlined below; read `skills/<id>/SKILL.md` on invocation.
- MCP: `~/.codex/config.toml` (generated entries). Env vars NOT expanded in config — use `scripts/with-secrets.sh` wrapper.
- No subagent dispatch: execute `[P]` tasks sequentially.
