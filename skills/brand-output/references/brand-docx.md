<!-- distilled from alfa skills/brand-docx -->
<!-- > -->
# Brand DOCX / Word Document Generation

## Purpose

Generate `.docx` artifacts that are deterministic, brand-token-compliant, and
validated as real Word packages. The skill may write the requested DOCX
artifact, but validation must stay offline and must pass the local contract
before delivery. [CONFIG]

Deterministic means: same inputs (tokens + content + caller-supplied date)
produce byte-stable structure, with no network calls, no runtime clock, and no
randomness. This is what lets `scripts/check.sh` run in CI without flaking. [INFERENCIA]

## Deterministic Resources

- `assets/manifest.json` declares all deterministic assets. [CÓDIGO]
- `assets/activation-policy.json` defines activation, routing, and false
  positives. [CÓDIGO]
- `assets/brand-docx-contract.json` defines required DOCX package parts,
  metadata, dependency boundaries, token rules, and validator checks. [CÓDIGO]
- `assets/fallback-brand-config.json` defines explicit fallback tokens when no
  brand config is supplied. [CÓDIGO]
- `assets/style-token-map.json` maps brand tokens to Word styles. [CÓDIGO]
- `assets/evidence-policy.json` defines evidence tags and report requirements.
  [CÓDIGO]
- `scripts/check.sh` validates valid and invalid DOCX fixtures offline.
  [CÓDIGO]

The contract JSON is the source of truth; this playbook is its human-readable
mirror. If they disagree, the contract wins and this file is stale. [SUPUESTO]
(Verify: diff the required-parts list here against `brand-docx-contract.json`.)

## When To Activate

Activate when the user asks for a Word document, `.docx`, branded proposal,
branded report, branded memo, cover page, python-docx generation, or a file
intended to open in Microsoft Word. [CONFIG]

Do not activate for HTML pages, XLSX spreadsheets, PDFs, slide decks, image
assets, or token extraction-only tasks. Route those requests to the appropriate
document or brand skill. [CONFIG]

Boundary cases [INFERENCIA]:
- "PDF from a Word file" → generate the `.docx` here; PDF export is out of scope
  and belongs to a downstream/print skill.
- "Word doc that is really a one-page form" → in scope; still a real DOCX
  package, not HTML.
- "Just give me the brand colors" → token extraction only; route away.

## Inputs

- Document type: proposal, report, memo, case study, brief, or cover page.
- Title, subtitle, section outline, tables, and footer requirements.
- Brand config path or inline brand tokens.
- Optional language and page size.
- Optional caller-supplied `artifact_date` and `year`; do not infer current
  date/time. If absent, leave the field blank or ask — never call the system
  clock (that breaks determinism). [CONFIG]
- Optional confidentiality flag.

Missing-input handling [INFERENCIA]:
- No title → stop and ask; a cover page without a title fails the contract.
- No outline → emit a minimal single-section body; do not invent content.
- No `year` but confidentiality requested → footer label still renders; year
  field stays blank rather than guessed.

## Brand Configuration

Search order (first hit wins):

1. Path passed as argument.
2. `./brand-config.json` in the working directory.
3. `references/brand/design-tokens.json` when the current repo brand applies.
4. `assets/fallback-brand-config.json` when no brand config exists.

Never read hidden user-level brand files for this skill. Rationale: the artifact
must be reproducible by anyone with the repo, so brand state lives in-repo, not
in a machine-local dotfile. [CONFIG]

Required token groups:

```json
{
  "brand": { "name": "", "wordmark": "", "tagline": "" },
  "colors": { "primary": "", "black": "", "white": "", "background": "", "muted": "" },
  "typography": { "display": "", "body": "", "fallback": "" },
  "docx": { "artifact_date": "", "year": "", "confidential": false }
}
```

A config missing any required key is invalid: fill the missing key from the
fallback config and tag the substitution, rather than partially merging two
brands. [INFERENCIA]

## Output Contract

Return exactly one of these outputs:

- A saved `.docx` artifact path plus validation evidence.
- A plan for generating the `.docx` when the user asks for instructions only.

The delivered `.docx` must include:

- Real DOCX ZIP package structure, not HTML renamed as `.docx`.
- `[Content_Types].xml`, `_rels/.rels`, `docProps/core.xml`,
  `word/document.xml`, and `word/styles.xml`.
