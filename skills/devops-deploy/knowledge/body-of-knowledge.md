# Body of Knowledge — devops-deploy

Domain knowledge for the CI/CD and release-engineering router. Grounded in the
ten reference playbooks. [DOC]

## 1. Key concepts

- **Router discipline.** One call resolves one `topic` and reads one playbook.
  The ten topics are the source of truth; the enum is not extensible at runtime. [CONFIG]
- **Delivery spine.** Discover → Analyze → Execute → Validate. Every topic runs
  this spine; "done" is the playbook's validation gate, not a green build. [DOC]
- **Script-first.** Prefer scripted, idempotent steps over manual ones; manual
  deploys lack an audit trail and are not reproducible for rollback. [INFERENCIA]
- **Evidence taxonomy.** `[CÓDIGO]` (from code), `[CONFIG]` (from config),
  `[DOC]` (from docs/standard), `[INFERENCIA]` (reasoned), `[SUPUESTO]`
  (assumption), `[EXPLICIT]` (verbatim source/user). Every claim tagged. [DOC]

## 2. Standards & policies

- **Least privilege (CI tokens).** Default `permissions: contents: read` at the
  workflow top level; widen per job only with a recorded reason. [DOC]
- **Supply-chain pinning.** Pin third-party actions to immutable SHA in release
  and deploy workflows; tags can be hijacked (tag drift). [DOC]
- **OIDC over static secrets.** Cloud deploys use `id-token: write` + a trusted
  role instead of long-lived credentials. [DOC]
- **Cache invalidation.** Cache keys must include the dependency lockfile hash;
  fork-written cache can poison builds. [DOC]
- **Concurrency.** `cancel-in-progress` for PR/branch CI; never cancel an
  in-flight deploy (half-applied release). [INFERENCIA]
- **Conventional Commits.** Blocking `commit-msg` regex:
  `^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(...\))?!?: .{1,72}`. [EXPLICIT]
- **Expand/contract migrations.** Ship backward-compatible (expand) first,
  contract one release later; never drop a column in the same release that stops
  writing it. [CÓDIGO]

## 3. Decision rules

| Decision | Rule | Trade-off |
|----------|------|-----------|
| OIDC vs static secret | OIDC when a configurable trust/role exists | removes rotation, needs provider trust setup [DOC] |
| SHA pin vs `@v4` tag | SHA for any privileged workflow | blocks tag hijack, needs Dependabot bumps [DOC] |
| Rollback pattern | flag-gated canary by default | smallest blast radius + instant kill switch [INFERENCIA] |
| Blue-green vs canary | blue-green for seconds-MTTR | 2x infra; drains in-flight sessions [SUPUESTO] |
| Where to gate hooks | fast staged-only at pre-commit | slow hooks train `--no-verify` habits [INFERENCIA] |
| Deploy risk tier | high if migration/breaking API/new dep | high-risk forces canary + longer monitoring [EXPLICIT] |

## 4. Failure modes (cross-topic)

- **Env/secret drift** — app boots, 500s on first real request. Mitigation:
  name-match build↔config; smoke test post-deploy. [INFERENCIA]
- **False-green handoff** — local plan validates but required checks were never
  enabled in branch protection. Mitigation: handoff lists exact checks. [EXPLICIT]
- **Silent over-permission** — top-level `write-all` leaks to every job.
  Mitigation: top-level read, per-job widening. [INFERENCIA]
- **Irreversible migration** — coupling expand + contract removes the rollback
  window. Mitigation: phase them across releases. [CÓDIGO]
- **Bypass leakage** — `--no-verify` skips local hooks. Mitigation: CI re-runs
  the same gates. [EXPLICIT]

## 5. Anti-scope

Infra provisioning (IaC apply), DNS cutover, capacity planning, secret rotation,
cloud OIDC trust-role provisioning, self-hosted runner management, and org-level
policy are out of scope — named as operator prerequisites, not performed. [EXPLICIT]
