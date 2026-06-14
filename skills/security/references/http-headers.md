<!-- distilled from alfa skills/http-headers -->
<!-- > -->
# Http Headers
> "Method over hacks."
## TL;DR
Audit and harden HTTP response headers: security (CSP, HSTS, frame/MIME), caching, compression, content negotiation. Output a per-header verdict (present/missing/misconfigured) with evidence tags and a concrete fix. [DOC]

## Procedure
### Step 1: Discover
- Capture live response headers (`curl -sI <url>`) and the config that sets them (server block, middleware, CDN/edge rules). [CONFIG]
- Note scheme (HTTPS required for HSTS), asset vs API routes (caching differs), and whether a CDN rewrites headers downstream.
### Step 2: Analyze
- Score each header below against its baseline. Per Constitution XIII/XIV, prefer the standard directive over a custom workaround. [DOC]
### Step 3: Execute
- Emit the corrected header value + the exact config location to change it; tag `[CÓDIGO]`/`[CONFIG]` only when checkable in-repo, else `[SUPUESTO]`.
### Step 4: Validate
- Re-fetch; confirm header present, value exact, and no duplicate/conflicting emission from app + edge.

## Baselines
| Header | Baseline value | Why |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Force HTTPS; add `preload` only if eligible. HTTPS-only. [DOC] |
| `Content-Security-Policy` | start `default-src 'self'`; tighten | Blocks XSS/injection; ship `Report-Only` first. [DOC] |
| `X-Content-Type-Options` | `nosniff` | Stops MIME sniffing. [DOC] |
| `X-Frame-Options` / CSP `frame-ancestors` | `DENY` or `frame-ancestors 'none'` | Clickjacking. CSP supersedes the legacy header. [INFERENCIA] |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limits referrer leakage. [DOC] |
| `Cache-Control` (static, hashed) | `public, max-age=31536000, immutable` | Long-cache fingerprinted assets. [DOC] |
| `Cache-Control` (HTML/API) | `no-store` or `private, no-cache` | Prevents stale/leaked dynamic data. [DOC] |
| `Vary` | `Accept-Encoding` (+ `Accept`/`Origin` as used) | Correct cache keying under negotiation. [DOC] |

## Decisions & trade-offs
- CSP nonces/hashes over `'unsafe-inline'`: stronger XSS defense, costs build wiring — accept the cost on auth/payment surfaces. [INFERENCIA]
- HSTS `preload`: irreversible for months; only with full-subdomain HTTPS confidence. [SUPUESTO] → verify every subdomain serves HTTPS before submitting.
- Compression (`gzip`/`br`): exclude already-compressed bodies; never compress secret-bearing responses that also reflect user input (BREACH). [DOC]

## Quality Criteria
- [ ] Evidence tags applied (Alfa core set, one per claim, consistent spelling)
- [ ] Constitution-compliant; standard directive over workaround
- [ ] Each finding pairs a verdict with an exact value + config location
- [ ] Re-fetch confirms no duplicate/conflicting headers (app vs edge)

## Usage
Example invocations:
- "/http-headers" — Run the full http headers workflow
- "http headers on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to live responses AND the config that emits them; headers-only audit cannot prove origin. [SUPUESTO]
- Requires English-language output unless otherwise specified. [DOC]
- Scope: response headers. Anti-scope: TLS cipher/cert config, WAF rules, cookie `Secure`/`SameSite` flags (separate skill), request-header validation. [DOC]
- Does not replace domain expert judgment for final CSP policy. [DOC]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Header set twice (app + CDN/edge) | Report both sources; dedupe at the outermost layer |
| HSTS requested on plain HTTP | Invalid — browsers ignore it; fix scheme first [DOC] |
| CSP breaks the app | Ship `Content-Security-Policy-Report-Only`, collect reports, then enforce |
| Header present but empty/malformed | Treat as missing; misconfiguration is not coverage |
