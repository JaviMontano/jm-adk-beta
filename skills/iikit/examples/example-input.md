# Example Input — iikit routing

A developer on a project that already has a validated `PREMISE.md` and a
`CONSTITUTION.md` (v1.0.0), but no spec yet, types:

```
Let users reset their password via an emailed link that expires in 1 hour.
```

No explicit `topic` is given and no `depth` is set.

Context on disk:
- `PREMISE.md` — present, passes `validate-premise.sh`
- `CONSTITUTION.md` — present, v1.0.0, `tdd_determination = optional`
- `specs/` — empty (no feature directory yet)

Expected routing behavior:
- Resolve `topic` by inferring the earliest **unmet** stage. Constitution exists;
  no spec exists → earliest unmet stage is `01-specify`.
- Confirm the predecessor (constitution) is present — proceed.
- Read exactly one playbook: `references/01-specify.md`.
- Run Step 0 bug-fix detection: "reset their password" is a new capability, not a
  fix to broken behavior → proceed as a feature.
- `depth` defaults to `quick`.
