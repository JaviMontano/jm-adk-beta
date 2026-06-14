# Deep Variation — testing-qa

`depth=deep`: apply the routed playbook exhaustively, verifying at every step.

## Use when
The request is high-stakes (payment/auth flows, a release gate, a regression-prone
module) or asks for a complete, defensible testing posture rather than a single
artifact.

## Procedure
1. Route to one `topic` (still exactly one playbook — depth widens coverage, not
   the number of playbooks).
2. Run the full spine exhaustively:
   - **Discover** — enumerate every in-scope surface, current coverage, CI gate
     points, and the highest-risk flows (payments, auth, data integrity).
   - **Analyze** — derive the full level mix / all applicable quality angles / the
     complete engine matrix / lab + field budgets; justify each by risk, not
     uniformity.
   - **Execute** — the complete artifact set: configs, mocks/POMs/feature files,
     CI assertions, and test-data strategy with isolation.
   - **Validate** — run every decisive check: diff coverage on all four metrics +
     3× flake run; 3-engine CI; budgets at p75 in field, not just lab; gate
     verified to actually block.
3. Cross-check against the playbook's Failure Modes table and Self-Correction
   triggers; resolve each before output.
4. Emit via `templates/output.md` with full evidence tagging and an explicit
   residual-risk note.

## Guardrails
Exhaustive means more checks, never more playbooks and never green-as-success.
Every relaxed threshold is gated and tagged, not silent.
