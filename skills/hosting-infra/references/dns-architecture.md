<!-- distilled from alfa skills/dns-architecture -->
<!-- > -->
# Dns Architecture
> "Method over hacks."
## TL;DR
DNS design: record topology, TTL strategy, failover, geo-routing. [EXPLICIT]

## Procedure
### Step 1: Discover
- Inventory zones, registrars, current records, TTLs, and who controls each. [EXPLICIT]
- Capture SLA targets (RTO/RPO) and traffic geography. [EXPLICIT]
### Step 2: Analyze
- Evaluate failover/geo options per Constitution XIII/XIV. [EXPLICIT]
- Map each requirement to a record type + TTL (table below). [EXPLICIT]
### Step 3: Execute
- Stage changes; lower TTL ahead of any cutover (see Decisions). [EXPLICIT]
### Step 4: Validate
- `dig +trace`, resolve from ≥2 geos, confirm propagation before raising TTL. [EXPLICIT]

## Record & TTL Strategy
| Need | Record | TTL | Note |
|------|--------|-----|------|
| Apex → host | A / AAAA or ALIAS | 300–3600s | Apex CNAME is invalid; use ALIAS/ANAME or A. [EXPLICIT] |
| Subdomain → host | CNAME | 3600s | Never on apex. [EXPLICIT] |
| Failover/geo (managed) | provider routing policy | 30–60s | Short TTL = faster failover, more queries. [EXPLICIT] |
| Mail | MX + SPF/DKIM/DMARC (TXT) | 3600s | Missing SPF/DMARC → spoofing + spam-folder. [EXPLICIT] |
| Cutover window | any | 60–300s | Lower 24–48h before; raise after verify. [EXPLICIT] |

## Decisions & Trade-offs
- **Low TTL (30–60s)** for failover targets: faster recovery, higher query volume/cost. Default 300s elsewhere. [EXPLICIT]
- **DNS failover vs. anycast/LB**: DNS failover is cheap but bounded by resolver TTL caching (clients may hold stale records past TTL); anycast/global LB fails over in-network, faster but costlier. Pick per RTO. [EXPLICIT]
- **Geo-routing (latency vs. geolocation)**: latency-based optimizes speed; geolocation enforces data-residency/compliance. Don't conflate. [EXPLICIT]
- **CAA records** pin allowed CAs — set before relying on auto-issued certs. [EXPLICIT]

## Worked Example — active/passive failover
1. Health-checked primary A → 198.51.100.10, TTL 60. [EXPLICIT]
2. Secondary A → 203.0.113.10 as failover target, same TTL. [EXPLICIT]
3. Provider health check on primary; on fail, serve secondary. [EXPLICIT]
4. Expected recovery ≈ TTL + check interval (~2–3 min), not instant. [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Apex uses A/ALIAS (never CNAME); CAA + SPF/DKIM/DMARC present
- [ ] TTLs match cutover/failover intent; propagation verified from ≥2 geos

## Usage
Example invocations:
- "/dns-architecture" — Run the full dns architecture workflow
- "dns architecture on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes registrar/DNS-provider credentials are available to apply changes [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Out of scope: DNSSEC signing operations and registrar transfers [EXPLICIT]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Apex CNAME requested | Reject; use A/ALIAS — apex CNAME breaks NS/SOA/MX. [EXPLICIT] |
| Stale records after cutover | Resolvers cached old TTL; wait out prior TTL, don't re-edit. [EXPLICIT] |
| Failover slower than expected | Recovery ≥ TTL + check interval; lower TTL or use LB. [EXPLICIT] |
| Mail deliverability drops | Verify SPF/DKIM/DMARC alignment before blaming MX. [EXPLICIT] |
