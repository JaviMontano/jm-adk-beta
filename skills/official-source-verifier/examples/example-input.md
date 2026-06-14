# Example Input — GitHub CLI branch-delete default

## Question

Before updating our merge workflow, confirm: does `gh pr merge` delete the source branch
by default?

## Trigger

A team blog post (secondary) claims: "After `gh pr merge`, the branch is gone — branch
deletion is the default." Someone proposed removing our explicit cleanup step from the
workflow because "the CLI already does it."

## Context

- Repo uses GitHub CLI version 2.x in CI.
- Proposed change: delete the `gh api ... DELETE refs/heads/...` cleanup step from
  `.github/workflows/merge.yml`.
- The blog is the only source cited so far.

## What the verifier must produce

- A `source_registry` with the blog as `official=false, role=lead` and the GitHub CLI
  official manual as `official=true`.
- A claim about the branch-delete default, mapped to the official manual, with an ISO
  `accessed_date`.
- A `decision` stating whether the cleanup step may be removed, and any `blocking_gaps`.
