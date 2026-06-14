## Codex delta

Gaps the harness assumes but Codex lacks; each = gap → workaround → check. [INFERENCE]

- **Skill discovery**: no hooks, no native lookup. Skills table inlined below; on invoke read `skills/<id>/SKILL.md` verbatim first. Exact `<id>` only — no fuzzy-match, else abort. Check: `ls skills/<id>/SKILL.md` resolves.
- **MCP config**: generated into `~/.codex/config.toml`. Env vars NOT expanded — never inline secrets; launch via `scripts/with-secrets.sh`. Missing wrapper or unset var → fail loud, never run with empty creds. Check: wrapper exits 0, vars set.
- **Concurrency**: no subagent dispatch. Run `[P]` tasks sequentially in listed order (parallelism is an optimization, not correctness). Check: every `[P]` task ran once, ordered, before declaring done.
