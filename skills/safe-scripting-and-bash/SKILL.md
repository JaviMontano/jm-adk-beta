---
name: safe-scripting-and-bash
version: 1.1.0
description: "Design and review safe, portable, dry-run-first Bash scripts for local agentic workflows; gate writes, destructive commands, secrets, and offline validation."
owner: "JM Labs"
triggers:
  - safe-scripting
  - bash
  - shell-script
  - dry-run
  - script-safety
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Safe Scripting And Bash

Produce or review a Bash script that is portable, dry-run-first, and provably
non-destructive before it touches the filesystem. The deliverable is a script
(or review) plus a machine-checkable safety report that the offline validator
passes. [DOC]

## When To Use

- Creating or reviewing a local script for Alfa. [DOC]
- A script can write, move, generate, sync, or inspect many files. [DOC]
- Bash portability, dry-run behavior, repo-root detection, or rollback matters. [DOC]
- A reviewer must rule out `rm -rf`, force push, secret leaks, or broad overwrite. [INFERENCE]

## When Not To Use

- A one-line command suffices and has no durable value — return the command, not a skill. [DOC]
- The request is destructive and lacks explicit approval — refuse, do not soften. [DOC]
- Secrets or credentials would be read, printed, or stored — refuse and explain. [DOC]
- Another provider/runtime owns the work (e.g. PowerShell, Node CLI) — out of scope. [ASSUMPTION]

## Inputs (required before writing)

- Script purpose and trigger context. [DOC]
- Explicit inputs and outputs. [DOC]
- Files or directories in the write surface (paths, glob breadth). [DOC]
- Required permissions and whether `sudo` is implied. [DOC]
- Dry-run, `--apply`, `--force`, and fallback behavior. [DOC]

Missing write surface or dry-run intent is a `{VACIO_CRITICO}`-class gap for the
runbook family — stop and ask; never auto-fill the destructive default. [INFERENCE]

## Outputs

- Safe script or review. [DOC]
- Usage examples covering dry-run, apply, and force. [DOC]
- Risk notes with explicit rollback/fallback. [DOC]
- A validation command that runs offline. [DOC]

## Workflow

1. **Discover** — read existing scripts and repo conventions; note the write surface. [DOC]
2. **Analyze** — classify destructive risk, secrets risk, broad-write risk, portability gaps. [DOC]
3. **Execute** — implement with repo-root detection and dry-run-first when writes are possible. [DOC]
4. **Validate** — run syntax checks and non-destructive smoke tests; emit the safety report. [DOC]

## Deterministic Assets

- `assets/safe-scripting-and-bash-contract.json` — machine-checkable script plan or review. [CONFIG]
- `assets/write-surface-policy.json` — declare read/write scope, paths, broad-write risk. [CONFIG]
- `assets/dry-run-policy.json` — require dry-run default, explicit apply, explicit force for overwrites. [CONFIG]
- `assets/destructive-command-policy.json` — block unsafe shell patterns unless approved and isolated. [CONFIG]
- `assets/portability-policy.json` — portability, quoting, repo-root detection, tempdir rules. [CONFIG]
- `assets/validation-policy.json` — require syntax checks and deterministic smoke tests. [CONFIG]
- `assets/quality-rubric.json` — blocking safety checks and the bound-verdict rule; see `assets/README.md`. [CONFIG]

## Offline Validation (acceptance gate)

```bash
bash skills/safe-scripting-and-bash/scripts/check.sh
```

The validator FAILS on any of: missing dry-run, missing repo-root detection,
unknown write surface, unguarded destructive command, secrets exposure, unsafe
tempdir, missing validation, or a Guardian "pass" verdict over a failed check.
A green run is necessary, not sufficient — also satisfy Success Criteria. [CONFIG]
Never report green as success when any individual check failed. [DOC]

## Safety Limits (hard, non-negotiable)

- No `rm -rf`, `git reset --hard`, force push, or broad overwrite without explicit approval AND path isolation. [DOC]
- No absolute repo paths inside scripts — use `git rev-parse --show-toplevel` or equivalent. [CODE]
- No overwrites without `--force`; `--force` requires a prior dry-run. [DOC]
- No `curl`/network calls inside the validator or as a safety precondition — checks stay offline. [DOC]
- No printing or persisting env vars, tokens, or credentials, even for debugging. [DOC]

## Edge Cases

- **Broad write** (`**/*` or whole-repo rewrite): require dry-run, `--apply`, `--force`, and rollback notes before proceeding. [INFERENCE]
- **Tempdirs**: never a static name like `/tmp/foo`; use `mktemp -d` and trap-clean it. [CODE]
- **Unquoted expansion**: quote every `"$var"` and `"${arr[@]}"`; word-splitting is a write-surface hazard. [CODE]
- **Nested/sibling repos**: detect them so a sync does not escape the intended root. [INFERENCE]
- **Secret-in-output**: redact, do not echo; a leak fails the gate even if behavior is otherwise correct. [DOC]
- **CI / offline**: validation must not depend on a remote endpoint to decide local safety. [DOC]

## Self-Correction Triggers

- Caught yourself emitting `rm -rf`, `sudo`, or an absolute path → stop, isolate, or refuse. [DOC]
- About to print an env var → redact and re-route to a non-secret signal. [DOC]
- Validator passed but a check failed → treat as FAIL; never trust the aggregate verdict alone. [DOC]
- No dry-run yet a write is possible → add dry-run-first before continuing. [INFERENCE]

## Anti-Patterns / Anti-Scope

- Writing the script before the write surface is known. [DOC]
- Defaulting to apply/destroy instead of dry-run. [DOC]
- "Make it work" shortcuts: `sudo`, `chmod 777`, piping `curl | bash`. [DOC]
- Embedding machine-specific absolute paths. [CODE]
- Authoring non-Bash automation (out of scope — refuse or redirect). [ASSUMPTION]

## Success Criteria

- Script is stdlib/portable unless a deviation is justified inline. [DOC]
- Dry-run is the default for broad writes; apply and force are explicit. [DOC]
- Failure modes and rollback are documented. [DOC]
- Validation is documented and passes offline. [CONFIG]
- Every non-obvious claim in the report carries one Alfa-core tag, consistent spelling. [DOC]

## Fallback

If safe automation is unclear or a hard limit blocks it, produce a checklist and
manual commands instead of a script — never ship an unsafe script to "get it
done". [DOC]

## Examples

- Add a dry-run setup script for local profile creation (`--apply` to write, `--force` to overwrite). [DOC]
- Review a sync script for `rm -rf`, `sudo`, absolute paths, static tempdirs, and missing dry-run. [DOC]
- Refuse a "print all env vars" debug request; offer a redacted diagnostic instead. [DOC]
