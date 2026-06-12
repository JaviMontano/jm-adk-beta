<!-- distilled from alfa skills/dark-mode -->
<!-- > -->
# Dark Mode

> "In the darkness, good contrast becomes your best friend." — Unknown

## TL;DR

Implement dark mode with semantic CSS custom properties, `prefers-color-scheme` for system detection, a three-state toggle (system/light/dark) persisted to localStorage, a render-blocking pre-paint script to kill the flash, and deliberate handling of images, shadows, elevation, and form controls. Use when adding theme switching to any web application. [EXPLICIT]

## Procedure

### Step 1: Discover
- Audit current color usage (hardcoded hex values, existing design tokens)
- Check for existing theming infrastructure (CSS variables, Tailwind `dark:`, styled-components)
- Identify problematic elements: images, shadows, borders, charts, iframes, `<canvas>`, syntax-highlighted code
- Review third-party component theming capabilities (many ship only a light theme) [INFERENCIA]

### Step 2: Analyze
- Define color token architecture: semantic names (`--color-surface`, `--color-text-primary`) not raw values
- Plan three-state toggle: system default / light / dark (system is the default state, not a fourth) [INFERENCIA]
- Determine persistence strategy: localStorage for SPA; mirror to a cookie when SSR must render the correct theme server-side [INFERENCIA]
- Evaluate images that need dark variants, reduced brightness, or a `<picture>` source swap

### Step 3: Execute
- Define CSS custom properties on `:root` for light theme, `[data-theme="dark"]` for dark
- Add `@media (prefers-color-scheme: dark)` to set dark tokens as default when no explicit preference is saved
- Build theme toggle component that cycles: system → light → dark → system
- Store preference in localStorage and apply the `data-theme` attribute before first paint
- Add a render-blocking script in `<head>` to prevent the flash of incorrect theme (FOIT/FODT)
- Adjust images: reduce brightness/contrast, swap logos, handle transparent PNGs, set `<canvas>`/chart palettes per theme
- Set `color-scheme: light dark` (CSS property or `<meta name="color-scheme">`) for native form-control and scrollbar theming

### Step 4: Validate
- Test all pages in both themes — no unreadable text or invisible elements
- Verify contrast ratios meet WCAG AA in both themes (4.5:1 body text, 3:1 large text and UI components) [DOC]
- Confirm theme persists across page loads, navigations, and sessions
- Check third-party embeds and components render acceptably in dark mode

## Reference Implementation

Pre-paint script (place inline in `<head>`, before any stylesheet, so it runs blocking and sets the attribute before first paint — prevents the flash): [INFERENCIA]

```html
<script>
  (function () {
    var saved = localStorage.getItem('theme'); // 'light' | 'dark' | null
    var sysDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var theme = saved || (sysDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
  })();
</script>
```

Token layer (semantic names map to per-theme values; components reference only semantic tokens): [INFERENCIA]

```css
:root { color-scheme: light; --color-surface: #fff; --color-text-primary: #111; }
[data-theme="dark"] { color-scheme: dark; --color-surface: #121212; --color-text-primary: #eaeaea; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) { color-scheme: dark; --color-surface: #121212; --color-text-primary: #eaeaea; }
}
```

Toggle cycle (system clears the override so the OS media query takes back over): [INFERENCIA]

```js
function nextTheme(cur) { return cur === 'system' ? 'light' : cur === 'light' ? 'dark' : 'system'; }
// 'system' => localStorage.removeItem('theme') + remove data-theme; else setItem + setAttribute
```

## Decisions & Trade-offs

- **`data-theme` attribute vs `.dark` class**: attribute keeps theme orthogonal to other classes and reads cleanly in DevTools; class is what Tailwind's `darkMode: 'class'` expects. Pick one and stay consistent. [INFERENCIA]
- **Dark surfaces use elevation-by-lightness, not shadows**: shadows are nearly invisible on dark backgrounds. Raise elevated surfaces by lightening the background (e.g. overlay white at low opacity) instead of relying on `box-shadow`. [DOC]
- **Avoid pure black (`#000`) and pure white text on dark**: pure-black surfaces with `#fff` text cause halation/eye strain; use off-black surfaces (`~#121212`) and slightly-dimmed text. [DOC]
- **localStorage vs cookie**: localStorage is simplest but invisible to the server, so SSR pages flash. If rendering server-side, also write a cookie and read it during SSR. [INFERENCIA]

## Quality Criteria

- [ ] All colors defined as CSS custom properties — zero hardcoded color values in components [EXPLICIT]
- [ ] System preference respected by default, user override persisted across sessions [EXPLICIT]
- [ ] No flash of wrong theme on load (render-blocking pre-paint script in `<head>`, before stylesheets) [EXPLICIT]
- [ ] WCAG AA contrast maintained in both themes (4.5:1 text, 3:1 UI/large) [DOC]
- [ ] `color-scheme` declared so native controls, scrollbars, and form fields theme correctly [EXPLICIT]
- [ ] Evidence tags applied to all non-obvious claims [EXPLICIT]

## Anti-Patterns

- Inverting all colors with `filter: invert(1)` — destroys images, photos, and branding [INFERENCIA]
- Forgetting images, shadows, borders, charts, and code blocks in dark mode [EXPLICIT]
- Storing theme only in JS state — lost on reload [EXPLICIT]
- Loading the toggle script `async`/`defer` or after stylesheets — guarantees a flash [INFERENCIA]
- Hardcoding chart/`<canvas>` colors — they ignore CSS tokens and stay light-themed [INFERENCIA]
- Toggling a body class with a CSS transition on `*` — repaints the whole page on theme switch (jank) [INFERENCIA]

## Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Flash of light theme on load | Script deferred / after CSS / not blocking | Inline blocking script in `<head>` before stylesheets |
| Toggle works but resets on reload | Preference not persisted | Write to localStorage, read in pre-paint script |
| SSR page flashes despite saved pref | Server can't see localStorage | Mirror preference to a cookie, read during SSR |
| Native selects/checkboxes stay light | Missing `color-scheme` | Set `color-scheme` per theme |
| Charts/canvas stay light | Palette hardcoded in JS | Read theme and re-render palette on toggle |
| Text unreadable in one theme | Token failed contrast | Re-check against WCAG AA, adjust token |

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
- Anti-scope: does NOT cover high-contrast mode, forced-colors / Windows High Contrast, or per-component themes beyond light/dark [INFERENCIA]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| User changes OS theme while in `system` state | `matchMedia` change listener re-applies tokens live |
| Third-party iframe with no dark theme | Wrap/letterbox or accept; do not force-invert its content |
