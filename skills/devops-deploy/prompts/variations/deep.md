# Deep Variation — devops-deploy

Exhaustive path. Resolve one topic, read one playbook, apply it fully with
per-step verification.

## Steps
1. Map request → one enum topic; confirm scope vs anti-scope before starting.
2. Read `references/<topic>.md` at `depth=deep`.
3. **Discover** — inventory existing artifacts (workflows, lockfiles, hooks, env
   config, deploy targets); record observed-vs-assumed; surface every gap (no
   lockfile / no test command / no deploy target) rather than inventing defaults.
4. **Analyze** — apply the playbook's policy assets and decision rules; tier risk;
   choose patterns by MTTR / blast radius / least privilege.
5. **Execute** — build the full artifact via `templates/output.md`; run the
   deterministic scripts/validators (`validate_*`, `check.sh`, `compile-*`).
6. **Validate** — walk the playbook's full acceptance + quality criteria; verify
   each. Enumerate edge cases and failure modes with mitigations.

## Deep-mode requirements
- Every required field present or explicitly marked N/A with a reason.
- Trade-off table for each non-obvious decision (e.g. OIDC vs static secret,
  blue-green vs canary, SHA pin vs tag).
- Handoff lists every operator prerequisite a local plan cannot prove
  (branch-protection checks, OIDC trust role, environment approvals).
- Behavior evidence required before "done" — never green-as-success.
- All claims evidence-tagged; constitution v6.0.0.
