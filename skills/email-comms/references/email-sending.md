<!-- distilled from alfa skills/email-sending -->
<!-- > -->
# Email Sending

> "Email deliverability is a reputation game — earn it, don't burn it." — Unknown

## TL;DR

Guides email sending infrastructure setup — configuring providers like SendGrid or Mailgun, building template-based transactional emails, managing sender reputation, and handling bounces and complaints. Use when your application needs to send automated emails (verification, receipts, notifications, marketing). [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify email types needed (transactional, marketing, notification)
- Check existing email infrastructure and provider accounts
- Review sender domain DNS setup (SPF, DKIM, DMARC)
- Determine email volume estimates for provider plan selection

### Step 2: Analyze
- Choose provider: SendGrid (generous free tier), Mailgun (developer-friendly), SES (AWS cost-effective)
- Plan template strategy (provider-hosted templates vs code-generated HTML)
- Design email categories for separate sending domains/IPs if needed
- Evaluate tracking needs (opens, clicks, bounces, unsubscribes)

### Step 3: Execute
- Set up provider account and verify sender domain with DNS records
- Configure SPF, DKIM, and DMARC DNS records for deliverability
- Implement email sending via provider SDK in Cloud Functions
- Create reusable templates with dynamic variable substitution
- Add bounce and complaint webhook handlers to maintain sender reputation
- Implement unsubscribe handling with list-unsubscribe headers
- Set up email logging for debugging delivery issues

### Step 4: Validate
- Send test emails to multiple providers (Gmail, Outlook, Yahoo)
- Check email headers for SPF/DKIM pass with mail-tester.com
- Verify template variables render correctly with test data
- Confirm bounce webhooks update user records appropriately

## Quality Criteria

- [ ] SPF, DKIM, and DMARC DNS records configured and passing
- [ ] Bounce and complaint handling prevents sending to invalid addresses
- [ ] Unsubscribe mechanism compliant with CAN-SPAM / GDPR
- [ ] Email sending uses async processing (doesn't block user requests)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Sending from unverified domains (high spam probability)
- Not handling bounces (destroys sender reputation over time)
- Sending marketing emails without unsubscribe links (legal violation)

## Related Skills

- `email-templates` — HTML template design for these emails
- `cloud-functions` — email sending logic runs in Cloud Functions

## Usage

Example invocations:

- "/email-sending" — Run the full email sending workflow
- "email sending on this project" — Apply to current context


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
