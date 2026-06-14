<!-- distilled from alfa skills/email-sending -->
<!-- > -->
# Email Sending

> "Email deliverability is a reputation game — earn it, don't burn it." — Unknown

## TL;DR

Guides email sending infrastructure setup — configuring providers like SendGrid or Mailgun, building template-based transactional emails, managing sender reputation, and handling bounces and complaints. Use when your application needs to send automated emails (verification, receipts, notifications, marketing). [EXPLICIT]

## Scope & Anti-Scope

- IN: provider setup, domain auth (SPF/DKIM/DMARC), transactional + marketing send, templating, bounce/complaint/unsubscribe handling, deliverability validation. [EXPLICIT]
- OUT: HTML template design (→ `email-templates`), inbox/IMAP receiving, SMS/push, CRM segmentation logic, content/copywriting. [INFERENCE]
- Single brand per sending domain — never co-mingle brands on one IP/domain. [ASSUMPTION]

## Procedure

### Step 1: Discover
- Identify email types needed (transactional, marketing, notification) — they have different reputation rules and should not share a sending domain. [INFERENCE]
- Check existing email infrastructure and provider accounts.
- Review sender domain DNS setup (SPF, DKIM, DMARC).
- Estimate email volume (peak/day + burst) to size the provider plan and decide shared vs dedicated IP. [INFERENCE]

### Step 2: Analyze
- Choose provider: SendGrid (generous free tier), Mailgun (developer-friendly), SES (AWS cost-effective). Decision driver = existing cloud + volume, not headline pricing. [INFERENCE]
- Dedicated IP only at sustained volume (provider guidance ~ tens of thousands/month); below that a shared IP has better warmed reputation. [ASSUMPTION → confirm against provider docs for chosen vendor]
- Plan template strategy (provider-hosted templates vs code-generated HTML).
- Design email categories for separate sending domains/subdomains/IPs if needed (e.g. `mail.` for marketing, `txn.` for transactional). [INFERENCE]
- Evaluate tracking needs (opens, clicks, bounces, unsubscribes) against privacy/GDPR consent. [EXPLICIT]

### Step 3: Execute
- Set up provider account and verify sender domain with DNS records.
- Configure SPF, DKIM, and DMARC. Start DMARC at `p=none` to monitor, then move to `quarantine`/`reject` once aligned — never publish `reject` before DKIM/SPF pass. [ASSUMPTION → verify via DMARC aggregate reports]
- Implement email sending via provider SDK in Cloud Functions; enqueue rather than send inline so a request never blocks on the provider API. [INFERENCE]
- Make sends idempotent — key on (user, event) so retries do not double-send. [INFERENCE]
- Create reusable templates with dynamic variable substitution; escape user-supplied values to prevent HTML/header injection. [INFERENCE]
- Add bounce and complaint webhook handlers to maintain sender reputation; suppress on hard bounce, retry-then-suppress on repeated soft bounce. [INFERENCE]
- Implement unsubscribe handling with `List-Unsubscribe` and `List-Unsubscribe-Post` (one-click) headers. [EXPLICIT]
- Set up email logging (message-id, status, provider response) for debugging delivery issues; never log full recipient PII in plaintext. [INFERENCE]

### Step 4: Validate
- Send test emails to multiple providers (Gmail, Outlook, Yahoo) and to a fresh address (cold-inbox placement). [INFERENCE]
- Check email headers for SPF/DKIM/DMARC pass with mail-tester.com; target a clean score before production. [EXPLICIT]
- Verify template variables render correctly with test data, including empty/missing-variable cases.
- Confirm bounce/complaint webhooks update user records and suppression list appropriately.
- Send a one-click unsubscribe and confirm the address is suppressed on the next send. [INFERENCE]

## Worked Example: verification email on SES

1. Subdomain `txn.app.example.com`; publish SPF (`include:amazonses.com`), DKIM (3 CNAMEs from SES), DMARC `p=none; rua=...`. [EXPLICIT]
2. Cloud Function consumes a `user.signup` queue message, renders the template, calls SES `SendEmail` with an idempotency key = signup id. [INFERENCE]
3. SES SNS topic → webhook: `Bounce`/`Complaint` add the address to a suppression table; `Delivery` updates the log row. [INFERENCE]
4. After a week of clean `rua` reports, raise DMARC to `quarantine`. [ASSUMPTION → gated on report review]

## Quality Criteria

- [ ] SPF, DKIM, and DMARC DNS records configured and passing (DMARC alignment confirmed via aggregate reports). [EXPLICIT]
- [ ] Bounce and complaint handling maintains a suppression list and prevents sending to invalid addresses. [EXPLICIT]
- [ ] Unsubscribe mechanism compliant with CAN-SPAM / GDPR, including one-click `List-Unsubscribe-Post`. [EXPLICIT]
- [ ] Email sending uses async/queued processing (doesn't block user requests). [EXPLICIT]
- [ ] Sends are idempotent; retries do not duplicate. [INFERENCE]
- [ ] No recipient PII in plaintext logs. [INFERENCE]
- [ ] Evidence tags applied to all claims. [EXPLICIT]

## Anti-Patterns

- Sending from unverified domains (high spam probability). [EXPLICIT]
- Not handling bounces (destroys sender reputation over time). [EXPLICIT]
- Sending marketing emails without unsubscribe links (legal violation). [EXPLICIT]
- Publishing DMARC `p=reject` before DKIM/SPF align — silently drops legitimate mail. [INFERENCE]
- Blasting a cold dedicated IP at full volume without warm-up. [INFERENCE]
- Mixing transactional and marketing on one domain — a marketing complaint then poisons receipts. [INFERENCE]

## Failure Modes

| Symptom | Likely cause | Action |
|---------|-------------|--------|
| Mail lands in spam | DKIM/DMARC not aligned, or cold IP | Re-check alignment; warm IP gradually |
| Sudden delivery drop | Complaint spike / blocklist | Pause sends, inspect feedback loop, delist |
| Duplicate emails | Non-idempotent retry | Add idempotency key on (user, event) |
| Request latency on signup | Inline send | Move send to queue/worker |

## Related Skills

- `email-templates` — HTML template design for these emails
- `cloud-functions` — email sending logic runs in Cloud Functions

## Usage

Example invocations:

- "/email-sending" — Run the full email sending workflow
- "email sending on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Provider-specific thresholds (dedicated-IP volume, warm-up schedule) must be confirmed against the chosen vendor's current docs. [ASSUMPTION]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No DNS/registrar access | Stop — domain auth is a hard prerequisite, escalate to owner |
| High bounce/complaint rate at launch | Throttle sends, audit list hygiene before scaling |
