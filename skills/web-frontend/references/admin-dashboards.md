<!-- distilled from alfa skills/admin-dashboards -->
<!-- > -->
# Admin Dashboards

> "A dashboard should answer questions before they're asked." — Stephen Few

## TL;DR

Guides the architecture and implementation of admin dashboard interfaces featuring sortable/filterable data tables, CRUD operations, charts/metrics, real-time updates, audit trails, empty/loading/error states, responsive dense layouts, and role-based access control enforced beyond the UI. Use when building back-office tools, content management systems, or operational dashboards. Do not invent APIs, schemas, metrics, permissions, or realtime channels without repo evidence or explicit user input. [EXPLICIT]

**In scope:** list/inspect/CRUD/bulk/export/audit flows, table+chart UX, state design, RBAC UI surface, performance under load. **Anti-scope (defer or hand off):** backend authorization *implementation*, schema/migration design, billing/payments mutations, marketing-page polish, BI warehouse modeling — name these and route to the owning skill rather than guessing. [INFERENCE]

## Procedure

### Step 1: Discover
- Identify data entities and their relationships (users, orders, content, settings)
- Review user roles and permission levels (admin, editor, viewer)
- Check existing API endpoints and data schemas
- Determine real-time requirements (WebSocket, polling, SSE)
- Capture operational workflows: list, inspect, create, update, delete, bulk actions, export, audit, and recovery
- Quantify scale early: expected row counts, peak concurrent admins, largest export, write frequency — these decide pagination, virtualization, and realtime transport [INFERENCE]
- Mark missing backend, schema, permission, metric, or endpoint evidence as `[ASSUMPTION]` or `not verified`

### Step 2: Analyze
- Plan navigation structure (sidebar, breadcrumbs, nested routes)
- Design data table features (sort, filter, search, pagination, bulk actions)
- Choose chart library (Chart.js, Recharts, D3, Apache ECharts)
- Evaluate state management for complex filter/table interactions
- Define RBAC matrix: role x route x action x resource x backend enforcement point
- Define data contract: endpoint/query, parameters, pagination, sorting, filters, response shape, error shape, freshness, and owner
- Define state contract: empty, loading, partial error, permission denied, stale data, conflict, timeout, offline, and retry
- Define audit contract for create/update/delete/export and destructive actions

### Step 3: Execute
- Build sidebar layout with collapsible navigation and role-based menu items
- Implement data tables with server-side pagination, sorting, and column configuration
- Add CRUD forms with validation, optimistic updates, and confirmation dialogs
- Create metric cards and charts for KPI overview section
- Wire real-time updates via Firestore listeners or WebSocket connections
- Add export functionality (CSV, PDF) for table data
- Prefer established table/chart/form libraries already present in the repo; if none exist, document the selection rationale before adding dependencies
- Treat destructive operations and bulk actions as confirmable, auditable workflows with rollback or recovery notes
- Sanitize rendered cell content and exports; prevent formula injection in CSV-style outputs
- Preserve URL/query state for filters, search, sort, pagination, and selected views when useful

### Step 4: Validate
- Test with large datasets (1000+ rows) — no UI freezing
- Verify CRUD operations handle errors gracefully (network failures, conflicts)
- Confirm role-based access hides unauthorized actions, not just routes
- Check keyboard navigation for data tables and forms
- Verify backend/API authorization or mark RBAC as `not verified`; hiding buttons is not enough
- Verify empty/loading/error/permission-denied states for each critical panel
- Verify KPI formulas, units, time ranges, timezone, freshness, and data owner before presenting metrics as truth
- Verify responsive density across mobile, tablet, and desktop without losing critical actions

## Key Decisions & Trade-offs [INFERENCE]

| Decision | Default | Choose alternative when | Trade-off accepted |
|----------|---------|--------------------------|--------------------|
| Pagination model | Server-side, offset/cursor | Dataset < ~500 rows and stable → client-side | Server-side adds round-trips but bounds memory and keeps first paint fast |
| Cursor vs offset | Cursor (keyset) for large/append-heavy tables | Offset when total count + jump-to-page is required | Cursor loses "page N of M"; offset degrades on deep pages |
| Realtime transport | Polling (cheap, debuggable) | True low-latency needs → WebSocket/SSE; Firestore-native app → listeners | Sockets add reconnect/auth/fan-out complexity and cost |
| Table library | Headless (TanStack Table) + own markup | Need batteries-included grid (AG Grid) for huge/pivot data | Headless = more wiring; full grid = bundle size + license check |
| CRUD update UX | Optimistic + reconcile on response | Destructive/irreversible or low-trust network → pessimistic | Optimistic risks visible rollback flicker on conflict |
| Filter state home | URL query params (shareable, back-button safe) | Ephemeral/PII-bearing filters → in-memory only | URL state can leak filter values in logs/history |

