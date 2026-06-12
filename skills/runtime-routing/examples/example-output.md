# Example Output — Runtime Routing

> Worked answer to `examples/example-input.md` (repo-hardening + PR, secrets present).

**Task:** Apply a 3-file refactor, run lint + unit tests, open a PR; secrets present.
**Requested runtime / current IDE:** VS Code (current), choice open · **Output surface:** PR + passing local validation.

## 1. Recommendation

- **Run on:** `codex` (repo-CLI / local).
- **Permission level:** `repo-cli` — the lowest level that has evidence for every
  required capability.
- **Why it won:** file edits + shell validators + `git`/`gh` PR flow are all
  repo-local and auditable; `AGENTS.md` and `CODEX.md` provide evidence ids for
  each. VS Code/Antigravity would need `.agent/` IDE-rule evidence (absent), and a
  remote runtime would raise permission + secret-exposure risk with no offsetting
  capability gain. [INFERENCE]

## 2. Required capabilities

| # | Capability | Why the task needs it |
|---|---|---|
| 1 | Multi-file edits | The refactor spans three files |
| 2 | Shell validators | Lint + unit tests must prove green |
| 3 | `git`/`gh` PR flow | Output surface is a pull request |
| 4 | Secret-boundary enforcement | Files reference API keys |

## 3. Capability boundary table

| Capability | Runtime | Status | Evidence id | Tag |
|---|---|---|---|---|
| Multi-file edits | codex | `supported` | `CODEX.md` (file-edit flow) | [DOC] |
| Shell validators | codex | `supported` | `AGENTS.md` (lint + test scripts) | [DOC] |
| `git` PR flow | codex | `supported` | `CODEX.md` (git PR flow) | [DOC] |
| `gh` PR creation | codex | `validation pending` | `none` (`gh auth status` not executed) | [SUPUESTO] |
| IDE-rule routing | vscode/antigravity | `unsupported` | `.agent/` absent | [DOC] |
| MCP capability | claude | `validation pending` | `none` (no MCP config) | [SUPUESTO] |

> `gh` PR creation stays `validation pending` because auth was not verified this
> session — it is not promoted to `supported`. [DOC]

## 4. Local-first fallback

- **Markdown-first path:** apply edits and run the documented lint + test scripts
  locally; capture results in the report. [DOC]
- **Repo-local scripts:** the lint + unit-test scripts named in `AGENTS.md`. [DOC]
- **No-`gh`-auth path:** if `gh auth status` fails, skip the API PR; emit a
  Markdown PR body (title, summary, validation output) for manual paste. [DOC]
- **Secret boundary:** all three files and any keys stay local; nothing is sent to
  a remote runtime. [DOC]
- **Open markers:** `validation pending: gh PR creation (auth unverified)`. [DOC]

## 5. Offline gate

```bash
bash skills/runtime-routing/scripts/check.sh
```

- Gate result: `pass` — recommended runtime is catalog-listed and evidence-backed,
  fallback present, the one pending capability is visible, no failed validation is
  hidden. [INFERENCE]

## 6. Guardian sign-off

- [x] Every `supported` row cites a real evidence id (`AGENTS.md` / `CODEX.md`). [DOC]
- [x] `codex` is the lowest-permission evidence-backed survivor. [INFERENCE]
- [x] `codex` is in the catalog and not above the needed permission level. [CONFIG]
- [x] Fallback present with no-`gh`-auth path; the `gh` limit is visible. [DOC]
- [x] No referenced validation failed; secrets stayed local. [DOC]
