<!-- distilled from alfa skills/firebase-hosting -->
<!-- > -->
# Firebase Hosting

> "Deployment should be boring — if it's exciting, something is wrong." — Unknown

## TL;DR

Guides Firebase Hosting configuration and deployment — rewrite rules for SPAs, custom headers for security and caching, preview channels for PR reviews, multi-site hosting for multiple apps, and CDN cache control. Use when deploying static sites or SPAs to Firebase's global CDN. [EXPLICIT]

## Procedure

### Step 1: Discover
- Check existing `firebase.json` hosting configuration
- Identify hosting requirements (SPA rewrites, API proxying, custom headers)
- Determine multi-site needs (main site, admin panel, docs site)
- Review current deployment workflow (manual, CI/CD, preview channels)

### Step 2: Analyze
- Plan rewrite rules: SPA fallback, Cloud Function proxying, Cloud Run integration
- Design header strategy: security headers, cache control, CORS
- Evaluate preview channel workflow for PR-based deployments
- Determine CDN cache invalidation strategy

### Step 3: Execute
- Configure `firebase.json` hosting with public directory and ignore patterns
- Add SPA rewrite: `{"source": "**", "destination": "/index.html"}`
- Set security headers: `X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`
- Configure cache headers: long cache for hashed assets, short cache for HTML
- Set up preview channels: `firebase hosting:channel:deploy pr-123`
- Add multi-site config for separate hosting targets
- Configure custom domain in Firebase Console

### Step 4: Validate
- Deploy to preview channel and verify all routes work
- Check security headers with securityheaders.com
- Verify cache headers are set correctly for static assets vs HTML
- Confirm custom domain SSL is provisioned and active

## Quality Criteria

- [ ] SPA rewrite rule configured for client-side routing
- [ ] Security headers (CSP, HSTS, X-Frame-Options) configured
- [ ] Static assets cached with long-lived `max-age` and content hashing
- [ ] Preview channels used for pre-deployment review
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Deploying directly to production without preview channel testing
- Not setting cache headers (Firebase defaults may not be optimal)
- Using Firebase Hosting for server-rendered content without Cloud Run integration

## Related Skills

- `firebase-setup` — hosting is part of Firebase project initialization
- `firebase-deployment` — deployment workflows for production releases

## Usage

Example invocations:

- "/firebase-hosting" — Run the full firebase hosting workflow
- "firebase hosting on this project" — Apply to current context


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
