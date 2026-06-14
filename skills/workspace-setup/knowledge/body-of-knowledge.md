# Body of Knowledge — workspace-setup

Domain knowledge for designing a deterministic, dry-run-first plan for the local
profile `.jm-adk.local.json`. [DOC]

## 1. The artifact: `.jm-adk.local.json`

A per-developer, **uncommitted** local profile that holds reusable Alfa defaults.
It is never source-controlled (must be `.gitignore`-covered) and never holds
secrets. It is produced by a validated plan, not hand-edited blindly. [DOC]

### Required plan blocks
| Block | Holds | Class |
|-------|-------|-------|
| `target_file` | exactly `.jm-adk.local.json` | fixed |
| `mode` | `dry-run` (default) or `apply` | control |
| runtime preferences | goal, runtime, autonomy, workspace area, output format | mixed |
| `command_policy` | `allowed`, `prohibited`, `escalation-required` | security |
| `privacy_policy` | local-only, no-secret-storage, redaction categories, secret-scan-done | security |
| `write_policy` | explicit-apply, `.gitignore` coverage, `--force`-for-overwrite | security |
| `evidence` | entries with Alfa-core tags | governance |
| `validation_checks` | assets, deterministic_scripts, quality_criteria, runtime_preferences, command_policy, privacy_policy, write_policy, evidence | governance |

## 2. Input classes — the stop-on-missing rule

- **Security-relevant** inputs (command policy, privacy) must never be
  auto-filled. Missing one is `{VACIO_CRITICO}`-equivalent: stop and ask. A
  permissive default silently widens the trust boundary. [INFERENCE]
- **Cosmetic** inputs (output format) may be auto-filled and tagged
  `[ASSUMPTION]`. [DOC]

## 3. Command policy classes (decision rules)

- **allowed** — read-only / validation commands: `git status`, `git diff`,
  `python3 ... validate_*.py`, `bash check.sh`.
- **prohibited** — destructive / irreversible: `git reset --hard`, `rm -rf`,
  force-push to shared branches.
- **escalation-required** — anything that widens permissions or touches shared
  state; must be explicitly approved, never auto-granted. [DOC]

## 4. Privacy & secret detection

Credential shapes that MUST be rejected before planning: API keys/tokens
(`sk-`, `ghp_`, `xox`, long high-entropy strings), passwords, private keys
(`BEGIN ... PRIVATE KEY`), bearer/Authorization headers, raw email addresses,
and connection strings with embedded credentials. On a hit: name the **category**
(not the value), substitute a redaction placeholder, never echo the secret. [DOC]

## 5. Write safety invariants

1. Dry-run is the default; a write requires explicit `mode=apply` / `--apply`.
2. An existing profile is never overwritten without `--force`.
3. `.jm-adk.local.json` must be `.gitignore`-covered; never writable into a
   git-tracked path.
4. Never partial-write; on failure, return the preview + the exact re-run
   command. [DOC]

## 6. Determinism standard

Validation MUST be reproducible offline: no network, no wall-clock time, no
randomness, no live credentials. This trades richer live checks (e.g. verifying
a runtime binary exists) for byte-stable results across machines and CI. [INFERENCE]

## 7. Evidence taxonomy

Alfa core set only, one spelling per document: `[CODE]` `[CONFIG]` `[DOC]`
`[INFERENCE]` `[ASSUMPTION]`. Never mix the Jarvis `{...}` family. Planned-but-
absent assets are tagged `[ASSUMPTION]`, never `[CODE]`. [CONFIG]

## 8. Anti-scope boundary

Auditing or cleaning existing workspace session folders / task bridges is
`workspace-governance`, a different skill. workspace-setup designs the *profile
plan* only and never touches governance state. [INFERENCE]

## 9. Standards referenced

- JM-ADK skill Definition-of-Done (`scripts/validate-skill-dod.py`).
- Plan contract `assets/workspace-setup-plan-contract.json` validated by
  `scripts/validate_workspace_setup_plan.py` (planned build target). [ASSUMPTION]
