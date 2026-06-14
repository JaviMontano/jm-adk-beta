# guardrails — skill overview

Deterministic guard layer for JM-ADK. A thin router over hooks and offline
scripts that decide **allow / approve / block / pass / fail** with evidence-tagged
reasons. It never improvises guard logic the hooks already enforce, and it never
reports green-by-default. [EXPLICIT]

## What it does

Resolves one `topic` from the request, reads **exactly one** playbook from
`routes.json`, and returns that playbook's verdict. The twelve guards split into
four families:

- **Pre-execution** — `pre-tool-use-guard` (block dangerous commands, exit-code-2
  deny), `user-prompt-filter`, `permission-fast-path`, `input-tolerance`.
- **Post-execution** — `post-tool-use-validator`, `output-contract-enforcer`,
  `secrets-sanitization` (Gate G0), `stop-validator`.
- **Gate / governance** — `quality-gatekeeper` (G0–G3), `constitution-compliance`
  (v6.0.0, 18 principles), `integrity-chain-validation`.
- **Meta** — `management` (operate and audit the guard suite itself).

## When to use

A request targets a deterministic guard: block a command, validate a tool
result, filter a prompt, enforce an output contract, sanitize secrets, check a
quality gate or constitution principle, or validate the integrity chain / stop
conditions. Triggers: `/jm:verify`, `/jm:advance`, gate or PR readiness,
pre-delivery checks. [INFERENCE]

## How it routes and executes

1. Map the request to one `topic` (enum in `SKILL.md`). If two plausibly fit,
   disambiguate from the `desc` field in `routes.json`; if still ambiguous, ask —
   never load several playbooks. [EXPLICIT]
2. Read that one playbook. `quick` runs essentials; `deep` applies the full
   Discover → Analyze → Execute → Validate loop and verifies each step. [CONFIG]
3. Prefer the hook/script the playbook names (script-first). Fail closed: missing
   evidence ⇒ fail/block, never pass. [CONFIG]

## References

All playbooks live in `references/` and are listed in `routes.json`:
`pre-tool-use-guard.md`, `post-tool-use-validator.md`, `user-prompt-filter.md`,
`output-contract-enforcer.md`, `quality-gatekeeper.md`, `secrets-sanitization.md`,
`constitution-compliance.md`, `integrity-chain-validation.md`,
`permission-fast-path.md`, `stop-validator.md`, `input-tolerance.md`,
`management.md`. Tag canon: `../../references/verification-tags.md`.

## Evidence tags

Alfa core family only: `[EXPLICIT]` `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]`
`[ASSUMPTION]`. One tag per claim; never mix families. [DOC]

## Companion bundle

- `agents/` — role contracts (lead, specialist, support, guardian).
- `knowledge/` — body of knowledge + concept graph.
- `prompts/` — primary, meta, and quick/deep variations.
- `templates/output.md` — the guard verdict deliverable scaffold.
- `evals/evals.json` — scenario suite over real guard topics.
- `examples/` — a worked `pre-tool-use-guard` block decision.
- `assets/` — quality rubric and verdict checklist (see `assets/README.md`).
