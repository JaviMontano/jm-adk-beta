# Example Output — safe-scripting-and-bash

Safety report for the profile-fixtures regenerator from `example-input.md`. [DOC]

## Summary

- **Skill**: safe-scripting-and-bash
- **Mode**: design
- **Verdict**: PASS (every per-check row passed)
- **Scope**: Regenerate `local/profiles/*.json` from `templates/profile.tmpl`,
  dry-run by default.

## Required inputs (resolved)

| Input | Value |
|-------|-------|
| Purpose / trigger | Regenerate local profile fixtures from a template. |
| Inputs → outputs | `templates/profile.tmpl` → `local/profiles/*.json`. |
| Write surface | `local/profiles/*.json` (one directory, bounded glob). |
| Permissions / sudo | No sudo; user-owned paths. |
| Dry-run / apply / force | Dry-run default; `--apply` writes; `--force` overwrites after dry-run. |

## Risk classification

| Hazard | Present? | Resolution | Tag |
|--------|----------|------------|-----|
| Destructive command | no | none requested | [CONFIG] |
| Broad write | no | bounded to one directory | [CONFIG] |
| Secret exposure | no | no env/token read | [DOC] |
| Portability gap | yes | repo-root + quoting + mktemp applied | [CODE] |
| Offline-validation gap | no | smoke test is offline | [CONFIG] |

## Per-check results (gate)

| Check | Result |
|-------|--------|
| dry-run default present | pass |
| repo-root detection (`git rev-parse`) | pass |
| write surface declared | pass |
| no unguarded destructive command | pass |
| no secret exposure | pass |
| safe tempdir (`mktemp -d` + trap) | pass |
| validation present and offline | pass |

## Script

```bash
#!/usr/bin/env bash
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
src="$root/templates/profile.tmpl"
dest_dir="$root/local/profiles"

apply=0; force=0
for arg in "$@"; do
  case "$arg" in
    --apply) apply=1 ;;
    --force) force=1 ;;
    *) printf 'unknown flag: %s\n' "$arg" >&2; exit 2 ;;
  esac
done

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

for name in default ci local; do
  target="$dest_dir/$name.json"
  staged="$tmp/$name.json"
  sed "s/{{name}}/$name/g" "$src" > "$staged"
  if [ "$apply" -eq 0 ]; then
    printf 'DRY-RUN would write: %s\n' "$target"
    continue
  fi
  if [ -e "$target" ] && [ "$force" -eq 0 ]; then
    printf 'exists, use --force after a dry-run: %s\n' "$target" >&2
    exit 3
  fi
  cp "$staged" "$target"
  printf 'wrote: %s\n' "$target"
done
```

## Usage

- Dry-run: `bash scripts/regen-profiles.sh`
- Apply: `bash scripts/regen-profiles.sh --apply`
- Force overwrite (after a dry-run): `bash scripts/regen-profiles.sh --apply --force`

## Rollback / fallback

- Fixtures are git-tracked: `git checkout -- local/profiles/` reverts a bad run.
- If a hard limit blocks automation, ship the manual `sed`/`cp` checklist
  instead of an unsafe script. [DOC]

## Offline validation command

```bash
bash skills/safe-scripting-and-bash/scripts/check.sh
```

## Evidence

Repo-root detection and `mktemp -d` are `[CODE]`; policy mappings are `[CONFIG]`;
behavioral choices are `[DOC]`; the quick-vs-deep call is `[INFERENCE]`.
