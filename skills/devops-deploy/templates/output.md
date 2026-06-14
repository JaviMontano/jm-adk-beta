# devops-deploy — Deliverable

## Routing
- **Resolved topic:** `<one of the ten enum topics>`
- **Playbook read:** `references/<topic>.md`
- **Depth:** `quick | deep`
- **Why this topic (not the others):** <one line; evidence-tagged>

## 1. Discover (observed vs assumed)
| Fact | Source | Observed/Assumed | Tag |
|------|--------|------------------|-----|
| e.g. lockfile present | `package-lock.json` | observed | [CONFIG] |
| e.g. deploy target | — | gap (missing) | [INFERENCIA] |

Gaps surfaced (not silently defaulted):
- <gap 1>
- <gap 2>

## 2. Analyze
- **Risk tier / blast radius:** low | medium | high — <reason>
- **Key decisions & trade-offs:**

| Decision | Choice | Trade-off | Tag |
|----------|--------|-----------|-----|
| e.g. OIDC vs static secret | OIDC | needs provider trust setup | [DOC] |

## 3. Execute — artifact
<The concrete artifact the playbook defines: workflow YAML/JSON plan, hook plan,
completed checklist, env/secret matrix, or rollback runbook.>

- Secrets referenced by name only (no values).
- Commands shown verbatim and reviewable.
- Deterministic scripts run: `<validator>` → `<result>`

## 4. Validate — gate (done = all true)
- [ ] One topic resolved, one playbook read (not the cluster). [DOC]
- [ ] Topic ∈ routes.json enum. [CONFIG]
- [ ] Playbook acceptance + quality criteria all satisfied.
- [ ] No secret values embedded.
- [ ] Behavior evidence captured (smoke test / monitoring) — green build alone is NOT proof.
- [ ] All claims evidence-tagged; constitution v6.0.0.

**Gate result:** PASS | FAIL — <unmet condition if FAIL>

## 5. Handoff — operator prerequisites
- [ ] <e.g. enable required status checks in branch protection>
- [ ] <e.g. provision OIDC trust role>
- [ ] <e.g. configure environment approval reviewers>

## Evidence legend
`[CÓDIGO]` from code · `[CONFIG]` from config · `[DOC]` from docs/standard ·
`[INFERENCIA]` reasoned · `[SUPUESTO]` assumption · `[EXPLICIT]` verbatim source.