## Worked Example: Orders Table Data Contract [DOC]

Endpoint `GET /api/orders` (verify path against repo before relying on it — `[ASSUMPTION]` until confirmed):
- **Params:** `cursor`, `limit≤100`, `sort` (allowlisted columns only), `dir=asc|desc`, `filter[status]`, `q` (search), `tz`.
- **Response:** `{ data: Order[], page: { nextCursor, hasMore }, meta: { freshnessTs, owner } }`.
- **Error shape:** `{ error: { code, message, retryable } }` — UI maps `retryable` to a retry affordance, non-retryable to a terminal error state.
- **Server enforces:** the same RBAC the UI assumes; `sort`/`filter` keys are server-allowlisted to block injection and unindexed scans. Never trust client-supplied column names.

## Failure Modes & Mitigations [INFERENCE]

| Failure mode | Symptom | Mitigation |
|--------------|---------|------------|
| Unbounded fetch | Page jank / OOM on big tables | Server pagination + row virtualization; cap `limit` server-side |
| RBAC theater | Hidden buttons, open API | Enforce + test authorization at the API/rules layer; UI hiding is cosmetic |
| Optimistic drift | UI shows success, server rejected | Reconcile on response, surface conflict, offer retry/refresh |
| Stale realtime | Listener silently dropped | Show freshness timestamp + reconnect indicator; fall back to poll |
| CSV formula injection | `=`,`+`,`-`,`@` cells execute in Excel | Prefix risky leading chars with `'`; quote fields; document in export code |
| PII leak in audit/export | Sensitive payloads logged/shipped | Log diffs/IDs not full payloads; redact + governance-gate exports |
| Filter desync on back-nav | Restored view ≠ data shown | Single source of truth in URL; hydrate table state from it |
| Bulk action half-applied | Partial success on N items | Report per-item result; make idempotent; offer retry-failed-only |

## Quality Criteria

- [ ] Data tables handle sorting, filtering, and pagination without full page reload
- [ ] CRUD operations show loading states, success feedback, and error recovery
- [ ] Dashboard performance targets include measurement context, dataset size, and environment
- [ ] Role-based access enforced on both UI and API levels, or explicitly marked `not verified`
- [ ] Authorization matrix, data contract, state matrix, and audit trail are documented
- [ ] Exports protect PII and neutralize spreadsheet formula injection risks
- [ ] Empty, loading, error, offline, stale, and permission states are designed
- [ ] Responsive and keyboard-accessible flows are covered
- [ ] Bulk/destructive actions are idempotent, confirmable, and report per-item outcome
- [ ] Sort/filter keys are server-allowlisted; no client-named columns reach the query
- [ ] Evidence tags applied to all claims

## Acceptance Criteria (done means) [DOC]

- A 1000+ row table sorts/filters/paginates with no main-thread freeze and bounded memory (server pagination or virtualization in place).
- Every critical panel renders correct empty, loading, partial-error, and permission-denied states — demonstrated, not assumed.
- An unauthorized role receives a 403 from the API for a hidden action, proven by request, not just absent UI.
- Each KPI card states formula, unit, time range, timezone, and freshness source.
- Destructive and bulk actions write an audit entry (actor, action, target, timestamp, outcome) free of full sensitive payloads.

## Anti-Patterns

- Loading all records client-side instead of server-side pagination
- Building custom data tables from scratch when libraries like TanStack Table exist
- Hiding menu items but not protecting API routes for unauthorized roles
- Inventing `/api/*`, Firestore collections, WebSocket/SSE channels, or KPI formulas without evidence
- Treating admin dashboards as marketing pages instead of dense operational tools
- Logging full sensitive payloads in audit trails
- Exporting raw PII or spreadsheet formulas without governance
- Reporting performance targets without dataset and measurement context
- Trusting client-supplied sort/filter column names directly in the query (injection + unindexed-scan risk)

## Related Skills

- `firestore-queries` — efficient data fetching for dashboard tables
- `cloud-functions` — API endpoints backing CRUD operations

## Usage

Example invocations:

- "/admin-dashboards" — Run the full admin dashboards workflow
- "admin dashboards on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Uses the language of the user request unless repo conventions require otherwise [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Does not certify backend authorization unless policies, middleware, rules, or endpoint checks were inspected or provided [EXPLICIT]
- Does not create or mutate files when the user asks for design/spec only [EXPLICIT]
- Library/endpoint/schema names in examples are illustrative placeholders, valid only after repo confirmation [ASSUMPTION]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Dataset too large to count | Use cursor pagination; drop total-count UI rather than scan |
| Mixed-permission rows in one table | Filter at query level by role; never render-then-hide restricted rows |
| Concurrent edit conflict | Detect via version/etag; surface conflict, never silently overwrite |
| Export exceeds safe size | Stream/paginate or queue async job; warn before generating |

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
