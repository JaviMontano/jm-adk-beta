<!-- distilled from alfa skills/indexability-validator -->
<!-- > -->
# Indexability Validator

> "If a directory doesn't explain itself, it doesn't belong in the repo."

## TL;DR

Enforces Constitution XVIII: every directory MUST have a README.md. Scans the repository, flags directories missing READMEs, identifies orphan folders (not linked from parent), checks .gitignore has comments, and validates the index-driven navigation chain from root to leaves. Can generate stub READMEs for missing directories. [EXPLICIT]

**Anti-scope** (what this does NOT do): grade README *content* quality, fix broken intra-doc links, enforce naming conventions, or audit code. It checks README *presence*, the parent→child link chain, and .gitignore comments only. [EXPLICIT]

**Exit signal**: indexability score ≥ 95% AND zero orphans → G3-ready. Below 95% → blocking finding. [EXPLICIT]

## Procedure

### Step 1: Discover
- List all directories, excluding by default: `node_modules`, `.git`, `workspace/`, `dist`, `build`, `.next`, `coverage`, `__pycache__`, `.venv`, any path in `.gitignore`. Exclusion set is configurable; record it in the report header so the score is reproducible. [EXPLICIT]
- For each directory, check if `README.md` exists (case-sensitive on Linux/CI; treat `readme.md` as a finding, not a pass — case mismatch breaks links on case-sensitive filesystems). [EXPLICIT]
- Read root README.md and extract top-level directory links (markdown directory links and bare `path/` references).
- Check .gitignore for comment coverage.
- **Decision**: walk the tree top-down, not via `git ls-files`. Trade-off — top-down catches empty/untracked dirs that should be documented or removed; `git ls-files` would miss them but is faster. Correctness wins here. [EXPLICIT]

### Step 2: Analyze
- Classify each directory into exactly one bucket (priority order resolves overlap: Missing README > Orphan > Stale > Complete):
  - **Complete**: has README, linked from parent index
  - **Missing README**: no README.md present (highest severity)
  - **Orphan**: has README but not linked from parent index (navigation dead-end)
  - **Stale**: no updates >30 days (check `git log -1 --format=%cr -- <dir>`)
- Check .gitignore: every exclusion pattern should have a comment on the line above or trailing it.
- Calculate indexability score: `{complete}/{total scanned}` as a percentage. A directory in any non-Complete bucket does not count toward the numerator. [EXPLICIT]
- **Stale is advisory, not blocking** — recency ≠ correctness; a stable utility dir may be legitimately untouched. Surface it for human acknowledgment, never auto-fail G3 on staleness alone. [EXPLICIT]

### Step 3: Execute
- Generate report:
  ```
  === Indexability Report ===
  Excluded: node_modules, .git, workspace/, dist, build  (5 patterns)
  Score: 85% (42/49 directories complete) | Orphans: 1 (BLOCKING)

  Missing README:
  - skills/new-skill/ — NEEDS README
  - templates/node-api/ — NEEDS README

  Orphan (not linked from parent):
  - references/priming-rag/ — not in references/README.md

  Stale (>30 days):
  - .specify/decisions/ — last update 45 days ago

  .gitignore coverage: 8/10 patterns have comments
  ```
- Optionally generate stub READMEs:
  ```markdown
  # {Directory Name}

  > Purpose: {inferred from contents}

  ## Contents

  {list of files/subdirectories}
  ```
- Fix .gitignore: add comments to uncommented patterns

### Step 4: Validate (acceptance criteria)
- All scanned directories have README.md (0 in Missing bucket)
- Root README links to all top-level directories
- Each directory README links to its children (0 orphans)
- .gitignore has 100% comment coverage
- No stale directories without review acknowledgment
- Indexability score ≥ 95% for G3 passage

**Why 95%, not 100%**: the long tail (transient scaffolding, dirs pending a same-PR README) shouldn't hard-block a gate while the chain is otherwise navigable. Set 100% only on a frozen/released tree where every dir is final. Orphans are held at 0 regardless of score — an orphan is a broken navigation edge, not a rounding gap. [EXPLICIT]

## Failure Modes

| Failure | Cause | Mitigation |
|---------|-------|------------|
| Score looks high but tree is unnavigable | Orphans not counted as failures, or `total` shrunk by over-broad exclusions | Report orphan count separately; echo the exclusion set in the header |
| False "Missing README" on case-sensitive CI | `readme.md` vs `README.md` | Flag case mismatch explicitly; never silently pass it |
| Stub README overwrites a real one | Generator not idempotent | Generate ONLY when no README exists; never clobber. Dry-run by default, write on `--apply` |
| `.gitignore` shows 100% but patterns wrong | Comment present, pattern still over/under-broad | This skill checks comment *presence*, not pattern correctness — out of scope, note in report |
| Score drifts between runs | Nondeterministic dir ordering or unpinned exclusions | Sort directories; pin and log exclusion set |

## Quality Criteria

- [ ] All directories scanned
- [ ] Missing READMEs flagged with path
- [ ] Orphan directories identified
- [ ] Stale directories flagged (>30 days)
- [ ] .gitignore comments validated
- [ ] Indexability score calculated
- [ ] Stub READMEs generated for gaps (optional)

## Related Skills

- `repository-organization` — Broader structural health audit
- `code-review` — Sustainability check includes README presence (XII)
- `workspace-governance` — Workspace follows same README rules

## Usage

Example invocations:

- "/indexability-validator" — Run the full indexability validator workflow
- "indexability validator on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty directory (no files) | Flag as Missing README; recommend either documenting purpose or deleting — empty dirs git can't even track |
| Symlinked directory | Resolve once, do not follow into target; skip to avoid double-counting and cycles |
| Monorepo with nested `.gitignore` files | Merge exclusion patterns per subtree; a child `.gitignore` scopes only its subtree |
| Directory documented in a parent OTHER than its immediate parent | Still an orphan — the chain must hold link-by-link, not skip levels |
| Generated/vendored dir not in exclusion list | Add to exclusions and re-run; do not author a README for code you don't own |
| No git history (fresh clone, shallow) | Skip Stale classification (advisory), report all other buckets normally |
