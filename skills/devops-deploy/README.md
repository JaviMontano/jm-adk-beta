# devops-deploy

A CI/CD and release-engineering **router** skill. It owns exactly ten delivery
topics and, per call, resolves one `topic` and reads one playbook from
`routes.json` / `references/`. It never loads the whole cluster. [DOC]

## What it does

Turns a delivery / release / repo-hygiene request into a single grounded
playbook execution that produces a verifiable artifact — workflow YAML, hook
plan, deploy checklist, environment matrix, or rollback runbook — with every
claim carrying an evidence tag. [DOC]

## When to use

Use it when the task maps to one of these topics:

| Topic | Use when | Playbook |
|-------|----------|----------|
| `ci-pipeline-design` | shaping a pipeline's job graph / gates before YAML | `references/ci-pipeline-design.md` |
| `dependency-management` | lockfiles, upgrades, audit, supply-chain hygiene | `references/dependency-management.md` |
| `deployment-checklist` | pre/post go-live validation before a prod deploy | `references/deployment-checklist.md` |
| `environment-management` | dev/staging/prod separation, env vars, CLI aliases | `references/environment-management.md` |
| `file-watcher` | local dev rebuild/reload watchers | `references/file-watcher.md` |
| `git-hook-integration` | pre-commit / commit-msg / pre-push hooks | `references/git-hook-integration.md` |
| `github-actions-ci` | authoring or hardening GitHub Actions workflows | `references/github-actions-ci.md` |
| `lighthouse-ci` | perf/web-vitals budgets enforced in CI | `references/lighthouse-ci.md` |
| `linting-formatting` | lint/format config and enforcement | `references/linting-formatting.md` |
| `rollback-strategy` | choosing a revert pattern before deploy | `references/rollback-strategy.md` |

Do not use it for infra provisioning (IaC apply), DNS cutover, secret
rotation, or cloud OIDC trust-role setup — those are named as prerequisites and
handed to sibling skills. [INFERENCIA]

## How it routes / executes

1. Map the request to **one** `routes.json` topic. Synonyms: "release/ship" →
   `deployment-checklist`; "GHA/workflow" → `github-actions-ci`; "revert/undo
   deploy" → `rollback-strategy`; "pre-commit/husky" → `git-hook-integration`;
   "perf budget in CI" → `lighthouse-ci`; "lockfile/upgrade/audit" →
   `dependency-management`. [INFERENCIA]
2. Ambiguous or genuinely multi-topic → ask which one; never guess across. [DOC]
3. Read that one playbook. `depth=deep` → apply exhaustively and verify each
   step; `quick` → essentials only. [CONFIG]
4. Spine: **Discover → Analyze → Execute → Validate**. Done only when the
   playbook's validation gate is all-true. [DOC]

## Evidence taxonomy

Every user-facing claim is tagged: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]`
`[SUPUESTO]` (`[EXPLICIT]` for verbatim user/source statements). Green pipeline
≠ verified behavior — never mark done on green alone. Constitution v6.0.0. [DOC]

## References

All ten playbooks live in `references/`; the routing table is `routes.json`.
The DoD bundle around this skill is documented below.

## Bundle map

- `agents/` — lead, specialist, support, guardian role contracts for this skill.
- `knowledge/` — body of knowledge + concept knowledge graph.
- `prompts/` — primary, meta, and quick/deep variation prompts.
- `templates/output.md` — the deliverable scaffold.
- `evals/evals.json` — routing + execution evaluation cases.
- `examples/` — a worked GitHub Actions hardening example.
- `assets/` — quality rubric and reviewer checklist used by SKILL.md and evals.
