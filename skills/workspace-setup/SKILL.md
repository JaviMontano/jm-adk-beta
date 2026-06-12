---
name: workspace-setup
version: 1.2.0
last_updated: 2026-06-11
description: "Design a deterministic, dry-run-first local workspace profile plan for .jm-adk.local.json covering runtime preferences, command policy, privacy boundaries, write safety, evidence tags, and offline validation; write only on explicit apply."
owner: "JM Labs"
status: active
triggers:
  - workspace-setup
  - setup-workspace
  - local-profile
  - workspace-profile
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Workspace Setup

## Purpose

Produce a safe, deterministic plan for the local profile `.jm-adk.local.json`.
Default output is a dry-run preview; the skill validates runtime preferences,
command policy, privacy boundaries, write safety, and evidence, and writes the
file ONLY when an explicit apply mode is present and overwrite policy passes. [DOC]

Evidence tags in outputs use the Alfa core set (kit-facing audience):
`[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]` `[ASSUMPTION]`. One spelling per
document; never mix the Jarvis `{...}` family here. See
`references/verification-tags.md`. [CONFIG]

## When To Use

- User has approved creating local Alfa profile configuration. [DOC]
- First-use onboarding has collected goal, runtime, autonomy, command policy,
  privacy, and output preferences. [DOC]
- A developer wants reusable local defaults without committing personal state. [DOC]

## When Not To Use (anti-scope)

- User has NOT approved writing local configuration — produce nothing past a
  preview offer. [DOC]
- The request includes secrets/credentials — reject input, do not plan. [DOC]
- A one-shot answer that needs no persistent local profile state. [DOC]
- Auditing/cleaning existing workspace session folders or task bridges — that is
  `workspace-governance`, a different skill. Do not touch it. [INFERENCE]

## Inputs

- Primary goal with Alfa.
- Project/product type and known stack.
- Preferred runtime (e.g., Codex). [ASSUMPTION]
- Autonomy level.
- Commands allowed / prohibited / escalation-required.
- Privacy constraints.
- Workspace area and output format.

Missing a required input is `{VACIO_CRITICO}`-equivalent: stop and ask rather
than auto-filling a security-relevant default (command policy, privacy). Cosmetic
defaults (output format) may be auto-filled and tagged `[ASSUMPTION]`. [INFERENCE]

## Outputs

- Dry-run preview of `.jm-adk.local.json` unless `mode=apply` is explicit. [DOC]
- A validated setup plan matching the contract.
- The local profile file ONLY when `--apply` is explicit AND overwrite policy
  passes (no existing file, or `--force`). [DOC]
- Setup summary: evidence, validation result, residual risks. [DOC]

## Deterministic Contract

Validate every plan against `assets/workspace-setup-plan-contract.json` with
`scripts/validate_workspace_setup_plan.py`. (Contract, validator, and fixtures
are planned deliverables of this skill, not yet present in-repo — treat their
paths as the build target.) [ASSUMPTION]

A valid plan MUST include:

- `target_file` exactly `.jm-adk.local.json`. [DOC]
- `mode` ∈ {`dry-run`, `apply`}, with `dry-run` as the default. [DOC]
- Runtime preferences: goal, runtime, autonomy, workspace area, output format. [DOC]
- Command policy: allowed, prohibited, and escalation-required classes. [DOC]
- Privacy policy: local-only storage, no secret storage, redaction categories,
  and a completed secret scan. [DOC]
- Write policy: explicit apply required, `.gitignore` coverage, `--force` for
  overwrite. [DOC]
- Evidence entries using approved tags. [CONFIG]
- Validation checks for: assets, deterministic scripts, quality criteria,
  runtime preferences, command policy, privacy policy, write policy, evidence. [DOC]

## Workflow

1. **Discover** — read existing local profile state WITHOUT printing sensitive
   content (report presence/shape, not values). [DOC]
2. **Analyze** — run the secret scan on all inputs; detect overwrite risk
   (does `.jm-adk.local.json` already exist?). [DOC]
3. **Plan** — build the deterministic plan: target file, runtime preferences,
   command policy, privacy policy, write policy, evidence, validation checks. [DOC]
4. **Validate** — run the offline validator; a failing check blocks any apply. [DOC]
5. **Execute** — dry-run by default; write only with explicit `--apply` and a
   passing overwrite guard. [DOC]

