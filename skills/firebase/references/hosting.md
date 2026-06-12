<!-- distilled from alfa skills/firebase-hosting -->
# Firebase Hosting

> "Deployment should be boring — if it's exciting, something is wrong." — Unknown

## TL;DR

Configure and deploy Firebase Hosting: SPA rewrite rules, security/cache headers, preview channels for PR review, multi-site targets, and CDN cache control to Firebase's global edge. Use when shipping static sites or SPAs; for SSR/dynamic content, rewrite to Cloud Run or Cloud Functions instead. [DOC]

## Scope & Anti-Scope

- IN: static assets, SPA routing, header policy, preview channels, multi-site, custom domains. [DOC]
- OUT: server-side rendering logic (delegate to Cloud Run/Functions), backend auth, database rules, build pipeline internals. [SUPUESTO] → confirm framework before assuming static output.

## Procedure

### Step 1: Discover
- Read existing `firebase.json` `hosting` block and `.firebaserc` targets. [CONFIG]
- Identify routing needs: SPA fallback, API proxy, Cloud Run/Functions rewrite.
- Determine multi-site needs (main, admin, docs) and their build output dirs.
- Review deploy workflow: manual, CI/CD, preview channels.

### Step 2: Analyze
- Plan rewrites: order matters — specific routes BEFORE the `**` catch-all, else the SPA fallback shadows them. [INFERENCIA]
- Design headers: security (HSTS, X-Frame-Options, CSP) + cache (immutable hashed assets vs revalidated HTML).
- Decide preview-channel TTL and expiry policy for PR flows.
- Define CDN invalidation: rely on content-hashed filenames over manual purge. [INFERENCIA]

### Step 3: Execute
- Set `public` dir + `ignore` patterns (`firebase.json`, `**/.*`, `**/node_modules/**`).
- SPA fallback: `{"source": "**", "destination": "/index.html"}` — keep it LAST.
- Function/Run proxy: `{"source": "/api/**", "function": "api"}` or `"run": {"serviceId": "..."}`.
- Headers: see worked example below.
- Preview: `firebase hosting:channel:deploy pr-123 --expires 7d`.
- Multi-site: `firebase target:apply hosting admin my-admin-site`, then per-target `firebase.json` entries.
- Custom domain: add in Console, then point DNS; SSL auto-provisions.

### Step 4: Validate
- Deploy to a preview channel; click through every route incl. deep links + hard refresh on a sub-route (catches missing SPA fallback). [INFERENCIA]
- Scan headers with securityheaders.com (target grade A) and `curl -I`.
- Verify `cache-control` differs: hashed assets `immutable`, HTML `no-cache`/short.
- Confirm custom-domain SSL is `ACTIVE`, not `PENDING`, before promoting to live.

## Worked Example — firebase.json

```json
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      { "source": "/api/**", "function": "api" },
      { "source": "**", "destination": "/index.html" }
    ],
    "headers": [
      {
        "source": "**/*.@(js|css|woff2)",
        "headers": [{ "key": "Cache-Control", "value": "public,max-age=31536000,immutable" }]
      },
      {
        "source": "/index.html",
        "headers": [{ "key": "Cache-Control", "value": "no-cache" }]
      },
      {
        "source": "**",
        "headers": [
          { "key": "X-Frame-Options", "value": "DENY" },
          { "key": "X-Content-Type-Options", "value": "nosniff" },
          { "key": "Strict-Transport-Security", "value": "max-age=31536000; includeSubDomains" }
        ]
      }
    ]
  }
}
```

Decision: hash-and-cache-forever for assets, never-cache for `index.html`, so a deploy is atomic — new HTML references new hashed assets, and stale HTML is never served past one revalidation. Trade-off: an extra revalidation round-trip on HTML for guaranteed freshness. [INFERENCIA]

## Quality Criteria

- [ ] SPA fallback rule present and ordered LAST among rewrites. [CONFIG]
- [ ] Security headers (HSTS, X-Frame-Options, X-Content-Type-Options; CSP where feasible) set. [CONFIG]
- [ ] Hashed assets `max-age=31536000, immutable`; `index.html` not long-cached. [CONFIG]
- [ ] Preview channel used before any production promote. [DOC]
- [ ] Custom domain SSL status `ACTIVE` prior to live cutover. [DOC]
- [ ] Every non-obvious claim carries one Alfa-set tag (EN spelling). [DOC]

## Anti-Patterns

- Deploying straight to production with no preview channel. [DOC]
- Catch-all `**` rewrite placed before specific API/function routes — shadows them. [INFERENCIA]
- Long-caching `index.html` → users pinned to a stale build after deploy. [INFERENCIA]
- Serving SSR content from static Hosting without Cloud Run/Functions. [DOC]
- Relying on manual CDN purge instead of content-hashed filenames. [INFERENCIA]

## Failure Modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Sub-route 404 on hard refresh | Missing/last-ordered SPA fallback absent | Add `**` → `/index.html` as final rewrite. [INFERENCIA] |
| Stale app after deploy | `index.html` long-cached at CDN/browser | Set HTML `no-cache`; keep assets hashed. [INFERENCIA] |
| `/api/**` returns the SPA shell | Catch-all rewrite precedes the function rewrite | Reorder: specific routes first. [INFERENCIA] |
| SSL stuck `PENDING` | DNS records not propagated / wrong values | Verify A/TXT records; wait for propagation before cutover. [SUPUESTO] |
| securityheaders.com grade low | Headers omitted or scoped to wrong `source` | Broaden `source` glob; add missing headers. [CONFIG] |

## Related Skills

- `firebase-setup` — hosting is part of project initialization.
- `firebase-deployment` — production release workflows.

## Usage

- "/firebase-hosting" — run the full hosting workflow.
- "firebase hosting on this project" — apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, configs, build output). [SUPUESTO]
- English-language output unless otherwise specified. [DOC]
- Assumes a static or hash-versioned build; SSR is out of scope here. [SUPUESTO] → confirm framework output before deploy.
- Does not replace domain-expert judgment for final decisions. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding. |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. |
| Out-of-scope (SSR/backend) request | Redirect to Cloud Run/Functions or appropriate skill. |
| Multiple build outputs, one project | Define per-target `firebase.json` entries via `target:apply`. |
| Monorepo with shared assets | Set `public` per target; avoid cross-target `ignore` leaks. [INFERENCIA] |
