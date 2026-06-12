# Routing & validation checklist — data-governance

A pre-flight and gate checklist the guardian and lead run on every invocation.

## Pre-flight (before loading a playbook)
- [ ] Request is about *governing* data, not authoring ETL / tuning schemas.
- [ ] One `topic` resolved from: audit-trail-design, data-documentation,
      data-governance, data-privacy-patterns, data-storytelling, data-strategy,
      pipeline-governance.
- [ ] Weakest-overlap rule applied; on a tie, one clarifying question asked.
- [ ] `depth` set (quick | deep).
- [ ] Required inputs available (inventory, schema/catalog access, regime);
      otherwise a `[SUPUESTO]` blocker is raised, not an inference.

## Execution
- [ ] Exactly ONE `references/<topic>.md` read. No siblings.
- [ ] Inputs captured from source (DDL, catalog, profiling), not from memory.
- [ ] Output assembled from `templates/output.md`.

## Gate (before "done")
- [ ] Output answers the resolved topic, not the router.
- [ ] Topic-specific quality criteria met (see assets/quality-rubric.json).
- [ ] Alfa evidence tags present; every `[SUPUESTO]` has a verification step.
- [ ] No invented prices; criteria not vendors; no client PII; single brand.
- [ ] Verdict emitted: pass only when every applicable box is checked.
