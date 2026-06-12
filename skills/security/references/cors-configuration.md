<!-- distilled from alfa skills/cors-configuration -->
<!-- > -->
# Cors Configuration
> "Method over hacks."
## TL;DR
CORS policies, preflight handling, credentials, origin whitelisting. CORS is a browser-enforced read-protection on cross-origin responses; it is NOT authentication, NOT a server-side firewall, and does nothing against non-browser clients (curl, server-to-server). [EXPLICIT]

## Procedure
### Step 1: Discover
- Enumerate every legitimate origin (prod, staging, preview deploys, localhost ports) and whether requests carry credentials (cookies, `Authorization`, TLS client certs). [DOC]
### Step 2: Analyze
- Choose origin strategy per Constitution XIII/XIV; map which routes need credentials vs. public read. [INFERENCIA]
### Step 3: Execute
- Emit `Access-Control-Allow-Origin` by reflecting a *validated* origin from an allowlist; set `Vary: Origin` so caches don't serve one origin's header to another. [EXPLICIT]
### Step 4: Validate
- Test preflight (`OPTIONS`) and actual request from an allowed AND a disallowed origin; confirm credentials path. [EXPLICIT]

## Decisions & Trade-offs
| Decision | Choose when | Cost / risk |
|----------|-------------|-------------|
| Allowlist + reflect origin | Multiple known origins, credentials needed | Must store/validate list; missing `Vary: Origin` causes cache poisoning [DOC] |
| `Origin: *` (wildcard) | Truly public, no credentials | Browser **forbids** `*` with `credentials: include` — request fails [EXPLICIT] |
| Regex origin match | Dynamic preview subdomains | Unanchored regex (`.example.com`) matches `evil-example.com`; anchor `^https://([a-z0-9-]+\.)?example\.com$` [INFERENCIA] |

## Preflight (OPTIONS)
- Triggered by non-simple method/header or custom `Content-Type`. Server must answer 2xx with `Access-Control-Allow-Methods`, `-Allow-Headers`, and `Access-Control-Max-Age` to cache the preflight (e.g. 600s) and cut round-trips. [DOC]
- Auth middleware must let unauthenticated `OPTIONS` through — preflight carries no credentials. [EXPLICIT]

## Credentials rule (hard constraint)
- With `Access-Control-Allow-Credentials: true`: `Allow-Origin` MUST be an exact echoed origin (never `*`), and `Allow-Headers`/`Allow-Methods` likewise cannot be `*`. [EXPLICIT]

## Quality Criteria
- [ ] Allowlist validated server-side; no blind reflection of arbitrary `Origin` [EXPLICIT]
- [ ] `Vary: Origin` present whenever the ACAO header is dynamic [DOC]
- [ ] No `*` paired with credentials [EXPLICIT]
- [ ] Preflight bypasses auth and returns 2xx [EXPLICIT]
- [ ] Evidence tags applied; Constitution-compliant; actionable output

## Usage

Example invocations:

- "/cors-configuration" — Run the full cors configuration workflow
- "cors configuration on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Scope: browser CORS only. Does NOT cover CSRF (use SameSite cookies + tokens), server-side SSRF, or auth — CORS is not a substitute for any of these. [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| `Origin` absent (same-origin / non-browser) | No CORS headers needed; do not fabricate an allow header [INFERENCIA] |
| Disallowed origin | Omit ACAO entirely (browser blocks); do NOT return a 403 that leaks the allowlist [SUPUESTO] |
| Wildcard subdomain previews | Anchor regex; reject look-alike domains [INFERENCIA] |
| Response cached by CDN | Ensure `Vary: Origin` or per-origin cache keys to prevent header bleed [DOC] |
