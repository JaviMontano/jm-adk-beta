# Example Output — GitHub CLI branch-delete default

- **Question**: Does `gh pr merge` delete the source branch by default?
- **Status**: `pass`
- **Repo version under decision**: GitHub CLI 2.x (CI)
- **Output mode**: human-readable
- **Date of verification**: 2026-06-12

## Source registry

| source_id | source_type | publisher | url | accessed_date | official | role |
|-----------|-------------|-----------|-----|---------------|----------|------|
| blog-merge-tip | blog | team blog | https://example.com/blog/gh-merge-cleanup | 2026-06-12 | false | lead |
| gh-cli-manual | manual | GitHub (cli.github.com) | https://cli.github.com/manual/gh_pr_merge | 2026-06-12 | true | authority |

## Claims

| claim_id | statement | source_ids | official_source_ids | status | tag |
|----------|-----------|-----------|---------------------|--------|-----|
| c1 | `gh pr merge` deletes the source branch only when `--delete-branch` (`-d`) is passed; it is NOT the default. | gh-cli-manual, blog-merge-tip | gh-cli-manual | verified | [DOC] |

Official extract (paraphrase): the manual documents a `--delete-branch` / `-d` flag to
delete the local and remote branch after merge. Absent that flag, the branch is retained.
The blog's "deletion is the default" claim is contradicted by the official manual and is
discarded as authority.

## Priority & conflicts

- Priority order applied: official > vendor > spec > repo > secondary. The GitHub CLI
  manual (official) overrides the blog (secondary).
- Conflicts between official sources: none.
- Version-currency findings: manual covers `gh` 2.x; matches repo CI. No version conflict.

## Decision

- **change_authorized**: false
- **justified_change**: Do NOT remove the explicit branch-cleanup step. The official
  manual shows deletion requires `--delete-branch`, so the workflow's `gh api DELETE`
  cleanup is still needed (or the merge command must add `-d`). The blog's premise is
  false.
- **scope**: `.github/workflows/merge.yml` — no removal authorized.
- **blocking_gaps**: none.

## Self-correction log

- Blog claim initially looked like authority; degraded to `role=lead` after the official
  manual contradicted it. `change_authorized` held at `false` because removing the step
  rests on a refuted claim.

## Acceptance gate

- [x] Every source has url, publisher, accessed_date (ISO), source_type.
- [x] The claim has non-empty official_source_ids (gh-cli-manual).
- [x] No `official=false` source is sole evidence of the `verified` claim.
- [x] `change_authorized=false` — consistent with the verified finding.
- [x] `blocking_gaps` empty; status `pass` is legitimate.
- [x] Report would pass `scripts/check.sh` when rendered as the JSON contract.

Single brand (JM Labs); no invented prices; green earned by evidence, not assumed; no
client PII.
