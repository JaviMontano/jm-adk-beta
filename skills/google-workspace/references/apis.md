<!-- distilled from alfa skills/google-workspace-apis -->
<!-- > -->
# Google Workspace APIs

## TL;DR

Use this playbook to design a Google Workspace automation that spans Gmail,
Calendar, Drive, Docs, Sheets, and Slides. It produces an OFFLINE integration
plan: service matrix, OAuth scopes, MCP tool-contract mapping, mutation gates,
retry/idempotency policy, secrets policy, and validation matrix. [DOC]

Reach for this when the workflow crosses two or more services or must coordinate
REST and MCP execution paths in one plan. For a single interactive service,
prefer the specialized MCP skill instead (see MCP Integration). [INFERENCE]

## Scope & Anti-Scope

In scope: offline plan generation, scope/operation validation, contract mapping
between intent and MCP tools. [DOC]
Out of scope (this playbook never does these): [DOC]
- Live API/OAuth/MCP/network calls — those belong to a separate sandbox phase. [DOC]
- Proving OAuth grants, quota headroom, billing state, IAM permissions, or that a
  resource exists. The compiler cannot see provider state. [DOC]
- Inventing prices, quotas, or rate limits — cite the official reference or mark
  the value `[ASSUMPTION]` with a verify step. [DOC]
- Single-service interactive work better served by a dedicated MCP skill. [INFERENCE]

## Deterministic Contract

- `assets/workspace-service-matrix.json` is the operation catalog. [DOC]
- `assets/auth-scope-policy.json` defines least-privilege scope profiles. [DOC]
- `assets/mcp-tool-contract.json` applies when a workflow uses Workspace MCP tools. [DOC]
- Run `scripts/compile-google-workspace-apis.py` against a structured JSON input
  before finalizing a plan. [DOC]
- Run `scripts/check.sh` to verify positive and negative fixtures offline. [DOC]
- Skill scripts MUST NOT call Google APIs, OAuth, MCP servers, or any network
  resource — determinism and reproducibility depend on this. [DOC]

Asset paths are relative to the alfa `google-workspace-apis` kit, not this repo;
treat them as the source contract, confirm presence before relying on them. [ASSUMPTION]

## Procedure

### Step 1: Discover

- Identify target Workspace services and exact operations (method-level, e.g.
  `spreadsheets.values.update`, not just "Sheets"). [DOC]
- Classify each operation as read-only or mutating — this drives the scope
  profile and whether a confirmation gate is required. [INFERENCE]
- Determine the implementation path: direct REST/client library, MCP, or mixed. [DOC]
- Capture concrete resource identifiers (file IDs, calendar IDs, spreadsheet IDs)
  needed for sandbox validation; a plan without them cannot be validated live. [INFERENCE]

### Step 2: Analyze

- Select the narrowest scope profile from `assets/auth-scope-policy.json`.
  Decision: prefer a per-resource scope (e.g. `drive.file`) over a broad one
  (`drive`); trade-off is more consent friction for far smaller blast radius —
  default to narrow unless the operation provably cannot work under it. [INFERENCE]
- Prefer a read-only probe before every write (read-before-write), so a mutation
  acts on confirmed current state, not an assumption. [DOC]
- Map MCP tools to the same operation intent when MCP is part of the flow;
  tool availability is not proof of OAuth access (see Anti-Patterns). [DOC]
- Define idempotency keys, rollback/compensation, and retry policy BEFORE writes,
  not after a failure. [DOC]
- Confirm credential storage, token handling, and key restrictions. [DOC]

### Step 3: Compile

```bash
python3 skills/google-workspace-apis/scripts/compile-google-workspace-apis.py \
  --input skills/google-workspace-apis/scripts/fixtures/google-workspace-apis-input.json
```

The compiler emits a deterministic Markdown plan. It FAILS (non-zero exit) if:
scopes are too broad for the requested operation; a mutating operation lacks a
confirmation gate; a write skips read-before-write; or an MCP tool does not match
the service. A clean compile means the plan is internally consistent — NOT that
the live grant exists. [DOC]

### Step 4: Validate

