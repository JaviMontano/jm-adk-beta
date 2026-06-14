---
name: devops-deploy
version: 1.0.0
description: "CI/CD and release engineering router: pipelines, environments, deployment gates, rollbacks, git hooks, watchers, and repo hygiene. Routes one topic per call. Topics: ci-pipeline-design, dependency-management, deployment-checklist, environment-management, file-watcher, git-hook-integration, github-actions-ci, lighthouse-ci, linting-formatting, rollback-strategy."
params:
  topic:
    enum: [ci-pipeline-design, dependency-management, deployment-checklist, environment-management, file-watcher, git-hook-integration, github-actions-ci, lighthouse-ci, linting-formatting, rollback-strategy]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  ci-pipeline-design: references/ci-pipeline-design.md
  dependency-management: references/dependency-management.md
  deployment-checklist: references/deployment-checklist.md
  environment-management: references/environment-management.md
  file-watcher: references/file-watcher.md
  git-hook-integration: references/git-hook-integration.md
  github-actions-ci: references/github-actions-ci.md
  lighthouse-ci: references/lighthouse-ci.md
  linting-formatting: references/linting-formatting.md
  rollback-strategy: references/rollback-strategy.md
---

# devops-deploy

Router skill for CI/CD and release engineering. Resolve `topic`, then Read
EXACTLY ONE playbook from `routes:`. [DOC]

## When to use
A delivery / release / repo-hygiene task that maps to one `routes:` topic. This
router owns only these ten topics; hand non-deploy parts to sibling skills. [INFERENCE]

## Inputs → Outputs
- **In:** `topic` (required; infer), `depth` (quick|deep). [CONFIG]
- **Out:** the artifacts the playbook defines (workflow YAML, hook script,
  checklist, env matrix, rollback runbook), each claim tagged. [DOC]

## Routing procedure
1. Map the request to one topic. Synonyms: "release/ship" → deployment-checklist;
   "GHA/workflow" → github-actions-ci; "revert/undo deploy" → rollback-strategy;
   "pre-commit/husky" → git-hook-integration; "perf budget/web vitals in CI" →
   lighthouse-ci; "lockfile/upgrade/audit" → dependency-management. [INFERENCE]
2. Ambiguous or genuinely multi-topic → ask which one; never guess across. [DOC]
3. Read that one playbook. `deep` → apply exhaustively, verify each step;
   `quick` → essentials only. [CONFIG]

Spine: Discover → Analyze → Execute → Validate. [DOC]

Gate tooling: `assets/` holds the quality rubric and reviewer checklist that
back the validation gate below. [DOC]

## Validation gate (done = all true)
- Exactly one topic resolved and one playbook Read — not the cluster. [DOC]
- Topic ∈ the `routes:` enum (no invented topics; enum is source of truth). [CONFIG]
- Script-first honored: prefer scripted/idempotent steps over manual ones. [DOC]
- Evidence tags present (Alfa core, one spelling); constitution v6.0.0 holds. [DOC]

## Anti-patterns
- Loading multiple playbooks "to be safe" — defeats the router. [INFERENCE]
- Answering a deploy question inline without Reading the playbook. [INFERENCE]
- Renaming/extending topics, or editing `routes:` to fit the request. [CONFIG]
- Marking done on a green pipeline alone — green ≠ verified behavior. [DOC]

## Self-correction triggers
A step lacks its verification → re-read the playbook. Mid-task the real need is
a different topic → re-route. [INFERENCE]