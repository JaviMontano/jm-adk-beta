# google-workspace — README

Router skill for Google APIs / Google Workspace work. One request, one topic,
one playbook. This skill does not call Google, OAuth, HTTP, or MCP endpoints —
it resolves the right reference and compiles an offline, evidence-tagged plan or
checklist that a human reviews before any live mutation. [DOC]

## What it does

Given a Google-surface request, `google-workspace` selects exactly one of ten
topic playbooks under `references/` and loads it. Each playbook is a distilled
"alfa" skill covering least-privilege scopes, official REST/MCP operation
mapping, read-only-first discovery, retry/idempotency policy, secrets policy,
and a human-confirmation gate before mutations. [DOC]

## When to use

- A request touches a single Google surface — Sheets, Docs, Slides, Drive,
  Calendar, Maps, or GA4/Analytics. [INFERENCE]
- A request spans two or more Google services and needs an auth/scope/quota/
  retry integration plan. [DOC]
- If no Google surface is involved, decline. [INFERENCE]

## How it routes

Resolve `topic` from the request, then Read EXACTLY ONE route from `routes.json`.
Never load the whole cluster. [DOC]

| topic | playbook | surface |
|---|---|---|
| `analytics-implementation` | `references/analytics-implementation.md` | GA4/Firebase/BigQuery/Looker setup [EXPLICIT] |
| `apis` | `references/apis.md` | cross-service Workspace automation (Gmail/Cal/Drive/Docs/Sheets/Slides) [DOC] |
| `google-analytics` | `references/google-analytics.md` | GA4/GTM measurement planning, Data API reporting [DOC] |
| `google-apis-integration` | `references/google-apis-integration.md` | multi-service integration (Sheets/Docs/Calendar/Maps JS/YouTube) [DOC] |
| `google-calendar-mcp` | `references/google-calendar-mcp.md` | agenda/availability/event CRUD via workspace-mcp [DOC] |
| `google-docs-mcp` | `references/google-docs-mcp.md` | documents.create/get/batchUpdate via workspace-mcp [DOC] |
| `google-drive-mcp` | `references/google-drive-mcp.md` | search/upload/export/share via workspace-mcp [DOC] |
| `google-maps-integration` | `references/google-maps-integration.md` | Maps JS, markers, Places/Geocoding/Directions [DOC] |
| `google-sheets-mcp` | `references/google-sheets-mcp.md` | values + structural Sheets ops via workspace-mcp [DOC] |
| `google-slides-mcp` | `references/google-slides-mcp.md` | presentations REST ops via workspace-mcp [DOC] |

### Disambiguation rules

- One service named → that topic. [INFERENCE]
- Two+ services or "integrate/connect Google APIs" → `google-apis-integration`
  (or `apis` for Gmail-inclusive Workspace automation). [DOC]
- `analytics-implementation` = GA4/Firebase/BigQuery *setup*; `google-analytics`
  = reporting/Data API *querying*. Do not conflate. [DOC]
- Ambiguous between two topics → ask one disambiguating question, don't guess. [INFERENCE]

## How it executes

`depth=quick` (default) walks the minimal correct path; `depth=deep` applies the
playbook exhaustively with verification at each step. The spine is Discover →
Analyze → Execute → Validate, gated by constitution v6.0.0 enforcement, Alfa
evidence tags, and the script-first rule. Live MCP/API execution is always a
separate human-reviewed step. [DOC]

## References

All ten playbooks live in `references/`; `routes.json` is the canonical
topic→playbook map. See `SKILL.md` for the routing contract and acceptance gate.

## Supporting bundle

- `agents/` — lead, specialist, support, guardian role contracts. [DOC]
- `knowledge/` — body of knowledge + concept graph. [DOC]
- `prompts/` — primary, meta, quick, deep prompt variants. [DOC]
- `templates/output.md` — the routing-decision deliverable scaffold. [DOC]
- `evals/evals.json` — routing and safety eval cases. [DOC]
- `examples/` — a worked routing example. [DOC]
- `assets/` — quality rubric and routing checklist (see `assets/README.md`). [DOC]
