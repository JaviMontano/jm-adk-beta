# workspace-setup

Design a deterministic, **dry-run-first** plan for the local profile
`.jm-adk.local.json` — runtime preferences, command policy, privacy boundaries,
write safety, evidence, and offline validation — and write the file **only on an
explicit apply**.

## What it does

Turns onboarding answers (goal, runtime, autonomy, command policy, privacy,
output format) into a single validated plan. The plan is the unit of work:
it is previewed, validated offline, and applied only when `mode=apply` is
explicit and the overwrite guard passes (no existing file, or `--force`).

## When to use

- The user has approved creating a local Alfa profile and onboarding has
  collected the required inputs.
- A developer wants reusable local defaults that are never committed.

Do **not** use it to audit or clean existing session folders / task bridges
(that is `workspace-governance`), or for a one-shot answer that needs no
persistent profile.

## How it routes / executes

`Discover → Analyze → Plan → Validate → Execute` (see SKILL.md "Workflow"):

1. **Discover** existing profile *shape* without printing sensitive values.
2. **Analyze** — run the secret scan; detect overwrite risk.
3. **Plan** — build the deterministic plan against the contract.
4. **Validate** — run the offline validator; a failing check blocks any apply.
5. **Execute** — dry-run by default; write only on explicit `--apply` + passing
   overwrite guard.

## Evidence taxonomy

Alfa core set only, one spelling per document: `[CODE]` `[CONFIG]` `[DOC]`
`[INFERENCE]` `[ASSUMPTION]`. Never the Jarvis `{...}` family.

## Layout

- `SKILL.md` — the contract, workflow, safety limits, acceptance criteria.
- `agents/` — `lead` (orchestrates the flow), `specialist` (profile-schema and
  secret-shape depth), `support` (executes scan/validate/write), `guardian`
  (the apply/overwrite/secret/offline gate).
- `knowledge/` — `body-of-knowledge.md` and `knowledge-graph.json` over the
  profile schema, policy classes, and safety invariants.
- `prompts/` — `primary`, `meta`, and `variations/{quick,deep}`.
- `templates/output.md` — the setup-plan-and-summary deliverable scaffold.
- `evals/evals.json` — activation + check cases (dry-run, apply, blocked,
  rejected, false-positives).
- `examples/` — a concrete dry-run worked example.
- `assets/` — `manifest.json`, `quality-rubric.json`, `apply-checklist.md`,
  plus the planned plan-contract reference.
