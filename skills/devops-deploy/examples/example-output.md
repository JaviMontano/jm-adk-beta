# Example Output — devops-deploy

## Routing
- **Resolved topic:** `github-actions-ci`
- **Playbook read:** `references/github-actions-ci.md`
- **Depth:** `deep`
- **Why this topic:** the request is to review/harden a GitHub Actions workflow
  before go-live — not a generic deploy checklist. [EXPLICIT]

## 1. Discover (observed vs assumed)
| Fact | Source | Observed/Assumed | Tag |
|------|--------|------------------|-----|
| Trigger uses `pull_request_target` | workflow YAML | observed | [CONFIG] |
| Top-level `permissions: write-all` | workflow YAML | observed | [CONFIG] |
| AWS creds hardcoded in `env:` | workflow YAML | observed | [CÓDIGO] |
| `actions/*` pinned to `@v4` tags | workflow YAML | observed | [CONFIG] |
| `npm install` (not `npm ci`) | workflow YAML | observed | [CÓDIGO] |
| `package-lock.json` committed | context | observed | [CONFIG] |
| Deploy job has no protected environment | workflow YAML | observed | [CONFIG] |

Gaps surfaced: no `concurrency`, no cache, no environment gate, no OIDC role.

## 2. Analyze
- **Risk tier:** HIGH — privileged trigger + write-all token + static cloud
  secrets + deploy from non-protected path. [INFERENCIA]

| Decision | Choice | Trade-off | Tag |
|----------|--------|-----------|-----|
| Auth model | OIDC `id-token: write` + AWS role | removes key rotation; needs trust setup | [DOC] |
| Action pinning | SHA-pin for deploy job | blocks tag hijack; needs Dependabot | [DOC] |
| Trigger | drop `pull_request_target`; use `pull_request` | loses fork-secret access (intended) | [DOC] |

## 3. Execute — hardened workflow
```yaml
name: ci
on:
  pull_request:                                  # was pull_request_target (fork-token exposure)
  push: { branches: [main] }
permissions: { contents: read }                  # was write-all
concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<SHA>             # pin to immutable SHA
      - uses: actions/setup-node@<SHA>
        with: { node-version: 20, cache: npm }   # cache keyed on package-lock.json
      - run: npm ci                              # was npm install (non-reproducible)
      - run: npm test
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'          # never from a PR
    runs-on: ubuntu-latest
    environment: production                       # approval gate
    permissions: { contents: read, id-token: write }   # OIDC, no static secret
    concurrency: { group: deploy-prod }           # serialize prod, no cancel
    steps:
      - uses: actions/checkout@<SHA>
      - uses: aws-actions/configure-aws-credentials@<SHA>
        with: { role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}, aws-region: us-east-1 }
      - run: aws s3 sync ./dist s3://app
```
- Secrets removed from YAML; AWS auth now via assumed role (no values). [CÓDIGO]
- Validator run: `scripts/validate_github_actions_ci.py` → plan conforms to
  `assets/ci-workflow-contract.json`. [CÓDIGO]

## 4. Validate — gate
- [x] One topic, one playbook read. [DOC]
- [x] Topic ∈ enum (`github-actions-ci`). [CONFIG]
- [x] Least-privilege token, SHA pinning, lockfile cache, protected env, no
      untrusted trigger, no inline secrets. [DOC]
- [ ] Behavior evidence: deploy not yet run against the real role — owed. [INFERENCIA]

**Gate result:** FAIL (one open item) — assume-role deploy must succeed once in
staging before "production-safe" is claimed. Green plan ≠ verified deploy. [DOC]

## 5. Handoff — operator prerequisites
- [ ] Provision the AWS OIDC trust role; set `vars.AWS_DEPLOY_ROLE_ARN`.
- [ ] Delete the leaked static AWS keys (rotate immediately — they were committed).
- [ ] Enable required status check `test` in branch protection for `main`.
- [ ] Add reviewers to the `production` environment.
