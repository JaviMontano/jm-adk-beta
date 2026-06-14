# legal-compliance — README

Router skill that sends legal/compliance work to exactly one playbook, then runs
that playbook end to end with evidence-tagged output and a mandatory legal
disclaimer. One topic resolves to one file — the cluster is never loaded whole.

## What it does

Resolves a `topic` and `depth`, reads a single reference playbook, and produces a
decision-support deliverable for one of three lanes:

| topic | Playbook | Produces |
|-------|----------|----------|
| `compliance-assessment` | `references/compliance-assessment.md` | Gap matrix, remediation roadmap, regulatory risk heat map (GDPR, SOX, PCI-DSS, HIPAA, ISO 27001, NIST CSF) |
| `compliance-framework` | `references/compliance-framework.md` | Control-to-evidence map, audit-readiness checklist (SOC2, ISO 27001, GDPR) |
| `contract-review` | `references/contract-review.md` | Clause-by-clause risk findings, redline-ready negotiation points, renewal/exit timeline |

## When to use

- Reviewing a contract/clause for risk, obligations, or red flags → `contract-review`.
- Measuring posture against a named regulation/standard → `compliance-assessment`.
- Designing controls, policies, or a control library from scratch → `compliance-framework`.
- NOT for: drafting net-new legal text, litigation strategy, jurisdiction-specific
  enforceability opinions, certification issuance — flag and defer to qualified counsel.

## How it routes and executes

1. Infer `topic` from the request. If two lanes fit, ask one disambiguating
   question — never guess.
2. Set `depth`: `quick` (essentials only) or `deep` (apply the playbook
   exhaustively, verify at each step).
3. Read only the routed file (`routes.json` / SKILL.md `routes:` map). Multi-topic
   requests run sequentially, one playbook each.
4. Spine: **Discover → Analyze → Execute → Validate**. The validation gate must
   pass before "done".

## Evidence taxonomy (Alfa core set)

Every non-obvious claim carries exactly one tag, one spelling throughout:
`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Each `[SUPUESTO]` pairs
with a concrete verification step. See `references/verification-tags.md`.

## Mandatory disclaimer

Every output carries verbatim: "This is a technical compliance gap assessment, not
legal advice. Regulatory interpretations and penalty exposure must be validated by
qualified legal counsel before action." Never assert PASS/compliant as fact; never
invent clause numbers, fines, or citations — degrade to `[SUPUESTO]` and flag.

## Bundle map

- `agents/` — lead, specialist, support, guardian role contracts.
- `knowledge/` — body of knowledge + knowledge graph for the three lanes.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — deliverable scaffold.
- `evals/evals.json` — scenario suite.
- `examples/` — worked contract-review input/output.
- `assets/` — quality rubric and routing checklist; see `assets/README.md`.
