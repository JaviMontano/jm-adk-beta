# brand-output

Router skill for **branded deliverable generation** with design-system tokens
(MetodologIA DS / MetodologIA brand). It does not generate artifacts itself — it
resolves a `topic` and Reads **exactly one** downstream playbook from `routes.json`
that owns the actual generation contract. [EXPLICIT]

## What it does

Takes a request to produce a branded artifact (HTML page, folio, DOCX, XLSX,
slide deck, or reusable template), infers which of 8 topics applies, and loads
the single matching playbook. The playbook then enforces token compliance,
determinism, and an offline validation gate before delivery. [CONFIG]

## When to use

Use it whenever the user asks for a branded output and the exact format/topic
needs disambiguation. Do **not** use it for raw content authoring with no brand,
or non-DS output — route those elsewhere. [INFERENCE]

## How it routes

1. Infer `topic` from the request; ask only if ≥2 enums fit equally. [EXPLICIT]
2. Read that single playbook (`deep` → exhaustive; `quick` → essentials). [EXPLICIT]
3. Format-vs-topic disambiguation:
   - HTML → `brand-html` (general) · `html-brand` (MetodologIA DS, token-heavy) ·
     `branded-html-output` (MetodologIA template, lightweight) ·
     `folio-generator` (numbered paginated folios). [INFERENCE]
   - Slides → `presentation-design`. DOCX → `brand-docx`.
     XLSX → `brand-xlsx` (one-off binary) vs `xlsx-template-creator` (reusable spec). [INFERENCE]

Spine: **Discover → Analyze → Execute → Validate.**

## Topics and references

| topic | playbook | output |
|---|---|---|
| `brand-html` | [references/brand-html.md](references/brand-html.md) | self-contained HTML page |
| `html-brand` | [references/html-brand.md](references/html-brand.md) | MetodologIA DS HTML deliverable |
| `branded-html-output` | [references/branded-html-output.md](references/branded-html-output.md) | MetodologIA template HTML |
| `folio-generator` | [references/folio-generator.md](references/folio-generator.md) | numbered folio `PREFIX-YYYY-NNN` |
| `brand-docx` | [references/brand-docx.md](references/brand-docx.md) | `.docx` Word package |
| `brand-xlsx` | [references/brand-xlsx.md](references/brand-xlsx.md) | `.xlsx` Excel package |
| `xlsx-template-creator` | [references/xlsx-template-creator.md](references/xlsx-template-creator.md) | workbook spec (no binary) |
| `presentation-design` | [references/presentation-design.md](references/presentation-design.md) | Minto-structured deck |

## Evidence taxonomy

Alfa core kit, never mixed with other families:
`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. The SKILL.md routing
notes use the harness kit set `[EXPLICIT]`/`[INFERENCE]`/`[ASSUMPTION]`. [DOC]

## Bundle

- `agents/` — lead, specialist, support, guardian role contracts for this router.
- `knowledge/` — domain body-of-knowledge + concept graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — routing-decision + artifact-handoff scaffold.
- `evals/evals.json` — routing and gate scenarios.
- `examples/` — a worked routing example.
- `assets/` — quality rubric and routing checklist (see `assets/README.md`).
