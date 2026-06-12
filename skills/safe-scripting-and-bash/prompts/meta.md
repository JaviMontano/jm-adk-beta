# Meta Prompt — safe-scripting-and-bash

Use this to self-evaluate a `safe-scripting-and-bash` run before declaring done.
It mirrors the Guardian gate so the Lead does not over-claim. [DOC]

## Self-check questions

1. **Scope** — Is this a durable Bash script/review, not a one-liner and not
   non-Bash automation? If not, redirect or refuse. [DOC]
2. **Inputs** — Are purpose, inputs/outputs, write surface, sudo implication, and
   dry-run/apply/force intent all present? If the write surface or dry-run intent
   is missing, did I stop and ask instead of defaulting? [INFERENCE]
3. **Dry-run** — Is dry-run the default whenever a write is possible? Is `--force`
   gated behind a prior dry-run? [DOC]
4. **Portability** — Repo-root via `git rev-parse`, every expansion quoted,
   tempdir via `mktemp -d` + trap, no absolute paths, no Bashism left
   unjustified? [CODE]
5. **Destructive** — Any `rm -rf` / `git reset --hard` / force push guarded by
   approval AND path isolation, or refused? [DOC]
6. **Secrets** — No env var / token / credential read, printed, or persisted? [DOC]
7. **Offline** — Does the validator decide safety with zero network calls? [DOC]
8. **Verdict integrity** — Is the final verdict bound to per-check results, with
   no green-as-success over a failed check? [DOC]

## Failure routing

- Any "no" on 2, 5, 6, or 7 → Guardian block; do not ship. [DOC]
- Any "no" on 3 or 4 → return to Support for correction. [INFERENCE]

## Evidence discipline

Confirm every non-obvious claim carries exactly one Alfa-core tag with consistent
spelling before declaring done. [DOC]
