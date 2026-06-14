<!-- distilled from alfa skills/xlsx-template-creator -->
<!-- [EXPLICIT] -->
# XLSX Template Creator

Generate a renderer-ready workbook **specification**, not a binary `.xlsx` file. The output is a structured Markdown or YAML-like spec that defines sheets, columns, formulas, dropdowns, named ranges, validation evidence, and handoff notes for a downstream XLSX renderer. [EXPLICIT]

This skill validates **structure and formulas**; it does not emit cells, styles, charts, or ZIP packages. Binary generation belongs to `brand-xlsx` (the renderer). If the user wants a finished workbook, hand the spec to that skill. [EXPLICIT]

## Scope And Anti-Scope

| In scope | Out of scope (route elsewhere) |
|---|---|
| Sheet/column/formula/named-range spec | Binary `.xlsx` emission → `brand-xlsx` [CONFIG] |
| Formula safety + dropdown wiring | Chart/sparkline objects → renderer handoff note [EXPLICIT] |
| Validation evidence rows | Brand tokens, fonts, theme colors → `brand-xlsx` [CONFIG] |
| Two template archetypes | Free-form sheet design / pivot tables [SUPUESTO] |

Anti-scope rationale: keeping spec and render separate makes the contract diffable and lets one spec target multiple renderers. [EXPLICIT]

## Deterministic Bundle

Use the local compiler whenever the user needs a repeatable template contract, validation before handoff, or a diffable workbook spec. The compiler is the source of truth — never hand-author the YAML block. [CÓDIGO]

```bash
python3 scripts/compile-xlsx-template.py --input path/to/workbook-spec.json --format markdown
python3 scripts/compile-xlsx-template.py --input path/to/workbook-spec.json --format yaml --output workbook-template.yml
```

The compiler loads:

| File | Purpose |
|---|---|
| `assets/xlsx-template-schema.json` | Required workbook, sheet, column, named range, validation, and handoff fields. |
| `assets/template-policy.json` | Accepted template types, required sheets, semantic colors, and formatting minimums. |
| `assets/formula-policy.json` | Formula safety rules, dropdown source prefixes, blocked functions, and named range patterns. |
| `assets/report-template.md` | Stable Markdown report shape. |

Run `bash scripts/check.sh` after changing this skill, its assets, or fixtures. A green `check.sh` is the only acceptance signal — a passing compile on one spec does not certify the policy assets. [CÓDIGO]

## Workflow

1. Identify the template type: `tracking-matrix` for task/compliance/item tracking, or `metrics-dashboard` for KPI monitoring and thresholds. [EXPLICIT]
2. Ask only for missing essentials: title, locale, workbook audience, required fields, dropdown values, KPI names, targets, thresholds, and renderer constraints. Do not ask for fields the chosen archetype already mandates. [CONFIG]
3. Create a JSON workbook spec that follows `assets/xlsx-template-schema.json`. [CÓDIGO]
4. Validate the spec with `scripts/compile-xlsx-template.py`; fix **every** error before returning the template. A spec that does not compile is a FAIL, not a draft. [CÓDIGO]
5. Return the compiled Markdown for human review, or YAML when the next step is machine rendering. [EXPLICIT]
6. Include handoff notes that name the intended renderer and any features that renderer must add natively, such as charts or sparklines. [EXPLICIT]

## Template Types

| Signal | Choose | Required sheets |
|---|---|---|
| Tasks, owners, due dates, priorities, compliance rows, status tracking | `tracking-matrix` | `Tracker`, `Summary`, `Config` |
| KPIs, current vs target, trends, thresholds, alert queues | `metrics-dashboard` | `KPIs`, `Trends`, `Alerts`, `Config` |

If the user needs both, produce two specs and give them distinct titles. Do not merge archetypes into one workbook — required-sheet validation is per-archetype and a hybrid fails both. [CONFIG]

## Workbook Rules

- Every sheet must declare `purpose`, `columns`, and `printArea`. [CÓDIGO]
- Data sheets must enable `autoFilter` when they are `Tracker`, `KPIs`, or `Alerts`. [CONFIG]
- Data areas must set `mergedCellsInDataArea: false`. Merged cells break autoFilter, sort, and per-row formulas. [CÓDIGO]
- Dropdown columns must source values from `Config!` ranges or an explicit named range formula. [CONFIG]
- Division formulas must use an `IF` guard, for example `=IF(C2=0,0,B2/C2)`. [CÓDIGO]
- Do not use volatile or external formulas such as `INDIRECT`, `OFFSET`, `NOW`, `RAND`, `WEBSERVICE`, or HTTP hyperlinks. These break determinism (re-render diffs) or reach the network. [CÓDIGO]
- Conditional formatting must use semantic colors from `assets/template-policy.json` — never raw hex. [CONFIG]
- Named ranges must point to sheet cell ranges such as `Config!$A$2:$A$50` (absolute, bounded, single sheet). [CÓDIGO]
- `Config` must clearly tell users it is editable. [EXPLICIT]

## Output Shape

For human review, return Markdown with these sections, in order: [EXPLICIT]

1. `Summary`
2. `Sheets`
3. `Columns`
4. `Named Ranges`
5. `Validation`
6. `Handoff`

