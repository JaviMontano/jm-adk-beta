<!-- distilled from alfa skills/localization-guide -->
<!-- > -->
# Localization Guide
> "Method over hacks."
## TL;DR
Ship UI text that survives translation: externalized keys, ICU plural/gender, locale-aware dates/numbers, RTL mirroring, and translator context. Scope = frontend strings + formatting. Out of scope: backend i18n, content/CMS translation, machine-translation pipelines. [DOC]

## Procedure
### Step 1: Discover
- Inventory user-facing strings; confirm target locales, RTL needs, and the i18n lib in use (e.g. i18next, FormatJS, `Intl`). [CONFIG]
- Flag hardcoded strings, concatenated sentences, and baked-in date/number formats — all blockers. [INFERENCIA]
### Step 2: Analyze
- Choose key strategy (namespaced semantic keys, not English-as-key) and ICU message format for plurals/gender per Constitution XIII/XIV. [DOC]
- Decide RTL approach: CSS logical properties (`margin-inline-start`) over physical, `dir="rtl"`, mirrored icons. [DOC]
### Step 3: Execute
- Externalize every string to catalogs; pass variables as ICU args, never string concat. Format dates/numbers/currency via `Intl`, not manual templates. [CÓDIGO]
- Provide translator context: comments, screenshots, max-length, placeholder meaning. [DOC]
### Step 4: Validate
- Run pseudo-localization (accents + 40% expansion) to catch truncation/clipping. [INFERENCIA]
- Verify each criterion below; check fallback locale resolves and no missing-key warnings. [DOC]

## Quality Criteria
- [ ] Evidence tags applied (Alfa core set) [DOC]
- [ ] No hardcoded or concatenated user-facing strings
- [ ] ICU plural/gender for every count- or person-dependent message
- [ ] Locale-aware date/number/currency via `Intl`
- [ ] RTL verified with logical properties; layout mirrors cleanly
- [ ] Pseudo-loc passes; no truncation at +40% length
- [ ] Every key has translator context and a fallback

## Usage

Example invocations:

- "/localization-guide" — Run the full localization guide workflow
- "localization guide on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, configs, string catalogs). [SUPUESTO]
- Covers frontend string/format localization only — not translation quality, copy, or CMS content. [DOC]
- English-language working output unless a target locale is specified. [SUPUESTO]
- Does not replace a native-speaker review for final translations. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Plurals beyond one/other (ar, ru, pl) | Use full ICU CLDR categories, never `count === 1` |
| String shorter/longer per locale (de, ja) | Reserve space; pseudo-loc at +40%; no fixed-width text |
| Variable word order across languages | Interpolate named ICU args; never concatenate fragments |
| Missing translation key | Resolve to fallback locale + log; never ship raw key |
| Bidi text mixing LTR data in RTL UI | Apply Unicode isolates (`⁦`/`⁩`) around injected values |
