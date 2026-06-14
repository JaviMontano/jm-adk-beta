<!-- distilled from alfa skills/brand-xlsx -->
<!-- > -->
# Brand XLSX / Excel Workbook Generation

## Purpose

Generate `.xlsx` artifacts that are deterministic, brand-token-compliant, and
validated as real Excel packages. The skill may write the requested XLSX
artifact, but validation must stay offline and must pass the local contract
before delivery. [CONFIG]

## Deterministic Resources

- `assets/manifest.json` declares all deterministic assets. [CÓDIGO]
- `assets/activation-policy.json` defines activation, routing, and false
  positives. [CÓDIGO]
- `assets/brand-xlsx-contract.json` defines required XLSX package parts,
  workbook features, dependency boundaries, token rules, and validator checks.
  [CÓDIGO]
- `assets/fallback-brand-config.json` defines explicit fallback tokens when no
  brand config is supplied. [CÓDIGO]
- `assets/style-token-map.json` maps brand tokens to workbook styles. [CÓDIGO]
- `assets/evidence-policy.json` defines evidence tags and report requirements.
  [CÓDIGO]
- `scripts/check.sh` validates valid and invalid XLSX fixtures offline.
  [CÓDIGO]

## When To Activate

Activate when the user asks for an Excel workbook, `.xlsx`, branded
spreadsheet, spreadsheet report, KPI dashboard, openpyxl generation, or a file
intended to open in Microsoft Excel. [CONFIG]

Do not activate for CSV-only exports, HTML pages, DOCX documents, PDFs, slide
decks, image assets, or token extraction-only tasks. Route those requests to
the appropriate document or brand skill. [CONFIG]

## Inputs

- Workbook type: report, KPI dashboard, inventory table, financial summary, or
  operational workbook.
- Title, subtitle, sheet name, headers, rows, KPI blocks, and footer needs.
- Brand config path or inline brand tokens.
- Optional caller-supplied `artifact_date`, `year`, and `domain`; do not infer
  current date/time.
- Optional wide-data and print/freeze-pane requirements.

## Brand Configuration

Search order:

1. Path passed as argument.
2. `./brand-config.json` in the working directory.
3. `references/brand/design-tokens.json` when the current repo brand applies.
4. `assets/fallback-brand-config.json` when no brand config exists.

Never read hidden user-level brand files for this skill. [CONFIG]

Required token groups:

```json
{
  "brand": { "name": "", "wordmark": "", "tagline": "" },
  "colors": { "primary": "", "black": "", "white": "", "background": "", "muted": "", "primarySoft": "" },
  "typography": { "body": "" },
  "xlsx": { "artifact_date": "", "year": "", "domain": "" }
}
```

## Output Contract

Return exactly one of these outputs:

- A saved `.xlsx` artifact path plus validation evidence.
- A plan for generating the `.xlsx` when the user asks for instructions only.

Acceptance criteria (all must hold before delivery): the file opens in
Excel/LibreOffice without a repair prompt; `check.sh` exits `0`; every
validation-gate box below is checked with evidence. A partial or
repair-prompting workbook is a FAIL, not a warning. [CONFIG]

The delivered `.xlsx` must include:

- Real XLSX ZIP package structure, not HTML or CSV renamed as `.xlsx`.
- `[Content_Types].xml`, `_rels/.rels`, `docProps/core.xml`,
  `xl/workbook.xml`, `xl/_rels/workbook.xml.rels`, `xl/styles.xml`, and at
  least one `xl/worksheets/sheet*.xml`.
- Core properties with title, creator, and caller-supplied artifact date.
- Meaningful sheet names, not `Sheet1`.
- Primary tab color.
- Merged title region, header row, data rows, and footer metadata.
- Brand colors and fonts in `xl/styles.xml`.
- Freeze panes, auto filter, and bounded column widths.
- Footer metadata with wordmark, tagline, caller-supplied year, and domain.
- No unresolved `{{PLACEHOLDER}}` tokens.
- No remote fonts, remote logos, remote images, base64 images, external
  relationships, runtime current-date calls, or random values.

## Edge Cases

- Empty `rows`: still emit header row, freeze panes, and footer; do not skip
  styling or emit a zero-sheet workbook. [INFERENCIA]
- Sheet names: max 31 chars; strip `\ / ? * [ ] :`; must be unique. Truncate
  deterministically (no counters that change per run). [CÓDIGO]
