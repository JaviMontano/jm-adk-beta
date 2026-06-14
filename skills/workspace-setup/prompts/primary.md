# Primary prompt — workspace-setup

You are running the **workspace-setup** skill. Design a deterministic,
dry-run-first plan for the local profile `.jm-adk.local.json`, and write it only
on an explicit apply.

## Inputs to gather (stop-on-missing for security-relevant)
- Primary goal with Alfa; project/product type and known stack.
- Preferred runtime (e.g. Codex); autonomy level.
- Command policy: allowed / prohibited / escalation-required classes.
- Privacy constraints; workspace area; output format.

If a **security-relevant** input (command policy, privacy) is missing, STOP and
ask one question — never auto-fill. A **cosmetic** input (output format) may be
auto-filled and tagged `[ASSUMPTION]`.

## Procedure
1. **Discover** — report whether `.jm-adk.local.json` exists and its key shape;
   never print its contents.
2. **Analyze** — run the secret scan on every input. On a credential shape
   (`sk-`, `ghp_`, `xox`, passwords, `BEGIN ... PRIVATE KEY`, bearer headers,
   raw emails, credentialed connection strings): reject the input, name the
   *category*, substitute a redaction placeholder, never echo the value.
3. **Plan** — assemble: `target_file` = `.jm-adk.local.json`; `mode` (default
   `dry-run`); runtime preferences; command policy; privacy policy; write policy;
   evidence; validation checks (assets, deterministic_scripts, quality_criteria,
   runtime_preferences, command_policy, privacy_policy, write_policy, evidence).
4. **Validate** — run the offline validator; any failing check blocks apply. No
   network, clock, or randomness.
5. **Execute** — emit a dry-run preview by default. Write only when `--apply` is
   explicit AND the overwrite guard passes (no existing file, or `--force`) AND
   `.gitignore` covers the file. Never partial-write.

## Output
Use `templates/output.md`: the plan preview + setup summary (evidence,
validation result, residual risks). If a safe write is impossible, return the
JSON preview plus the exact later-apply command.

## Governance
Alfa core evidence tags only (`[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]`
`[ASSUMPTION]`), one family. No prices, no PII, single brand (JM Labs). Green is
never assumed. Do not do `workspace-governance` work.
