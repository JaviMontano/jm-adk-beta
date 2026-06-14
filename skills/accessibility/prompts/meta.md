# Meta Prompt — accessibility self-check

Use before declaring an accessibility deliverable done. Answer each honestly; any
"no" blocks completion.

## Routing integrity
- Did I load **exactly one** playbook (audit / design / testing / writing)?
- Does the chosen `topic` match the user's actual intent, not the easiest path?
- If the request spanned two topics, did I sequence them instead of merging?

## Scope honesty
- Did I state the target artifact and the assumed WCAG level (AA unless told)?
- If no runnable target/asset existed, did I return a gap report instead of inventing one?

## Evidence
- Does every finding cite a specific WCAG success criterion and a concrete fix?
- Is automated evidence (command, tool, rule id, selector, artifact) recorded, and
  separated from manual evidence?
- Did I treat axe "0 violations" as "no automated violations found", not "accessible"?
- Is each unverifiable item marked `not verified` with a named next action?

## Status discipline
- Is the final status one of `pass` / `conditional` / `fail` / `not verified`?
- Did I avoid green-as-success (a clean scan / green CI never overrides a manual blocker)?

## Tag & governance integrity
- Does every claim carry exactly one tag from a single family (no tag drift)?
- For `writing`: is reader-facing copy tag-free with a separate validation table?
- No invented prices, no client PII, single-brand?

If any answer is "no", return to the failing step before producing the deliverable.
