<!-- distilled from alfa skills/internationalization -->
<!-- > -->
# Internationalization

> "The limits of my language mean the limits of my world." — Ludwig Wittgenstein

## TL;DR

Guides full i18n/l10n implementation for web apps — from extracting translatable strings and setting up translation files to handling RTL layouts, pluralization, and locale-specific date/number/currency formatting. Use when your app needs to support multiple languages or regions. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify all user-facing strings in the codebase (UI labels, error messages, notifications)
- Check for existing i18n libraries (i18next, react-intl, vue-i18n, @angular/localize)
- Detect hardcoded locale assumptions (date formats, currency symbols, text direction)
- Inventory assets that need localization (images with text, PDFs, emails)

### Step 2: Analyze
- Determine target locales and their requirements (RTL, pluralization rules, script complexity)
- Evaluate translation management workflow (JSON files, PO files, cloud TMS)
- Assess ICU MessageFormat needs for complex plurals and gender
- Identify components requiring layout changes for RTL (flexbox direction, margins, icons)

### Step 3: Execute
- Set up i18n library with namespace-based translation files
- Extract strings into locale JSON/YAML files with consistent key naming
- Implement locale detection (URL prefix, browser preference, user setting)
- Add RTL stylesheet or logical CSS properties (inline-start/end vs left/right)
- Configure Intl API for dates (`Intl.DateTimeFormat`), numbers (`Intl.NumberFormat`), and relative time

### Step 4: Validate
- Verify all visible strings are translated (no raw keys shown)
- Test RTL layout with actual Arabic/Hebrew content (not just `dir="rtl"`)
- Confirm date/number formats match locale expectations
- Check pseudo-localization for string expansion (German ~30% longer than English)

## Quality Criteria

- [ ] Zero hardcoded user-facing strings in components
- [ ] RTL layout works without visual breaks or mirrored icons that shouldn't mirror
- [ ] Date, number, and currency formatting uses Intl API or equivalent
- [ ] Pluralization handles all CLDR plural categories for target locales
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Concatenating translated fragments instead of using parameterized messages
- Using CSS `float: left/right` instead of logical properties for RTL support
- Storing translations in code instead of external resource files

## Related Skills

- `accessibility-testing` — i18n and a11y overlap on lang attributes and screen reader support
- `web-components` — Shadow DOM requires special i18n context propagation

## Usage

Example invocations:

- "/internationalization" — Run the full internationalization workflow
- "internationalization on this project" — Apply to current context


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
