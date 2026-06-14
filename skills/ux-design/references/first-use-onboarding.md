<!-- distilled from alfa skills/first-use-onboarding -->
<!-- First-use and cold-start onboarding for JM-ADK after clone, greeting, or missing task context. -->
# First Use Onboarding

Cold-start protocol: classify ambiguous input, decide whether to onboard or proceed, never block an explicit task to run setup. [DOC]

## When To Use

- User sends only a greeting or no concrete task.
- Alfa is freshly cloned or lacks `.jm-adk.local.json`. [CONFIG]
- There is no active task, issue, backlog, spec, or workspace context.
- The user asks what Alfa can do before starting work.

## When Not To Use

- User gives an explicit technical task; use micro-context and proceed.
- Repo cannot be confirmed as Alfa; stop with `[SUPUESTO]` flagged as `Dato requerido`.
- User only asks a narrow factual question that does not need setup.

## Anti-Scope

- Not a tutorial engine: one round of setup, then hand off — do not loop teaching. [INFERENCIA]
- Not a credential collector or profile writer (see Safety Limits).
- Does not re-onboard a session that already has a valid profile + active task. [INFERENCIA]

## Inputs

- User input (raw text classified as greeting / task / question / empty).
- Workspace diagnosis from `scripts/diagnose-first-use.py`. [CÓDIGO]
- Known runtime preference, autonomy level, command policy, privacy constraints, output format if already configured. [CONFIG]

## Outputs

- Alfa greeting and short capability explanation.
- One-round guided setup questions (no follow-up interrogation).
- Proposed local profile values with assumptions marked `[SUPUESTO]`.
- Handoff question for the first concrete task.

## Workflow

1. Discover: confirm repo signals and classify the input.
2. Analyze: decide `guided_first_use`, `micro_context_then_task`, `ask_first_task`, or `stop`.
3. Execute: present onboarding only when appropriate.
4. Validate: ensure no secrets were requested and no explicit task was blocked.

### Decision Matrix

| Repo is Alfa | Profile exists | Input shape | Action |
|---|---|---|---|
| no / unknown | — | any | `stop` → `Dato requerido` |
| yes | no | greeting / empty | `guided_first_use` |
| yes | no | explicit task | `micro_context_then_task` |
| yes | yes | greeting / empty | `ask_first_task` |
| yes | yes | explicit task | proceed (no onboarding) |

Tie-break: an explicit task always outranks missing profile — collect only blocking context, never the full guided round. [INFERENCIA]

## Safety Limits

- Do not ask for passwords, API keys, tokens, private keys, or credentials.
- Do not write `.jm-adk.local.json`; route to `setup-workspace-profile.py --apply` only after explicit approval. [CÓDIGO]
- Do not claim runtime capability without repo evidence or executed validation.
- If the user pastes a secret unprompted, do not echo or persist it; warn and continue. [SUPUESTO]

## Edge Cases & Failure Modes

- Greeting + task in one message → treat as task; skip guided round. [INFERENCIA]
- `diagnose-first-use.py` missing or errors → degrade to manual repo-signal check, mark `[SUPUESTO]`, do not crash.
- Partial profile (some keys set) → ask only for unset keys, not the full set.
- Non-Latin / non-Spanish greeting → still classify as greeting; respond in the user's language.
- Repo looks like Alfa but lacks expected scripts → treat identity as unconfirmed → `stop`. [INFERENCIA]

## Fallback

If the user does not provide non-blocking setup details, use safe defaults and mark `[SUPUESTO]` (`Supuesto`). If repo identity is unclear, mark it `Dato requerido` and stop before editing.

## Success Criteria

- Greeting-only input activates the onboarding message.
- Workspace without profile asks for safe setup inputs in a single round.
- Explicit task goes to `task-intake-agent` without a forced setup detour. [CÓDIGO]
- Non-Alfa workspace stops before editing.
- No credential is ever requested; no profile written without explicit approval.
- Every proposed default carries a `[SUPUESTO]` tag with a verification path. [DOC]

## Examples

- Input: `hola` → repo is Alfa, no profile → `guided_first_use`: present Alfa, ask one round of safe setup questions.
- Input: `crea un agente para QA` → `micro_context_then_task`: collect only missing critical context, route to `task-intake-agent`.
- Input: `hola, arregla el lint` → greeting + task → treat as task; skip guided round. [INFERENCIA]
- Input: `hola` in an unconfirmed repo → `stop` with `Dato requerido`; no onboarding, no edits.
