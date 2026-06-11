<!-- distilled from alfa skills/domain-management -->
<!-- > -->
# Domain Management

> "DNS is the phonebook of the internet — misconfigure it, and nobody can find you." — Unknown

## TL;DR

Guides domain management — configuring DNS records (A, CNAME, TXT, MX), setting up nameservers, provisioning SSL certificates, configuring email routing, and managing domain redirects. Use when connecting a custom domain to hosting, setting up email, or troubleshooting DNS issues. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the domain registrar and current DNS configuration
- Check nameserver delegation (registrar default, Cloudflare, hosting provider)
- Review existing DNS records and their purposes
- Determine services requiring DNS configuration (hosting, email, verification)

### Step 2: Analyze
- Plan DNS record requirements per service
- Design subdomain strategy (www, app, api, staging)
- Evaluate SSL certificate options (Let's Encrypt, registrar-provided, Cloudflare)
- Plan email routing (Google Workspace, Zoho, registrar email, forwarding)

### Step 3: Execute
- Configure A/AAAA records pointing to hosting IP addresses
- Set up CNAME records for subdomains (www → apex, app → hosting)
- Add TXT records for domain verification (Google, Firebase, email SPF)
- Configure MX records for email routing with correct priorities
- Set up SPF, DKIM, and DMARC TXT records for email authentication
- Provision SSL certificate and configure HTTPS redirect
- Add CAA records to restrict certificate authority issuance
- Set TTL appropriately (low during migration, high for stable records)

### Step 4: Validate
- Verify DNS propagation with `dig` or dnschecker.org
- Confirm SSL certificate is valid and covers all subdomains
- Test email delivery with configured MX records
- Check SPF/DKIM/DMARC pass with mail-tester.com

## Quality Criteria

- [ ] All required DNS records configured and propagated
- [ ] SSL certificate valid for apex domain and www subdomain
- [ ] SPF, DKIM, and DMARC records configured for email authentication
- [ ] DNS TTL set appropriately for stability
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using low TTL permanently (increases DNS query load without benefit)
- Forgetting to set up www redirect (users type it, and it should work)
- Not configuring DMARC (email spoofing protection)

## Related Skills

- `hostinger-deployment` — domain DNS for Hostinger-hosted sites
- `email-sending` — DNS records required for email deliverability

## Usage

Example invocations:

- "/domain-management" — Run the full domain management workflow
- "domain management on this project" — Apply to current context


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