- Leading `= + - @` in any cell value: prefix with `'` (text) so Excel does
  not evaluate it. Generated workbooks never emit live formulas. [CÓDIGO]
- Wide data (> 26 columns): bound each width and keep auto filter across the
  full used range, not just A–Z. [CONFIG]
- Long strings / numbers: store numbers as numeric cells (not text) so sums
  work; keep IDs that have leading zeros as text. [INFERENCIA]
- Non-ASCII / emoji in titles or headers: valid; XML-escape and keep UTF-8.

## Failure Modes (reject before delivery)

- HTML or CSV renamed to `.xlsx` — not a ZIP; fails the package check. [CÓDIGO]
- Missing `_rels/.rels` or `xl/_rels/workbook.xml.rels` — Excel shows a repair
  prompt; treat repair prompt as FAIL. [CÓDIGO]
- `Sheet1` left as a name, or merged region without an anchor value. [CONFIG]
- Unresolved `{{PLACEHOLDER}}`, legacy hardcoded palette, or remote/base64
  asset — token or asset violation, not cosmetic. [CONFIG]
- Runtime `=TODAY()`/`NOW()` or `random()` — breaks determinism; two runs with
  identical inputs must yield byte-stable structure. [CÓDIGO]

## Token Rules

- Use supplied brand tokens or explicit fallback tokens only.
- Do not hardcode legacy palettes such as `#122562`, `#FFD700`, `#137DC5`, or
  `#FF7E08` unless they are explicitly supplied in the active brand config.
  [CONFIG]
- Fallback defaults are `#2563EB`, `#0F172A`, `#FFFFFF`, `#F8FAFC`,
  `#475569`, `#EFF6FF`, and `Calibri`.
- Preserve tokens in generated styles so validation can trace them.

## Validation Gate

- [ ] Brand config or fallback tokens are explicitly declared.
- [ ] Output is a real `.xlsx` package, not HTML/CSV/Markdown.
- [ ] Required XLSX ZIP parts exist.
- [ ] Core properties include caller-supplied title/date.
- [ ] Sheet names are meaningful.
- [ ] Tab color uses primary token.
- [ ] Title/footer regions are merged.
- [ ] Headers, alternating rows, and footer use deterministic branded styles.
- [ ] Freeze panes, auto filter, and bounded column widths are present.
- [ ] No unresolved placeholders.
- [ ] No remote assets, base64 images, runtime dates, or randomness.
- [ ] `bash skills/brand-xlsx/scripts/check.sh` passes.

## Decisions And Trade-offs

- Validator uses the Python standard library (`zipfile` + XML parsing), not
  `openpyxl`. Trade-off: more validation code, but CI runs with zero third-party
  deps so the gate cannot drift with a library upgrade. [CONFIG]
- `openpyxl` is allowed for *generation* when available; it is not required for
  *validation*. Generation path and validation path are decoupled. [CONFIG]
- Determinism over convenience: no runtime dates or randomness, so identical
  inputs produce a structurally identical package, enabling diff-based review.
  [CÓDIGO]

## Assumptions And Limits

- Creates XLSX/Excel artifacts only; does not build HTML, DOCX, PDF, slide
  decks, or CSV-only exports. Route those elsewhere. [CONFIG]
- Excel rendering varies by installed fonts; fallback font must be declared so
  layout degrades predictably. [INFERENCIA]
- Anti-scope: no macros/VBA (`.xlsm`), no live external data connections, no
  pivot caches, no charts requiring remote images. [CONFIG]

## Worked Example

Input: `/brand-xlsx "AtlasOps KPI Workbook" ./brand-config.json`, 1 KPI block
(3 boxes) + 40-row data table, `artifact_date=2026-06-11`, `year=2026`.
Expected output: one `.xlsx` whose sheet is named `KPI Workbook` (not
`Sheet1`), tab color = primary token, merged title region A1, frozen header at
row 2, auto filter on the used range, alternating row fill from
`colors.primarySoft`, footer with wordmark + tagline + `2026` + domain, and
`check.sh` exit `0`. [CÓDIGO]

## Usage

- `/brand-xlsx "AtlasOps KPI Workbook" ./brand-config.json`
- `Generate a branded XLSX report with KPI boxes and a data table`
- `Use openpyxl to create an Excel workbook using these brand tokens`
