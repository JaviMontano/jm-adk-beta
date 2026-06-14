<!-- distilled from alfa skills/email-template-builder -->
<!-- Responsive HTML email templates. Table-based layout, inline CSS, 600px max-width. Firebase Extensions trigger. [EXPLICIT] -->
# email-template-builder {Frontend} (v1.1)
> **"Ship pixels that perform, accessible by default."**
## Purpose
Responsive HTML email templates. Table-based layout, inline CSS, 600px max-width, Firebase Extensions (firestore-send-email) trigger. [EXPLICIT]
**When to use:** Building/transactional email HTML in the Firebase/Google/Hostinger stack. [EXPLICIT]
**Anti-scope:** Web pages/SPAs (use a frontend skill), copywriting, deliverability/DNS setup (SPF/DKIM/DMARC), list management. [INFERRED]
## Core Principles
1. **Email ≠ web.** Render engines are ~2003-era. Tables for layout, inline CSS for styling, no `<div>` grids, no flex/grid, no external/JS. [INFERRED]
2. **Inline-first.** Every style inlined on the element; keep one `<style>` in `<head>` only for media queries and pseudo-states (clients strip it silently). [INFERRED]
3. **Accessibility.** `role="presentation"` on layout tables, `alt` on all images, `lang` on `<html>`, real text over image-text, 4.5:1 contrast (WCAG 2.1 AA). [EXPLICIT]
4. **Graceful degradation > perfection.** Outlook/Windows (Word engine) and Dark Mode will differ — define an acceptable floor, do not chase pixel-parity. [INFERRED]
## Core Process
### Phase 1: Structure
1. Outer `role="presentation"` table at `width="100%"`; inner centered table `max-width:600px` (`width="600"` attr + CSS for Outlook). [INFERRED]
2. Apply design tokens from `.agent/.shared/design-tokens.md` as literal inline hex/px (no CSS vars — unsupported). [EXPLICIT]
3. Mobile-first single column; stack multi-column via media query, default to stacked when unsupported. [EXPLICIT]
### Phase 2: Build
1. Inline all CSS; keep `<style>` only for `@media` + dark-mode + states. [INFERRED]
2. Wire the Firebase Extensions trigger: write doc to the `mail` collection (`to`, `message.subject`, `message.html`) consumed by `firestore-send-email`. [EXPLICIT]
3. Images: absolute HTTPS URLs (Storage), explicit `width`/`height`, `alt`, `display:block`; never lazy-load (unsupported) — strip web perf habits. [INFERRED]
4. Add preheader (hidden ~90-char preview) and plain-text alternative for deliverability. [INFERRED]
### Phase 3: Validate
1. Litmus/Email-on-Acid render matrix — not Lighthouse (it scores web pages, not email). [INFERRED]
2. Inbox test across Gmail (web+app), Apple Mail, Outlook Win/Mac, iOS; check Dark Mode. [INFERRED]
3. Send a live doc through `firestore-send-email` to a seed inbox; confirm delivery + spam placement. [EXPLICIT]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Requirements/spec | Text/File | Yes | Email purpose, content blocks, CTA |
| Brand tokens | File | No | `.agent/.shared/design-tokens.md`; falls back to neutral defaults |
| Output | Type | Description |
|--------|------|-------------|
| Email template | HTML (inlined) | Table-based, ≤600px, client-tested |
| Plain-text part | Text | Fallback body for deliverability |
| Trigger payload | Firestore doc | `mail`-collection shape for `firestore-send-email` |
## Acceptance Criteria
- Renders acceptably in Gmail, Apple Mail, Outlook Win/Mac, iOS (defined floor, not pixel-parity). [INFERRED]
- All CSS inlined; removing the `<head>` `<style>` leaves layout intact. [INFERRED]
- ≤600px content width; single-column on mobile. [EXPLICIT]
- Every image has `alt`; layout tables `role="presentation"`; AA contrast. [EXPLICIT]
- Live send via `firestore-send-email` lands in inbox (not spam) with working preheader + plain-text part. [INFERRED]
## Validation Gate
- [ ] Table-based layout, `role="presentation"` on layout tables
- [ ] 100% inline CSS (head `<style>` only for media/state)
- [ ] ≤600px width, single-column mobile fallback
- [ ] WCAG 2.1 AA: alt text, contrast, `lang`
- [ ] Firestore `mail`-doc trigger verified end-to-end
- [ ] Cross-client + Dark Mode render checked
## 5. Self-Correction Triggers
> [!WARNING]
> IF using `<div>`/flex/grid for layout THEN refactor to `role="presentation"` tables. [INFERRED]
> IF styles live only in `<head>` `<style>` THEN inline them (Gmail strips head CSS). [INFERRED]
> IF width > 600px or unstyled on mobile THEN cap width and add the stacking media query. [EXPLICIT]
> IF an image is decorative-only or missing `alt` THEN add `alt` (empty `alt=""` if purely decorative). [INFERRED]
> IF reaching for Lighthouse/JS/lazy-load THEN stop — those are web habits, invalid in email. [INFERRED]

## Usage

Example invocations:

- "/email-template-builder" — Run the full email template builder workflow
- "email template builder on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, design tokens) [EXPLICIT]
- Assumes `firestore-send-email` extension installed with `mail`-collection wiring [INFERRED]
- English-language output unless otherwise specified [EXPLICIT]
- No client-side interactivity: JS, forms, video, web fonts are unreliable/blocked across clients [INFERRED]
- Does not cover deliverability infra (SPF/DKIM/DMARC) or domain reputation [INFERRED]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [INFERRED] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [INFERRED] |
| Out-of-scope request | Redirect to appropriate skill or escalate [INFERRED] |
| Outlook (Word engine) breaks layout | Use VML/ghost-table or MSO conditional comments; accept degraded floor [INFERRED] |
| Dark Mode inverts colors/logos | Provide dark-mode media query; use transparent-padded logo [INFERRED] |
| Images blocked by default | Ensure layout + meaning survive image-off via alt + background colors [INFERRED] |
