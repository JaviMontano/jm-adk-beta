<!-- distilled from alfa skills/cdn-configuration -->
<!-- > -->
# Cdn Configuration
> "Method over hacks."
## TL;DR
CDN setup, cache headers, edge functions, purge strategies. Decide cacheability per route, set explicit `Cache-Control`, version assets for immutable caching, and use targeted purge over global flush. [EXPLICIT]

## Procedure
### Step 1: Discover
- Inventory routes and classify: static (immutable, hashed), dynamic-cacheable (HTML/API with TTL), never-cache (auth, cart, PII). [EXPLICIT]
- Capture current cache hit ratio and origin egress as the baseline to beat. [EXPLICIT]
### Step 2: Analyze
- Choose cache key dimensions (path, query allowlist, `Accept-Encoding`, device/geo only if content actually varies). Over-keying kills hit ratio. [INFERENCIA]
- Decide edge-compute need: redirects/A-B/auth-gate at edge vs origin. Evaluate per Constitution XIII/XIV. [EXPLICIT]
### Step 3: Execute
- Emit explicit headers (see table). Hashed assets → `immutable`; HTML → short TTL + `stale-while-revalidate`. [EXPLICIT]
- Implement purge by surrogate-key/tag, not URL lists, so one content change invalidates all dependent pages. [EXPLICIT]
### Step 4: Validate
- Confirm hit ratio rose and origin egress fell vs baseline; verify no never-cache route is being cached. [EXPLICIT]

## Cache-Control Reference
| Asset class | Header | Rationale |
|-------------|--------|-----------|
| Hashed JS/CSS/img (`app.a1b2.js`) | `public, max-age=31536000, immutable` | Content-addressed; URL changes on edit, so cache forever. [EXPLICIT] |
| HTML / SSR pages | `public, max-age=0, s-maxage=60, stale-while-revalidate=600` | Fresh-ish at edge, instant serve while revalidating. [EXPLICIT] |
| JSON API (cacheable) | `public, s-maxage=30, stale-if-error=86400` | Short edge TTL; survive origin outage. [EXPLICIT] |
| Auth / cart / PII | `private, no-store` | Must never sit in shared edge cache. [EXPLICIT] |

## Decisions & Trade-offs
- **Purge by tag, not URL** — URL purges miss derived pages and race deploys; tag purge is atomic but needs tag emission discipline. [EXPLICIT]
- **`stale-while-revalidate` over hard TTL** — trades possible brief staleness for zero user-facing revalidation latency; reject for inventory/price where stale misleads. [INFERENCIA]
- **Edge compute** — cuts origin round-trips but adds cold-start + harder debugging; use only when origin latency or fan-out justifies it. [SUPUESTO]

## Failure Modes
- `Set-Cookie` on a cacheable response → CDN refuses to cache or leaks one user's cookie to others. Strip before caching. [EXPLICIT]
- `Vary: *` or `Vary: User-Agent` → near-zero hit ratio from key explosion. Vary only on real dimensions. [EXPLICIT]
- Caching `302`/error responses without short TTL → users stuck on a transient redirect/error. [EXPLICIT]
- Global flush on every deploy → origin thundering-herd; prefer tag purge + warming. [EXPLICIT]

## Quality Criteria
- [ ] Every route classified static / dynamic-cacheable / never-cache [EXPLICIT]
- [ ] Explicit `Cache-Control` (and `s-maxage`) emitted; no implicit-default routes [EXPLICIT]
- [ ] Purge keyed by surrogate-tag, verified to invalidate dependents [EXPLICIT]
- [ ] No `no-store` route observed in cache; no `Set-Cookie` on cached responses [EXPLICIT]
- [ ] Hit ratio and origin egress measured against baseline [EXPLICIT]

## Usage

Example invocations:

- "/cdn-configuration" — Run the full cdn configuration workflow
- "cdn configuration on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and to CDN/edge config + analytics. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Anti-scope: does not tune origin app performance, WAF/security rules, or DNS — see `dns-architecture.md` and `ssl-management.md`. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Cannot distinguish cacheable vs private route | Default to `no-store`; never cache on ambiguity [EXPLICIT] |
| Purge/tag API unavailable | Fall back to versioned URLs; document manual flush risk [EXPLICIT] |
