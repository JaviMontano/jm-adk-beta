# Example output — workspace-setup (dry-run preview)

# Workspace Setup Plan — TypeScript CLI with Alfa pairing

- **Target file:** `.jm-adk.local.json`
- **Mode:** `dry-run`  _(no `--apply` given; default)_
- **Overwrite risk:** `none` (no existing profile)
- **Apply authorized:** `no`

## 1. Runtime preferences
| Field | Value | Tag |
|-------|-------|-----|
| Goal | Ship a TypeScript CLI with Alfa pairing | [DOC] |
| Runtime | Codex | [DOC] |
| Autonomy level | propose-then-act | [DOC] |
| Workspace area | repo root | [DOC] |
| Output format | markdown + evidence tags | [DOC] |

## 2. Command policy
- **Allowed:** `git status`, `git diff`, repo validation scripts. [DOC]
- **Prohibited:** `git reset --hard`, `rm -rf`. [DOC]
- **Escalation-required:** any command that widens permissions. [DOC]

## 3. Privacy policy
- Local-only storage: `yes` [DOC]
- Secret storage: `forbidden` [DOC]
- Redaction categories: api_key, password, private_key, bearer_token, email,
  connection_string [CONFIG]
- Secret scan completed: `yes` — **1 hit redacted**: category `api_key`
  (a `ghp_`-shaped token in the goal text). Value never stored or echoed. [DOC]

## 4. Write policy
- Explicit apply required: `yes` [DOC]
- `.gitignore` coverage of `.jm-adk.local.json`: `yes` (already listed) [DOC]
- Overwrite requires `--force`: `yes` [DOC]

## 5. Evidence
- Dry-run chosen because no `--apply` flag was present. [INFERENCE]
- `.gitignore` already covers the target file. [CONFIG]
- Output format inherited from the user's request, not assumed. [DOC]

## 6. Validation result
| Check | Result |
|-------|--------|
| assets | pass |
| deterministic_scripts | pass |
| quality_criteria | pass |
| runtime_preferences | pass |
| command_policy | pass |
| privacy_policy | pass |
| write_policy | pass |
| evidence | pass |

Determinism: no network / clock / randomness consumed. [DOC]

## 7. Plan preview (JSON)
```json
{
  "target_file": ".jm-adk.local.json",
  "mode": "dry-run",
  "runtime_preferences": {
    "goal": "Ship a TypeScript CLI with Alfa pairing",
    "runtime": "Codex",
    "autonomy": "propose-then-act",
    "workspace_area": "repo-root",
    "output_format": "markdown+tags"
  },
  "command_policy": {
    "allowed": ["git status", "git diff", "repo-validation-scripts"],
    "prohibited": ["git reset --hard", "rm -rf"],
    "escalation_required": ["permission-widening"]
  },
  "privacy_policy": {
    "local_only": true,
    "store_secrets": false,
    "redaction_categories": ["api_key", "password", "private_key", "bearer_token", "email", "connection_string"],
    "secret_scan_completed": true
  },
  "write_policy": {
    "explicit_apply_required": true,
    "gitignore_covered": true,
    "force_required_for_overwrite": true
  }
}
```

## 8. Setup summary
- **Outcome:** preview only — nothing written.
- **Residual risks:** the redacted token must be rotated by the user if it was a
  real credential; the skill stored only its category. [INFERENCE]
- **Next command (to apply later):**
  `python3 skills/workspace-setup/scripts/validate_workspace_setup_plan.py <plan>`
  then re-run with `--apply` (no `--force` needed; no existing profile). [DOC]

## Guardian decision
`proceed` — dry-run default honored, secret contained and redacted, offline
validation passed, `.gitignore` covers the target, evidence single-family. [DOC]