- Core properties with title, creator, and caller-supplied artifact date.
- Cover or opening section with wordmark, title, tagline, and document type.
- Section headings styled from brand display font and primary underline.
- Body text styled from brand body font and black/muted tokens.
- Tables with primary header fill and white header text when tables exist.
- Footer metadata with caller-supplied year and confidentiality label when
  requested.
- No unresolved `{{PLACEHOLDER}}` tokens.
- No remote fonts, remote logos, remote images, base64 images, external scripts,
  runtime current-date calls, or random values.

## Token Rules

- Use supplied brand tokens or explicit fallback tokens only.
- Do not hardcode legacy palettes such as `#122562`, `#FFD700`, or `#137DC5`
  unless they are explicitly supplied in the active brand config. [CONFIG]
- Fallback defaults are `#2563EB`, `#0F172A`, `#FFFFFF`, `#F8FAFC`,
  `#475569`, `Aptos Display`, and `Aptos`.
- Preserve tokens in generated styles so validation can trace them. Concretely:
  emit the resolved hex/font into `word/styles.xml` so the validator can grep it
  back to a token — do not bury color only in inline run properties. [INFERENCIA]

## Validation Gate

- [ ] Brand config or fallback tokens are explicitly declared.
- [ ] Output is a real `.docx` package, not HTML or Markdown.
- [ ] Required DOCX ZIP parts exist.
- [ ] Core properties include caller-supplied title/date.
- [ ] Brand colors and fonts are present in document XML/styles.
- [ ] Tables, if present, use deterministic branded header styling.
- [ ] Footer metadata includes caller-supplied year and confidentiality state.
- [ ] No unresolved placeholders.
- [ ] No remote assets, base64 images, runtime dates, or randomness.
- [ ] `bash skills/brand-docx/scripts/check.sh` passes.

## Failure Modes

Common ways delivery fails the gate, and the fix [INFERENCIA]:

- **HTML renamed to `.docx`** → opens corrupt in Word; `[Content_Types].xml`
  missing. Build a real ZIP (python-docx or a templated package), never rename.
- **Color only inline, not in styles** → validator's token trace fails. Push
  color/font into named styles in `word/styles.xml`.
- **Runtime date leaked in** → non-deterministic; `check.sh` diff flips. Use
  only `artifact_date`/`year` from inputs.
- **Legacy palette hardcoded** → token rule violation even if it "looks branded."
  Resolve every color through the active config.
- **Unresolved `{{PLACEHOLDER}}`** → ships a template, not a document. Fail
  loudly if a required field is empty instead of emitting the placeholder.
- **Base64 or remote logo** → offline/determinism violation. Embed the local
  asset bytes declared in the manifest.

## Worked Example (proposal)

Inputs: type `proposal`, title `"AtlasOps Technical Proposal"`, config
`./brand-config.json`, one KPI table, `confidential: true`, `year: "2026"`.

Expected artifact [INFERENCIA]:
- Cover: wordmark + title + tagline + "Proposal" label, display font, primary
  underline on headings.
- KPI table: primary header fill, white header text, body in body font.
- Footer: "2026 · Confidential", no clock call.
- `check.sh` passes; evidence report lists each gate item as met.

## Assumptions And Limits

- This skill creates DOCX/Word artifacts only; it does not build HTML pages,
  XLSX spreadsheets, PDFs, or slide decks. [CONFIG]
- `python-docx` is a suitable implementation path when available, but the
  validation gate uses the Python standard library so CI remains deterministic.
  [CONFIG]
- Word rendering can vary by installed fonts; fallback fonts must be specified.
  [INFERENCIA]
- The validator checks structure, tokens, and determinism — not visual fidelity.
  A doc can pass the gate and still look wrong if the style map is mis-tuned;
  that is a style-token-map fix, not a validator gap. [SUPUESTO]
- Out of scope: macros/VBA, embedded OLE objects, tracked changes, and digital
  signatures. None are emitted; requests for them route elsewhere. [INFERENCIA]

## Usage

- `/brand-docx proposal "AtlasOps Technical Proposal" ./brand-config.json`
- `Generate a branded DOCX report with a cover page and KPI table`
- `Use python-docx to create a Word proposal using these brand tokens`
