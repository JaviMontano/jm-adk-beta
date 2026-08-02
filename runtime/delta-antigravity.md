## Antigravity delta

Deltas vs baseline harness. Apply only here; do not port to other runtimes. [EXPLICIT]

- No hooks engine [INFERENCE]: run `bash scripts/session-init.sh` at session start — only when state is needed (resume, multi-task, or `[P]` work); skip for one-shot reads. Idempotent; rerun is safe.
- Skill index `.agent/skills_index.json` (generated, minimal fields) [CONFIG]: do not hand-edit — regenerate. MCP config: `~/.gemini/config/mcp_config.json` [CONFIG].
- No subagent dispatch [INFERENCE]: execute `[P]` tasks sequentially in listed order; no parallel fan-out, no nested agents.
- **First-prompt routing** [DOC]: `bash scripts/first-prompt-router.sh` (already run if session-init invoked) emits `ROUTE-*`; emit one `ENTENDIDO/MODO/SUPUESTOS/GAPS/PERFIL/SKILL/TAREA/GATE` block before acting (fields: `runtime/delta-claude.md` § First-prompt routing). No Stop-hook sensor here — enforce manually. `create_project`/`new_task` → `scripts/workspace-bootstrap.sh <slug> --apply`.
- Done = init ran (if required), `[P]` tasks all sequential, no hook/subagent assumptions leaked [ASSUMPTION]. If a step needs a missing engine, stop and flag — never silently emulate. [EXPLICIT]
