# Prompt — meta (carrera self-check)

Use this prompt to audit a `carrera` run before it ships. Answer each question
with evidence, not assertion. Any "no" returns the work to the specialist.

## Routing
- Was exactly ONE `routes.json` playbook loaded? Name it and its path.
- Was `topic` resolved unambiguously, or was one disambiguating question asked?
- Was `depth` applied (quick = essentials, deep = exhaustive) without weakening
  the gates?

## Faithfulness
- Does every specific claim trace to a supplied evidence id, or is it marked
  open? List any unsupported claim.
- Are all numbers (salary, settlement, FX, scores) supplied or computed from
  supplied figures — never invented?
- Are relative dates preserved and blocking, with no wall-clock math?

## Contract & determinism
- Does the output match the playbook's `assets/output-contract.json` and
  `templates/output.md`?
- Did the deterministic validator exit `0`, and is that exit reported (not
  assumed)?
- Would identical input produce identical bytes (sort keys honored)?

## Tags & governance
- One tag family throughout (authoring OR provenance), spelled consistently?
- No PII echoed, single brand, no green-as-success, no FOMO/servility in
  gratitude/counterproposal text?
- On any `{VACIO_CRITICO}`, did the run stop and ask instead of auto-filling?

Return: pass/fail per section + the one fix that most improves faithfulness.