- `bash skills/google-workspace-apis/scripts/check.sh` — positive + negative fixtures. [DOC]
- `python3 -B scripts/validate-skill-dod.py --skill google-workspace-apis` — definition-of-done. [DOC]
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-workspace-apis` — script contracts. [DOC]
- Live API calls are a separate sandbox/live phase requiring explicit human
  approval; never fold them into this offline pass. [DOC]

## Worked Example (cross-service, abbreviated)

Intent: "Email each row owner in a sheet a link to their Drive folder." [DOC]
- Services/ops: `spreadsheets.values.get` (read) → `drive.files.list` (read) →
  `gmail.users.messages.send` (mutate). [INFERENCE]
- Scopes: `spreadsheets.readonly`, `drive.metadata.readonly`, `gmail.send` —
  no broad `mail.google.com` or full `drive`. [INFERENCE]
- Gates: the two reads run unattended; the send is mutating → human confirmation
  + idempotency key (row ID + date) so a re-run does not double-send. [INFERENCE]
- Retry: exponential backoff on 429/5xx for the send only; reads are safe to
  retry freely. [INFERENCE]

## Quality Criteria

- [ ] Exact Workspace services and method-level operations are listed. [DOC]
- [ ] OAuth scopes are minimal for the operation class (read vs mutate). [DOC]
- [ ] Mutations require human confirmation and read-before-write. [DOC]
- [ ] MCP tool names map to service-compatible operations. [DOC]
- [ ] Secrets are never committed; tokens live in approved storage. [DOC]
- [ ] Retry, idempotency, quota, and rollback are explicit per write. [DOC]
- [ ] Validation matrix covers static, fixture, sandbox, and live-read-only layers. [DOC]

## Anti-Patterns

- Requesting broad Drive/Gmail scopes for read-only tasks. [DOC]
- Sending email, creating events, or changing files without confirmation. [DOC]
- Treating MCP tool availability as proof of OAuth access — the tool can be
  registered while the grant is absent or revoked. [INFERENCE]
- Storing OAuth clients, refresh tokens, service-account keys, or API keys in
  repo files. [DOC]
- Skipping partial-response `fields` selection, then blaming quota/performance
  later — unbounded responses inflate payloads and quota cost. [INFERENCE]
- Compiling clean and assuming the live integration works; compile proves plan
  consistency only. [INFERENCE]

## Failure Modes & Handling

- `403 insufficientPermissions` / `insufficientScopes` → granted scope narrower
  than the operation; re-run Analyze with the correct profile, re-consent. [INFERENCE]
- `429` / `userRateLimitExceeded` → back off exponentially with jitter; do not
  treat as fatal. Quota numbers are provider-side, not assertable here. [INFERENCE]
- `404` on a captured resource ID → ID stale or access lost; re-discover before
  retrying the write. [INFERENCE]
- Duplicate side effect after retry → idempotency key missing or not honored;
  add/repair the key, never just disable retries. [INFERENCE]
- Partial `batchUpdate` failure → know in advance whether the API is atomic;
  if not, plan compensation for the applied-then-failed subset. [ASSUMPTION]

## MCP Integration

For direct interactive access, prefer the specialized skills: `gmail-mcp`,
`google-calendar-mcp`, `google-drive-mcp`, `google-docs-mcp`, `google-sheets-mcp`,
and `google-slides-mcp`. Use this integrator when the workflow crosses services
or when REST/API and MCP execution paths must be coordinated in one plan. [DOC]

## Official References

- Google Workspace overview: https://developers.google.com/workspace
- Workspace auth overview: https://developers.google.com/workspace/guides/auth-overview
- Google Workspace MCP server guide: https://developers.google.com/workspace/guides/build-with-llms
- MCP tools spec: https://modelcontextprotocol.io/specification/draft/server/tools
- Gmail REST: https://developers.google.com/workspace/gmail/api/reference/rest
- Calendar REST: https://developers.google.com/calendar/api/v3/reference
- Drive REST: https://developers.google.com/drive/api/reference/rest/v3
- Docs REST: https://developers.google.com/workspace/docs/api/reference/rest
- Sheets REST: https://developers.google.com/workspace/sheets/api/reference/rest
- Slides REST: https://developers.google.com/workspace/slides/api/reference/rest

## Related Skills

- `gmail-mcp`
- `google-calendar-mcp`
- `google-drive-mcp`
- `google-docs-mcp`
- `google-sheets-mcp`
- `google-slides-mcp`
- `google-apis-integration`

## Assumptions & Limits

- The compiler validates plans offline; it does not prove OAuth, quota, billing,
  permissions, or resource existence. [DOC]
- Live execution requires a separate sandbox account, explicit human approval,
  and provider-side validation. [DOC]
- Evidence tags use the Alfa core set (EN spelling) per SKILL.md: `[DOC]`,
  `[CONFIG]`, `[CÓDIGO]`, `[INFERENCE]`, `[ASSUMPTION]`. Every `[ASSUMPTION]`
  here pairs with a verify step (confirm assets, check atomicity). [DOC]
