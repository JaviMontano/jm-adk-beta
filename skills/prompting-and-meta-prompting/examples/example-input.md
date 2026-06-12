# Example Input — Vague PR-Review Request

A team lead types into the assistant:

> "We keep getting messy pull-request reviews. Can you give me a prompt our
> reviewers can paste so reviews are consistent? We use GitHub, reviews should
> focus on correctness and tests, not style nitpicks, and they should never ask
> the author to paste secrets or tokens. Output should be something we can drop
> into a PR comment."

## What the skill extracts (Discover)

| Field | Value | Status |
|---|---|---|
| Objective | Consistent, paste-ready PR-review prompt | Provided [DOC] |
| Audience | Code reviewers on the team | Provided [DOC] |
| Context | GitHub PRs; focus correctness + tests | Provided [DOC] |
| Constraints | No style nitpicks; never request secrets/tokens | Provided [DOC] |
| Output target | A PR comment (Markdown) | Provided [DOC] |
| Runtime/model | Not stated | `Dato requerido` → portable Markdown fallback [INFERENCE] |
| Definition of done | Not stated explicitly | Assume: review covers correctness, tests, risk; no style-only blocks `[ASSUMPTION]` |

## Ambiguity check

No two competing interpretations of the objective survive Discover, so the skill
proceeds to Analyze without asking a disambiguating question. [INFERENCE]

## Safety pre-check

The request explicitly forbids asking for secrets/tokens — consistent with the
skill's safety boundary, so no Guardian block is needed at intake. [DOC]
