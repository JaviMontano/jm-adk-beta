<!-- distilled from alfa skills/infrastructure-design -->
<!-- > -->
# Infrastructure Design

> "There is no cloud. It's just someone else's computer." — Chris Watterston

## TL;DR

Designs hosting topologies, CDN configurations, DNS setups, SSL/TLS management, and load balancing strategies for reliable, performant web applications. Use this skill when architecting deployment infrastructure, optimizing content delivery, or designing for high availability. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify hosting requirements: compute, storage, bandwidth, geographic distribution
- Gather traffic patterns: peak loads, geographic distribution, request types
- Review current infrastructure: providers, configurations, costs
- Assess compliance requirements: data residency, sovereignty, certifications

### Step 2: Analyze
- Choose hosting model: serverless (Firebase Hosting + Cloud Functions), containers (Cloud Run), VMs
- Design CDN strategy: edge locations, cache rules, origin shielding
- Plan DNS architecture: domain structure, TTL values, failover records
- Evaluate SSL/TLS: certificate management, HSTS, certificate transparency
- Design for high availability: multi-region, health checks, automatic failover

### Step 3: Execute
- Document infrastructure topology diagram with all components and connections
- Configure CDN with appropriate cache headers and purge mechanisms
- Set up DNS with proper TTL, CNAME/A records, and health check routing
- Implement SSL/TLS with auto-renewal (Let's Encrypt or managed certificates)
- Design load balancing: global HTTP(S) LB with backend health checks
- Create Infrastructure-as-Code templates (Terraform, Pulumi, or Firebase config)

### Step 4: Validate
- Verify SSL/TLS configuration scores A+ on SSL Labs
- Confirm CDN is serving content from edge locations nearest to users
- Test failover scenarios: what happens when a region goes down
- Validate DNS propagation and TTL behavior during changes

## Quality Criteria

- [ ] Infrastructure topology diagram covers all components
- [ ] CDN configuration optimizes cache hit ratio for target audience
- [ ] SSL/TLS scores A+ on Qualys SSL Labs test
- [ ] Infrastructure-as-Code enables reproducible deployments
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Manual infrastructure changes without Infrastructure-as-Code
- Single-region deployment for globally distributed users
- Wildcard SSL certificates without proper key rotation

## Related Skills

- `caching-strategy` — CDN caching is part of overall cache architecture
- `performance-architecture` — infrastructure impacts Core Web Vitals
- `security-architecture` — infrastructure security controls and hardening

## Usage

Example invocations:

- "/infrastructure-design" — Run the full infrastructure design workflow
- "infrastructure design on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
