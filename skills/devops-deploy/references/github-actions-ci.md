<!-- distilled from alfa skills/github-actions-ci -->
<!-- > -->
# GitHub Actions CI/CD

> "If it is not automated, it is not reliable."

## TL;DR

Use this skill when creating, reviewing, or hardening GitHub Actions workflows
for lint, test, build, package, deploy, release, or quality gate automation.
[EXPLICIT]

The output must be a verifiable workflow plan, not just YAML prose. It must
define triggers, job graph, permissions, pinned third-party actions, dependency
caching, matrix strategy, secrets, environment protection, concurrency, and
validation evidence before claiming the pipeline is ready. [EXPLICIT]

A plan that omits any required field is **not ready** — emit the
missing-evidence report from `assets/ci-workflow-contract.json` instead of
fabricated YAML. [EXPLICIT]

## Procedure

### Step 1: Discover Pipeline Surface

- Inspect existing `.github/workflows/`, package manifests, lockfiles, test
  commands, build commands, deploy targets, environments, and branch policy.
- Record which facts are observed from files and which are assumptions.
- Identify the auth model: cloud deploys should use OIDC (`id-token: write` +
  trusted role) over long-lived secrets; record which is in use. [INFERENCIA]
- If no lockfile, no test command, or no deploy target is found, treat each as a
  gap and surface it — do not invent defaults silently. [EXPLICIT]

### Step 2: Design Deterministic Workflow

- Use `assets/ci-workflow-contract.json` for required output fields.
- Use `assets/triggers-policy.json`, `assets/permissions-policy.json`,
  `assets/action-pinning-policy.json`, `assets/cache-policy.json`, and
  `assets/matrix-policy.json` to define deterministic workflow behavior.
- Use `assets/secrets-policy.json` and `assets/deployment-policy.json` before
  adding deploy jobs.
- Default `permissions: contents: read` at workflow top level; widen per job
  only with a recorded reason (least privilege). [DOC]
- Add `concurrency` with `cancel-in-progress` for PR/branch runs to avoid
  overlapping or wasted runs; never cancel an in-flight deploy. [INFERENCIA]

### Step 3: Block Unsafe Patterns

- Do not use broad repository permissions unless a job-specific reason is
  recorded.
- Do not use unpinned third-party actions in release or deploy workflows.
- Do not write secrets into workflow YAML.
- Do not deploy from `pull_request` events or unprotected branches.
- Do not run untrusted code with secrets in scope: `pull_request_target` and
  `workflow_run` expose write tokens to fork code — never check out and execute
  PR head there. [DOC]
- Do not interpolate untrusted input (`github.event.*` titles, branch names)
  directly into `run:` shell — pass via `env:` to block script injection. [DOC]
- Do not mark CI ready without validation commands and expected checks.

### Step 4: Validate And Handoff

- Validate structured JSON workflow plans with
  `scripts/validate_github_actions_ci.py` or `scripts/check.sh`.
- For YAML implementation, preserve the same contract in the review summary.
- Mark the pipeline ready only when local validation evidence and required
  workflow protections are documented.
- Handoff lists the exact required status checks to enable in branch protection;
  a green local plan is not a green remote run. [EXPLICIT]

## Quality Criteria

- [ ] Trigger policy is explicit for PR, push, manual, schedule, or release.
- [ ] Every job has a purpose, runner, dependency graph, permissions, and
  validation command.
- [ ] Third-party actions are pinned to immutable SHA references when required.
- [ ] Cache keys include dependency lockfile or equivalent invalidation source.
- [ ] Matrix entries are bounded and justified.
- [ ] Secrets are referenced by name only and never embedded as values.
- [ ] Deploy jobs use protected environments, branch gates, and concurrency.
- [ ] Top-level token defaults to read; write scopes are per-job and justified.
- [ ] No untrusted input flows into `run:` shell or into a privileged trigger.
- [ ] Evidence tags are applied to user-facing factual claims.

