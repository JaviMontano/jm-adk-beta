# Example Output

## 1. Routing decision

- **Request:** Verification emails fail/land in spam; inline send times out the signup request.
- **Resolved topic:** `email-sending`
- **Why this topic:** Symptoms are deliverability (spam placement, missing mail) and send-path architecture (inline blocking) — not HTML render or content. [INFERENCE]
- **Prerequisite sequence:** none (single topic).
- **Depth:** `deep`
- **Playbook read:** `references/email-sending.md`

## 2. Discover

- ~300 signups/day with launch-day bursts — well below dedicated-IP territory, so SES shared IP is fine. [INFERENCE]
- Sending from the root domain with zero authentication published. [CONFIG]
- Send is inline in the Cloud Function, so SES latency surfaces as request timeouts. [CODE]
- Open `[ASSUMPTION]`: SES account is out of sandbox (must confirm before production volume). [ASSUMPTION]

## 3. Analyze

- **Use a dedicated subdomain** `txn.app.example.com` for transactional mail so a future marketing complaint can't poison receipts. [INFERENCE]
- **Authenticate** before any volume: SPF, three SES DKIM CNAMEs, DMARC starting at `p=none`. [DOC]
- **Move the send off the request path** via a queue + worker; key idempotency on the signup id. [INFERENCE]

## 4. Execute — deliverable

**DNS (publish on `txn.app.example.com`):** [CONFIG]

```
TXT  txn.app.example.com   "v=spf1 include:amazonses.com -all"
CNAME <token1>._domainkey.txn.app.example.com -> <token1>.dkim.amazonses.com
CNAME <token2>._domainkey.txn.app.example.com -> <token2>.dkim.amazonses.com
CNAME <token3>._domainkey.txn.app.example.com -> <token3>.dkim.amazonses.com
TXT  _dmarc.txn.app.example.com  "v=DMARC1; p=none; rua=mailto:dmarc@app.example.com"
```

**Send path (queued, idempotent):** [CODE]

```
signup handler  -> enqueue { signupId, email } on "verify-email" queue (returns immediately)
worker (Cloud Function on queue):
    if alreadySent(signupId): return          # idempotency on (user, event)
    render template (escape email/display name)
    ses.sendEmail(..., from="no-reply@txn.app.example.com")
    markSent(signupId); log { messageId, status }   # no plaintext PII
```

**Bounce/complaint handling:** SES → SNS topic → webhook; `Bounce`/`Complaint`
add address to a suppression table, `Delivery` updates the log row. [INFERENCE]

## 5. Validate (gate)

| Check | Result | Evidence |
|-------|--------|----------|
| SPF/DKIM/DMARC pass (mail-tester + headers) | pass | [DOC] |
| DMARC alignment confirmed via `rua` before raising policy | pending review | [ASSUMPTION] |
| Send queued, not inline (no signup timeout) | pass | [CODE] |
| Idempotent on signupId (no duplicate verification mail) | pass | [INFERENCE] |
| Bounce/complaint suppression active | pass | [INFERENCE] |
| No recipient PII in plaintext logs | pass | [INFERENCE] |
| Evidence tags on every claim (Alfa core EN) | pass | [DOC] |

## 6. Handoffs & follow-ups

- After a week of clean `rua` reports, raise DMARC to `quarantine`. [ASSUMPTION]
- Confirm SES production access (out of sandbox) before launch day. [ASSUMPTION]
- If they later want branded HTML for this email, route to `email-template-builder`.
