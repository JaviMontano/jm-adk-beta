# Example input — docs-writing

Scenario handed to the router by a backend team. [DOC]

## Request

> "We shipped a small Tasks API. Here are the route definitions from our Express app and
> a partial `openapi.yaml`. Generate the developer-facing API reference: endpoint docs
> with request/response examples, the auth scheme, and an error-code catalog. Depth:
> deep — this goes on our public developer portal."

## Provided artifacts

Route definitions (`src/routes/tasks.ts`):

```ts
router.post("/v1/tasks", requireBearer, createTask);   // 201, 400, 401, 429
router.get("/v1/tasks/:id", requireBearer, getTask);   // 200, 401, 404
```

Partial spec (`openapi.yaml`):

```yaml
openapi: 3.0.3
info:
  title: Tasks API
  version: 1.0.0
servers:
  - url: https://api.example.com
```

Auth: bearer JWT in `Authorization` header. Rate limit: 100 req/min per token. [CONFIG]

## Expected routing

- **Topic:** `api-documentation` (output noun = API reference). [CONFIG]
- **Depth:** `deep` (public portal → publication-grade). [CONFIG]
- **Gap to flag:** `getTask` 404 body schema is undocumented → `[SUPUESTO]`, verify
  against handler. [SUPUESTO]
