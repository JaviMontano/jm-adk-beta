# Body of Knowledge — brand-output

Domain knowledge for routing and producing branded deliverables with design-system
tokens. Evidence kit: Alfa core (`[CÓDIGO]`/`[CONFIG]`/`[DOC]`/`[INFERENCIA]`/`[SUPUESTO]`). [DOC]

## 1. Core concept: router, not generator

`brand-output` is a dispatcher. Its job is to pick **one** of 8 topics and Read
its playbook; the playbook owns the generation contract. Loading more than one
playbook is the primary anti-pattern — it dilutes context and invites brand mixing. [EXPLICIT]

## 2. The 8 topics and their output classes

| topic | brand system | output class | binary? |
|---|---|---|---|
| `brand-html` | fallback config (`#2563EB` default) | self-contained HTML | yes (text file) |
| `html-brand` | MetodologIA DS (`#FFD700`, Poppins, Inter) | HTML deliverable | yes |
| `branded-html-output` | MetodologIA (navy `#122562`, gold `#FFD700`) | HTML from template | yes |
| `folio-generator` | neutral business tokens | numbered folio HTML/MD | yes |
| `brand-docx` | fallback + style-token-map | `.docx` OOXML | yes |
| `brand-xlsx` | fallback + style-token-map | `.xlsx` OOXML | yes |
| `xlsx-template-creator` | n/a (spec only) | workbook spec (MD/YAML) | **no** |
| `presentation-design` | brand chrome via brand-pptx | deck structure | no |

Key distinction: `xlsx-template-creator` emits a **spec**, not a binary — hand the
spec to `brand-xlsx` (the renderer) for a finished workbook. [CONFIG]

## 3. Determinism standard

Same brand config + same content + same caller-supplied `artifact_date` ⇒
byte-stable output. Forbidden at generate time: runtime system clock, remote
fetches, randomness. This is what lets each playbook's `scripts/check.sh` run
offline in CI without flaking. Never infer the current date — pass it explicitly. [INFERENCIA]

## 4. Token discipline

- Brand config search order (HTML family): arg path → `./brand-config.json` →
  `references/brand/design-tokens.json` → fallback config. First match wins. [CONFIG]
- Hardcoded hex/fonts allowed **only** inside `:root` token declarations or token
  files; every consumer references `var(--…)` / mapped styles. [CONFIG]
- Partial config → merge supplied tokens over fallback per-key; record each
  inherited key as `[SUPUESTO]` so the gap is auditable. [INFERENCIA]
- Never mix two brands in one output. Identify the brand before generating. [EXPLICIT]

## 5. Folio numbering rules

Format `PREFIX-YYYY-NNN`: `PREFIX` uppercase A–Z (COT/MEM/FAC/MIN/DOC + custom);
`YYYY` from the issue-date field, not the render clock; `NNN` a zero-padded
correlative that resets per `PREFIX-YYYY`. Reserve via `--apply` (atomic) only;
`--dry-run` previews without mutating the tracker. A spent number is never reused —
cancelled docs are marked void, not deleted. [CÓDIGO]

## 6. Format-specific contracts (decision rules)

- **HTML**: single file, semantic landmarks, ≥1 `@media`, SVG favicon (not remote,
  not base64), WCAG AA contrast or a recorded deterministic limitation, no
  surviving `{{PLACEHOLDER}}`, no external JS. [CONFIG]
- **DOCX/XLSX**: must be valid OOXML packages, generated via python-docx/openpyxl,
  validated against valid+invalid fixtures by `check.sh`. [CÓDIGO]
- **Presentation**: Minto pyramid — lead with the answer, group 3–5 MECE
  arguments, one idea per slide, title = the takeaway. Passes the title-only test. [EXPLICIT]

## 7. Governance standards

Constitution v6.0.0 enforcement; script-first generation; evidence tags on
non-obvious claims; no invented prices; no client PII; single-brand per output.
Never report a gate green by default — only when each box is verified. [DOC]

## 8. Anti-patterns (high-cost mistakes)

- Loading multiple playbooks to compare. [EXPLICIT]
- Taking the year from the render clock instead of the issue-date field. [CONFIG]
- Editing a tracker/state file with grep/sed. [CONFIG]
- Emitting a binary from `xlsx-template-creator` (spec-only skill). [EXPLICIT]
- Asserting contrast pass on a named-color/`var()` chain that can't be resolved. [SUPUESTO]