## Worked Example (minimal contract-conformant skeleton)

```yaml
name: ci
on:
  pull_request:
  push: { branches: [main] }
permissions: { contents: read }          # least privilege at top
concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA>      # pin third-party to immutable SHA
      - uses: actions/setup-node@<SHA>
        with: { node-version: 20, cache: npm }   # cache keyed on lockfile
      - run: npm ci
      - run: npm test
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'   # never from pull_request
    runs-on: ubuntu-latest
    environment: production               # protected env = approval gate
    permissions: { contents: read, id-token: write }   # OIDC, no static secret
    concurrency: { group: deploy-prod }   # serialize prod deploys, no cancel
    steps:
      - uses: actions/checkout@<SHA>
      - run: ./deploy.sh                  # role assumed via OIDC, secrets by name only
```

This skeleton satisfies trigger, permission, pinning, cache, environment, and
concurrency criteria; matrix and secrets-by-name are added per policy. [INFERENCIA]

## Decisions & Trade-offs

| Decision | Choose when | Trade-off |
|----------|-------------|-----------|
| OIDC vs static secret | Cloud deploy with a configurable trust/role | OIDC removes credential rotation but needs provider trust setup first [DOC] |
| SHA pin vs tag (`@v4`) | Release/deploy or any privileged workflow | SHA blocks tag-hijack supply-chain attacks but needs manual/Dependabot bumps [DOC] |
| Matrix breadth | Real support surface (LTS runtimes/OSes) | Each axis multiplies minutes; bound to supported versions, justify each [INFERENCIA] |
| `cancel-in-progress` | PR/branch CI churn | Speeds feedback for CI; must be OFF for deploy to avoid half-applied releases [INFERENCIA] |

## Usage

Example invocations:

- "/github-actions-ci" - Build a deterministic CI workflow plan.
- "Review this GitHub Actions workflow for unsafe permissions."
- "Add matrix tests and cache policy to this pipeline."
- "Validate this CI workflow JSON before creating YAML."

## Assumptions & Limits

- Assumes access to project artifacts, workflow YAML, or a supplied pipeline
  plan. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not create repository secrets or environment approvals by itself.
  [EXPLICIT]
- Does not claim a GitHub-hosted workflow passed without CI evidence. [EXPLICIT]
- Anti-scope: does not configure branch protection rules, provision cloud OIDC
  trust roles, manage self-hosted runners, or set org-level policy — it names
  these as prerequisites for the operator to complete. [EXPLICIT]
- Plans target GitHub-hosted Actions; GitLab CI, CircleCI, and Jenkins are out
  of scope. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce a missing-evidence report and do not emit ready YAML |
| Deploy requested from PR | Block deploy and require protected branch or manual gate |
| Missing lockfile for cache | Disable cache or require explicit invalidation source |
| Unpinned third-party action | Block release/deploy readiness until pinned |
| Secret value supplied inline | Remove value, reference secret name only, and flag risk |
| Matrix too broad | Bound versions and explain coverage tradeoff |
| `pull_request_target` / `workflow_run` with secrets | Flag fork-PR token exposure; do not check out untrusted head with write scope |
| Untrusted input in `run:` | Move value to `env:`, flag script-injection risk |
| Fork PR needs secrets | Mark not auto-runnable; require maintainer approval or split safe/privileged jobs |

## Failure Modes

- **Tag drift**: a pinned action retags to a malicious commit. Mitigation: SHA
  pin + Dependabot bump PRs. [DOC]
- **Cache poisoning**: stale or fork-written cache injects bad deps. Mitigation:
  scope cache keys to lockfile hash and trusted refs. [DOC]
- **Silent over-permission**: top-level `write-all` token leaks to every job.
  Mitigation: top-level read, per-job widening with reason. [INFERENCIA]
- **False-green handoff**: plan validates locally but required checks were never
  enabled in branch protection, so merges bypass CI. Mitigation: handoff lists
  exact checks to enable. [EXPLICIT]
