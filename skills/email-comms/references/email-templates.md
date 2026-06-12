<!-- distilled from alfa skills/email-templates -->
<!-- > -->
# Email Templates

> "Email is the cockroach of the internet — it survives everything, including bad HTML." — Unknown

## TL;DR

Guides creation of bulletproof HTML email templates that render consistently in Gmail, Outlook (Word engine), Apple Mail, Yahoo, and mobile clients. Covers MJML for rapid authoring, table-based layouts, inline CSS, responsive patterns, and dark mode. Use for transactional emails, newsletters, or marketing campaigns. [EXPLICIT]

## Scope & Anti-Scope

- In scope: layout, rendering compatibility, responsive + dark mode, authoring toolchain (MJML/Maizzle/hand-coded). [EXPLICIT]
- Out of scope: deliverability (SPF/DKIM/DMARC, IP warmup), list hygiene, send-time logic → `email-sending`. [DOC]
- Out of scope: AMP for Email and interactive (carousels/forms) — niche client support; treat as progressive enhancement only. [INFERENCIA]

## Procedure

### Step 1: Discover
- Identify email types (transactional, marketing, notification, digest) — each has different latency, personalization, and compliance needs. [DOC]
- Inventory existing infra and its template engine (SendGrid Handlebars, Mailgun, SES, Customer.io) — engine dictates variable syntax. [CONFIG]
- Capture brand tokens (hex colors, logo SVG+PNG, system-font fallback) before coding. [EXPLICIT]
- List target clients with traffic share; rendering effort scales to the long tail, not the top 3. [INFERENCIA]

### Step 2: Analyze
- Choose authoring: MJML (recommended — compiles to Outlook-safe tables), Maizzle (Tailwind + auto-inline), or hand-coded tables (max control, max cost). [DOC]
- Pick responsive strategy: fluid-hybrid (works without media queries, Gmail-app-safe) > media queries > fixed. Fluid-hybrid is the robust default. [INFERENCIA]
- Map dynamic blocks, personalization variables, and conditional sections; define fallback values for every variable. [EXPLICIT]
- Decide dark mode posture per client: Apple Mail/iOS auto-invert, Outlook.com forces its own palette, Gmail partial — design so forced inversion stays legible. [DOC]

### Step 3: Execute
- Build with nested `<table>` layout; Outlook desktop (Word engine) ignores `float`, `flex`, `grid`, and most `margin`. [DOC]
- Inline all CSS (build step) — Gmail strips `<head><style>`; keep a `<style>` block ONLY for media queries and `@media (prefers-color-scheme)`. [DOC]
- Wrap Outlook-only fixes in `<!--[if mso]>` conditional comments; use VML for background images and ghost tables for max-width centering. [CODE]
- Stack columns on mobile via `<td>` → `display:block; width:100% !important` inside a media query. [CODE]
- In MJML, compose with `<mj-section>`, `<mj-column>`, `<mj-text>`, `<mj-button>`; never hand-edit compiled output (it is regenerated). [INFERENCIA]
- Add preheader (hidden span, 40–100 chars), `alt` on every image, and a plain-text MIME part. [EXPLICIT]
- Cap total HTML at ~100 KB — Gmail clips beyond 102 KB, hiding the unsubscribe link and tracking pixel. [DOC]

### Step 4: Validate
- Render-test in Litmus or Email on Acid across 20+ client/device combos before send. [EXPLICIT]
- Verify with images blocked: layout holds, alt text is meaningful, CTA still reachable. [EXPLICIT]
- Check links, UTM parameters, and a working one-click unsubscribe (legally required for marketing). [DOC]
- Confirm dark mode: no invisible text, logo has a light-safe background or transparent halo. [INFERENCIA]
- Send a live seed test — rendering engines differ from the real client, especially Outlook. [INFERENCIA]

## Worked Example: bulletproof button (Outlook + others)

```html
<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"
  href="https://ex.co" style="height:44px;v-text-anchor:middle;width:200px;"
  arcsize="12%" fillcolor="#1a73e8"><center style="color:#fff;font-family:
  Arial,sans-serif;font-size:16px;"><![endif]-->
<a href="https://ex.co" style="background:#1a73e8;border-radius:6px;color:#fff;
  display:inline-block;font:16px Arial,sans-serif;padding:13px 24px;
  text-decoration:none;">Confirm</a>
<!--[if mso]></center></v:roundrect><![endif]-->
```
VML path renders the button in Outlook; the `<a>` serves every other client. [CODE]

## Quality Criteria

- [ ] Renders correctly in Outlook 2016+/365, Gmail web+app, Apple Mail, Yahoo. [EXPLICIT]
- [ ] Stacks to single column below 600px. [EXPLICIT]
- [ ] Every image has alt text; email is legible with images off. [EXPLICIT]
- [ ] CSS inlined — no reliance on `<style>` for core layout. [DOC]
- [ ] HTML under ~100 KB (no Gmail clipping). [DOC]
- [ ] Dark mode legible; one-click unsubscribe present and tested. [INFERENCIA]
- [ ] Evidence tags applied to all non-obvious claims. [EXPLICIT]

## Failure Modes

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| Layout breaks only in Outlook desktop | Word engine ignores div/flex/grid | Convert to nested tables; add MSO ghost tables. [DOC] |
| Spacing collapses in Outlook | `margin` unsupported | Use `padding` on `<td>` or spacer rows. [DOC] |
| Email body truncated, no footer | >102 KB → Gmail clip | Strip comments, dedupe inline CSS, trim HTML. [DOC] |
| White text vanishes in dark mode | Client forced a dark background | Avoid pure white-on-transparent; set explicit bg on container. [INFERENCIA] |
| Fonts look wrong | Web font stripped by client | Use system-font stack as the declared family. [DOC] |
| CTA unclickable on mobile | Tap target <44px | Pad button to ≥44px height. [INFERENCIA] |

## Anti-Patterns

- `div`-based layouts without table fallback for Outlook. [DOC]
- Web fonts as the only font — most clients strip them; declare a system stack. [DOC]
- Fixed pixel widths with no `max-width` fluid container. [DOC]
- Background images without a VML fallback (invisible in Outlook). [INFERENCIA]
- Hand-editing MJML-compiled HTML (lost on next build). [INFERENCIA]

## Related Skills

- `email-sending` — delivery infrastructure for these templates.
- `dark-mode` — email dark mode differs from web dark mode (forced inversion, no full media-query support).

## Usage

Example invocations:

- "/email-templates" — Run the full email templates workflow.
- "email templates on this project" — Apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Client rendering behavior is a moving target; re-test after major client updates. [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding. [EXPLICIT] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution. [EXPLICIT] |
| Out-of-scope request | Redirect to appropriate skill or escalate. [EXPLICIT] |
| RTL language content | Set `dir="rtl"`; mirror table column order and padding. [INFERENCIA] |
| Client with no media-query support (Gmail app, older Outlook) | Rely on fluid-hybrid so layout degrades gracefully. [DOC] |
