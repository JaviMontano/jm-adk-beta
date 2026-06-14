# Body of Knowledge — google-workspace

Domain knowledge for routing and safely planning Google APIs / Google Workspace
work. This is a router skill: its core competence is selecting the right surface
and enforcing least-privilege, confirmation-gated, offline-compiled plans. [DOC]

## 1. Surface map (the ten topics)

| Surface | Topic | Auth model | Key operations |
|---|---|---|---|
| Sheets | `google-sheets-mcp` | OAuth | `spreadsheets.{get,create,batchUpdate}`, `values.{get,update,append,batchUpdate}` [DOC] |
| Docs | `google-docs-mcp` | OAuth | `documents.{create,get,batchUpdate}` [DOC] |
| Slides | `google-slides-mcp` | OAuth | five `presentations` REST operations [DOC] |
| Drive | `google-drive-mcp` | OAuth | search/list, upload, export, copy/update, share [DOC] |
| Calendar | `google-calendar-mcp` | OAuth | `events.{list,insert,patch,delete}`, freebusy [DOC] |
| Maps JS | `google-maps-integration` | restricted API key | map load, markers, clustering, Places/Geocoding/Directions [DOC] |
| GA4 setup | `analytics-implementation` | property/Firebase config | events, conversions, BigQuery export, Looker [EXPLICIT] |
| GA4 reporting | `google-analytics` | OAuth / Data API | event taxonomy, GTM tag, Consent Mode, DebugView [DOC] |
| Multi-service | `google-apis-integration` | mixed | Sheets/Docs/Calendar/Maps JS/YouTube plan [DOC] |
| Workspace automation | `apis` | OAuth | Gmail/Calendar/Drive/Docs/Sheets/Slides matrix [DOC] |

## 2. Routing decision rules

- One named service → that topic. [INFERENCE]
- Two+ services, or "integrate/connect Google APIs" → `google-apis-integration`;
  if Gmail is in the mix or it is general Workspace automation → `apis`. [DOC]
- `analytics-implementation` is **setup** (instrument events, wire BigQuery);
  `google-analytics` is **reporting/measurement** (query, tag, verify). Conflating
  them is the most common routing error. [DOC]
- Ambiguity between two topics → ask one disambiguating question. [INFERENCE]
- No Google surface → decline. [INFERENCE]

## 3. Least-privilege scope ladders

- **Sheets**: `spreadsheets.readonly` → `drive.file` (app-created/opened files) →
  `spreadsheets` (cross-file edit). Scopes bind to the spreadsheet file, not a
  tab. [DOC]
- **Docs**: `documents.readonly` → `documents`. [DOC]
- **Calendar**: `calendar.freebusy` → `calendar.events.readonly` →
  `calendar.events`; avoid broad `calendar`. [DOC]
- **Drive**: `drive.file` (per-file) before broad `drive`/`drive.readonly`. [DOC]
- **Maps JS**: no OAuth scope — a restricted API key with HTTP-referrer and API
  allowlist. Modeling it as OAuth is invalid. [DOC]
- **Rule**: choose the narrowest profile; broad write scopes need an explicit
  escalation reason. [CODE]

## 4. Read-before-write and mutation gates

- Mixed read+write workflows start with read-only discovery (`get`/`list`)
  before any mutation. [CODE]
- Every mutating operation requires human confirmation/consent =
  `confirmed`, a read-back verification step, a retry profile, and an
  idempotency key. [CODE]
- `update` vs `append` (Sheets): `update` overwrites a fixed `ValueRange`;
  `append` adds the next empty row. Using `update` for an append silently
  corrupts rows with no error. [DOC]

## 5. Retry / error taxonomy

Distinguish four classes and map error codes:

- **User-fix** — 400 `INVALID_ARGUMENT` (malformed range, missing
  `valueInputOption`). Do not retry; fix input. [DOC]
- **Auth** — 401/403 → refresh token or re-consent; 403 `PERMISSION_DENIED` often
  means scope too narrow, not a transient fault. [INFERENCE]
- **Quota/rate** — 429 → exponential backoff + batching. [DOC]
- **Transient** — 5xx → bounded retry with backoff and the same idempotency key. [DOC]

## 6. Secrets policy

Client secrets, refresh tokens, and key-file paths stay server-side and never
appear in browser code, fixtures, or rendered plans. Any secret-shaped value in
input is rejected before render. [CODE]

## 7. Offline / deterministic contract

The cluster's alfa skills ship deterministic compilers (e.g.
`compile-google-sheets-mcp.py`, `compile-google-apis-integration.py`) plus a
`check.sh`. They read only local `assets/` + JSON fixtures and never call Google,
OAuth, HTTP, or MCP. This skill compiles a plan/checklist; live execution is a
separate human-reviewed step. [CODE]

## 8. Evidence taxonomy (Alfa family)

`[DOC]` official surface fact · `[CONFIG]` local MCP/env state · `[CÓDIGO]`/
`[CODE]` deterministic asset/compiler behavior · `[INFERENCE]` reasoned gap ·
`[ASSUMPTION]`/`[SUPUESTO]` unverified premise paired with a verify step. Never
invent quotas or prices; never treat green as automatic success. [DOC]

## 9. Common pitfalls

- Loading multiple routes "to be safe" — defeats the router. [INFERENCE]
- Answering Google-API questions from memory instead of the playbook. [INFERENCE]
- Requesting `drive`/full scopes for read-only discovery. [DOC]
- Sending Calendar invites or editing Docs/Sheets without consent. [CODE]
- Inventing a surface or operation not in the catalog. [CODE]
