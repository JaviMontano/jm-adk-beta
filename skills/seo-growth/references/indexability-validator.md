<!-- distilled from alfa skills/indexability-validator -->
<!-- > -->
# Indexability Validator

> "If a directory doesn't explain itself, it doesn't belong in the repo."

## TL;DR

Enforces Constitution XVIII: every directory MUST have a README.md. Scans the repository, flags directories missing READMEs, identifies orphan folders (not linked from parent), checks .gitignore has comments, and validates the index-driven navigation chain from root to leaves. Can generate stub READMEs for missing directories. [EXPLICIT]

## Procedure

### Step 1: Discover
- List all directories in the repository (excluding node_modules, .git, workspace/)
- For each directory, check if README.md exists
- Read root README.md for top-level directory links
- Check .gitignore for comment coverage

### Step 2: Analyze
- Classify directories:
  - **Complete**: has README, linked from parent
  - **Missing README**: no README.md present
  - **Orphan**: has README but not linked from parent index
  - **Stale**: no updates >30 days (check git log)
- Check .gitignore: every exclusion pattern should have a comment
- Calculate indexability score: `{complete}/{total}` directories

### Step 3: Execute
- Generate report:
  ```
  === Indexability Report ===
  Score: 85% (42/49 directories complete)

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

### Step 4: Validate
- All directories have README.md
- Root README links to all top-level directories
- Each directory README links to its children
- .gitignore has 100% comment coverage
- No stale directories without review acknowledgment
- Indexability score >= 95% for G3 passage

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
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
