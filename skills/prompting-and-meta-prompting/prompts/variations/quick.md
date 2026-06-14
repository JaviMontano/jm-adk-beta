# Quick Variation — Fast Prompt Hardening

Use when the objective is clear and the user wants a tightened prompt fast.

## One-pass procedure

1. Restate the objective in one line; if ambiguous, ask one question and stop.
2. Add the four load-bearing components if missing: explicit output contract,
   constraints, anti-drift rule, missing-data handling.
3. Attach a minimal eval triplet: happy path, false positive, unsafe injection.
4. Run the short gate below; deliver or self-correct once.

## Short gate

- Output contract is an explicit shape (not prose).
- Anti-drift + safety are embedded in the prompt text.
- No secrets / PII; no hidden chain-of-thought request.

## Output

The hardened prompt + the three evals + one-line assumption note. Tag claims
`[DOC]` `[INFERENCE]` `[ASSUMPTION]`. Block (`expected_activation: false`) on any
safety conflict instead of partially complying.
