<!-- distilled from alfa skills/recaptcha-integration -->
<!-- > -->
# reCAPTCHA Integration

> "The best CAPTCHA is the one the user never sees." — Unknown

## TL;DR

Guides reCAPTCHA v3 + Firebase App Check integration for invisible bot protection: score-based verification on forms/API endpoints, App Check attestation for backend services, and graduated fallback for low-score interactions. Use when protecting forms, APIs, or Firebase services from automated abuse. [EXPLICIT]

## Scope & Anti-Scope

- **In scope:** reCAPTCHA v3 (score), v2 (challenge fallback), reCAPTCHA Enterprise, Firebase App Check on Firestore/Storage/Functions, server-side verification. [EXPLICIT]
- **Out of scope:** WAF/DDoS at the edge (Cloudflare/Cloud Armor), rate limiting, account-takeover ML, payment fraud scoring — reCAPTCHA complements but does not replace these. [INFERENCE]
- v3 returns a *risk signal*, not a binary verdict; final allow/deny is your policy decision. [DOC]

## Procedure

### Step 1: Discover
- Identify surfaces needing protection (forms, login, signup, password-reset, comment/API endpoints). [EXPLICIT]
- Inventory existing spam controls to avoid double-friction. [EXPLICIT]
- Confirm App Check compatibility with current Firebase services + SDK versions. [CONFIG]
- Determine friction tolerance (invisible v3 preferred; v2 challenge only as fallback). [EXPLICIT]

### Step 2: Analyze
- Choose v3 (score-based, invisible) vs v2 (explicit challenge). **Trade-off:** v3 is frictionless but never blocks alone — it informs policy; v2 blocks reliably but adds friction and abandonment. Default to v3 + v2 fallback for high-risk actions. [INFERENCE]
- Set score thresholds: `0.0`=bot, `1.0`=human, default cut at `0.5`. Tune per action — payments stricter (`0.7`), newsletter signup looser (`0.3`). [DOC]
- Design **graduated** fallback for borderline scores: step-up (email/SMS verify or v2) before hard block. [EXPLICIT]
- Evaluate App Check (reCAPTCHA Enterprise provider) for backend attestation. [CONFIG]

### Step 3: Execute
- Register site in reCAPTCHA admin console; obtain site key (public) + secret key (server-only). [CONFIG]
- Load v3 script and execute per action: `grecaptcha.execute(siteKey, {action: 'submit'})` — returns a single-use token. [CODE]
- Verify token **server-side** via `siteverify` with the secret key; check `success`, `score`, `action` (must match), and `hostname`. [CODE]
- Implement score-based decision logic in Cloud Functions. [CODE]
- Set up App Check with reCAPTCHA Enterprise provider; enforce on Firestore, Storage, Functions. [CONFIG]
- Register a debug token for local/emulator development. [CONFIG]

### Step 4: Validate
- Legitimate flows score high (>0.7). [EXPLICIT]
- Simulated bot behavior scores low and triggers fallback/block. [EXPLICIT]
- App Check rejects requests lacking valid attestation. [EXPLICIT]
- Debug tokens work in emulator and dev environments. [CONFIG]

## Worked Example: server-side verification (Cloud Function)

```js
// [CODE] Node Cloud Function — never trust client score
const params = new URLSearchParams({ secret: SECRET, response: token });
const r = await fetch('https://www.google.com/recaptcha/api/siteverify', {
  method: 'POST', body: params,
});
const v = await r.json();
// Reject if call failed, action mismatched (replay/tampering), or score below cut
if (!v.success || v.action !== 'submit' || v.score < 0.5) {
  return stepUpOrBlock(v.score);   // graduated, not a flat 403
}
```

`siteverify` error codes: `missing-input-secret`, `invalid-input-secret`, `missing-input-response`, `invalid-input-response`, `timeout-or-duplicate` (token reused/expired). [DOC]

## Quality Criteria

- [ ] v3 runs invisibly — no interaction for legitimate users. [EXPLICIT]
- [ ] Token verified **server-side only**; client score never trusted. [EXPLICIT]
- [ ] Server checks `success` AND `action` AND `score` AND `hostname` (not score alone). [DOC]
- [ ] Graduated fallback exists for borderline scores (not binary block/allow). [EXPLICIT]
- [ ] Each token consumed once; duplicate/expired tokens rejected. [DOC]
- [ ] App Check enforced on all sensitive backend services. [EXPLICIT]
- [ ] Score thresholds tuned per-action, not one global cut. [INFERENCE]
- [ ] Debug token registered for dev/emulator; not shipped to prod. [CONFIG]
- [ ] Evidence tags applied to all claims. [EXPLICIT]

## Anti-Patterns

- Verifying tokens client-side only — trivially bypassed; the secret must stay server-side. [EXPLICIT]
- Single global threshold with no fallback — blocks legitimate users on noisy scores. [EXPLICIT]
- Trusting `score` without validating `action`/`hostname` — enables token replay across endpoints. [DOC]
- Reusing a v3 token across requests — tokens are single-use and expire (~2 min). [DOC]
- Forgetting App Check debug tokens — breaks local testing. [EXPLICIT]
- Treating a low score as definitive bot proof — it is a probability; alone it is not grounds for a permanent ban. [INFERENCE]

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Script blocked (adblock/CSP) | `grecaptcha` undefined | Whitelist `recaptcha.net`/`gstatic.com` in CSP; degrade to v2. [CONFIG] |
| Token expired | `timeout-or-duplicate` | Re-execute `grecaptcha.execute` just before submit. [DOC] |
| Clock skew / network to siteverify | Verification times out | Fail-closed for high-risk actions, fail-open for low-risk; log either. [INFERENCE] |
| Uniformly low scores in prod | Legit users blocked | Check `action` match, correct site key (v3 vs Enterprise), domain registration. [CONFIG] |
| App Check enforced before clients ship token | Live traffic 403s | Roll out in **monitor mode** first, enforce after metrics confirm. [CONFIG] |

## Related Skills

- `firebase-auth` — reCAPTCHA protects auth flows from credential stuffing. [EXPLICIT]
- `cloud-functions` — server-side token verification in Cloud Functions. [EXPLICIT]

## Usage

Example invocations:

- "/recaptcha-integration" — Run the full recaptcha integration workflow
- "recaptcha integration on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]
- reCAPTCHA Enterprise and high-volume v3 assessments may incur Google billing — confirm quotas before enforcing. [INFERENCE]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| User on legacy browser without JS | Provide v2 checkbox or non-JS verification path |
| Privacy/GDPR-sensitive jurisdiction | Disclose reCAPTCHA use; consider consent-gated load |
