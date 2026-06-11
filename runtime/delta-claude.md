## Claude Code delta

Runtime behaviors specific to Claude Code; base ADK runtime applies otherwise. [DOC]

- Hooks (`hooks/hooks.json`) [CONFIG]: session-init, prompt filter, persona calibrate, pre/post tool guards, stop validator. Order is load order; a non-zero pre-tool guard blocks the call, stop validator can veto turn-end. [INFERENCE]
- Skills: auto-discovered from `skills/*/SKILL.md` (missing/malformed frontmatter -> skill skipped, not fatal). MCP via `.mcp.json` (generated; do not hand-edit, regenerate). [CONFIG]
- Subagents: parallel `[P]` tasks via Task tool; read-only agents hint `model: haiku`. [CODE]
- Acceptance: hooks fire in declared order, all skills resolve or are logged-skipped, `.mcp.json` valid, `[P]` tasks run concurrently. [ASSUMPTION]
- Anti-scope: no global Claude config, secrets, or provider/model swap here. [EXPLICIT]
