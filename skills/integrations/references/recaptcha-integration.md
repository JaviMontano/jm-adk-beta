<!-- distilled from alfa skills/recaptcha-integration -->
<!-- > -->
# reCAPTCHA Integration

> "The best CAPTCHA is the one the user never sees." — Unknown

## TL;DR

Guides reCAPTCHA v3 and Firebase App Check integration for invisible bot protection — scoring-based verification on forms and API endpoints, Firebase App Check for protecting backend services, and fallback strategies for low-score interactions. Use when protecting forms, APIs, or Firebase services from automated abuse. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify surfaces needing bot protection (forms, login, API endpoints)
- Check existing spam prevention measures
- Review Firebase App Check compatibility with current Firebase services
- Determine user friction tolerance (invisible preferred, challenge fallback)

### Step 2: Analyze
- Choose between reCAPTCHA v3 (score-based, invisible) and v2 (challenge-based)
- Plan score thresholds (0.0 = bot, 1.0 = human, typical threshold: 0.5)
- Design fallback flow for low scores (email verification, v2 challenge, block)
- Evaluate Firebase App Check for backend service protection

### Step 3: Execute
- Register site in reCAPTCHA admin console and obtain site key + secret key
- Add reCAPTCHA v3 script and execute on form actions: `grecaptcha.execute(siteKey, {action: 'submit'})`
- Verify token server-side via reCAPTCHA API with secret key
- Implement score-based decision logic in Cloud Functions
- Set up Firebase App Check with reCAPTCHA Enterprise provider
- Enforce App Check on Firestore, Storage, and Cloud Functions
- Add debug token for local development and testing

### Step 4: Validate
- Test with legitimate user flows and verify high scores (>0.7)
- Simulate bot behavior and confirm low scores trigger protection
- Verify Firebase App Check blocks requests without valid attestation
- Confirm debug tokens work in emulator and development environments

## Quality Criteria

- [ ] reCAPTCHA v3 runs invisibly — no user interaction required for legitimate users
- [ ] Token verification happens server-side (never trust client-side score)
- [ ] Fallback mechanism exists for borderline scores (not just block/allow)
- [ ] Firebase App Check enforced on all sensitive backend services
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Verifying reCAPTCHA tokens client-side only (easily bypassed)
- Using a single score threshold without fallback (blocks legitimate users)
- Forgetting App Check debug tokens for development (breaks local testing)

## Related Skills

- `firebase-auth` — reCAPTCHA protects auth flows from credential stuffing
- `cloud-functions` — server-side token verification in Cloud Functions

## Usage

Example invocations:

- "/recaptcha-integration" — Run the full recaptcha integration workflow
- "recaptcha integration on this project" — Apply to current context


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
