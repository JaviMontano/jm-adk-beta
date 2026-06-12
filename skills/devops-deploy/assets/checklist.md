# Reviewer Checklist — devops-deploy gate

Used by the Guardian agent and `templates/output.md` to gate any devops-deploy
deliverable. Check every applicable item before declaring done. [DOC]

## Routing integrity
- [ ] Exactly one `topic` resolved from the routes.json enum.
- [ ] Exactly one `references/<topic>.md` playbook was read (not the cluster).
- [ ] No topic invented, renamed, or routes.json edited to fit the request.

## Topic execution
- [ ] The playbook's own acceptance + quality criteria are all satisfied.
- [ ] `depth` honored (quick = essentials; deep = exhaustive + per-step verify).
- [ ] Deterministic scripts/validators run where they exist; result recorded.

## Security & supply chain (CI/deploy topics)
- [ ] Tokens least-privilege (`contents: read` top level; per-job widening reasoned).
- [ ] Third-party actions SHA-pinned for release/deploy workflows.
- [ ] No secret values embedded; referenced by name / assumed via OIDC role.
- [ ] No deploy from `pull_request` / `pull_request_target` / unprotected branch.
- [ ] No untrusted input interpolated into `run:` shell.

## Release safety
- [ ] Rollback path chosen and tested in staging before prod deploy.
- [ ] Migrations expand/contract-safe; no destructive change this release.
- [ ] Risk tier set; high-risk forces canary + longer monitoring window.

## Done-ness
- [ ] Behavior evidence captured (smoke test / monitoring) — green build is NOT proof.
- [ ] Handoff lists operator prerequisites (branch protection, OIDC role, approvals).
- [ ] Every user-facing claim carries an evidence tag; constitution v6.0.0.
