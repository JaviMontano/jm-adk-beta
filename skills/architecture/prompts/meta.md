# Meta prompt — architecture (self-check before responding)

Use this to audit your own architecture output before handoff. Answer each;
any "no" blocks done.

## Routing integrity
- Did I resolve to EXACTLY one `topic` in the enum?
- Did I load EXACTLY one playbook (no "load both to be safe")?
- If the request spanned topics, did I pick the dominant one and offer to chain
  rather than merge?
- If truly ambiguous, did I ask instead of guessing?

## Evidence discipline
- Does every non-obvious claim carry one Alfa-core tag, one family, one spelling?
- Is every `[ASSUMPTION]` paired with a concrete verification step?
- Did I avoid inventing prices (FTE-months only)?

## Architectural honesty
- Does every recommended pattern name a rejected alternative AND its cost?
- Do quality-attribute scenarios state a measure (number + unit), not an
  adjective?
- Did I avoid "we might need to scale" as a driver (that is `[ASSUMPTION]`)?

## Completeness
- Are all required `templates/output.md` fields filled (no `TBD`)?
- If `depth=quick`, did I name what I skipped?
- Does the deliverable match what the resolved playbook actually prescribes?

If all "yes", emit the artifact plus the guardian gate verdict. Otherwise fix
the failing item first.
