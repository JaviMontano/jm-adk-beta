<!-- distilled from alfa skills/google-drive-mcp -->
<!-- > -->
# Google Drive MCP

## TL;DR

Plan and execute Google Drive work through the local `workspace-mcp` server with
read-only discovery before mutation. Use this skill for Drive search/list,
upload, download/export, folder organization, copy/update, and
sharing/permissions. Use `scripts/compile-google-drive-mcp.py` when the request
can be represented as structured JSON and a reproducible offline checklist is
useful. [DOC]

**Mental model:** discovery is cheap and reversible; mutation is gated. Never
mutate before you have searched/listed the target, picked the least-privilege
scope, and obtained human confirmation. [INFERENCE]

## Prerequisites

- Google Workspace MCP server configured (see `docs/google-workspace-mcp-setup.md`)
- Google Drive API enabled and OAuth credentials authenticated through the local
  `workspace-mcp` setup
- Drive operations scoped to the narrowest available permission profile:
  prefer `drive.file` for created/opened files, `drive.metadata.readonly` for
  metadata-only discovery, and `drive.readonly` only when full read/download
  access is necessary

## Procedure

### Step 1: Discover Read-Only
- Confirm `.mcp.json` exposes `workspace-mcp` with Drive tools before using MCP.
- Use `mcp__workspace-mcp__search_drive_files` or
  `mcp__workspace-mcp__list_drive_items` before any upload, folder creation,
  copy/update, or sharing change.
- Make Drive search explicit: include a `q` query, `trashed = false`, `fields`,
  `spaces=drive`, and efficient `corpora` (`user` or a specific `drive` before
  `allDrives`). `allDrives` is the slowest and may silently drop results when
  paged — narrow first. [INFERENCE]
- Request only useful fields such as `files(id,name,mimeType,parents,webViewLink,
  capabilities/canDownload,capabilities/canShare)` and `nextPageToken`.

