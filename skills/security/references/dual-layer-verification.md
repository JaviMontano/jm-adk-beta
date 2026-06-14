<!-- distilled from alfa skills/dual-layer-verification -->
<!-- > -->
# Dual-Layer Verification

> "What static analysis misses, the browser reveals. What the browser hides, grep finds."

## TL;DR

Verify security invariants at two independent layers: (1) **static** analysis of source files and (2) **runtime** inspection of the deployed/served artifact via Playwright. The two layers fail differently, so agreement raises confidence and disagreement surfaces a real bug — never noise. Marginal cost of Layer 2 is near-zero when an E2E suite exists; marginal benefit is closing vectors static analysis structurally cannot see (runtime-injected DOM, headers set by CDN/proxy, dynamic imports, server-templated values). Required by Constitution VII for defense-in-depth. [DOC]

**Tagging:** this document uses the Alfa core set (`[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]` `[ASSUMPTION]`), EN spelling, one tag per claim. Canon: `references/verification-tags.md`. [DOC]

## Scope / Anti-Scope

- **In scope:** client-exposed secrets, DOM/XSS sinks, security response headers, access-path discipline (Firestore via service modules), input sanitization at boundaries. [DOC]
- **Out of scope:** server-side authz logic, dependency CVEs (use SCA), threat modeling, secrets in git history (use a dedicated scanner). Dual-layer verifies what ships to and renders in the browser, not the full backend. [INFERENCE]
- **Not a replacement** for domain-expert review on final go/no-go. [DOC]

## Procedure

### Step 1: Discover
- Enumerate the security invariants to verify:
  - No secrets/API keys in client-side code or network payloads
  - No `innerHTML`/`outerHTML`/`insertAdjacentHTML` with user-controlled data
  - CSP (and ideally HSTS, X-Frame-Options) present on all served pages
  - All Firestore access routed through service modules (no scattered queries)
  - Input sanitization applied at every boundary
- Inventory tooling: static (ESLint plugins, grep), runtime (is Playwright installed? is there a dev/preview server to point it at?).
- Decide the **served target** Layer 2 will hit: local preview, ephemeral deploy, or staging. Headers differ per environment — verifying against `localhost` dev mode gives false confidence about prod CSP. [ASSUMPTION] → confirm which environment gates G3; verify against an artifact built the same way prod is.

### Step 2: Analyze
- Define **static checks** (Layer 1 — source):
  - `innerHTML =` assignments fed by variables → XSS sink candidates
  - Secret-shaped literals (`AKIA…`, `AIza…`, `ghp_…`, `sk-…`)
  - ESLint `no-eval`, `no-implied-eval`, `no-script-url`
  - Firestore `collection(`/`doc(` calls outside `services/`
- Define **runtime checks** (Layer 2 — browser):
  - Inject XSS payloads into inputs, assert the rendered DOM is escaped/stripped
  - Read response headers for CSP/HSTS/X-Frame-Options
  - Assert no secret pattern in page source or any network response body
  - Capture console: zero CSP-violation or mixed-content warnings
- Map **each invariant to both layers**. An invariant covered by only one layer is a known gap — record it, don't silently drop it.

### Step 3: Execute
- **Layer 1 — Static Analysis** (always runs; the floor): [CODE]
  ```bash
  # Secrets scan (literals in shipped source)
  grep -rPl '(AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|ghp_[0-9a-zA-Z]{36})' \
    --include="*.js" --include="*.html" src/

  # innerHTML assigned from a variable (excludes static string literals)
  grep -rn 'innerHTML\s*=' --include="*.js" src/ | grep -v '= \x27\|= "'

  # Scattered Firestore queries outside service modules
  grep -rn 'collection(\|doc(' --include="*.js" src/ | grep -v 'services/'
  ```
- **Layer 2 — Runtime Inspection** (Playwright against the served target): [CODE]
  ```javascript
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
    expect(stored).toBe('Test');     // escaped, not executed
  });
  ```
- Produce a **combined report**: every invariant × {Layer 1 result, Layer 2 result}, cross-referenced, stored beside test output for gate G3.

### Step 4: Validate
- Layers do not contradict each other (see disagreement protocol below).
- Layer 2 catches ≥1 vector Layer 1 missed, **or** explicitly confirms Layer 1 was sufficient for this invariant set — state which.
- Zero critical findings in either layer.
- Combined coverage documented; gaps (single-layer invariants) named, not hidden.

## Worked Example: a vector only Layer 2 catches

A title field is escaped in the source template, so Layer 1 (grep for `innerHTML`) is clean. But a client-side i18n library re-injects the title via `innerHTML` at runtime after hydration. Layer 1 sees nothing; Layer 2's `XSS payload stripped` test renders `<script>alert(1)</script>` live and the assertion fails — exposing the sink. Fix: route the i18n write through `textContent`/a sanitizer. This is the canonical case for why runtime is not optional. [INFERENCE]

