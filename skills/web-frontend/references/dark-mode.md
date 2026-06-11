<!-- distilled from alfa skills/dark-mode -->
<!-- > -->
# Dark Mode

> "In the darkness, good contrast becomes your best friend." — Unknown

## TL;DR

Guides dark mode implementation using CSS custom properties for theming, `prefers-color-scheme` for system preference detection, a manual toggle with localStorage persistence, and proper handling of images, shadows, and elevation in dark contexts. Use when adding theme switching to any web application. [EXPLICIT]

## Procedure

### Step 1: Discover
- Audit current color usage (hardcoded hex values, existing design tokens)
- Check for existing theming infrastructure (CSS variables, Tailwind dark:, styled-components)
- Identify problematic elements for dark mode (images, shadows, borders, charts)
- Review third-party component theming capabilities

### Step 2: Analyze
- Define color token architecture: semantic names (--color-surface, --color-text-primary) not raw values
- Plan three-state toggle: system default / light / dark
- Determine persistence strategy (localStorage, cookie for SSR flash prevention)
- Evaluate images that need dark variants or reduced brightness

### Step 3: Execute
- Define CSS custom properties on `:root` for light theme, `[data-theme="dark"]` for dark
- Add `prefers-color-scheme: dark` media query as default when no explicit preference saved
- Build theme toggle component that cycles: system → light → dark
- Store preference in localStorage and apply `data-theme` attribute before paint
- Add script in `<head>` (blocking) to prevent dark mode flash (FODT)
- Adjust images: reduce brightness/contrast, swap logos, handle transparent PNGs
- Use `color-scheme: light dark` meta tag for native form element theming

### Step 4: Validate
- Test all pages in both themes — no unreadable text or invisible elements
- Verify contrast ratios meet WCAG AA in both themes (4.5:1 for text)
- Confirm theme persists across page loads and sessions
- Check third-party embeds and components render acceptably in dark mode

## Quality Criteria

- [ ] All colors defined as CSS custom properties — zero hardcoded color values in components
- [ ] System preference respected by default, user override persisted
- [ ] No flash of wrong theme on page load (FODT prevention script in `<head>`)
- [ ] WCAG AA contrast ratios maintained in both light and dark themes
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Simply inverting all colors with `filter: invert(1)` (destroys images and branding)
- Forgetting to handle images, shadows, and borders in dark mode
- Storing theme preference only in JavaScript state (lost on page reload)

## Related Skills

- `web-components` — CSS custom properties bridge themes into Shadow DOM
- `accessibility-testing` — contrast ratio validation in both themes

## Usage

Example invocations:

- "/dark-mode" — Run the full dark mode workflow
- "dark mode on this project" — Apply to current context


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
