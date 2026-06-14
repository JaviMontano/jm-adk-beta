<!-- distilled from alfa skills/internationalization -->
<!-- > -->
# Internationalization

> "The limits of my language mean the limits of my world." — Ludwig Wittgenstein

## TL;DR

Guides full i18n/l10n for web apps: extracting translatable strings, structuring translation files, RTL layout, CLDR pluralization, and locale-aware date/number/currency formatting via the `Intl` API. Use when an app must support multiple languages or regions. [EXPLICIT]

**Scope boundary**: this skill wires the *engineering* — extraction, runtime, formatting, RTL. It does NOT produce translations (that is human/TMS work) nor decide which locales to ship (product decision). [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify all user-facing strings (UI labels, error messages, notifications, `aria-label`, `alt`, `<title>`, email/PDF templates). [EXPLICIT]
- Check for an existing i18n library (i18next, react-intl/FormatJS, vue-i18n, `@angular/localize`) before adding one — two libraries fragment the catalog. [EXPLICIT]
- Detect hardcoded locale assumptions: `MM/DD/YYYY`, `$`, `1,000.00`, `left/right` CSS, baked-in singular/plural strings. [EXPLICIT]
- Inventory non-string assets needing localization (images with text, PDFs, transactional emails, OG metadata).

### Step 2: Analyze
- Determine target locales and their requirements: RTL (ar, he, fa, ur), CLDR plural categories, script complexity, line-break rules (CJK, Thai). [EXPLICIT]
- Choose a translation-management workflow (decision below) and a key-naming scheme.
- Assess ICU MessageFormat needs for plurals, gender (`select`), and nested interpolation.
- List components needing RTL layout changes (flex direction, margins/padding, directional icons, carousels).

### Step 3: Execute
- Set up the i18n library with namespace-split catalogs (`common`, `auth`, `checkout`) to enable lazy-loading per route. [EXPLICIT]
- Extract strings into locale resource files with consistent, hierarchical keys (`checkout.cta.pay`, not `button1`).
- Implement locale detection precedence: explicit user setting → URL prefix (`/es/`) → `Accept-Language` → default. Persist the choice. [EXPLICIT]
- Apply logical CSS properties (`margin-inline-start`, `inset-inline-end`, `text-align: start`) and set `dir` + `lang` on `<html>`. [EXPLICIT]
- Format via `Intl.DateTimeFormat`, `Intl.NumberFormat` (with `style:'currency'`), `Intl.PluralRules`, `Intl.RelativeTimeFormat`, `Intl.ListFormat`.

### Step 4: Validate
- Verify no raw keys render (missing-key handler throws in CI, warns in dev — never silently shows the key). [EXPLICIT]
- Test RTL with real Arabic/Hebrew content, not just `dir="rtl"` on Latin text — bidi mixing (numbers, URLs) only surfaces with real script.
- Confirm date/number/currency output matches each locale's expectations (decimal `,` vs `.`, currency symbol position).
- Run pseudo-localization for expansion: German/Finnish run ~30–40% longer; verify no truncation or overflow. [EXPLICIT]

## Decisions & Trade-offs

| Decision | Choose when | Trade-off |
|----------|-------------|-----------|
| **JSON catalogs** | Small/medium apps, dev-owned strings | Simple, diffable; no translator UX, no plural metadata [EXPLICIT] |
| **PO/gettext** | Translator-heavy, offline workflows | Mature tooling, context comments; extra build step [EXPLICIT] |
| **Cloud TMS** (Phrase, Lokalise, Crowdin) | Many locales, continuous translation | Live updates, glossary, review; cost + network dependency [EXPLICIT] |
| **ICU MessageFormat** | Plurals/gender/nesting needed | Correct for all CLDR rules; steeper authoring syntax [EXPLICIT] |
| **Logical CSS props** vs RTL stylesheet | New/modern codebase | One source of truth; needs evergreen-browser support [EXPLICIT] |
| **URL-prefix locale** vs cookie-only | SEO matters | Crawlable, shareable per-locale URLs; routing complexity [EXPLICIT] |

## Worked Example (ICU plural + currency)

```js
// en.json
{ "cart.items": "{count, plural, =0 {Your cart is empty} one {# item} other {# items}}" }
// Runtime
t('cart.items', { count: 3 });           // "3 items"
new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' })
  .format(1234.5);                        // "1.234,50 €"  (note comma decimal, trailing symbol)
```

## Quality Criteria

- [ ] Zero hardcoded user-facing strings in components (lint rule enforces this). [EXPLICIT]
- [ ] RTL layout has no visual breaks; icons that must not mirror (logos, clocks) are excluded via `[dir]` rules.
- [ ] Date/number/currency formatting uses `Intl` (or an equivalent CLDR-backed lib), never string templates.
- [ ] Pluralization covers all CLDR categories (`zero/one/two/few/many/other`) for every target locale. [EXPLICIT]
- [ ] Catalogs are namespace-split and lazy-loaded; initial bundle ships only the active locale.
- [ ] Evidence tags applied to all non-trivial claims. [EXPLICIT]

## Anti-Patterns & Failure Modes

- **Concatenating fragments** (`t('greeting') + name`) — breaks word order in VSO/SOV languages; use parameterized messages.
- **`float`/`left`/`right` CSS** instead of logical properties — silently breaks RTL.
- **Translations in code** instead of external resources — blocks translator handoff and lazy-loading.
- **Hardcoded English plural `if (n===1)`** — wrong for Slavic/Arabic plural systems; use `Intl.PluralRules`/ICU.
- **Shipping all locales in the main bundle** — bloats first load; split per locale.
- **Locale fallback that masks gaps** — falling back to English hides missing keys; surface a CI report instead. [EXPLICIT]
- **`new Date(str)` for display** — parses/formats in the runtime's locale, not the user's; always format through `Intl`.

## Anti-Scope

- Does NOT author or machine-translate copy — that is human/TMS responsibility. [EXPLICIT]
- Does NOT select which locales the product supports (product/market decision). [EXPLICIT]
- Does NOT localize legal/regulatory content for compliance — route to legal review. [EXPLICIT]

## Related Skills

- `accessibility-testing` — i18n and a11y overlap on `lang` attributes and screen-reader pronunciation.
- `web-components` — Shadow DOM needs explicit i18n context propagation across boundaries.

## Usage

Example invocations:

- "/internationalization" — Run the full internationalization workflow.
- "internationalization on this project" — Apply to current context.

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Assumes an evergreen-browser target for `Intl` and logical CSS; pre-2020 browsers need polyfills. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Locale with no translation yet | Surface in CI report; fall back to default but never silently |
| Mixed LTR/RTL content (URLs, code, numbers in Arabic) | Use Unicode bidi isolation (`<bdi>`, `dir="auto"`) |
| Right-to-left + directional icons | Exclude must-not-mirror icons via `[dir="rtl"]` rules |
| String expansion overflows UI | Caught by pseudo-localization; design flexible layouts |
