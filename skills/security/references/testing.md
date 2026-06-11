<!-- distilled from alfa skills/security-testing -->
<!-- > -->
# Security Testing

> "Security is not a product — it's a process." — Bruce Schneier

## TL;DR

Guides security testing practices — OWASP Top 10 checks, automated dependency scanning, secrets detection in code, security header validation, and penetration testing preparation. Use when auditing application security or establishing security testing in the development pipeline. [EXPLICIT]

## Procedure

### Step 1: Discover
- Run `npm audit` to identify known vulnerabilities in dependencies
- Check for hardcoded secrets, API keys, or credentials in codebase
- Review security headers on deployed application
- Identify authentication and authorization attack surfaces

### Step 2: Analyze
- Map OWASP Top 10 risks to the application's architecture
- Categorize vulnerabilities by severity (critical, high, medium, low)
- Evaluate XSS vectors (user input rendering, innerHTML usage)
- Check CSRF protection on state-changing endpoints

### Step 3: Execute
- Set up `npm audit` or Snyk in CI pipeline for dependency scanning
- Install pre-commit hooks for secrets detection (gitleaks, detect-secrets)
- Add security headers: CSP, HSTS, X-Content-Type-Options, X-Frame-Options
- Implement input sanitization using strip-first hierarchy (Constitution VII):
  Strip (remove HTML tags, keep text) > Escape (encode entities) > Allowlist (permit known-safe)
  Default to DOMParser-based stripping; use `textContent` over `innerHTML`
- Configure CORS properly (not `Access-Control-Allow-Origin: *` in production)
- Implement dual-layer security verification (Constitution VII):
  Layer 1: Static analysis (grep for secrets, innerHTML, scattered queries)
  Layer 2: Runtime inspection (Playwright checks DOM output, headers, network)
- Review Firebase security rules with the rules simulator
- Set up Dependabot or Renovate for automated dependency updates

### Step 4: Validate
- CI blocks deployment on critical/high vulnerability findings
- No secrets detected in repository history (use git-secrets or truffleHog)
- Security headers score A+ on securityheaders.com
- XSS payloads tested and blocked on all user input fields

## Quality Criteria

- [ ] Dependency vulnerability scanning runs on every CI build
- [ ] No hardcoded secrets in codebase (pre-commit hooks enforce)
- [ ] Security headers configured and validated
- [ ] Input sanitization uses strip-first default (not escape, not allowlist)
- [ ] Dual-layer verification performed (static + runtime)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Escape instead of strip | Escaped HTML can still render in edge cases | Strip tags, keep text content only |
| Client-only validation | Bypassable via DevTools | Mirror validation on server (Cloud Functions) |
| Static-only security checks | Misses runtime-injected content | Add runtime Playwright checks |

## Related Skills

- `input-sanitization` — Detailed strip-default implementation with DOMParser
- `dual-layer-verification` — Static + runtime verification methodology
- `firestore-security-rules` — Server-side rule enforcement
- `e2e-testing` — Playwright infrastructure for runtime verification

## Anti-Patterns

- Running security scans only before release (should be continuous)
- Ignoring `npm audit` warnings because "they're dev dependencies"
- Using `dangerouslySetInnerHTML` or `innerHTML` with user-provided content

## Related Skills

- `firestore-security-rules` — Firestore rules are a key security layer
- `code-review` — security review should be part of every PR review

## Usage

Example invocations:

- "/security-testing" — Run the full security testing workflow
- "security testing on this project" — Apply to current context


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
