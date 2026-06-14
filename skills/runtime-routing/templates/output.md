# Runtime Routing Report

**Task:** <one-line description of the work to be routed>
**Requested runtime / current IDE:** <runtime or "none stated"> · **Output surface:** <surface>

> If task type or output surface is missing, replace this report with
> `Dato requerido: <what is missing>` and stop. [DOC]

## 1. Recommendation

- **Run on:** `<claude | codex | gemini | antigravity | vscode | local>`
- **Permission level:** `<local | repo-cli | ide | hosted-agentic | remote-model>`
- **Why it won:** <lowest-permission runtime with evidence for every required
  capability; tie broken toward local + Markdown> [INFERENCE]

## 2. Required capabilities

| # | Capability | Why the task needs it |
|---|---|---|
| 1 | <e.g. shell validators> | <reason> |
| 2 | <e.g. gh PR flow> | <reason> |

## 3. Capability boundary table

| Capability | Runtime | Status | Evidence id | Tag |
|---|---|---|---|---|
| <capability> | <runtime> | `supported` | `<file / executed check / metadata / user config>` | [DOC]/[CONFIG]/[CÓDIGO] |
| <capability> | <runtime> | `validation pending` | `none` | [SUPUESTO]/[INFERENCE] |
| <capability> | <runtime> | `unsupported` | `<absence evidence>` | [DOC] |

> Every `supported` row MUST carry a promoting evidence id. Any row without one
> is downgraded to `validation pending`. [DOC]

## 4. Local-first fallback

- **Markdown-first path:** <repo-local instructions that need no remote runtime> [DOC]
- **Repo-local scripts:** <which scripts run the task / validators locally> [DOC]
- **No-`gh`-auth path:** <local validators + Markdown PR body if `gh` auth fails> [DOC]
- **Secret boundary:** local files, workspace state, and secrets stay local. [DOC]
- **Open markers:** `Dato requerido: …` / `validation pending: …` <list> [DOC]

## 5. Offline gate

```bash
bash skills/runtime-routing/scripts/check.sh
```

- Gate result: `<pass | fail>` — must be clean before this report is "done". [INFERENCE]

## 6. Guardian sign-off

- [ ] Every `supported` row has a citable evidence id. [DOC]
- [ ] Recommended runtime is lowest-permission among evidence-backed survivors. [INFERENCE]
- [ ] Runtime is in `assets/runtime-catalog-policy.json` and not above needed level. [CONFIG]
- [ ] Fallback present with no-auth path; no hidden limit. [DOC]
- [ ] No referenced validation failed; secrets stayed local. [DOC]
