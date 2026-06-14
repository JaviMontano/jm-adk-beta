# Example Input — safe-scripting-and-bash

A concrete request that exercises the design path, including the required inputs. [DOC]

## Request

> Design a Bash script that regenerates the local profile fixtures under
> `local/profiles/` from a template. It should default to a dry-run, write only
> on `--apply`, and overwrite existing fixtures only on `--force`. It runs on my
> machine and inside CI, so it must not hard-code my home directory.

## Required inputs as provided

| Input | Value |
|-------|-------|
| Purpose / trigger | Regenerate local profile fixtures from a template. |
| Inputs → outputs | Template `templates/profile.tmpl` → files in `local/profiles/`. |
| Write surface | `local/profiles/*.json` (bounded glob, single directory). |
| Permissions / sudo | No sudo; user-owned repo paths only. |
| Dry-run / apply / force / fallback | Dry-run default; `--apply` writes; `--force` overwrites after a dry-run; fallback is a manual checklist if a hard limit blocks. |

## Notes

- Write surface is bounded to one directory, so the quick variation could apply,
  but `--force` overwrite raises it to a normal four-step run. [INFERENCE]
- No secrets are involved; no destructive command is requested. [DOC]
- Repo root must be detected with `git rev-parse --show-toplevel` because the
  script runs both locally and in CI. [CODE]
