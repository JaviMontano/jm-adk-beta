<!-- distilled from alfa skills/infrastructure-design -->
<!-- > -->
# Infrastructure Design

> "There is no cloud. It's just someone else's computer." — Chris Watterston

## TL;DR

Designs hosting topologies, CDN, DNS, SSL/TLS, and load balancing for reliable, performant web apps. Use when architecting deployment infrastructure, optimizing content delivery, or designing for high availability. Output is a topology diagram + IaC templates + validation evidence, not running infra. [DOC]

## Procedure

### Step 1: Discover
- Compute/storage/bandwidth/geo-distribution requirements; quantify, don't guess [SUPUESTO]
- Traffic patterns: peak vs steady-state RPS, p50/p99 latency targets, request mix (static/dynamic/API)
- Current infra: providers, configs, cost baseline (so trade-offs are measurable, not aesthetic) [INFERENCIA]
- Compliance: data residency, sovereignty, certifications (SOC2/ISO/HIPAA) — these can veto a hosting model outright [INFERENCIA]

### Step 2: Analyze
- **Hosting model decision** (see Decisions table). Default to managed/serverless unless a constraint forces otherwise [SUPUESTO]
- CDN strategy: edge locations, cache rules per content type, origin shielding to cut origin load
- DNS architecture: domain structure, TTL by record purpose, failover/health-checked records
- SSL/TLS: managed certs + auto-renewal, HSTS (preload only after staging proof), cert transparency monitoring
- High availability: multi-region vs multi-AZ, health checks, automatic failover, defined RTO/RPO [INFERENCIA]

### Step 3: Execute
- Topology diagram: every component + connection + trust boundary (the diagram is the contract)
- CDN: cache headers per content type, explicit purge mechanism, stale-while-revalidate where safe
- DNS: TTL tuned (low pre-cutover, raise after), CNAME/A/AAAA, health-check routing
- SSL/TLS: auto-renewal (managed certs or ACME); never hand-rolled renewal [SUPUESTO]
- Load balancing: global HTTP(S) LB with backend health checks; pick algorithm per workload (Decisions table)
- IaC templates (Terraform/Pulumi/Firebase config) — no console-only changes

### Step 4: Validate
- SSL/TLS scores A+ on Qualys SSL Labs [DOC]
- CDN serves from edge nearest users (verify via response headers / synthetic checks from multiple regions)
- Failover drills: kill a region, observe actual failover time vs RTO target — not just "config looks right" [INFERENCIA]
- DNS propagation + TTL behavior verified during a staged change, not in prod-first

## Decisions & Trade-offs

| Decision | Default | When to deviate | Trade-off [INFERENCIA] |
|---|---|---|---|
| Hosting model | Serverless (Firebase Hosting + Cloud Functions) | Long-lived connections, custom runtime, heavy CPU → Cloud Run; legacy/stateful → VMs | Serverless = low ops + cold starts + per-invocation cost shape; VMs = full control + full ops burden |
| Regions | Multi-region for global users | Single region only if all users + data residency are co-located | Multi-region = HA + latency wins, but data-sync complexity and higher cost |
| LB algorithm | Round-robin / least-request | Sticky sessions → consistent hashing; uneven backends → least-request | Stickiness hurts even load distribution; pure RR ignores backend health weight |
| Cert management | Managed / ACME auto-renew | Pinned/internal CA only when policy demands | Wildcard = fewer certs but blast radius if key leaks; per-host = rotation overhead |
| Cache TTL | Long for immutable assets (hashed filenames), short/none for HTML | Personalized content → no-store or private | Aggressive caching = speed + cost cut, but stale risk without versioning |

## Quality Criteria

- [ ] Topology diagram covers all components, connections, and trust boundaries
- [ ] CDN config optimizes cache hit ratio for target audience (state the target %)
- [ ] SSL/TLS scores A+ on Qualys SSL Labs
- [ ] IaC enables reproducible deployments (clean-clone apply reproduces the topology)
- [ ] Failover tested with a measured RTO, not assumed
- [ ] Evidence tags applied to all non-obvious claims

## Anti-Patterns & Failure Modes

- Manual infra changes outside IaC → drift; the diagram lies and recovery is undocumented
- Single-region deployment for globally distributed users → latency + single point of failure
- Wildcard SSL without key rotation → one leaked key compromises every subdomain
- High DNS TTL discovered *during* an incident → failover blocked for the TTL window; lower TTL **before** cutover
- HSTS preload before staging proof → a cert/config mistake locks users out with no quick rollback [INFERENCIA]
- Health checks that probe the LB, not the actual dependency (DB/cache) → "healthy" backend serving 500s
- No origin shield → CDN cache miss storm hammers origin on purge or cold cache [INFERENCIA]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [SUPUESTO]
- English-language output unless otherwise specified [DOC]
- Does not replace domain-expert judgment for final decisions [DOC]
- Designs topology + IaC; does **not** provision, run live migrations, or manage secrets — those are separate, gated steps [SUPUESTO]
- Cost figures are relative/structural, never absolute prices — pricing is provider- and contract-specific [INFERENCIA]
- Out of scope: application-layer security logic, app code, and data modeling (→ `security-architecture`, owning app skills) [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding; do not assume traffic/geo |
| Conflicting requirements (e.g. residency vs multi-region) | Flag conflict explicitly, propose resolution, mark `[SUPUESTO]` until confirmed |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No cost baseline available | Proceed with relative trade-offs; flag cost claims `[SUPUESTO]` + name verification step |
| Compliance vetoes default model | Re-run Step 2 hosting decision under the binding constraint, don't bolt on after |
| Single-region mandated by constraint | Document the accepted HA risk explicitly; add health checks + fast restore as compensating control |

## Related Skills

- `caching-strategy` — CDN caching is part of overall cache architecture
- `performance-architecture` — infrastructure impacts Core Web Vitals
- `security-architecture` — infrastructure security controls and hardening

## Usage

Example invocations:

- "/infrastructure-design" — Run the full infrastructure design workflow
- "infrastructure design on this project" — Apply to current context

**Worked example.** Global SPA, ~500 RPS peak, p99 < 200ms, EU+US users, GDPR residency for EU PII.
→ Hosting: Firebase Hosting (static) + Cloud Functions (API), Cloud Run for the one long-poll service.
→ CDN: immutable hashed assets cached 1y; HTML `no-cache`; origin shield on.
→ DNS: TTL 60s pre-cutover (raise to 3600s after stable), health-checked failover records.
→ HA: multi-region US+EU, EU PII pinned to EU region; LB least-request; failover drill confirms RTO < 60s.
→ TLS: managed certs, A+ target, HSTS added only after a staging soak. [INFERENCIA]
