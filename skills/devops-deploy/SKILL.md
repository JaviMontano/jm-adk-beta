---
name: devops-deploy
description: "CI/CD and release engineering: pipelines, environments, deployment gates, rollbacks, hooks, and repo hygiene. Topics: ci-pipeline-design, dependency-management, deployment-checklist, environment-management, file-watcher, git-hook-integration, github-actions-ci, lighthouse-ci, linting-formatting, rollback-strategy."
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

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
