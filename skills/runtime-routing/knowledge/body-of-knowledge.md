# Runtime Routing — Body of Knowledge

Domain knowledge for deciding *where* an agentic task runs, grounded in repo
evidence rather than assumed runtime features. [DOC]

## 1. Core concepts

- **Runtime** — an execution surface that can carry agentic work: `claude`,
  `codex`, `gemini`, `antigravity`, `vscode`, `local` (CLI + Markdown). [DOC]
- **Capability** — a discrete thing a task needs done: file edits, shell
  validators, `git`/`gh` PR flow, hooks, MCP servers, sub-agents/skill routing,
  multimodal/large-context reasoning, IDE rules, workspace state, local file
  access. [DOC]
- **Permission level** — the blast radius a runtime carries. Lower is safer:
  `local` < repo-CLI (`codex`) < IDE (`vscode`/`antigravity`) < hosted-agentic
  (`claude`) < remote-model (`gemini`). Levels are normalized in
  `assets/runtime-catalog-policy.json`. [CONFIG]
- **Evidence id** — a pointer that grounds a capability claim: a repo file, an
  executed check, current runtime metadata, or explicit user config. [DOC]
- **Capability status** — `supported` (has evidence id) / `pending` (needed but
  unproven) / `unsupported` (known absent). [DOC]

## 2. The central decision rule

> Pick the **lowest-permission runtime that has evidence for every required
> capability.** Ties break toward `local` + Markdown. [INFERENCE]

This single rule subsumes the rubric in `SKILL.md`: each "lean toward" row is a
shortcut for "this capability class is evidenced on that runtime at lower cost."

## 3. Model capability vs repo capability

A frequent error is conflating what a *model* can do with what the *repo* proves.

| Class | Example | Grounding |
|---|---|---|
| Model capability | multimodal input, large-context reasoning | runtime metadata → `[SUPUESTO]` until confirmed |
| Repo capability | a Codex adapter, an MCP config, a passing script | a repo file / executed check → `[DOC]`/`[CONFIG]`/`[CÓDIGO]` |

Only repo capabilities (or executed checks / pinned user config) can promote a
row to `supported`. Model capabilities default to `validation pending`. [DOC]

## 4. Evidence taxonomy (decision rules)

- `[DOC]` — a repo doc/adapter (`AGENTS.md`, `CODEX.md`, `.agent/`). Promotes. [DOC]
- `[CONFIG]` — a config file (MCP server config, settings). Promotes. [CONFIG]
- `[CÓDIGO]` — a script or executed command output. Promotes. [CÓDIGO]
- `[INFERENCE]` — reasoned, not observed. Does **not** promote. [INFERENCE]
- `[SUPUESTO]` — assumption to confirm. Does **not** promote; stays `pending`. [SUPUESTO]

**Rule:** a `supported` row without a promoting evidence id is invalid → downgrade
to `validation pending`. [DOC]

## 5. Standards & invariants (the acceptance gate)

A routing report **fails** if it: [DOC]

1. recommends a runtime with no backing evidence id;
2. cites an unknown / fabricated evidence id;
3. recommends a runtime not in the catalog, or above the needed permission level;
4. hides a validation limit, or omits the local-first fallback;
5. lets Guardian pass while a referenced validation failed.

## 6. Fallback & secret-boundary rules

- Always ship a **local-first fallback**: Markdown-first instructions + repo-local
  scripts, with `Dato requerido` / `validation pending` markers. [DOC]
- If the route uses `gh`/CLI, include the **no-auth path** (local validators +
  Markdown PR body) because auth may fail. [DOC]
- **Never** move local files, workspace state, or secrets outside their local
  boundary; never escalate to a remote runtime for a local-doable task. [DOC]

## 7. Activation boundaries

- Empty / one-word input (`runtime-routing`) → request task type + output surface
  first; do not activate a recommendation. [DOC]
- Runtime-independent task the current tool already handles → routing adds
  ceremony; do not activate. [INFERENCE]
- Out-of-domain request (e.g. "write a thank-you note") → out of activation
  scope. [DOC]

## 8. Deterministic assets (machine-checkable contract)

| Asset | Governs |
|---|---|
| `assets/runtime-routing-contract.json` | route decision schema |
| `assets/runtime-catalog-policy.json` | allowed runtime ids + permission levels |
| `assets/evidence-policy.json` | what may ground a capability claim |
| `assets/capability-matrix-policy.json` | supported / pending / unsupported axes |
| `assets/fallback-policy.json` | required local-first fallback + visible limits |
| `assets/quality-rubric.json` | scored quality criteria for the deliverable |

The tables in `SKILL.md` are the human shortcut; these assets are the source of
truth. If an asset is absent in-repo, honor its rule as a requirement — do not
treat it as present evidence. [SUPUESTO]
