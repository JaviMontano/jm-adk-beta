# Assets — marketing-content

Reusable artifacts that support routing and the validation gate. Declared in
`manifest.json`.

| Asset | Type | Used by | Purpose |
|-------|------|---------|---------|
| `quality-rubric.json` | rubric | SKILL.md, agents/guardian.md | Weighted scoring across routing integrity, topic acceptance, evidence tagging, governance, and open-item disclosure; drives the dod verdict. |
| `checklist.md` | checklist | README.md, templates/output.md | Fast pre-return checklist for route → discover → execute → governance gates. |

## How to use
- The **guardian** scores a run against `quality-rubric.json`; `dod=pass` only
  when routing integrity, topic acceptance, and governance all pass.
- **support** and reviewers run `checklist.md` before return as a quick gate
  complementing the resolved playbook's own Quality/Acceptance Criteria.

Keep these in sync with the playbook acceptance criteria under `references/`.
