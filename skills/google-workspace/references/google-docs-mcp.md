<!-- distilled from alfa skills/google-docs-mcp -->
<!-- > -->
# Google Docs MCP

## TL;DR

Plan and execute Google Docs work through the local `workspace-mcp` server with
least-privilege scope selection and a hard human-confirmation gate before
`documents.create` or `documents.batchUpdate`. Use
`scripts/compile-google-docs-mcp.py` when the request can be represented as
structured JSON and a reproducible offline checklist is useful. [EXPLICIT]

The Docs surface is exactly three methods — `documents.create` (title-only),
`documents.get` (inspect), `documents.batchUpdate` (all mutations). Everything
else is request composition and confirmation discipline. [DOC]

## Prerequisites

- Google Workspace MCP server configured (see `docs/google-workspace-mcp-setup.md`) [DOC]
- Google Docs API enabled and OAuth credentials authenticated through the local
  `workspace-mcp` setup [CONFIG]
- Local reference assets under `assets/` and deterministic checks under `scripts/` [CONFIG]

## Procedure

### Step 1: Confirm Server And Scope
- Confirm `.mcp.json` exposes `workspace-mcp` with Docs tools before live use. [CONFIG]
- Use `assets/scope-policy.json` to select the narrowest scope profile. [CONFIG]
- Prefer `documents.readonly` for read-only inspection and `drive.file` for
  documents created or explicitly opened for the app. [DOC]
- Escalate to full `documents` only with a written reason. [EXPLICIT]
- **Trade-off:** `drive.file` cannot open arbitrary existing docs the app never
  created/opened; if the user supplies a foreign doc ID, `documents` (or a Drive
  picker grant) is required — surface this rather than silently broadening. [INFERENCE]

### Step 2: Create Or Resolve The Document
- Use `documents.create` only for a blank document with a title. [DOC]
- Do not include body content in `documents.create`; insert initial content with a
  follow-up `documents.batchUpdate` request. [DOC]
- Capture the created document ID before planning later operations. [DOC]
- A fresh empty doc still contains one default paragraph; its body ends at index
  `1`, so the first safe `insertText` location is `index: 1`. [INFERENCE]

### Step 3: Inspect Before Batch Update
- Use `documents.get` before editing an existing or newly created document. [DOC]
- Request only useful fields — document ID, title, body content, tabs, and
  revision ID — when the workflow needs safe writes. [CODE]
- Capture current structure, indexes, and revision information before composing
  ranges for `documents.batchUpdate`. [DOC]
- Indexes are UTF-16 code-unit offsets into the document body; the body starts at
  index `1` (index `0` is the implicit document start). Emoji and other
  surrogate-pair characters consume two index units — never assume one char = one
  index. [DOC]
- For multi-tab documents, ranges are scoped per tab; resolve the target tab ID
  from `documents.get` before building any range. [DOC]

### Step 4: Compose Batch Update Requests
- Use `documents.batchUpdate` for real Docs operations such as `insertText`,
  `deleteContentRange`, `replaceAllText`, `updateTextStyle`,
  `updateParagraphStyle`, `createParagraphBullets`, `insertTable`, and
  `insertPageBreak`. [DOC]
- Include `writeControl.requiredRevisionId` when a prior `documents.get` captured
  a revision ID. [CODE]
- Keep request order explicit because batch-update requests are applied in the
  order provided by the API. [DOC]
- **Insertion shifts indexes.** Each `insertText` moves every later index forward
  by the inserted length. When batching multiple inserts in one request, either
  order them back-to-front (highest index first) or recompute offsets per request;
  the API does not re-resolve your earlier indexes for you. [INFERENCE]
- Use `replaceAllText` (match by text) rather than computed ranges when the target
  string is unambiguous — it is index-independent and survives concurrent edits. [DOC]

### Step 5: Confirm Mutations And Validate
- Ask for human confirmation before any `documents.create` or
  `documents.batchUpdate` operation. [EXPLICIT]
- Report selected MCP tool, Docs API method, scope profile, confirmation state,
  request checklist, validation result, and residual limits. [EXPLICIT]
- Validate by a post-write `documents.get` (revision ID advanced; target text/style
  present) — not by the absence of an error in the batch response. [INFERENCE]
- Run `scripts/check.sh` when changing this skill. [CONFIG]

## Worked Example: create + populate (title-only, then batch)

```jsonc
// 1. create — title only, no body  [CODE]
documents.create { "title": "Q3 Planning Notes" }
//    → returns documentId "1AbC...", revisionId "r0"

// 2. get — capture indexes + revision before writing  [CODE]
documents.get { "documentId": "1AbC...",
  "fields": "documentId,title,revisionId,body(content)" }

// 3. batchUpdate — insert at index 1, guard on revision  [CODE]
documents.batchUpdate { "documentId": "1AbC...",
  "writeControl": { "requiredRevisionId": "r0" },
  "requests": [
    { "insertText": { "location": { "index": 1 },
        "text": "Agenda\nOwners\n" } },
    { "updateParagraphStyle": {
        "range": { "startIndex": 1, "endIndex": 7 },
        "paragraphStyle": { "namedStyleType": "HEADING_1" },
        "fields": "namedStyleType" } }
  ] }
```

