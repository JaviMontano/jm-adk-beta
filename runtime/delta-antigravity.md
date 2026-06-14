## Antigravity delta

Deltas vs baseline harness. Apply only here; do not port to other runtimes. [EXPLICIT]

- No hooks engine [INFERENCE]: run `bash scripts/session-init.sh` at session start — only when state is needed (resume, multi-task, or `[P]` work); skip for one-shot reads. Idempotent; rerun is safe.
- Skill index `.agent/skills_index.json` (generated, minimal fields) [CONFIG]: do not hand-edit — regenerate. MCP config: `~/.gemini/config/mcp_config.json` [CONFIG].
- No subagent dispatch [INFERENCE]: execute `[P]` tasks sequentially in listed order; no parallel fan-out, no nested agents.
- Done = init ran (if required), `[P]` tasks all sequential, no hook/subagent assumptions leaked [ASSUMPTION]. If a step needs a missing engine, stop and flag — never silently emulate. [EXPLICIT]
