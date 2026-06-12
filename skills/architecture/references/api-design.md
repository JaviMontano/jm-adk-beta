<!-- distilled from alfa skills/api-design -->
<!-- > -->
# API Design

> "A well-designed API is like a good joke — it needs no explanation." — Unknown

## TL;DR

Designs RESTful and GraphQL API contracts with OpenAPI specifications, versioning strategies, pagination, error handling, and rate limiting patterns. Use this skill when designing new APIs, evolving existing contracts, or establishing API design standards for a team. [EXPLICIT]

**Style picker** (choose before designing — the contract shape follows from it): [INFERRED]
- **REST** — resource CRUD, broad client/cache/proxy compatibility, public APIs. Default unless a driver below overrides.
- **GraphQL** — many client-shaped views over one graph, mobile bandwidth pressure, avoiding endpoint sprawl. Cost: query-complexity limits and N+1 resolver risk.
- **gRPC** — internal service-to-service, low latency, streaming, strict schema. Cost: weak browser support without a proxy.

## Procedure

### Step 1: Discover
- Identify API consumers: frontend, mobile, third-party, internal services — note each one's auth model, versioning tolerance, and SLA. [INFERRED]
- Gather domain entities and operations from requirements/domain model
- Review existing APIs for consistency and established patterns
- Determine API style: REST, GraphQL, gRPC, or hybrid (see Style picker)

### Step 2: Analyze
- Design resource hierarchy and URL structure (REST) or schema graph (GraphQL)
- Define HTTP methods, status codes, and idempotency guarantees. Make POST safe to retry via an `Idempotency-Key` header so client retries don't double-create. [INFERRED]
- Plan versioning strategy: URL path, header, or query parameter
- Design pagination: cursor-based (preferred) or offset-based. Offset drifts and skips/duplicates rows under concurrent writes; cursors are stable. [INFERRED]
- Plan authentication and authorization model per endpoint

### Step 3: Execute
- Write OpenAPI 3.1 specification with schemas, examples, and descriptions
- Define error response format: error code, message, details, trace ID
- Document rate limiting policy and quota headers (`RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`; `Retry-After` on 429). [INFERRED]
- Design webhook/callback patterns for async operations — sign payloads (HMAC) and require consumer idempotency, since webhooks deliver at-least-once. [INFERRED]
- Create API design guidelines document for team consistency

### Step 4: Validate
- Verify API follows RESTful constraints (stateless, uniform interface, HATEOAS where applicable)
- Confirm all endpoints have request/response examples
- Check error responses cover all failure modes (400, 401, 403, 404, 409, 422, 429, 500)
- Validate naming consistency: plural nouns for collections, consistent casing
- Run the spec through a linter (e.g. Spectral) in CI and gate breaking diffs (e.g. oasdiff) before merge. [INFERRED]

## Versioning Decision

| Strategy | Use when | Trade-off [INFERRED] |
|----------|----------|-----------|
| URL path (`/v1/...`) | Public APIs, human-discoverable, hard cutovers | Couples version to routing; URL no longer identifies one resource |
| Header (`Accept: ...;v=2`) | Many fine-grained versions, content negotiation | Invisible in logs/browser; harder to test by hand |
| Query (`?version=2`) | Quick opt-in, gradual rollout | Pollutes cache keys; easy to omit |

Rule: additive changes (new optional field, new endpoint) are non-breaking and need no bump; removing/renaming a field, tightening validation, or changing a type IS breaking and requires a new version. [INFERRED]

## Status Code Cheat Sheet [INFERRED]

| Code | Use for |
|------|---------|
| 400 | Malformed syntax / unparseable body |
| 401 / 403 | Not authenticated / authenticated but not allowed |
| 404 | Resource absent (also to hide existence from unauthorized callers) |
| 409 | State conflict (duplicate, version mismatch on optimistic concurrency) |
| 422 | Well-formed but semantically invalid (validation) |
| 429 | Rate limit exceeded — pair with `Retry-After` |
| 5xx | Server fault — never leak stack traces; return trace ID |

## Worked Example — error envelope

```json
{
  "error": {
    "code": "validation_error",
    "message": "email is not a valid address",
    "details": [{ "field": "email", "issue": "format" }],
    "trace_id": "01HMW9..."
  }
}
```
`code` is a stable machine-readable string (clients branch on it); `message` is human-facing and may change. [INFERRED]

## Quality Criteria

- [ ] OpenAPI spec is valid and includes examples for all operations
- [ ] Versioning strategy is defined and consistently applied
- [ ] Pagination uses cursor-based approach for large collections
- [ ] Error format is standardized with machine-readable error codes
- [ ] Breaking-change diff gated in CI; non-breaking changes ship without a bump [INFERRED]
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Verb-based URLs (POST /createUser) instead of resource-oriented (POST /users)
- Returning 200 for everything with error in response body
- Breaking changes without version increment
- Offset pagination on large/mutating collections (drift, skipped rows) [INFERRED]
- Unbounded list endpoints with no default page size or max limit [INFERRED]
- Leaking internal exceptions/stack traces in error bodies [INFERRED]

## Related Skills

- `system-architecture` — API boundaries derive from system decomposition
- `security-architecture` — API authentication and authorization patterns
- `database-design` — data models underlying API resources

## Usage

Example invocations:

- "/api-design" — Run the full api design workflow
- "api design on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Anti-scope: does not implement servers, generate client SDKs, or run load tests — contract design only [INFERRED]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Breaking change demanded on a live public contract | Version it; run old + new in parallel with a deprecation window and `Sunset` header [INFERRED] |
| Bulk/batch operation needed | Define explicit batch endpoint with partial-success (207-style) semantics, not N round-trips [INFERRED] |
