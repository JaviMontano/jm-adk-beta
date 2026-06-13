# Meta prompt — workspace-setup (self-check before emitting)

Run this checklist on your own draft plan **before** returning it. Any failure
re-plans; do not rationalize a violation into a warning.

## Mode & write safety
- [ ] Is `mode` `dry-run` unless the user explicitly said `apply` / `--apply`?
- [ ] If `mode=apply` and a profile already exists, did the user pass `--force`?
      If not → preview + exact `--force` command, no write.
- [ ] Is `.gitignore` coverage of `.jm-adk.local.json` asserted? Never write into
      a git-tracked path.
- [ ] No partial write anywhere.

## Secrets
- [ ] Did the secret scan run on every input?
- [ ] Did any credential shape (`sk-`, `ghp_`, `xox`, password, private key,
      bearer header, raw email, credentialed connection string) reach the plan
      body? If yes → reject, redact, re-plan.
- [ ] Is every flagged secret named by *category*, never by value?

## Inputs & policy
- [ ] Were security-relevant inputs (command policy, privacy) provided, not
      auto-filled? If missing → one question, stop.
- [ ] Are `allowed` / `prohibited` / `escalation-required` all present?
- [ ] Was any permission widened? If so, is it in `escalation-required` and
      explicitly approved?

## Validation & evidence
- [ ] Does the offline validator pass, with no network / clock / randomness?
- [ ] Do `validation_checks` cover assets, deterministic_scripts,
      quality_criteria, runtime_preferences, command_policy, privacy_policy,
      write_policy, evidence?
- [ ] Are all evidence tags one Alfa-core family, consistent spelling, no
      Jarvis `{...}` mixing?

## Scope & governance
- [ ] Is this profile-plan work only — no `workspace-governance` (session-folder
      / task-bridge) actions?
- [ ] Single brand, no prices, no PII?

If all boxes are checked, hand to the guardian for `proceed`.
