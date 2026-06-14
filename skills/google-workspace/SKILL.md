---
name: google-workspace
version: 1.0.0
description: "Router for Google APIs/Workspace work — pick one topic and load its playbook: Sheets, Docs, Slides, Drive, Calendar, Maps, Analytics/GA4, or multi-service API integration (auth/scope/quota/retry). Topics: analytics-implementation, apis, google-analytics, google-apis-integration, google-calendar-mcp, google-docs-mcp, google-drive-mcp, google-maps-integration, google-sheets-mcp, google-slides-mcp."
params:
  topic:
    enum: [analytics-implementation, apis, google-analytics, google-apis-integration, google-calendar-mcp, google-docs-mcp, google-drive-mcp, google-maps-integration, google-sheets-mcp, google-slides-mcp]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  analytics-implementation: references/analytics-implementation.md
  apis: references/apis.md
  google-analytics: references/google-analytics.md
  google-apis-integration: references/google-apis-integration.md
  google-calendar-mcp: references/google-calendar-mcp.md
  google-docs-mcp: references/google-docs-mcp.md
  google-drive-mcp: references/google-drive-mcp.md
  google-maps-integration: references/google-maps-integration.md
  google-sheets-mcp: references/google-sheets-mcp.md
  google-slides-mcp: references/google-slides-mcp.md
---

# google-workspace

Router skill. Resolve `topic`, then Read EXACTLY ONE playbook from `routes:`.
Never load the whole cluster — one route per invocation. [DOC]

## When to use
A request touches a Google API/Workspace surface (Sheets, Docs, Slides, Drive,
Calendar, Maps, GA4/Analytics) or spans several Google services and needs an
auth/scope/quota/retry plan. If no Google surface is involved, decline. [INFERENCE]

## Routing
- One service named → that topic (e.g. "GA4 events" → `analytics-implementation`;
  "read a spreadsheet" → `google-sheets-mcp`). [INFERENCE]
- Two+ services or "integrate/connect Google APIs" → `google-apis-integration`. [DOC]
- `analytics-implementation` = GA4/Firebase/BigQuery setup; `google-analytics` =
  reporting/Data API querying. Don't conflate. [DOC]
- Ambiguous between two topics → ask one disambiguating question, don't guess. [INFERENCE]

## Depth
- `quick` (default): essentials only — the minimal correct path. [DOC]
- `deep`: apply the playbook exhaustively with verification at each step. [DOC]

## Spine
Discover → Analyze → Execute → Validate. Quality gates: constitution v6.0.0
(enforcement), evidence tags (Alfa set: `[DOC]`/`[CONFIG]`/`[CÓDIGO]`/
`[INFERENCE]`/`[ASSUMPTION]`), script-first rule. [DOC]

## Acceptance gate (before "done")
- Exactly one playbook was loaded; `topic` matches the user's actual surface. [DOC]
- Credentials/scopes confirmed present; no secrets pasted inline. [ASSUMPTION]
- Output carries one-family evidence tags; assumptions pair with a verify step. [DOC]

## Assets
Routing gate is backed by `assets/` — `assets/routing-checklist.md` (resolve →
load → plan → gate) and `assets/quality-rubric.json` (8-criterion acceptance
gate). See `assets/README.md`. [DOC]

## Anti-patterns
- Loading multiple routes "to be safe" — defeats the router. [INFERENCE]
- Answering Google-API questions from memory instead of the playbook. [INFERENCE]
- Guessing `topic` when the request is ambiguous, or inventing quotas/prices. [DOC]
