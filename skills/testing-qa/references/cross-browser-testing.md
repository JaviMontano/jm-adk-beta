<!-- distilled from alfa skills/cross-browser-testing -->
<!-- > -->
# Cross-Browser Testing

> "It works on my machine is not a deployment strategy — or a browser testing strategy." — Unknown

## TL;DR

Guides cross-browser compatibility testing and fixes — identifying browser-specific issues, using feature detection with progressive enhancement, implementing polyfills for missing APIs, and setting up automated cross-browser testing. Use when your application must work across Chrome, Firefox, Safari, and Edge. [EXPLICIT]

## Procedure

### Step 1: Discover
- Define browser support matrix from analytics data (which browsers users actually use)
- Check `browserslist` config in `package.json` or `.browserslistrc`
- Identify CSS and JS features requiring vendor prefixes or polyfills
- Review caniuse.com for feature support across target browsers

### Step 2: Analyze
- Categorize features by support level: universal, needs prefix, needs polyfill, unsupported
- Plan progressive enhancement strategy (core experience for all, enhanced for modern)
- Evaluate CSS feature queries (`@supports`) for conditional styling
- Determine polyfill loading strategy (conditional vs unconditional)

### Step 3: Execute
- Configure `browserslist` to match actual target audience
- Set up Autoprefixer via PostCSS for CSS vendor prefixes
- Use `@supports` for progressive CSS enhancement
- Implement feature detection (not browser detection) for JavaScript
- Add polyfills conditionally with dynamic imports or polyfill.io
- Test in BrowserStack or Sauce Labs for real browser coverage
- Set up Playwright with multiple browser engines in CI

### Step 4: Validate
- Test core user flows in all supported browsers
- Verify no JavaScript errors in browser console across targets
- Confirm CSS renders correctly (flexbox, grid, custom properties)
- Check that polyfills load only when needed (no performance penalty for modern browsers)

## Quality Criteria

- [ ] Browser support matrix documented and aligned with `browserslist`
- [ ] Progressive enhancement ensures core experience works everywhere
- [ ] Autoprefixer configured for CSS vendor prefix management
- [ ] Feature detection used instead of browser sniffing
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using browser user-agent sniffing instead of feature detection
- Loading all polyfills unconditionally (bloats modern browser bundles)
- Only testing in Chrome during development

## Related Skills

- `e2e-testing` — Playwright supports multi-browser e2e testing
- `build-optimization` — browserslist affects transpilation and bundle size

## Usage

Example invocations:

- "/cross-browser-testing" — Run the full cross browser testing workflow
- "cross browser testing on this project" — Apply to current context


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
