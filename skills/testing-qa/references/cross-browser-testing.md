<!-- distilled from alfa skills/cross-browser-testing -->
<!-- > -->
# Cross-Browser Testing

> "It works on my machine is not a deployment strategy — or a browser testing strategy." — Unknown

## TL;DR

Guides cross-browser compatibility testing and fixes — identifying browser-specific issues, using feature detection with progressive enhancement, implementing polyfills for missing APIs, and setting up automated cross-browser testing. Use when your application must work across Chrome, Firefox, Safari, and Edge. [EXPLICIT]

## Scope & Anti-Scope

- **In scope**: web (DOM/CSS/JS) compatibility across evergreen browsers, prefix/polyfill strategy, CI engine coverage. [EXPLICIT]
- **Out of scope**: native mobile apps, email-client HTML rendering, accessibility audits (separate skill), pixel-perfect visual regression (use a screenshot-diff tool), performance profiling beyond polyfill cost. [EXPLICIT]
- **Engine reality**: test by *engine*, not brand — Blink (Chrome/Edge/Opera/Brave), Gecko (Firefox), WebKit (Safari iOS+macOS). iOS browsers (incl. "Chrome on iOS") are forced to WebKit, so Safari testing covers them. Testing all four brands but only two engines wastes budget. [EXPLICIT]

## Procedure

### Step 1: Discover
- Define browser support matrix from analytics data (which browsers users actually use), not assumptions. [EXPLICIT]
- Check `browserslist` config in `package.json` or `.browserslistrc`; run `npx browserslist` to see the resolved list. [EXPLICIT]
- Identify CSS and JS features requiring vendor prefixes or polyfills.
- Review caniuse.com for feature support across target browsers.

### Step 2: Analyze
- Categorize features by support level: universal, needs prefix, needs polyfill, unsupported (needs fallback or graceful degradation). [EXPLICIT]
- Plan progressive enhancement strategy (core experience for all, enhanced for modern).
- Evaluate CSS feature queries (`@supports`) for conditional styling.
- Determine polyfill loading strategy (conditional vs unconditional).

### Step 3: Execute
- Configure `browserslist` to match actual target audience.
- Set up Autoprefixer via PostCSS for CSS vendor prefixes (driven by `browserslist`, so the two never drift). [EXPLICIT]
- Use `@supports` for progressive CSS enhancement.
- Implement feature detection (not browser detection) for JavaScript.
- Add polyfills conditionally with dynamic imports or polyfill.io.
- Test in BrowserStack or Sauce Labs for real browser coverage (real devices catch engine bugs emulators miss). [EXPLICIT]
- Set up Playwright with multiple browser engines in CI (`chromium`, `firefox`, `webkit`). [EXPLICIT]

### Step 4: Validate
- Test core user flows in all supported browsers.
- Verify no JavaScript errors in browser console across targets.
- Confirm CSS renders correctly (flexbox, grid, custom properties).
- Check that polyfills load only when needed (no performance penalty for modern browsers).

## Decisions & Trade-offs

| Decision | Choose when | Trade-off / cost | Evidence |
|----------|-------------|------------------|----------|
| Feature detection over UA sniffing | Always (default) | Slightly more code than a UA string; UA sniffing breaks silently on every new release | [EXPLICIT] |
| Polyfill.io (runtime, UA-served) | Wide unknown audience, want minimal modern-browser bytes | Third-party request on critical path; UA-keyed cache; outage = missing polyfill | [EXPLICIT] |
| Bundled polyfills (`core-js` via Babel `useBuiltIns: 'usage'`) | Need offline/self-hosted, predictable bundle | Larger bundle even for modern browsers unless differential serving is used | [EXPLICIT] |
| Differential serving (modern/legacy bundles via `<script type=module>` / `nomodule`) | Legacy support still required but modern majority | Two builds, more CI time and cache entries | [EXPLICIT] |
| Graceful degradation vs polyfill | Feature is enhancement, not core | Degraded path must be tested too, or it rots | [EXPLICIT] |

## Quality Criteria

- [ ] Browser support matrix documented and aligned with `browserslist` (and verified via `npx browserslist`). [EXPLICIT]
- [ ] Progressive enhancement ensures core experience works everywhere.
- [ ] Autoprefixer configured for CSS vendor prefix management.
- [ ] Feature detection used instead of browser sniffing.
- [ ] CI runs the suite on all three engines (Chromium, Gecko, WebKit), not just Chromium. [EXPLICIT]
- [ ] Evidence tags applied to all claims.

## Anti-Patterns

- Using browser user-agent sniffing instead of feature detection.
- Loading all polyfills unconditionally (bloats modern browser bundles).
- Only testing in Chrome during development.
- Treating Chrome + Edge as two engines (both Blink) while skipping WebKit entirely. [EXPLICIT]
- Hand-maintaining vendor prefixes instead of letting Autoprefixer derive them from `browserslist`. [EXPLICIT]

## Failure Modes

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Works in Chrome, blank/broken in Safari | WebKit-unsupported API or CSS used without fallback | Add `@supports`/feature detect; verify in real WebKit, not emulator | 
| Polyfill loads for everyone, modern bundle bloated | Unconditional import or `useBuiltIns: 'entry'` mis-set | Switch to conditional load / `usage` + differential serving |
| New browser release breaks layout | UA sniffing matched an old string | Replace with feature detection |
| CI green but prod breaks on iOS | CI ran Chromium only; iOS = WebKit | Add `webkit` project to Playwright config |
| Prefixes missing after refactor | `browserslist` narrowed, Autoprefixer dropped them | Re-check matrix vs analytics; widen targets if needed |

## Related Skills

- `e2e-testing` — Playwright supports multi-browser e2e testing
- `build-optimization` — browserslist affects transpilation and bundle size

## Usage

Example invocations:

- "/cross-browser-testing" — Run the full cross browser testing workflow
- "cross browser testing on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Cloud device labs (BrowserStack/Sauce) and polyfill.io are third-party; their availability and cost are outside this skill's control. [EXPLICIT]
- Emulated/headless engines approximate but do not guarantee real-device behavior, especially for WebKit on iOS. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No analytics data for matrix | Fall back to `browserslist` `defaults`; flag the assumption [EXPLICIT] |
| Required browser past EOL (e.g. IE11) | Confirm it is genuinely required; quote the polyfill/bundle cost before committing [EXPLICIT] |
