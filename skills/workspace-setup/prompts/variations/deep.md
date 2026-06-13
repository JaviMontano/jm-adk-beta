# Deep variation — workspace-setup

Full plan, validation, and (if authorized) guarded apply, with explicit
reasoning at each gate.

1. **Discover** — report existence/shape of `.jm-adk.local.json` (never its
   values); note overwrite risk.
2. **Analyze** — run the secret scan; for each input class, justify why it is
   security-relevant (stop-on-missing) or cosmetic (auto-fill + `[ASSUMPTION]`).
3. **Plan** — assemble every block; for command policy, justify each command's
   class (allowed / prohibited / escalation-required) and confirm no silent
   widening.
4. **Validate** — run the offline validator AND `check.sh`; enumerate the result
   of each check (assets, deterministic_scripts, quality_criteria,
   runtime_preferences, command_policy, privacy_policy, write_policy, evidence).
   Prove determinism: no network / clock / randomness consumed.
5. **Pre-apply gate** — restate the overwrite guard and `.gitignore` coverage;
   if applying over an existing profile without `--force`, block and return the
   exact `--force` command.
6. **Execute** — write only on explicit `--apply` + passing guard; then emit the
   setup summary with residual risks ranked.
7. **Guardian** — require a `proceed` decision before declaring done; surface any
   `blocked` / `needs-confirmation` with the failing gate and corrective step.

Alfa core tags only, one family. No prices, no PII, single brand. Never do
`workspace-governance` work.
