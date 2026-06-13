# Quick variation — workspace-setup

Fast dry-run preview. Use when the user wants to *see* the `.jm-adk.local.json`
plan, not write it.

1. Confirm `mode=dry-run`. Never write in quick mode.
2. Run the secret scan on inputs; on any hit, reject + redact by category.
3. If a security-relevant input (command policy, privacy) is missing, ask ONE
   question and stop. Cosmetic gaps (output format) → auto-fill, tag
   `[ASSUMPTION]`.
4. Emit the plan preview (target file, runtime preferences, command policy,
   privacy policy, write policy, evidence, validation checks) + a one-paragraph
   setup summary.
5. End with the exact later-apply command:
   `python3 skills/workspace-setup/scripts/validate_workspace_setup_plan.py <plan>`
   then apply with `--apply` (`--force` only if a profile exists).

Alfa core tags only. No write, no network, no PII, single brand.