## Quality Criteria

- [ ] Operation plan uses real Docs API methods: `documents.create`,
      `documents.get`, and `documents.batchUpdate` [CODE]
- [ ] `documents.create` remains title-only; body content is inserted by
      `documents.batchUpdate` [DOC]
- [ ] Existing document edits include a prior `documents.get` inspection step [DOC]
- [ ] Batch update requests use stable request objects and explicit ordering,
      with index shifts from earlier inserts accounted for [INFERENCE]
- [ ] `updateTextStyle` / `updateParagraphStyle` requests carry a `fields` mask;
      omitting it is rejected by the API [DOC]
- [ ] Mutations have human confirmation before live MCP execution [EXPLICIT]
- [ ] OAuth scope profile is least privilege for the requested operation [CONFIG]
- [ ] Scripts stay offline and deterministic; no Docs, OAuth, or MCP calls [CONFIG]
- [ ] Validation is a post-write `documents.get`, not a non-error response [INFERENCE]
- [ ] Evidence tags applied to all claims [EXPLICIT]

## Anti-Patterns

- Inserting body content directly into `documents.create` [DOC]
- Running `documents.batchUpdate` without a prior `documents.get` [DOC]
- Mutating a document without an explicit human-confirmation record [EXPLICIT]
- Using full `documents` scope when `documents.readonly` or `drive.file` is enough [DOC]
- Guessing text indexes instead of reading document structure first [DOC]
- Batching multiple front-to-back inserts without re-offsetting for prior inserts [INFERENCE]
- Omitting the `fields` mask on style update requests [DOC]
- Overwriting entire documents when scoped batch-update requests are sufficient [DOC]
- Treating export (or a non-error batch response) as proof that a live edit succeeded [INFERENCE]

## Failure Modes

| Failure | Signal | Recovery |
|---------|--------|----------|
| Stale revision | `400 / FAILED_PRECONDITION` on `requiredRevisionId` | Re-run `documents.get`, recompute indexes, retry [INFERENCE] |
| Index out of range | `400 INVALID_ARGUMENT` on a range | Re-inspect body; clamp `endIndex` to body end [INFERENCE] |
| Missing `fields` mask | `400` on style request | Add explicit `fields` listing changed properties [DOC] |
| Scope too narrow | `403 / PERMISSION_DENIED` | Escalate scope with written reason, or use a doc the app owns [INFERENCE] |
| Partial batch | Some requests applied before error | Treat batch as non-atomic per request; reconcile via `documents.get` [INFERENCE] |

## Related Skills

- `google-drive-mcp` - file search, sharing, and export boundaries
- `google-sheets-mcp` - spreadsheet data workflows
- `google-slides-mcp` - presentation creation and updates
- `google-workspace-apis` - programmatic Google Workspace API patterns

## Usage

- `/google-docs-mcp` - interactive document management
- "create a Google Doc with these meeting notes"
- "inspect this document and plan a safe batch update"
- "compile a Docs MCP plan from this JSON fixture"

## Assumptions & Limits

- Requires authenticated local Google Workspace MCP server [EXPLICIT]
- Uses local assets under `assets/` for deterministic Docs API policy, not live
  Google Docs inspection [EXPLICIT]
- `scripts/compile-google-docs-mcp.py` renders a plan/checklist only; it does not
  call Docs, OAuth, or MCP [EXPLICIT]
- Real Docs outcomes depend on account access, OAuth scopes, document ACLs,
  current revision state, and user confirmation [EXPLICIT]
- **Anti-scope:** no Drive-level operations (search, share, move, export) — those
  belong to `google-drive-mcp`; no Sheets/Slides surfaces; no suggestion-mode or
  comment APIs (this reference covers direct edits only). [INFERENCE]
- `batchUpdate` is not transactional across requests: a mid-batch failure may
  leave earlier requests applied. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Create a document with content | `documents.create` for the title, then `documents.batchUpdate` for content |
| Existing document edit | Require `documents.get` before batch-update index or style requests |
| Unknown indexes | Stop and inspect structure before generating ranges |
| Broad scope request | Surface risk and require a written escalation reason |
| Mutation requested without confirmation | Return a confirmation checklist instead of calling mutating tools |
| Multiple inserts in one batch | Order back-to-front or re-offset so later requests use post-insert indexes |
| Concurrent edit during the plan | Use `requiredRevisionId`; on precondition failure re-inspect and recompute |
| Foreign document ID under `drive.file` | Surface scope gap; do not silently escalate to full `documents` |
| Emoji / multi-tab document | Treat indexes as UTF-16 units; resolve the tab ID before building ranges |
