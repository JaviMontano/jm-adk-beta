<!-- distilled from alfa skills/domain-management -->
<!-- > -->
# Domain Management

> "DNS is the phonebook of the internet — misconfigure it, and nobody can find you." — Unknown

## TL;DR

Configures DNS (A/AAAA, CNAME, TXT, MX, CAA), nameserver delegation, SSL provisioning, email routing, and redirects. Use when connecting a custom domain to hosting, standing up email, or troubleshooting DNS. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify registrar and where authoritative DNS lives (registrar, Cloudflare, hosting provider) — these can differ. [EXPLICIT]
- Snapshot existing records before any change; note each record's purpose so nothing is silently overwritten. [INFERENCIA]
- Enumerate services needing DNS: hosting, email, domain verification, third-party (CDN, status page). [EXPLICIT]

### Step 2: Analyze
- Map record requirements per service; resolve conflicts (e.g. two services wanting the apex). [INFERENCIA]
- Design subdomain strategy (www, app, api, staging) and which point at apex vs. provider hostnames. [EXPLICIT]
- Choose SSL path (Let's Encrypt auto, registrar-provided, Cloudflare edge) — decision table below. [EXPLICIT]
- Plan email routing (Google Workspace, Zoho, registrar, forwarding) and its SPF/DKIM/DMARC trio. [EXPLICIT]

### Step 3: Execute
- A/AAAA → hosting IPs at apex; AAAA only if the host serves IPv6. [EXPLICIT]
- CNAME for subdomains (`www` → apex, `app` → provider hostname). Never CNAME the apex — see Edge Cases. [DOC]
- TXT for verification (Google, Firebase) and SPF. [EXPLICIT]
- MX with correct priorities (lower = preferred); remove stale MX from prior providers. [DOC]
- SPF + DKIM + DMARC TXT for email auth; DMARC starts at `p=none` for monitoring, then tightens. [DOC]
- Provision SSL, force HTTPS redirect, enable HSTS only after HTTPS is confirmed stable. [INFERENCIA]
- CAA to restrict which CAs may issue; must include the CA your SSL path uses or issuance breaks. [DOC]
- TTL low (300s) during migration, raise (3600s+) once records are stable. [EXPLICIT]

### Step 4: Validate
- `dig +short <record> <host>` and dnschecker.org for propagation across resolvers. [EXPLICIT]
- Confirm cert validity, full chain, and SAN coverage of every served subdomain. [EXPLICIT]
- Send a test email; verify SPF/DKIM/DMARC all pass on mail-tester.com. [EXPLICIT]
- Confirm apex and www both resolve and redirect as designed. [INFERENCIA]

## Worked Examples

Apex + www on a host using an IP, with Google Workspace email: [EXPLICIT]

```dns
@      A      300    203.0.113.10
www    CNAME  300    example.com.
@      MX     3600   1  smtp.google.com.
@      TXT    3600   "v=spf1 include:_spf.google.com ~all"
google._domainkey TXT 3600 "v=DKIM1; k=rsa; p=MIGf...AB"
_dmarc TXT    3600   "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
@      CAA    3600   0 issue "letsencrypt.org"
```

Provider that requires a CNAME at apex (e.g. Netlify/Vercel): use the provider's
ALIAS/ANAME/flattened-CNAME feature, or point apex A at the provider's documented
IP and keep `www` as the CNAME. [DOC]

## Quality Criteria

- [ ] Pre-change record snapshot captured. [DOC]
- [ ] All required records configured and propagated across resolvers. [EXPLICIT]
- [ ] Cert valid with full chain; SAN covers apex + every served subdomain. [EXPLICIT]
- [ ] SPF, DKIM, DMARC present and passing; CAA permits the issuing CA. [DOC]
- [ ] TTL stabilized post-migration. [EXPLICIT]
- [ ] Every non-obvious claim carries exactly one tag. [DOC]

## Decisions & Trade-offs

| Decision | Choice | Trade-off | When to revisit |
|----------|--------|-----------|-----------------|
| SSL source | Let's Encrypt auto | Free, auto-renew; depends on host's ACME support and CAA allowing it | Host lacks ACME, or wildcard needed → registrar/Cloudflare cert [INFERENCIA] |
| Edge proxy | Cloudflare orange-cloud | Hides origin IP, edge SSL; origin cert/host header gotchas, extra hop | Latency-sensitive or origin needs real client IP [INFERENCIA] |
| DMARC policy | Start `p=none` | Safe monitoring; provides no enforcement yet | After ~2 weeks of clean `rua` reports → `quarantine`/`reject` [DOC] |
| Nameservers | Move to Cloudflare | One control plane, fast edits; registrar email/records may break if not migrated first | Registrar offers needed features natively [SUPUESTO] |

## Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Site loads on IP but not domain | A record missing/wrong, or NS not delegated | Verify NS at registrar, then A record [INFERENCIA] |
| Intermittent old vs new site | Stale cache vs. low TTL not yet expired | Wait out the *old* TTL; can't shorten retroactively [DOC] |
| Cert errors on a subdomain | SAN doesn't cover it, or CNAME chain broken | Reissue covering subdomain; verify CNAME target [DOC] |
| `pending issuance` / cert won't issue | CAA blocks the CA | Add/adjust CAA `issue` to permit the CA [DOC] |
| Email to spam / DMARC fail | SPF too strict, DKIM unsigned, or alignment off | Align From domain with SPF/DKIM; check `~all` vs `-all` [DOC] |
| Email silently lost | Stale MX from prior provider still preferred | Remove old MX; confirm priorities [INFERENCIA] |

## Anti-Patterns

- Permanent low TTL — needless query load with no benefit once records are stable. [INFERENCIA]
- No www redirect — users type it and expect it to work. [EXPLICIT]
- No DMARC — leaves the domain spoofable. [DOC]
- Editing live records without a snapshot — no rollback path. [INFERENCIA]
- Jumping straight to DMARC `p=reject` — silently drops legitimate mail. [DOC]

## Anti-Scope

- Does not register or transfer domains, or handle registrar billing. [EXPLICIT]
- Does not configure application-layer routing, load balancers, or WAF rules beyond DNS/SSL. [SUPUESTO]
- Does not manage mailbox/user provisioning inside the email provider. [EXPLICIT]

## Related Skills

- `hostinger-deployment` — domain DNS for Hostinger-hosted sites.
- `dns-architecture` — multi-zone and split-horizon DNS design.
- `ssl-management` — certificate lifecycle and renewal automation.

## Usage

Example invocations:

- "/domain-management" — Run the full workflow.
- "domain management on this project" — Apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Assumes registrar/DNS-provider credentials are available to apply changes. [SUPUESTO]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding. |
| Conflicting requirements (two services want apex) | Flag explicitly; propose subdomain or ALIAS resolution. |
| CNAME requested at apex | Reject raw CNAME; use ALIAS/ANAME/flattening or apex A record. |
| Provider needs CAA but none present | A missing CAA means "any CA"; add one only when restricting. |
| Out-of-scope request | Redirect to the appropriate skill or escalate. |
