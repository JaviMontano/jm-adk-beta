# Apply checklist — `.jm-adk.local.json`

Run top-to-bottom before any write. A single unchecked item blocks apply;
return a dry-run preview instead.

## Pre-apply gates
- [ ] `mode=apply` is explicit (user passed `--apply`). Otherwise → dry-run only.
- [ ] Secret scan ran on all inputs; zero credential shapes reached the plan body.
- [ ] Any flagged secret is named by category and redacted — never echoed.
- [ ] Security-relevant inputs (command policy, privacy) were provided, not
      auto-filled. Missing → ask one question and stop.
- [ ] `command_policy` has all three classes: allowed, prohibited,
      escalation-required. No permission widened without escalation.
- [ ] Offline validator passed; no network / clock / randomness consumed.
- [ ] `validation_checks` cover assets, deterministic_scripts, quality_criteria,
      runtime_preferences, command_policy, privacy_policy, write_policy, evidence.

## Write-safety gates
- [ ] `.gitignore` covers `.jm-adk.local.json` (not a git-tracked path).
- [ ] If a profile already exists, `--force` was passed. If not → preview + the
      exact `--force` command, no write.
- [ ] Write is atomic (no partial write); on failure, return preview + re-run
      command.

## Governance gates
- [ ] All evidence tags are one Alfa-core family, consistent spelling, no Jarvis
      `{...}` mixing.
- [ ] Single brand (JM Labs); no invented prices; no PII.
- [ ] No `workspace-governance` (session-folder / task-bridge) work leaked in.

## Post-apply
- [ ] Setup summary emitted: outcome, residual risks, next command.
- [ ] Guardian returned `proceed`.
