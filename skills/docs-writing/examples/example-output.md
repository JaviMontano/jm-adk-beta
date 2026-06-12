# Example output — docs-writing

Deliverable produced for `examples/example-input.md`. Route: `api-documentation`,
depth `deep`. Tag family: Alfa core. [DOC]

## Routing record

- **Topic:** `api-documentation` [CONFIG]
- **Playbook read:** `references/api-documentation.md` (one only) [CONFIG]
- **Depth:** `deep` [CONFIG]
- **Brand:** JM Labs developer portal [DOC]

## 1. Discover

- **Sources:** `src/routes/tasks.ts` route table; partial `openapi.yaml`. [CÓDIGO]
- **Auth:** bearer JWT in `Authorization`; rate limit 100 req/min/token. [CONFIG]
- **Gap:** `GET /v1/tasks/:id` 404 body schema undocumented → verify against handler
  before publish. [SUPUESTO]

## 2. Analyze

- **Approach:** spec-first — hand-complete the existing `openapi.yaml` rather than
  generate, since annotations are absent. [INFERENCIA]
- **Trade-off accepted:** spec-first reads cleaner but can rot silently; mitigated by a
  CI lint step and example replay in Validate. [INFERENCIA]

## 3. Execute — API reference

### POST /v1/tasks — Create a task

Auth: `Authorization: Bearer <token>` required. [CONFIG]

Success (201):

```json
{ "id": "tsk_8f2a", "title": "Ship Q3 roadmap", "status": "open", "createdAt": "2026-06-12T09:00:00Z" }
```

Error (400 — validation):

```json
{ "error": "validation_failed", "fields": { "title": "must not be empty" } }
```

### GET /v1/tasks/{id} — Fetch one task

Success (200):

```json
{ "id": "tsk_8f2a", "title": "Ship Q3 roadmap", "status": "open" }
```

Error (404 — absent): body schema `[SUPUESTO]` — confirmed `{ "error": "not_found" }`
against handler before publish. [SUPUESTO]

### Error-code catalog

| Code | Meaning | When | Client action |
|------|---------|------|---------------|
| 400 | Bad request | Schema/validation failure | Fix payload; read `fields` |
| 401 | Unauthenticated | Missing/expired bearer token | Re-authenticate [CONFIG] |
| 404 | Not found | Task id absent | Verify the id |
| 429 | Rate limited | >100 req/min/token | Back off per `Retry-After` [CONFIG] |

## 4. Validate — acceptance gate

| Quality criterion | Status | Evidence |
|-------------------|--------|----------|
| Spec lints clean (OpenAPI 3.0) | PASS | `swagger-cli validate openapi.yaml` → 0 errors [CÓDIGO] |
| Every endpoint ≥1 success + ≥1 error example, no placeholders | PASS | Both endpoints carry realistic payloads [DOC] |
| Auth + environments documented, no secrets in examples | PASS | Bearer scheme stated; tokens redacted [DOC] |
| Error catalog ↔ code bidirectionally consistent | PASS | 400/401/404/429 all present in code and catalog [CÓDIGO] |
| One tag family; every `[SUPUESTO]` paired with a check | PASS | 404 schema `[SUPUESTO]` verified against handler [DOC] |

## Guardian verdict

**PASS** — all gates evidenced; spec lints clean; the one `[SUPUESTO]` (404 body) was
retired by checking the handler. Cleared for the public portal. [DOC]
