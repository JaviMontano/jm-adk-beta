<!-- distilled from alfa skills/caching-strategy -->
<!-- Firebase Hosting CDN cache headers. Firestore offline persistence. Client-side cache (localStorage/IndexedDB). [EXPLICIT] -->
# caching-strategy {Backend} (v1.1)
> "There are only two hard things in computer science: cache invalidation and naming things." — Phil Karlton

## TL;DR
Design a layered cache for Firebase/Google apps: CDN edge (Hosting `Cache-Control`), client (localStorage/IndexedDB, Firestore offline persistence), and function-level memoization. Use when pages re-fetch unchanged data, server round trips dominate latency, or read costs are high. Optimize for correctness first (no stale critical data), then hit rate. [EXPLICIT]
**Scope:** read-path caching + invalidation. **Anti-scope:** write consistency, DB schema, auth (see `system-architecture`, `api-design`). [EXPLICIT]

## Core Principles
1. **Law of Layers:** Cache at the cheapest layer that can serve it — edge > client > function. Each layer needs its own TTL + invalidation. [EXPLICIT]
2. **Law of Invalidation:** Every cached entry has a defined expiry AND an explicit bust path (key version, tag, or purge). Never cache without an exit. [EXPLICIT]
3. **Law of Freshness Tiers:** Classify data as static (immutable assets), semi-static (config, catalogs), or live (user/session). TTL and layer follow the tier. [EXPLICIT]
4. **Law of Safe Defaults:** Authenticated/personalized responses are `private, no-store` unless proven cacheable — never leak one user's data via shared cache. [EXPLICIT]

## Core Process
### Phase 1: Classify & Design
1. Inventory read paths; tag each by freshness tier and read volume. [EXPLICIT]
2. Pick layer + key + TTL per path. Hashed/fingerprinted assets → `max-age=31536000, immutable`; HTML/API → short `max-age` + `stale-while-revalidate`. [EXPLICIT]
3. Define invalidation: content-hash filenames (auto-bust), cache keys with a version segment, or explicit purge on write. [EXPLICIT]
4. Decide offline scope: enable Firestore persistence only for collections that tolerate eventual consistency. [EXPLICIT]

### Phase 2: Implement
1. Firebase Hosting `firebase.json` `headers`: long `Cache-Control` for `/static/**` immutable assets; `no-cache` for `index.html` so deploys propagate. [EXPLICIT]
2. Client cache: localStorage for small/sync config; IndexedDB for large/structured data; store `{value, expiresAt}` and check expiry on read. [EXPLICIT]
3. Firestore offline: `enableIndexedDbPersistence()` once at init; treat cache hits as possibly stale via snapshot `metadata.fromCache`. [EXPLICIT]
4. Function memoization: cache hot reads in a module-scope map keyed by input; bound size; reset on cold start (acceptable for non-critical data). [EXPLICIT]

### Phase 3: Validate & Deploy
1. Emulator: confirm headers and offline reads via Firebase Emulator Suite. [EXPLICIT]
2. Verify cache hit/miss via response `Age`/`X-Cache` headers and Firestore `fromCache` flag. [EXPLICIT]
3. Deploy (`firebase deploy --only hosting,functions`); confirm a fresh deploy invalidates HTML but keeps fingerprinted assets cached. [EXPLICIT]

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Read-path inventory | Text/Spec | Yes | Endpoints/queries + freshness tier + volume |
| Consistency constraints | Text | Yes | What must never be stale |

| Output | Type | Description |
|--------|------|-------------|
| Cache policy | Config/Doc | Per-path layer, key, TTL, invalidation rule |
| `firebase.json` headers | Config | CDN `Cache-Control` block |

## Validation Gate
- [ ] Every cached path has a TTL AND an invalidation path
- [ ] Fingerprinted assets `immutable`; `index.html` `no-cache`
- [ ] No authenticated/personalized data in a shared/CDN cache (`private`/`no-store`)
- [ ] Firestore `fromCache` handled in UI for offline-tolerant reads
- [ ] Emulator confirms headers + offline behavior
- [ ] No AWS/Azure services (R-002)

## 5. Self-Correction Triggers
> [!WARNING]
> IF a cached entry has no expiry or bust path THEN add a versioned key or explicit purge.
> IF `index.html` is cached long-lived THEN set `no-cache` so deploys propagate.
> IF a personalized response is publicly cacheable THEN switch to `private, no-store`.
> IF stale data breaks a critical flow THEN drop to a live (uncached) read for that path.

## Anti-Patterns
- Long `max-age` on un-fingerprinted HTML → users stuck on old builds after deploy. [EXPLICIT]
- Caching authenticated responses on a shared CDN → cross-user data leak. [EXPLICIT]
- Unbounded in-memory function cache → memory growth, cold-start inconsistency. [EXPLICIT]
- Treating Firestore `fromCache` hits as guaranteed-fresh. [EXPLICIT]

## Related Skills
- `performance-architecture` — CDN/browser caching reduces server round trips
- `system-architecture` — placement of cache layers in the topology
- `api-design` — `Cache-Control`/`ETag`/`Vary` contract on responses

## Usage
Example invocations:
- "/caching-strategy" — Run the full caching strategy workflow
- "caching strategy on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes Firebase Hosting + Firestore stack; non-Firebase CDNs need header mapping [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements (freshness vs. hit rate) | Flag conflict; default to correctness, propose tiered TTL |
| Personalized + high-volume read | Cache client-side per user; keep CDN `private` |
| Offline write then reconnect | Defer to Firestore conflict resolution; do not cache writes |
| Out-of-scope request | Redirect to appropriate skill or escalate |
