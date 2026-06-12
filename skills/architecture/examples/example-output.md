# Example output — architecture (topic: api-design, depth: deep)

## 1. Routing record
- **Resolved topic:** api-design
- **Depth:** deep
- **Why this topic (not the near neighbor):** the request is about the contract
  shape (versioning, pagination, errors, idempotency), not system decomposition
  (`system-architecture`) or read caching (`caching-strategy`). [INFERENCE]
- **Skipped:** n/a (deep run)

## 2. Context & drivers
- **Goal:** public REST contract for the orders service. [DOC]
- **Ranked drivers:**
  1. Stable, non-regrettable versioning for external partners. [DOC]
  2. Pagination correct under concurrent writes. [DOC]
  3. Retry-safe order creation (no double-charge). [DOC]
- **Consumers:** web frontend, partner integration, mobile app — partner has the
  lowest versioning tolerance. [DOC]

## 3. Analysis
- **Style:** REST confirmed — resource CRUD, broad client/cache compatibility,
  public audience. GraphQL/gRPC rejected: no many-view graph need, browser
  reach required. [INFERENCE]
- **Versioning:** URL path `/v1/...`. Chosen over header negotiation because the
  partner needs a human-discoverable, log-visible version and hard cutovers.
  Cost: version couples to routing. [INFERENCE]
- **Pagination:** cursor-based. Offset rejected — it drifts and skips/duplicates
  rows when orders are created concurrently. [INFERENCE]
- **Idempotency:** `Idempotency-Key` header on `POST /v1/orders` so client
  retries don't double-create. [INFERENCE]
- **Quality-attribute scenario:** under 200 req/s normal ops, `GET /v1/orders`
  returns p95 < 250 ms or 503-sheds within 50 ms. [DOC]

## 4. Decision
| # | Option | Versioning visibility | Pagination stability | Verdict |
|---|--------|-----------------------|----------------------|---------|
| 1 | URL path + cursor + idempotency-key | high | stable under writes | **selected** |
| 2 | Header version + offset | low | drifts under writes | rejected |
| 3 | No versioning (do nothing) | n/a | n/a | rejected (breaks partner on first change) |

- **Trade-off pair:** chose **URL-path + cursor** over **header + offset**
  because partner discoverability and write-time correctness outrank the routing
  cleanliness of header versioning. [INFERENCE]
- **Sensitivity:** if partners later demand many fine-grained versions, revisit
  toward header negotiation. [INFERENCE]

## 5. ADR
- **Status:** accepted
- **Context:** public API, low-tolerance partner consumer, concurrent order
  creation. [DOC]
- **Decision:** REST, `/v1` URL versioning, cursor pagination, RFC-9457-style
  error envelope, `Idempotency-Key` on creates. [DOC]
- **Consequences:** breaking changes require `/v2` with parallel run + `Sunset`
  header; cursors must be opaque + signed; idempotency store needed server-side. [DOC]
- **Rejected alternatives:** header versioning (invisible in logs); offset
  pagination (row drift). [INFERENCE]

## 6. Artifacts
Error envelope:
```json
{ "error": { "code": "validation_error", "message": "email is not a valid address",
  "details": [{ "field": "email", "issue": "format" }], "trace_id": "01HMW9..." } }
```
Status codes: 400 malformed, 401/403 auth, 404 absent, 409 duplicate/version
conflict, 422 validation, 429 rate-limit (+`Retry-After`), 5xx fault (trace id,
no stack trace). [DOC]

## 7. Assumptions & verification
| Assumption | How to verify | Owner |
|------------|---------------|-------|
| Partner needs log-visible version `[ASSUMPTION]` | Confirm in partner onboarding doc | API PM |
| Order volume reaches tens of thousands `[ASSUMPTION]` | Check current p95 list size | Data |

## 8. Acceptance gate
- [x] One playbook loaded (api-design); topic ∈ enum; no bleed
- [x] Claims tagged; single Alfa-core family
- [x] Each `[ASSUMPTION]` has a verification step
- [x] Every recommendation names a rejected alternative + cost
- [x] Scenario uses number + unit (p95 < 250 ms)
- [x] No invented prices
- [x] Revisit trigger: partners demand many fine-grained versions
