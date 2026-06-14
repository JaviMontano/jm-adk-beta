<!-- distilled from alfa skills/security-testing -->
<!-- > -->
# Security Testing

> "Security is not a product — it's a process." — Bruce Schneier

## TL;DR

Guides security testing — OWASP Top 10 checks, automated dependency scanning, secrets detection, security-header validation, and pentest prep. Use when auditing application security or wiring security testing into the pipeline. [DOC]

## Scope & Anti-Scope

- IN: app-layer testing (deps, secrets, headers, OWASP Top 10, CI gating, Firebase rules). [DOC]
- OUT: infra/network pentesting, cloud IAM audits, formal threat modeling, compliance attestation (SOC2/PCI) — route to the relevant skill. [SUPUESTO]
- Assumes a web/Node-Firebase stack; for other stacks the tools change but the procedure holds. [SUPUESTO] Verify by checking the repo's package manager and host. [POR_CONFIRMAR→use repo manifest]

## Procedure

### Step 1: Discover
- `npm audit --json` (or `pnpm audit`, `pip-audit`) for known-vuln dependencies. [CÓDIGO]
- Scan for hardcoded secrets/API keys/credentials in code AND git history. [CÓDIGO]
- Review security headers on the deployed app (`curl -sI <url>`). [CONFIG]
- Enumerate auth/authz attack surfaces (login, token refresh, role checks). [INFERENCIA]

### Step 2: Analyze — OWASP Top 10 (2021) mapping
| Risk | Check | Tool/signal |
|---|---|---|
| A01 Broken Access Control | authz on every state-changing endpoint | manual + server rules [DOC] |
| A02 Cryptographic Failures | TLS-only, no plaintext secrets at rest | headers + secret scan [CONFIG] |
| A03 Injection (incl. XSS) | input rendering, `innerHTML`, query building | static grep + runtime [CÓDIGO] |
| A05 Security Misconfiguration | headers, CORS, default creds | `curl -I`, config review [CONFIG] |
| A06 Vulnerable Components | dependency CVEs | `npm audit`, Snyk [CÓDIGO] |
| A07 Auth Failures | session, brute-force, MFA | manual + log review [INFERENCIA] |
| A08 Data Integrity | unsigned deps, CI supply chain | lockfile + provenance [CONFIG] |

Categorize each finding by severity (critical/high/medium/low) using CVSS or the advisory's rating. [DOC]

### Step 3: Execute
- Add `npm audit` or Snyk to CI for dependency scanning. [CÓDIGO]
- Pre-commit hooks for secrets (gitleaks, detect-secrets). [CÓDIGO]
- Security headers: CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy. [CONFIG]
- Input sanitization, strip-first hierarchy (Constitution VII):
  Strip (remove HTML, keep text) > Escape (encode entities) > Allowlist (permit known-safe).
  Default to DOMParser stripping; prefer `textContent` over `innerHTML`. [CÓDIGO]
- CORS scoped to known origins — never `Access-Control-Allow-Origin: *` in production. [CONFIG]
- Dual-layer verification (Constitution VII):
  Layer 1 static (grep secrets, `innerHTML`, scattered queries);
  Layer 2 runtime (Playwright checks DOM output, headers, network). [CÓDIGO]
- Review Firebase rules with the rules simulator; mirror client validation server-side (Cloud Functions). [CÓDIGO]
- Dependabot or Renovate for automated dependency updates. [CONFIG]

### Step 4: Validate
- CI blocks deploy on critical/high findings (SLA: critical ≤24h, high ≤7d — adjust per policy). [SUPUESTO] Confirm thresholds with the security owner. [POR_CONFIRMAR→ask owner]
- No secrets in repo history (git-secrets, trufflehog). [CÓDIGO]
- Headers score A+ on securityheaders.com (or equivalent self-hosted scan). [CONFIG]
- XSS payloads tested and blocked on every user-input field. [CÓDIGO]

## Worked Examples

```bash
# Dependency scan, fail CI on high+
npm audit --audit-level=high

# Secret scan over full history
gitleaks detect --source . --redact

# Header check
curl -sI https://app.example.com | grep -iE 'content-security-policy|strict-transport|x-frame'
```
XSS probe: submit `<img src=x onerror=alert(1)>` into a text field; pass = renders inert text, no script execution (verify via Playwright `page.on('dialog')` never firing). [CÓDIGO]

## Quality Criteria
- [ ] Dependency scanning runs on every CI build. [CÓDIGO]
- [ ] No hardcoded secrets (pre-commit hooks enforce). [CÓDIGO]
- [ ] Security headers configured and validated. [CONFIG]
- [ ] Input sanitization uses strip-first default (not escape, not allowlist). [CÓDIGO]
- [ ] Dual-layer (static + runtime) verification performed. [CÓDIGO]
- [ ] Server-side mirrors every client-side check. [INFERENCIA]
- [ ] Evidence tags applied to all claims. [DOC]

## Anti-Patterns
| Anti-Pattern | Why It's Bad | Do This Instead |
|---|---|---|
| Escape instead of strip | Escaped HTML can still render in edge cases | Strip tags, keep text content only |
| Client-only validation | Bypassable via DevTools | Mirror validation server-side (Cloud Functions) |
| Static-only checks | Misses runtime-injected content | Add runtime Playwright checks |
| Scan only before release | Drift accumulates between releases | Run continuously in CI |
| Ignoring audit warnings as "dev deps" | Dev tooling runs in CI/build with repo access | Triage by reachability, not by dep type |
| `dangerouslySetInnerHTML`/`innerHTML` with user content | Direct XSS sink | Strip + `textContent` |

## Failure Modes
- Scanner green but vuln present — unreachable advisory DB or pinned-but-vulnerable transitive dep. Cross-check with a second scanner. [INFERENCIA]
- Headers set at app layer but stripped by proxy/CDN — test the production edge, not localhost. [INFERENCIA]
- Secret rotated in code but live in history — history scan + key revocation both required. [SUPUESTO]

## Related Skills
- `input-sanitization` — strip-default implementation with DOMParser
- `dual-layer-verification` — static + runtime methodology
- `firestore-security-rules` — server-side rule enforcement
- `e2e-testing` — Playwright runtime verification
- `code-review` — security review as part of every PR

## Usage
- "/security-testing" — run the full workflow
- "security testing on this project" — apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [SUPUESTO]
- English-language output unless otherwise specified. [DOC]
- Does not replace domain-expert judgment for final go/no-go. [DOC]

## Edge Cases
| Scenario | Handling |
|---|---|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No CI available | Run locally as a gate; flag CI absence as a finding |
| Monorepo / multiple manifests | Scan each package; aggregate severity |
