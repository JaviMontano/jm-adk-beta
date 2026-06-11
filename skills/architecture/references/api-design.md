<!-- distilled from alfa skills/api-design -->
<!-- > -->
# API Design

> "A well-designed API is like a good joke — it needs no explanation." — Unknown

## TL;DR

Designs RESTful and GraphQL API contracts with OpenAPI specifications, versioning strategies, pagination, error handling, and rate limiting patterns. Use this skill when designing new APIs, evolving existing contracts, or establishing API design standards for a team. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify API consumers: frontend, mobile, third-party, internal services
- Gather domain entities and operations from requirements/domain model
- Review existing APIs for consistency and established patterns
- Determine API style: REST, GraphQL, gRPC, or hybrid

### Step 2: Analyze
- Design resource hierarchy and URL structure (REST) or schema graph (GraphQL)
- Define HTTP methods, status codes, and idempotency guarantees
- Plan versioning strategy: URL path, header, or query parameter
- Design pagination: cursor-based (preferred) or offset-based
- Plan authentication and authorization model per endpoint

### Step 3: Execute
- Write OpenAPI 3.1 specification with schemas, examples, and descriptions
- Define error response format: error code, message, details, trace ID
- Document rate limiting policy and quota headers
- Design webhook/callback patterns for async operations
- Create API design guidelines document for team consistency

### Step 4: Validate
- Verify API follows RESTful constraints (stateless, uniform interface, HATEOAS where applicable)
- Confirm all endpoints have request/response examples
- Check error responses cover all failure modes (400, 401, 403, 404, 409, 422, 429, 500)
- Validate naming consistency: plural nouns for collections, consistent casing

## Quality Criteria

- [ ] OpenAPI spec is valid and includes examples for all operations
- [ ] Versioning strategy is defined and consistently applied
- [ ] Pagination uses cursor-based approach for large collections
- [ ] Error format is standardized with machine-readable error codes
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Verb-based URLs (POST /createUser) instead of resource-oriented (POST /users)
- Returning 200 for everything with error in response body
- Breaking changes without version increment

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

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
