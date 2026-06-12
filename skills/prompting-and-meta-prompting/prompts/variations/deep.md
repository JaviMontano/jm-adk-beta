# Deep Variation — Full Prompt System with Meta-Review

Use when building a reusable prompt system intended for repeated, audited use.

## Procedure

1. **Discover** — full input table: objective, audience, constraints, allowed
   tools, privacy boundaries, definition of done, runtime target, examples. Flag
   every gap as `Dato requerido` before drafting.
2. **Analyze** — choose a pattern, enumerate failure modes, and decide whether a
   meta-prompt and a JSON prompt-system report are in scope.
3. **Execute**
   - Build the primary prompt (all eight components).
   - Build a meta-prompt with the seven review dimensions (see `prompts/meta.md`).
   - Author the full eval suite: happy path, minimal input, conflicting
     requirements, false positive, unsafe injection, plus hidden-CoT and
     credential-capture rejections.
   - If a JSON report is produced, align it to the `assets/` policies and validate
     with `bash skills/prompting-and-meta-prompting/scripts/check.sh`.
4. **Validate** — run the full validation gate and the Guardian safety boundaries.
   Confirm Guardian decisions are consistent with the eval `expected_activation`
   values. Deliver only on full pass.

## Output

A complete bundle: primary prompt, meta-prompt, acceptance criteria, full eval
suite, assumptions, safety note, and (when applicable) the validated JSON report.
All load-bearing claims tagged with the Alfa core set.
