---
name: runtime-routing
version: 1.1.0
description: "Route agentic work across Claude, Codex, Gemini, Antigravity, VS Code, and local adapters, picking the lowest-permission runtime that has evidence for the task and labeling every unverified capability."
owner: "JM Labs"
triggers:
  - runtime-routing
  - codex
  - claude
  - antigravity
  - gemini
  - vscode
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Runtime Routing

Decide *where* a task runs (Claude / Codex / Gemini / Antigravity / VS Code /
local) before it runs, grounded in repo evidence — never in assumed runtime
features. [DOC]

## When To Use

- User asks where to run a piece of work, or names a target runtime/IDE. [DOC]
- A task depends on a runtime-specific capability: hooks, MCP servers,
  multimodal input, local file access, generated adapters, or IDE rules. [DOC]
- Output must stay portable across two or more runtimes. [DOC]
- A required capability is uncertain and the user needs the boundary made
  explicit rather than a guess. [INFERENCE]

## When Not To Use

- The task is runtime-independent and the current tool already does it — routing
  adds ceremony with no decision to make. [INFERENCE]
- The user wants a *guarantee* about a capability that cannot be observed in repo
  evidence or an executed check — route, but label it pending; do not certify. [DOC]

## Inputs

| Input | Why it matters | If missing |
|---|---|---|
| Requested runtime or current IDE | Anchors the candidate set | Infer from repo adapters; else ask [SUPUESTO] |
| Task type + output surface | Maps to required capabilities | `Dato requerido`, stop [DOC] |
| Repo adapter evidence (`AGENTS.md`, `CODEX.md`, `.agent/`, MCP config) | Grounds capability claims | Treat capability as pending [INFERENCE] |
| Required capabilities + validation status | Drives lowest-permission choice | Default to local-first fallback [INFERENCE] |

## Outputs

- One recommended runtime path with the reason it won. [DOC]
- A capability boundary table: supported / pending / unsupported per capability. [DOC]
- A local-first fallback with `Dato requerido` or `validation pending` markers
  wherever evidence is absent. [DOC]

## Runtime Decision Rubric

Pick the **lowest-permission runtime that has evidence for every required
capability**. Ties break toward local + Markdown. [INFERENCE]

| Signal in the task | Lean toward | Reason |
|---|---|---|
| File edits + shell validators + `git`/`gh` PR flow | Codex / local CLI | Repo-local, auditable, lowest blast radius [INFERENCE] |
| IDE-rule or workspace-state dependent | VS Code / Antigravity (if `.agent/` evidence) | Capability is IDE-bound [SUPUESTO] |
| Multimodal / large-context reasoning | Gemini / Claude | Model capability, not repo capability [SUPUESTO] |
| Hooks, MCP, sub-agents, skill routing | Claude | First-class agentic surface [SUPUESTO] |
| No runtime-specific need | Current tool + Markdown | Avoid needless permission escalation [INFERENCE] |

Runtime ids, permission levels, and capability comparisons are governed by the
deterministic assets below; the table is the human-readable shortcut, the assets
are the machine-checkable source of truth. [DOC]

## Workflow

1. **Discover** — Grep/Read repo docs and adapters for runtime evidence; note
   which capabilities have a file or executed check behind them. [DOC]
2. **Analyze** — Apply the rubric; choose the lowest-permission runtime whose
   required capabilities are all evidence-backed. [INFERENCE]
3. **Execute** — Route to the matching doc, command, skill, or script. [DOC]
4. **Validate** — Mark every unverified capability `validation pending`; emit the
   fallback; never invent support to fill a gap. [DOC]

## Deterministic Assets

These JSON policies + validator make the route machine-checkable. They are the
intended contract for this skill; if a file is absent in-repo, treat its rule as
a requirement to honor, not as present evidence. [SUPUESTO]

- `assets/runtime-routing-contract.json` — route decision schema. [SUPUESTO]
- `assets/runtime-catalog-policy.json` — allowed runtime ids + permission levels. [SUPUESTO]
- `assets/evidence-policy.json` — every capability claim must ground in a repo
  file, an executed check, current runtime metadata, or explicit user config. [SUPUESTO]
- `assets/capability-matrix-policy.json` — supported / pending / unsupported axes. [SUPUESTO]
- `assets/fallback-policy.json` — require a local-first fallback + visible limits. [SUPUESTO]

## Offline Validation (Acceptance Gate)

```bash
bash skills/runtime-routing/scripts/check.sh
```

The validator (and the manual gate when the script is absent) **fails** if a
report does any of: [DOC]

- recommends a runtime with no backing evidence id;
- cites an unknown / fabricated evidence id;
- recommends a runtime not in the catalog or above the needed permission level;
- hides a validation limit, or omits the local-first fallback;
- lets Guardian pass while a referenced validation failed.

A report is **done** only when every check above is clean. [INFERENCE]

## Edge Cases & Self-Correction

- **Adapter docs exist but MCP/IDE state is not observable** → route on the docs,
  mark MCP/state `validation pending`, keep the fallback. [DOC]
- **`gh`/CLI auth may fail** → still route, and include the no-auth path
  (local validators + Markdown PR body) in the fallback. [DOC]
- **Empty or one-word input** (`runtime-routing` alone) → do not activate the
  recommendation; request task type + output surface first. [DOC]
- **Self-correction trigger:** if you wrote a capability as "supported" without a
  citable evidence id, downgrade it to `validation pending` before emitting. [INFERENCE]

## Anti-Patterns (do NOT)

- Claim Antigravity / Codex / Claude / Gemini / VS Code support beyond visible
  repo evidence or an executed check. [DOC]
- Escalate to a remote runtime when a local script can do a local-repo task —
  remote raises permission and secret-exposure risk. [INFERENCE]
- Move local files, workspace state, or secrets outside their local boundary. [DOC]
- Green-light Guardian on a failed validation, or auto-fill past a
  `Dato requerido`. [DOC]
- Touch other skills while completing this one (upgrade-safety scope). [DOC]

## Success Criteria

- User gets one concrete runtime recommendation with its reason. [DOC]
- Every unsupported/uncertain capability is labeled `validation pending`. [DOC]
- A local-first fallback exists and secrets stay local. [DOC]
- The offline gate (or its manual equivalent) passes clean. [INFERENCE]

## Fallback

When runtime feature support is unclear, default to Markdown-first instructions
and repo-local scripts; degrade gracefully rather than asserting unverified
runtime behavior. [DOC]

## Examples

- "How should I run this in Codex?" → route to `CODEX.md` + `AGENTS.md`; if a
  needed MCP capability isn't evidenced, mark it pending. [DOC]
- "Prepare for Antigravity" → use `.agent/` adapter evidence; mark runtime
  validation pending where the adapter doesn't prove the capability. [DOC]
- "PR workflow: edits + validators + `gh`" → Codex / local CLI (lowest
  permission, fully auditable); fallback gives the no-`gh`-auth path. [INFERENCE]
- "Claim full Antigravity support, no evidence" → refuse the claim; route with
  `validation pending` and the fallback. [DOC]