For renderer handoff, return YAML-like output from the compiler and do not add prose inside the machine block — downstream parsers treat stray prose as a malformed document. [CÓDIGO]

## Edge Cases

- **Missing dropdown values:** create placeholder `Config` columns and mark the validation row as `warn` with the missing source named. Never omit the column — a silent gap renders as a free-text field. [CONFIG]
- **Unknown renderer:** set `handoff.renderer` to `xlsx-renderer` and put renderer assumptions in `handoff.notes`. [CONFIG]
- **KPI target can be zero:** every attainment formula must guard the denominator with `IF(C2=0,0,...)`; a zero target is valid input, not an error. [CÓDIGO]
- **Too many KPI categories for one dashboard:** keep required sheets and add category columns instead of creating ad hoc sheet names unless the user asks. [EXPLICIT]
- **Requested charts or sparklines:** document them as renderer handoff notes; this skill validates structure and formulas, not binary chart objects. [EXPLICIT]
- **Locale with comma decimal separator:** declare `locale` in the spec; formulas stay `,`-argument form and the renderer localizes display — do not hand-edit formula separators. [SUPUESTO]
- **Per-row formula over a growing table:** anchor with absolute refs to `Config!`/named ranges so fill-down stays correct; relative-only refs drift. [CÓDIGO]

## Good vs Bad

Good formula:

```text
=IF(C2=0,0,B2/C2)
```

Bad formula:

```text
=B2/C2
```

Good dropdown source (bounded, anchored to `Config`):

```text
Config!A2:A50
```

Bad dropdown source (whole-column, off-sheet, unbounded):

```text
Owners!A:A
```

## Failure Modes (reject before delivery)

- Spec emitted without compiling, or with compiler errors suppressed. [CÓDIGO]
- Required sheet for the archetype missing or renamed. [CONFIG]
- Volatile/external function present anywhere in the spec. [CÓDIGO]
- Division/attainment formula without an `IF` denominator guard. [CÓDIGO]
- Dropdown bound to a whole-column or off-sheet range instead of `Config!`/named range. [CONFIG]
- Conditional formatting using raw hex instead of a semantic color key. [CONFIG]
- Prose mixed into the YAML machine block. [CÓDIGO]
- Handoff block missing renderer, output format, or rendering notes. [EXPLICIT]

## Decisions And Trade-offs

- **Spec over binary:** a diffable contract is reviewable and renderer-agnostic. Trade-off: the user must run a second step (the renderer) to get an openable file. [EXPLICIT]
- **Two fixed archetypes:** `tracking-matrix` and `metrics-dashboard` cover the common cases and let required-sheet validation be deterministic. Trade-off: bespoke layouts need a manual extension, not this skill. [SUPUESTO]
- **Ban volatile functions:** guarantees byte-stable re-renders and no network reach. Trade-off: live-recalc patterns (e.g. `NOW`, `OFFSET` tables) must be reframed as static columns the renderer or user refreshes. [CÓDIGO]
- **`Config`-sourced dropdowns only:** keeps validation lists editable and bounded. Trade-off: more setup than a whole-column reference, but avoids unbounded ranges and orphaned validations. [CONFIG]

## Assumptions And Limits

- Assumes the `scripts/` compiler and `assets/*.json` policies referenced above ship with the skill; if absent, treat every rule as unverified and do not claim a passing gate. [SUPUESTO]
- Assumes a single downstream renderer per spec; multi-renderer fan-out needs one spec each. [SUPUESTO]
- Limit: no pivot tables, macros/VBA, external data connections, or multi-workbook references. [EXPLICIT]
- Limit: structural and formula validation only — cell-level value correctness, brand styling, and chart rendering are out of band. [EXPLICIT]

## Worked Example (metrics-dashboard)

Input: 3 KPIs (Uptime, MTTR, Cost), each current vs target, red/amber/green threshold. Resulting spec skeleton (then compiled, never hand-finished): [EXPLICIT]

- Sheets: `KPIs`, `Trends`, `Alerts`, `Config` (all required present). [CONFIG]
- `KPIs` columns: `Name` (text), `Current` (number), `Target` (number), `Attainment` (formula), `Status` (formula). [CÓDIGO]
- Attainment formula guards the zero target:

```text
=IF(C2=0,0,B2/C2)
```

- `Status` thresholds map to semantic colors from `template-policy.json` (no raw hex). [CONFIG]
- `Config` holds the threshold values and is labeled editable; `Status` reads from `Config!` named ranges. [CONFIG]
- Handoff: `renderer: brand-xlsx`, note "render RAG status as conditional formatting; sparkline on Trends is renderer-native." [EXPLICIT]

## Validation Gate

- [ ] Required sheets exist for the chosen template type.
- [ ] Every column has `header`, `width`, `type`, and `description`.
- [ ] Dropdown columns reference `Config!` or a named range formula.
- [ ] Formula columns start with `=` and pass formula-policy checks.
- [ ] Division formulas use `IF` guards.
- [ ] Conditional formatting uses approved semantic colors.
- [ ] Data sheets avoid merged cells and declare print areas.
- [ ] Named ranges are workbook-safe and point to cell ranges.
- [ ] Validation rows include status and evidence.
- [ ] Handoff names the renderer, output format, and rendering notes.
- [ ] Spec compiles clean via `compile-xlsx-template.py`; `check.sh` is green.
