<!-- distilled from alfa skills/email-templates -->
<!-- > -->
# Email Templates

> "Email is the cockroach of the internet — it survives everything, including bad HTML." — Unknown

## TL;DR

Guides the creation of bulletproof HTML email templates that render consistently in Gmail, Outlook, Apple Mail, and mobile clients. Covers MJML for rapid development, table-based layouts, inline CSS, responsive patterns, and dark mode compatibility. Use when building transactional emails, newsletters, or marketing campaigns. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify email types needed (transactional, marketing, notification, digest)
- Check existing email infrastructure (SendGrid, Mailgun, SES templates)
- Review brand guidelines for email (colors, fonts, logo usage)
- Determine target email clients and their rendering quirks

### Step 2: Analyze
- Choose authoring approach: MJML (recommended), Maizzle, or hand-coded tables
- Plan responsive strategy (fluid hybrid vs media queries vs Gmail-safe)
- Identify dynamic content blocks and personalization variables
- Evaluate dark mode behavior across clients (auto-invert, honor prefers-color-scheme)

### Step 3: Execute
- Build layout with nested tables (Outlook requires `<table>` layout)
- Inline all CSS or use a build step to inline from `<style>` blocks
- Add MSO conditional comments for Outlook-specific fixes
- Implement responsive stacking with `display:block` on `<td>` elements
- Create MJML source with `<mj-section>`, `<mj-column>`, `<mj-text>` components
- Add preheader text, alt text for images, and plain-text fallback

### Step 4: Validate
- Test in Litmus or Email on Acid across 20+ client/device combos
- Verify images load with and without (alt text visible)
- Check links, UTM parameters, and unsubscribe functionality
- Confirm dark mode renders acceptably (no invisible text)

## Quality Criteria

- [ ] Renders correctly in Outlook 2016+, Gmail web/app, Apple Mail, Yahoo
- [ ] Responsive — stacks to single column on mobile (<600px)
- [ ] All images have alt text; email is readable with images off
- [ ] Inline CSS applied — no reliance on `<style>` blocks alone
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using `div`-based layouts without table fallbacks for Outlook
- Relying on web fonts (most clients strip them — use system font stack)
- Setting fixed pixel widths without max-width fluid containers

## Related Skills

- `email-sending` — delivery infrastructure for these templates
- `dark-mode` — email dark mode is a different beast than web dark mode

## Usage

Example invocations:

- "/email-templates" — Run the full email templates workflow
- "email templates on this project" — Apply to current context


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
