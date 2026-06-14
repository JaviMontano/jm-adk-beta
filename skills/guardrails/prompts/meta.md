# Meta prompt — guardrails

Use this to author or refine a guardrails playbook, eval, or verdict packet —
i.e. to reason **about** the guard layer, not to run a single guard.

## Design invariants any guard must preserve

1. **One topic, one playbook.** The router reads exactly one reference. A new
   guard must slot into the `topic` enum and `routes.json` without tempting
   multi-load. [EXPLICIT]
2. **Fail-closed default.** Define the restrictive verdict for every undecidable
   path (unparseable command, missing asset, absent artifact). Silence ≠ pass.
   [EXPLICIT]
3. **Script-first determinism.** Name an offline validator + a `check.sh` with
   positive AND negative fixtures. No clock/network/model/random in the verdict.
   [CONFIG]
4. **Evidence taxonomy.** Alfa core family only, one tag per claim, single family.
   [DOC]
5. **No green-by-default.** Acceptance criteria must make a false `pass`
   detectable (e.g. forbid empty checks arrays, require triggering-rule citation).
   [EXPLICIT]

## When designing a guard, answer

- What is the verdict vocabulary (allow/approve/block vs pass/fail/blocked)?
- What is the fail-closed precedence, top-down, first-match-wins?
- Which JSON policy assets are the single source of truth, and what happens when
  one is missing? (→ `blocked`/`needs_evidence`, never improvise.)
- What is the worst-segment / worst-row rule for compound inputs?
- How are secrets masked so the report itself never leaks?

## Anti-scope to encode

State explicitly what the guard does NOT do, and where that work routes instead
(e.g. pre-tool-use-guard does not validate OUTPUT — that is
post-tool-use-validator). [INFERENCE]
