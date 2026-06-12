<!-- distilled from alfa skills/ssl-management -->
<!-- > -->
# Ssl Management
> "Method over hacks."
## TL;DR
TLS certificate lifecycle: issuance, auto-renewal, HSTS, and (sparingly) pinning. Goal is zero unplanned expiries and no downgrade paths. [DOC]

## Scope & Anti-Scope
- In: cert issuance/renewal (ACME), chain assembly, HSTS rollout, OCSP stapling, pinning decisions, expiry monitoring. [DOC]
- Out: WAF/CDN config, mTLS client-auth design, secrets-manager internals, DNS registrar ops — redirect to the owning skill. [SUPUESTO]

## Procedure
### Step 1: Discover
- Inventory hosts, SANs, current issuer, expiry dates, and renewal mechanism (ACME vs manual). [CONFIG]
- Confirm the ACME challenge type in use: HTTP-01 (port 80 reachable) or DNS-01 (registrar API token). Wildcards require DNS-01. [DOC]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV. [DOC]
- Decide renewal lead time: renew at <=30 days remaining; 90-day certs leave margin for 1–2 retry windows. [INFERENCIA]
- Pinning trade-off: HPKP/pin only with a backup pin and a kill plan — a lost pinned key bricks clients until cache expiry. Default OFF. [SUPUESTO]
### Step 3: Execute
- Issue/renew, then assemble the **full chain** (leaf + intermediates), not just the leaf. Enable OCSP stapling. [CONFIG]
- HSTS: ramp `max-age` (300 → 86400 → 31536000); add `includeSubDomains`/`preload` only after every subdomain is HTTPS. [DOC]
### Step 4: Validate
- Verify chain, expiry, protocol floor (TLS 1.2+), and that renewal is automated and idempotent. [CONFIG]

## Quality Criteria
- [ ] Full chain served; no missing-intermediate errors
- [ ] Auto-renewal proven (dry-run or forced renew succeeds)
- [ ] Expiry alerting at <=21 days, independent of the renewer
- [ ] TLS 1.2+ only; weak ciphers disabled
- [ ] Evidence tags applied; Constitution-compliant; actionable output

## Worked Example
Wildcard `*.app.example` on Nginx: DNS-01 via registrar token → certbot renews at 30d via cron/systemd-timer → deploy hook reloads Nginx → `fullchain.pem` served with stapling → external monitor pings expiry weekly. [SUPUESTO]

## Usage

Example invocations:

- "/ssl-management" — Run the full ssl management workflow
- "ssl management on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [SUPUESTO]
- Requires English-language output unless otherwise specified. [SUPUESTO]
- Does not replace domain expert judgment for final decisions. [SUPUESTO]
- Renewal automation needs persistent credentials (ACME account key, DNS token) the runner can reach. [SUPUESTO]

## Edge Cases & Failure Modes

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Renewal silently failing | Alert on expiry independently; never trust the renewer's own logs alone [INFERENCIA] |
| Missing intermediate cert | Serve full chain; mobile/old clients fail without it even when browsers pass [DOC] |
| Clock skew on host | Reject; cert `notBefore`/`notAfter` checks break under bad NTP [INFERENCIA] |
| Pinned key lost | Treat as outage; rotate to backup pin, wait out pin max-age [SUPUESTO] |
| HSTS preload regret | Removal is slow (browser-shipped lists); never preload until certain [DOC] |
