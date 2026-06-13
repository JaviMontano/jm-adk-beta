# Example input — workspace-setup

A developer onboarding to Alfa supplies these answers, then asks for a preview:

> "Set up my local Alfa profile. My goal is to ship a TypeScript CLI with Alfa
> pairing on it. Runtime is Codex, autonomy is 'propose-then-act'. For commands:
> allow `git status`, `git diff`, and the repo validation scripts; prohibit
> `git reset --hard` and `rm -rf`; treat any permission widening as
> escalation-required. Privacy must be local-only and store no secrets. Output
> format: markdown with evidence tags. Show me the plan first — don't write the
> file yet."

Context the skill also observes:
- `.jm-adk.local.json` does **not** yet exist in the repo (no overwrite risk).
- `.gitignore` already lists `.jm-adk.local.json`.
- No `mode=apply` / `--apply` flag was given → default to `dry-run`.
- One inline string in the goal looks like a token (`ghp_examplexxxx`) and must
  be caught by the secret scan and redacted by category, not stored.
