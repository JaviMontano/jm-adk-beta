# Deep variation — docs-writing (depth=deep)

Publication-grade path. Every spine stage is exhausted and each carries an explicit
verification.

## Use when

The deliverable will be published, audited, or read by an external audience.

## Steps

1. Resolve `topic`; confirm it is the single best route (state why the alternatives lose).
2. Read `references/<topic>.md` — only that one.
3. **Discover** every source the route can use; enumerate gaps as `[SUPUESTO]` with the
   step that confirms each.
4. **Analyze** options and log the trade-off accepted per decision (not just the winner).
5. **Execute** every section of `templates/output.md` with realistic, redacted examples.
6. **Validate** the FULL Quality Criteria with active checks:
   - api-documentation: lint the spec, replay ≥1 example against staging, prove error
     catalog ↔ code consistency.
   - changelog-writing: confirm every breaking change has a migration path; semver bump
     matches the highest-impact change.
   - documentation-standards: front-matter complete, quadrant declared, links lint clean.
   - internal-memo: a reader skimming only BLUF + action items can still act correctly.

## Output

The full deliverable plus a verification log per criterion and the guardian's PASS/BLOCK
verdict. One tag family; every `[SUPUESTO]` retired or carried with its check.
