# Example Input

> Context: a small SaaS on Firebase + AWS SES. They want signup verification
> emails to actually land in the inbox.

**User request:**

"New users aren't getting their verification emails — when they do arrive, Gmail
puts them in spam. We send from `no-reply@app.example.com` and we're on AWS SES.
The send happens synchronously inside our signup Cloud Function and occasionally
the signup request times out. Get this working reliably."

**Known facts:**

- Stack: Firebase Auth + Cloud Functions, AWS SES for outbound mail.
- Sending address: `no-reply@app.example.com` (root domain, no subdomain).
- No SPF / DKIM / DMARC records published yet.
- Send is inline in the signup handler (blocks the request).
- Volume: ~300 signups/day, occasional bursts at launch days.

**Depth requested:** `deep` (this is going to production).
