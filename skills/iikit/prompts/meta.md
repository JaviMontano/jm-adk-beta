# Meta Prompt — iikit self-check

Use before finalizing any iikit invocation. Answer each; if any answer is "no" or
"unsure", fix before reporting done.

## Routing integrity
- Did I resolve `topic` to a single enum value, and read **exactly one**
  playbook? (Loading the cluster is a defect.)
- If intent was described rather than named, did I route to the *earliest unmet*
  stage — not the most convenient one?
- On ambiguity, did I ask one consolidated question instead of guessing or
  fanning out?

## Dependency integrity
- Does the predecessor artifact exist (or was it explicitly created)? Did I avoid
  running a stage on a missing predecessor?
- For testify/implement: is the assertion hash lock intact, stored in BOTH
  context.json and the git note?

## Determinism
- Did I run the `iikit-core` scripts the playbook prescribes, instead of
  re-deriving their output in-model?
- Did I surface any missing/non-zero script verbatim rather than assuming success?

## Output integrity
- One evidence-tag family only? No mixed Spanish/English tags?
- Zero placeholder tokens? No invented prices? No client PII? Single brand?
- Did I never report green as success without the gate evidence behind it?

## Failure-mode scan
- Constitution: any tech/stack leak, sub-3 principles, version mismatch?
- Specify: any orphan SC (no FR), surviving `[NEEDS CLARIFICATION]`, HOW-detail?
- Testify: any dangling `@FR/@SC/@US`, recycled `@TS-XXX`, unhashed assertions?
