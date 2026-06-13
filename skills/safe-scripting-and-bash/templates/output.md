# Safety Report — <script-name>

## Summary

- **Skill**: safe-scripting-and-bash
- **Mode**: <design | review>
- **Verdict**: <PASS | BLOCK>  (bound to per-check results below)
- **Scope**: <one-paragraph description of the script's purpose>

## Required inputs (resolved)

| Input | Value |
|-------|-------|
| Purpose / trigger | <...> |
| Inputs → outputs | <...> |
| Write surface (paths + glob breadth) | <...> |
| Permissions / sudo implied | <yes/no + detail> |
| Dry-run / --apply / --force / fallback | <...> |

> If write surface or dry-run intent was missing, this section records the
> `{VACIO_CRITICO}`-class gap and the BLOCK. [INFERENCE]

## Risk classification

| Hazard | Present? | Resolution | Tag |
|--------|----------|------------|-----|
| Destructive command (`rm -rf`, `git reset --hard`, force push) | <y/n> | <approval+isolation / refused> | [CONFIG] |
| Broad write (`**/*`) | <y/n> | <dry-run+apply+force+rollback> | [CONFIG] |
| Secret exposure | <y/n> | <redacted / refused> | [DOC] |
| Portability gap (paths, quoting, tempdir) | <y/n> | <fix> | [CODE] |
| Offline-validation gap | <y/n> | <made offline> | [CONFIG] |

## Per-check results (gate)

| Check | Result |
|-------|--------|
| dry-run default present | <pass/fail> |
| repo-root detection (`git rev-parse`) | <pass/fail> |
| write surface declared | <pass/fail> |
| no unguarded destructive command | <pass/fail> |
| no secret exposure | <pass/fail> |
| safe tempdir (`mktemp -d` + trap) | <pass/fail> |
| validation present and offline | <pass/fail> |

> Verdict is PASS only if every row is pass. Never report green-as-success when
> any row failed. [DOC]

## Script (or review edits)

```bash
# repo-root detection, set -euo pipefail, dry-run-first, quoted expansions
```

## Usage

- Dry-run (default): `bash <script>`
- Apply: `bash <script> --apply`
- Force overwrite (after a dry-run): `bash <script> --apply --force`

## Rollback / fallback

- <how to revert; what happens if a hard limit blocks automation>

## Offline validation command

```bash
bash skills/safe-scripting-and-bash/scripts/check.sh
```

## Evidence

Every non-obvious claim above carries one Alfa-core tag: `[DOC]` `[CONFIG]`
`[CODE]` `[INFERENCE]` `[ASSUMPTION]`.
