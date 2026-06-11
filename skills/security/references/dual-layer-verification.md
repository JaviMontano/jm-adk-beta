<!-- distilled from alfa skills/dual-layer-verification -->
<!-- > -->
# Dual-Layer Verification

> "What static analysis misses, the browser reveals. What the browser hides, grep finds."

## TL;DR

Verifies security invariants at two independent layers: (1) static analysis of source files and (2) runtime inspection of deployed/served artifacts via Playwright. The marginal cost of the second layer is near-zero when E2E tests already exist; the marginal benefit is closing vectors that static analysis cannot detect. Required by Constitution VII for defense-in-depth. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify security invariants to verify:
  - No secrets/API keys in client-side code
  - No `innerHTML` with user-controlled data
  - CSP headers present on all pages
  - No unauthorized access patterns (all Firestore access via service modules)
  - Input sanitization applied at all boundaries
- Check existing static analysis tools (ESLint plugins, grep patterns)
- Check existing E2E infrastructure (Playwright installed?)

### Step 2: Analyze
- Define **static checks** (Layer 1 — source files):
  - `grep -r "innerHTML" --include="*.js"` → flag user-data assignments
  - `grep -rP "(AKIA|AIza|ghp_|sk-)" --include="*.js"` → detect secrets
  - ESLint `no-eval`, `no-implied-eval`, `no-script-url` rules
  - Scan for scattered Firestore queries outside service modules
- Define **runtime checks** (Layer 2 — browser):
  - Playwright navigates app, fills inputs with XSS payloads, inspects DOM output
  - Check response headers for CSP, HSTS, X-Frame-Options
  - Verify no secrets visible in page source or network requests
  - Console error capture: no security warnings
- Map each invariant to both layers

### Step 3: Execute
- **Layer 1 — Static Analysis**:
  ```bash
  # Secrets scan
  grep -rPl '(AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|ghp_[0-9a-zA-Z]{36})' \
    --include="*.js" --include="*.html" src/

  # innerHTML with variables (not static strings)
  grep -rn 'innerHTML\s*=' --include="*.js" src/ | grep -v '= \x27\|= "'

  # Scattered Firestore queries
  grep -rn 'collection(\|doc(' --include="*.js" src/ | grep -v 'services/'
  ```
- **Layer 2 — Runtime Inspection**:
  ```javascript
  // Playwright security verification
  test('no secrets in page source', async ({ page }) => {
    await page.goto('/');
    const content = await page.content();
    expect(content).not.toMatch(/AKIA[0-9A-Z]{16}/);
    expect(content).not.toMatch(/sk-[0-9a-zA-Z]{48}/);
  });

  test('CSP header present', async ({ page }) => {
    const response = await page.goto('/');
    const csp = response.headers()['content-security-policy'];
    expect(csp).toBeDefined();
  });

  test('XSS payload stripped', async ({ page }) => {
    await page.goto('/admin');
    await page.fill('#title-input', '<script>alert(1)</script>Test');
    await page.click('#save');
    const stored = await page.textContent('#title-display');
    expect(stored).toBe('Test');
  });
  ```
- Produce combined report: findings from both layers, cross-referenced

### Step 4: Validate
- Both layers agree on findings (no contradictions)
- Runtime catches at least one vector that static analysis missed (or confirms static is sufficient)
- Zero critical findings in either layer
- Combined coverage documented in security report
- Report stored alongside test results for gate G3

## Quality Criteria

- [ ] Security invariants explicitly listed
- [ ] Static analysis checks implemented (grep/ESLint)
- [ ] Runtime inspection checks implemented (Playwright)
- [ ] Both layers cover the same invariant set
- [ ] Combined report produced
- [ ] Zero critical findings before gate passage
- [ ] Runtime layer is optional if Playwright unavailable (static always runs)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Static-only verification | Misses runtime-injected content, dynamic imports | Add runtime layer |
| Runtime-only verification | Misses source patterns that haven't triggered yet | Add static layer |
| Treating layers as redundant | Each catches different classes of issues | Run BOTH, compare |
| Skipping runtime because "too slow" | Marginal cost is near-zero with existing E2E | Add security checks to existing E2E suite |
| No combined report | Findings get lost | Single report with both layers' findings |

## Related Skills

- `security-testing` — Broader security testing framework
- `input-sanitization` — The sanitization that dual-layer verifies
- `e2e-testing` — Playwright infrastructure that runtime layer uses
- `lighthouse-ci` — Performance verification in the same CI pipeline

## Usage

Example invocations:

- "/dual-layer-verification" — Run the full dual layer verification workflow
- "dual layer verification on this project" — Apply to current context


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
