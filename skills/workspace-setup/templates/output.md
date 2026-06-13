# Workspace Setup Plan — `<goal-or-project>`

- **Target file:** `.jm-adk.local.json`
- **Mode:** `dry-run` | `apply`   _(dry-run is the default; apply only if explicit)_
- **Overwrite risk:** `none` | `existing-profile-present`
- **Apply authorized:** `no` | `yes (--apply` + `--force?` `)`

## 1. Runtime preferences
| Field | Value | Tag |
|-------|-------|-----|
| Goal | … | [DOC] |
| Runtime | … | [DOC] |
| Autonomy level | … | [DOC] |
| Workspace area | … | [DOC] |
| Output format | … | [ASSUMPTION] if auto-filled |

## 2. Command policy
- **Allowed:** `git status`, `git diff`, validation scripts, … [DOC]
- **Prohibited:** `git reset --hard`, `rm -rf`, force-push to shared branches … [DOC]
- **Escalation-required:** any permission-widening command … [DOC]

## 3. Privacy policy
- Local-only storage: `yes` [DOC]
- Secret storage: `forbidden` [DOC]
- Redaction categories: api_key, password, private_key, bearer_token, email,
  connection_string [CONFIG]
- Secret scan completed: `yes` — hits (by category, no values): … [DOC]

## 4. Write policy
- Explicit apply required: `yes` [DOC]
- `.gitignore` coverage of `.jm-adk.local.json`: `yes` [DOC]
- Overwrite requires `--force`: `yes` [DOC]

## 5. Evidence
- … claim … [TAG]

## 6. Validation result
| Check | Result |
|-------|--------|
| assets | pass / fail |
| deterministic_scripts | pass / fail |
| quality_criteria | pass / fail |
| runtime_preferences | pass / fail |
| command_policy | pass / fail |
| privacy_policy | pass / fail |
| write_policy | pass / fail |
| evidence | pass / fail |

Determinism: no network / clock / randomness consumed. [DOC]

## 7. Plan preview (JSON)
```json
{ "target_file": ".jm-adk.local.json", "mode": "dry-run", "...": "..." }
```

## 8. Setup summary
- **Outcome:** preview only | written
- **Residual risks:** … [INFERENCE]
- **Next command (if not yet applied):**
  `… validate_workspace_setup_plan.py <plan>` → apply with `--apply`
  (`--force` only if a profile exists). [DOC]

## Guardian decision
`proceed` | `blocked` | `needs-confirmation` — failing gate + corrective step if
not `proceed`. [DOC]
