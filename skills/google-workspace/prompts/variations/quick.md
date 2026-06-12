# Quick Variation — google-workspace

`depth=quick`. Walk the minimal correct path: resolve one topic, load one
playbook, emit the essential plan only. [DOC]

## Steps

1. Name the Google surface in the request.
2. Resolve `topic` (one service → that topic; two+ → `google-apis-integration`/
   `apis`; GA4 setup → `analytics-implementation`, GA4 reporting →
   `google-analytics`). If ambiguous, ask ONE question and stop.
3. Read EXACTLY ONE `references/<topic>.md`.
4. Emit the minimal plan: per operation → official surface, least-privilege
   scope/key, and (for mutations) the consent + read-before-write gate.
5. Tag claims with Alfa evidence tags. Note that live execution is separate.

## Quick example

Request: "read row 1 of my tracking spreadsheet's Log tab."
→ topic `google-sheets-mcp`; operation `spreadsheets.values.get` on `Log!A1:E1`;
scope `spreadsheets.readonly`; read-only, no consent gate needed; render. [DOC]

Skip the deep test matrix and exhaustive edge-case enumeration — that is `deep`.
