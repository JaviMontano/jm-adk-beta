## Claude Code delta

Runtime behaviors specific to Claude Code; base ADK runtime applies otherwise. [DOC]

- Hooks (`hooks/hooks.json`) [CONFIG]: session-init, prompt filter, persona calibrate, pre/post tool guards, stop validator. Order is load order; a non-zero pre-tool guard blocks the call, stop validator can veto turn-end. [INFERENCE]
- Skills: auto-discovered from `skills/*/SKILL.md` (missing/malformed frontmatter -> skill skipped, not fatal). MCP via `.mcp.json` (generated; do not hand-edit, regenerate). [CONFIG]
- Subagents: parallel `[P]` tasks via Task tool; read-only agents hint `model: haiku`. [CODE]
- Acceptance: hooks fire in declared order, all skills resolve or are logged-skipped, `.mcp.json` valid, `[P]` tasks run concurrently. [ASSUMPTION]
- Anti-scope: no global Claude config, secrets, or provider/model swap here. [EXPLICIT]

## First-prompt routing (ICM Layer 1, harness-engineering guides+sensors) [DOC]

`scripts/first-prompt-router.sh` (invoked by `session-init.sh`) emits `ROUTE-*`
KEY:VALUE lines. On the **first turn** the model MUST emit, before acting, one
block with these fields: `ENTENDIDO:` (paraphrase), `MODO:` (create_project |
resume_project | new_task | resume_task | ambiguous), `SUPUESTOS:` ([SUPUESTO],
ratio ≤30%), `GAPS:` (coverage_gap; ask blocking datum before editing), `PERFIL:`,
`SKILL/ROUTER candidato:` (from catalog/skills.json), `TAREA PROPUESTA` (3 steps +
done), `GATE:` (validate-coverage | check-token-budget | validate-evals).

- `create_project`/`new_task`: run `scripts/workspace-bootstrap.sh <slug> --apply`
  on user confirm; else propose slug and ask.
- `resume_project`/`resume_task`: read `workspace/<WS_ID>/` `CONTEXT.md` + last
  stage `output/` (anti lost-in-the-middle: load 2-8k tok, not all).
- `ambiguous`: emit `coverage_gap`, ask, do NOT edit.
- `stop-validator.sh` is the SENSOR: vetoes (exit 1) if the transcript lacks the
  block; skips when transcript unreadable or `stop_hook_active`.
- Edit-source: fix routing in `first-prompt-router.sh` / this delta, not outputs.