## Secret Detection (analyze gate)

Reject and do not store inputs matching credential shapes, including: API keys /
tokens (`sk-`, `ghp_`, `xox`, long high-entropy strings), passwords, private
keys (`BEGIN ... PRIVATE KEY`), bearer/Authorization headers, raw email
addresses, and connection strings with embedded credentials. [INFERENCE]
On a hit: reject the input, name the category (not the value), and continue with
a redaction placeholder. Never echo the secret back. [DOC]

## Safety Limits

- Never commit `.jm-adk.local.json` (require `.gitignore` coverage). [DOC]
- Never overwrite an existing profile without `--force`. [DOC]
- Never store secrets; use placeholders and policy text. [DOC]
- Never require network, wall-clock time, randomness, or live credentials for
  validation — validation MUST be reproducible offline. [DOC]
- Never widen command permissions silently; widening is `escalation-required`. [DOC]

## Self-Correction Triggers

Stop and re-plan if any holds: planning to write while `mode=dry-run`;
overwrite intended without `--force`; a secret reached the plan body; validation
checks are incomplete or the validator was skipped; command policy widened
without explicit escalation; profile would be writable into a git-tracked path.
[INFERENCE]

## Anti-Patterns

- Writing on the first pass "to save a round-trip" instead of previewing. [INFERENCE]
- Auto-filling command/privacy policy from assumptions instead of asking. [INFERENCE]
- Printing existing profile contents during Discover. [DOC]
- Tagging planned-but-absent assets as `[CODE]` instead of `[ASSUMPTION]`. [INFERENCE]
- Mixing Jarvis `{...}` and Alfa `[...]` tag families in one output. [CONFIG]

## Decisions and Trade-offs

- **Dry-run default** trades one extra confirmation step for a hard guarantee
  that no profile is written without explicit intent. The friction is the
  feature. [INFERENCE]
- **Offline-only validation** trades richer live checks (e.g., verifying a
  runtime exists) for determinism and reproducibility across machines and CI. [INFERENCE]
- **Stop-on-missing for security inputs** trades convenience for the guarantee
  that no permissive default silently widens the trust boundary. [INFERENCE]

## Acceptance Criteria (validation gate)

- [ ] Dry-run is the default; no write occurred without explicit `--apply`. [DOC]
- [ ] `--apply` produces a profile that passes the contract validator. [DOC]
- [ ] Existing profile preserved unless `--force` was passed. [DOC]
- [ ] Every secret-like input was rejected and never stored. [DOC]
- [ ] Offline validator accepts valid fixtures and rejects unsafe fixtures. [DOC]
- [ ] All evidence tags come from a single family, consistent spelling. [CONFIG]
- [ ] No network / clock / randomness was needed to validate. [DOC]

## Edge Cases

- **Existing profile + apply, no `--force`** → block; return preview + the exact
  `--force` command. [DOC]
- **Apply requested but secret detected** → reject before planning; secret never
  enters the plan. [DOC]
- **Network-required validation requested** → refuse; substitute the offline
  validator. [DOC]
- **Workspace-governance phrasing** ("audit stale session folders") → do not
  activate; defer to that skill. [INFERENCE]
- **One-shot answer requested** → do not activate; answer without persisting. [DOC]

## Fallback

If a safe write is not possible, return the JSON preview plus the exact command
for a later authorized apply. Never partial-write. [DOC]

## Scripts

```bash
# Validate a plan fixture offline (build target; see Deterministic Contract).
python3 skills/workspace-setup/scripts/validate_workspace_setup_plan.py \
  skills/workspace-setup/scripts/fixtures/valid-dry-run-profile.json
bash skills/workspace-setup/scripts/check.sh
```

## Examples

- **Dry-run** — Codex runtime, evidence tags required, local-only state:
  emits a preview of `.jm-adk.local.json`, validator passes, nothing written. [DOC]
- **Apply (safe)** — approved profile, no existing file (or `--force`): writes
  the validated profile, then prints the setup summary. [DOC]
- **Apply (blocked)** — existing profile, no `--force`: returns preview + the
  `--force` command; no write. [DOC]
- **Rejected** — input contains an API token: secret scan rejects it, plans
  with a redaction placeholder, never stores the token. [DOC]