Worked example (find decks edited in the user's own corpus, last 30 days): [INFERENCE]
```
q = "mimeType='application/vnd.google-apps.presentation' and trashed=false and modifiedTime > '2026-05-12T00:00:00'"
corpora=user  spaces=drive  pageSize=50
fields=nextPageToken,files(id,name,mimeType,parents,modifiedTime,webViewLink,capabilities/canShare)
```
Page until `nextPageToken` is absent; do not assume one page is complete. [INFERENCE]

### Step 2: Select Scope And Operation Mode
- Use `assets/scope-policy.json` to choose the least-privilege scope profile.
- Treat `drive.file` as the preferred mutation profile for files created or
  selected for the app; do not escalate to full `drive` unless the task truly
  requires account-wide mutation. Trade-off: `drive.file` cannot see files the
  app did not create/open, so account-wide search needs `drive.readonly` for
  read or full `drive` for mutation — request the wider scope only for that
  step, not the whole session. [INFERENCE]
- Treat metadata-only lookup as `drive.metadata.readonly`; treat download/export
  of all accessible files as `drive.readonly`.
- Keep the offline compiler in `scripts/` for plan generation only. It must not
  call Drive, OAuth, or MCP.

### Step 3: Plan File And Folder Work
- Uploads — pick `uploadType` from size and metadata need, and justify: [INFERENCE]
  - `media`: small (<5 MB) content-only, no metadata. Fewest round-trips.
  - `multipart`: small upload that also sets name/parents/mimeType in one call.
  - `resumable`: files >5 MB OR any interruption-prone link. Survives network
    drops via byte-range resume; default to it when size is unknown.
- Downloads distinguish blob files from Google Workspace files: blob content uses
  media download semantics, while Google Docs/Sheets/Slides require an export MIME
  type. Export reference: [DOC]

  | Source type | Export to | MIME type |
  |---|---|---|
  | Docs | PDF / DOCX / Markdown | `application/pdf`, `…wordprocessingml.document`, `text/markdown` |
  | Sheets | XLSX / CSV | `…spreadsheetml.sheet`, `text/csv` (CSV = first sheet only) |
  | Slides | PPTX / PDF | `…presentationml.presentation`, `application/pdf` |

  Export caps the output at ~10 MB; for larger Workspace files export to PDF via
  `webContentLink` or split the source. [INFERENCE]
- Folders use `application/vnd.google-apps.folder`. Verify the parent exists and
  check inherited sharing before creating or moving content — a child inherits
  the parent's permissions on move. [INFERENCE]

### Step 4: Confirm Mutations
- Ask for human confirmation before upload, folder creation, copy/update, or
  permission changes. Confirmation is per mutation, not per session. [INFERENCE]
- For sharing, verify `capabilities.canShare`, permission `type`, role, email or
  domain target, notification behavior, expiration if applicable, and whether
  link/domain/anyone access is being introduced.
- Avoid broad `anyone` or domain-level sharing unless the user explicitly
  confirms recipient, role, duration, and business reason.

Worked example (least-privilege share confirmation prompt): [INFERENCE]
```
Mutation: add permission to folder <id>
type=user  role=writer  emailAddress=ana@company.com
sendNotificationEmail=true  expirationTime=<none>
canShare=true (verified)  introduces anyone/domain access? NO
Confirm? (y/N)
```

### Step 5: Validate And Report
- Return evidence-tagged output with source of truth, selected MCP tool, query or
  upload/export parameters, confirmation state, and residual limits.
- Run `scripts/check.sh` when changing this skill.

## Quality Criteria

- [ ] Read-only discovery happens before mutating Drive actions
- [ ] Search/list requests include `q`, `fields`, `trashed = false`, `spaces`, and
      efficient `corpora`; results paged until `nextPageToken` is absent
- [ ] OAuth scope profile is least privilege for the requested operation
- [ ] Upload plan selects `media`, `multipart`, or `resumable` from file size and
      metadata needs (>5 MB or interruption-prone → `resumable`)
- [ ] Download/export plan distinguishes blob content from Google Workspace
      document export and names the target export MIME type
- [ ] Folder operations verify parent, MIME type, and inherited permission impact
- [ ] Sharing/permission changes include human confirmation and capability checks
- [ ] Scripts stay offline and deterministic; no Drive, OAuth, or MCP calls
- [ ] Evidence tags applied to all claims, one tag per claim, single family

## Anti-Patterns

- Deleting files without user confirmation
- Running a mutating MCP tool before search/list discovery
- Searching without `trashed = false`, partial `fields`, or an efficient corpus
- Sharing with `anyone` or a whole domain without explicit confirmation
- Uploading credentials, tokens, `.env`, or private local state to Drive
- Treating Google Workspace documents as blob downloads instead of exports
- Using full `drive` scope when `drive.file`, `drive.readonly`, or
  `drive.metadata.readonly` is sufficient
- Deep recursive folder moves without a count, parent, and inherited-permission
  review
- Assuming one page of search results is complete (ignoring `nextPageToken`)
- Retrying a non-resumable upload from byte zero after a network drop instead of
  switching to `resumable`

## Related Skills

- `google-docs-mcp` — edit Google Docs content
- `google-sheets-mcp` — read/write spreadsheet data
- `google-slides-mcp` — create presentations
- `google-workspace-apis` — programmatic Drive API patterns

## Usage

- `/google-drive-mcp` — interactive Drive management
- "upload the report to my Drive in /Projects/Q2"
- "search Drive for presentation files from last month"
- "share the proposal folder with ana@company.com as editor"
- "compile a safe Drive MCP plan from this JSON fixture"

## Assumptions & Limits

- Requires authenticated local Google Workspace MCP server [ASSUMPTION]
- Uses local assets under `assets/` for deterministic Drive API policy, not live
  Drive inspection [DOC]
- `scripts/compile-google-drive-mcp.py` renders a plan/checklist only; it does
  not call Drive, OAuth, or MCP [DOC]
- Real Drive outcomes depend on account access, OAuth scopes, Shared Drive
  policy, file capabilities, and user confirmation [DOC]
- Large files may take time to upload/download/export in real MCP execution [DOC]
- Anti-scope: this playbook plans Drive operations; it does not own Docs/Sheets/
  Slides content editing (delegate to the sibling skills) or org-level Admin SDK
  policy. [INFERENCE]
- Drive API quotas and per-user rate limits are enforced server-side; this
  playbook cannot raise them, only respect them. [INFERENCE]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or broad search | Request a narrower `q`, target corpus, fields, and page size before calling Drive |
| Paginated results | Loop on `nextPageToken`; treat a present token as "more results exist", never stop at page 1 [INFERENCE] |
| Shared Drive target | Use `corpora=drive`, `driveId`, and `supportsAllDrives`/`includeItemsFromAllDrives` flags when the MCP tool exposes them |
| Google Docs/Sheets/Slides download | Export to a supported MIME type instead of blob download; honor the ~10 MB export cap |
| Export exceeds 10 MB | Export to PDF or split the source; do not silently truncate [INFERENCE] |
| Permission mutation | Require human confirmation and verify `capabilities.canShare` first |
| `canShare=false` | Stop; surface that the account lacks share rights rather than attempting the call [INFERENCE] |
| Broad access request | Surface risk and ask for explicit recipient, role, expiry, and reason |
| Rate limit / 403 `userRateLimitExceeded` | Back off with exponential retry + jitter; do not hammer the quota [INFERENCE] |
| Resumable upload interrupted | Resume from the last confirmed byte offset, not from zero [INFERENCE] |
| Duplicate name in target folder | Drive allows duplicate names by `id`; confirm intent before creating a second same-named file/folder [INFERENCE] |
| Abusive-content export blocked | A `cannotDownloadAbusiveFile`/scan flag blocks export; report it, do not bypass [INFERENCE] |
