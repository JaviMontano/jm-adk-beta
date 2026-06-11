## Codex delta

Capabilities the base harness assumes but Codex lacks; each line = gap → workaround → check. [INFERENCE] from Codex runtime constraints.

- **Skill discovery**: no hooks, no native lookup. Skills table is inlined below; on invocation read `skills/<id>/SKILL.md` verbatim before acting. Anti-scope: don't fuzzy-match skill names — exact `<id>` only, else abort. Check: `ls skills/<id>/SKILL.md` resolves.
- **MCP config**: entries generated into `~/.codex/config.toml`. Env vars are NOT expanded there — never inline secrets; launch via `scripts/with-secrets.sh` wrapper. Edge case: missing wrapper or unset var → fail loud, do not run with empty credentials. Check: wrapper exits 0 and required vars are set.
- **Concurrency**: no subagent dispatch. Execute `[P]`-tagged tasks sequentially in listed order (parallelism is an optimization, not a correctness requirement). Trade-off: slower wall-clock, but deterministic and replayable. Acceptance: every `[P]` task ran exactly once, ordered, before declaring done.
