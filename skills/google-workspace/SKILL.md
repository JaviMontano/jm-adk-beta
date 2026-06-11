---
name: google-workspace
description: "Google APIs and Workspace: sheets, docs, slides, drive, calendar, maps, analytics, API integration. Topics: analytics-implementation, apis, google-analytics, google-apis-integration, google-calendar-mcp, google-docs-mcp, google-drive-mcp, google-maps-integration, google-sheets-mcp, google-slides-mcp."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