## Layer-Disagreement Protocol

| Layer 1 | Layer 2 | Meaning | Action |
|---|---|---|---|
| flags | clean | Sink exists in source but no exploitable path hit at runtime | Keep finding open; the path may trigger under other state/route. Add a runtime case that reaches it before closing. [INFERENCE] |
| clean | flags | Runtime-injected/templated vector invisible to source scan | **Real bug.** Fix, then add a static pattern if one can be written. |
| flags | flags | Confirmed | Fix; both should go green together. |
| clean | clean | Either truly safe or both blind | Confirm the invariant is actually reachable by the tests, not a no-op. |

Never resolve a disagreement by deleting the noisier check — that re-creates the single-layer blind spot the whole skill exists to remove. [DOC]

## Decisions & Trade-offs

- **Playwright over a headless fetch.** Fetch sees initial HTML and headers but not post-hydration DOM; the i18n example above slips past it. Playwright executes scripts, so it observes the DOM users actually get. Cost: slower, needs a browser. [INFERENCE]
- **Static is the floor, runtime is the ceiling.** If Playwright is unavailable, Layer 1 still runs and the gate degrades to static-only with that limitation recorded — it does not block. [DOC]
- **Regexes are intentionally narrow.** Broad secret patterns flood the report with false positives and get muted; precise prefixes (`AKIA`, `AIza`, `ghp_`, `sk-`) catch the common keys with near-zero noise. Tune per provider; document additions. [ASSUMPTION] → review the key formats your stack actually issues.

## Failure Modes

- **Verifying dev mode, shipping prod.** Dev servers often omit CSP/HSTS; the test passes, prod is exposed. Point Layer 2 at a prod-equivalent build. [INFERENCE]
- **Headers set at the edge.** CDN/proxy may add CSP after the origin response. Test against the same edge that serves users, or the header assertion is meaningless. [INFERENCE]
- **Auth-gated routes.** XSS/admin tests behind login silently no-op if the harness isn't authenticated. Assert you reached the page (e.g. a known element) before asserting the security property.
- **SPA timing.** Assertions firing before hydration read stale DOM. Use Playwright auto-waiting / `expect(...).toPass()`; never a fixed `sleep`.
- **Minified/bundled output evades source grep.** Run Layer 1 on source `src/`, not the bundle, and let Layer 2 cover what only exists post-build.

## Quality Criteria

- [ ] Security invariants explicitly listed
- [ ] Static checks implemented (grep/ESLint) and runnable
- [ ] Runtime checks implemented (Playwright) against a prod-equivalent target
- [ ] Each invariant mapped to both layers; single-layer gaps named
- [ ] Layer-disagreement protocol applied to every mismatch
- [ ] Combined report produced and stored for gate G3
- [ ] Zero critical findings before gate passage
- [ ] Runtime layer optional only if Playwright unavailable (static always runs), and the degradation is recorded
- [ ] Evidence tags applied (single family, consistent spelling)

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Static-only verification | Misses runtime-injected content, dynamic imports, edge headers | Add runtime layer |
| Runtime-only verification | Misses source sinks not yet triggered by a test path | Add static layer |
| Treating layers as redundant | Each catches a different issue class | Run BOTH, compare |
| Resolving a disagreement by muting a check | Re-creates the blind spot | Apply the disagreement protocol |
| Skipping runtime as "too slow" | Marginal cost ≈ 0 on existing E2E | Fold security asserts into the E2E suite |
| Verifying dev mode | Prod headers/CSP differ | Target a prod-equivalent build |
| No combined report | Findings get lost between layers | One report, both layers, cross-referenced |

## Related Skills

- `security-testing` — Broader security testing framework
- `input-sanitization` — The sanitization that dual-layer verifies
- `e2e-testing` — Playwright infrastructure the runtime layer reuses
- `lighthouse-ci` — Performance verification in the same CI pipeline

## Usage

Example invocations:

- "/dual-layer-verification" — Run the full dual-layer verification workflow
- "dual layer verification on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts: source, a buildable/served target, configs. [ASSUMPTION]
- Assumes the served target reflects production (same build, same edge). If not, header findings are advisory only. [ASSUMPTION] → confirm the target environment.
- English-language output unless otherwise specified. [DOC]
- Does not replace domain-expert judgment for final go/no-go. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Playwright not installed | Run static-only; record runtime layer as skipped, not passed |
| Auth-gated security routes | Authenticate first; assert page reached before asserting the property |
| Headers added by CDN/proxy | Test against the edge users hit, not the origin |
