<!-- distilled from alfa skills/api-documentation -->
<!-- > -->
# Api Documentation

> "Method over hacks. Evidence over assumption."

## TL;DR

Generates developer-facing API documentation from code or specs: OpenAPI 3.0 spec files, Swagger/Redoc UI setup, endpoint reference with request/response examples, auth docs, and an error-code catalog. Complements `api-design` (which owns the contract); this skill owns the docs *about* that contract. [EXPLICIT]

## Scope & Anti-Scope

- IN: OpenAPI/Swagger artifacts, endpoint reference, auth + error docs, example payloads, doc-site wiring. [EXPLICIT]
- OUT: designing the contract (use `api-design`), implementing endpoints (use `rest-api-development`), versioning policy decisions, SLA/rate-limit *negotiation*. Document those once decided; do not author them. [EXPLICIT]

## Procedure

### Step 1: Discover
- Inventory endpoints from source: route definitions, decorators/annotations, existing `openapi.yaml|json`, Postman collections. [EXPLICIT]
- Identify auth scheme (apiKey, bearer/JWT, OAuth2 flow), base URL(s), and environment variants (prod/staging). [EXPLICIT]
- Record gaps: undocumented params, missing status codes, examples that drift from current schema. [INFERENCIA]

### Step 2: Analyze
- Choose source of truth: code-first (generate spec from annotations) vs spec-first (hand-authored OpenAPI). Default code-first when annotations exist, to prevent drift. [EXPLICIT]
- Trade-off: code-first stays in sync but leaks implementation detail; spec-first reads cleaner but rots silently. Pick one per repo, never mix for the same surface. [INFERENCIA]
- Apply Constitution XIII (Think First), XIV (Simple First); map output to quality gates below.

### Step 3: Execute
- Emit OpenAPI 3.0: `info`, `servers`, `paths` (each verb with `parameters`, `requestBody`, `responses`), `components.schemas`, `components.securitySchemes`. [EXPLICIT]
- For every endpoint: at least one success example AND one error example, with realistic (non-`foo`/`bar`) values; redact secrets/PII. [EXPLICIT]
- Author the error-code catalog (see table). Wire a renderer (Swagger UI or Redoc) pointing at the spec. Apply evidence tags to claims; use brand template if HTML output. [EXPLICIT]

### Step 4: Validate
- Lint spec (e.g. `spectral`/`swagger-cli validate`) — zero errors. [EXPLICIT]
- Round-trip check: at least one documented example replayed against a live/staging endpoint matches the documented schema and status. [EXPLICIT]
- Confirm every `4xx`/`5xx` returned by code appears in the catalog, and vice versa (no orphan codes). [EXPLICIT]

## Error-Code Catalog (template)

| Code | Meaning | When | Client action |
|------|---------|------|---------------|
| 400 | Bad request | Schema/validation failure | Fix payload; see field errors |
| 401 | Unauthenticated | Missing/expired token | Re-authenticate |
| 403 | Forbidden | Valid identity, no permission | Request scope/role |
| 404 | Not found | Resource absent or hidden | Verify id/path |
| 409 | Conflict | Idempotency/state clash | Reconcile then retry |
| 429 | Rate limited | Quota exceeded | Back off per `Retry-After` |
| 5xx | Server error | Unhandled/internal | Retry w/ backoff; report id |

## Quality Criteria (acceptance)

- [ ] Spec validates against OpenAPI 3.0 with zero lint errors [EXPLICIT]
- [ ] Every endpoint has ≥1 success + ≥1 error example, no placeholder values [EXPLICIT]
- [ ] Auth scheme + all environments documented; no secrets/PII in examples [EXPLICIT]
- [ ] Error catalog ↔ code are bidirectionally consistent [EXPLICIT]
- [ ] Evidence tags applied; Constitution-compliant; renderer loads the spec clean

## Failure Modes

- Spec drift: code changes, docs don't → prefer code-first generation in CI. [INFERENCIA]
- Example rot: payloads no longer match schema → validate examples against schema in Step 4. [EXPLICIT]
- Leaked secrets: real tokens/keys copied into examples → mandatory redaction pass. [EXPLICIT]

## Related Skills

- `api-design` — API contract design
- `rest-api-development` — REST implementation
- `cloud-functions` — Firebase Functions API docs

## Usage

- "/api-documentation" — Run the full api documentation workflow
- "api documentation on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, routes, configs, any existing spec) [EXPLICIT]
- English-language output unless otherwise specified [EXPLICIT]
- Documents the contract as-is; does not redesign it or replace domain-expert judgment [EXPLICIT]
- No live traffic capture; examples come from code/spec/staging, not prod logs [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No existing spec, code-first impossible | Bootstrap minimal spec-first stub, flag as authoritative |
| Mixed auth across endpoints | Document per-endpoint `security` overrides, not just global |
