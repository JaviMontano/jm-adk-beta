# Body of Knowledge — guardrails

Deterministic guard layer for JM-ADK. Concepts, standards, and decision rules
that govern allow/approve/block and pass/fail/blocked verdicts. [DOC]

## 1. Core concepts

- **Guard topic.** One of twelve deterministic checks (see `routes.json`). A
  request resolves to exactly one. [EXPLICIT]
- **Verdict.** The guard's output. Pre-execution guards emit
  `allow | approve | block`; post-execution and gate guards emit
  `pass | fail | blocked` (or `not_verified` for governance). [EXPLICIT]
- **Fail-closed.** The default safety posture: when safety cannot be proven,
  return the restrictive verdict. Silence is never a pass; absence of evidence is
  not evidence of absence. [EXPLICIT]
- **Script-first.** Each playbook names an offline validator + a `check.sh`
  fixture gate; the script's result is authoritative over prose. [CONFIG]
- **Determinism.** Same input ⇒ same packet. No clock, network, model provider,
  MCP tool, or randomness in a verdict. [EXPLICIT]

## 2. The exit-code deny pattern (pre-execution)

Hooks signal decisions by exit code:
`0` = allow, `1` = approve (explicit human confirmation), `2` = block. A `block`
MUST carry `exit_code: 2`; an `allow` MUST carry `exit_code: 0` plus non-empty
`evidence`. Worst-segment-governs: a compound command (`&&`, `;`, `|`,
substitution) is blocked if ANY segment is a blocker. [EXPLICIT]

## 3. Gate model G0–G3 (governance)

- **G0** — secrets: no unmasked credentials anywhere (hard stop, precondition).
- **G1** — structure/format and required sections/fields.
- **G2** — quality criteria and evidence-tag conformance.
- **G3** — release/constitution compliance (v6.0.0, 18 principles).

Gates are sequential: a later gate cannot pass while an earlier one is unmet.
Each gate decision emits a score-history entry contract. [EXPLICIT]

## 4. Decision rules

| Situation | Verdict | Rule |
|---|---|---|
| Destructive shell (`rm -rf`, `git reset --hard`, `git clean -fd`) | `block` (exit 2) | dangerous-command-policy [EXPLICIT] |
| Write outside `allowed_write_roots` | `block` | write-boundary-policy [EXPLICIT] |
| Touch `.env`, credentials, private path | `block` | private-path-policy [EXPLICIT] |
| Any unmasked token-like value | `block`/`FAIL` | token-pattern-policy, G0 [EXPLICIT] |
| Unresolved Critical finding | `FAIL` | secrets G0 precedence rule 3 [EXPLICIT] |
| Contract/input missing | `blocked` | cannot check ≠ wrong [INFERENCE] |
| Artifact present but violates contract | `fail` | checked and wrong [INFERENCE] |
| Required check fails, others pass | overall non-`pass` | aggregate, never short-circuit [EXPLICIT] |

## 5. fail vs blocked vs not_verified

- `fail` — "I checked and it is wrong." Routes to the artifact author.
- `blocked` — "I could not check" (missing contract/input/asset). Routes to the
  contract owner.
- `not_verified` — governance row with no evidence; downgrades overall status away
  from pass. [INFERENCE]

## 6. Secret masking standard

Reveal at most the first 4 chars, redact the rest (`AKIA****…`, `ghp_****…`,
`sk-…last4`); collapse PEM bodies to `-----BEGIN … REDACTED … END-----`. Reference
findings by `path:line` + masked token. An unmasked value in the report is itself
a Critical finding. [EXPLICIT]

## 7. Evidence taxonomy

Alfa core family only: `[EXPLICIT]` `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]`
`[ASSUMPTION]`. One tag per claim; mixing two families in one artifact is itself
an evidence failure. Canon: `../../references/verification-tags.md`. [DOC]

## 8. Anti-patterns

Loading multiple playbooks "to be safe"; guessing `topic` under ambiguity;
reimplementing logic the hook already enforces; emitting `pass` with an empty
checks array; auto-renaming files; reporting success without running the gate.
[DOC]

## 9. Standards anchored

JM-ADK Constitution v6.0.0; exit-code-2 hook deny convention; Gate G0–G3 quality
model; single-family evidence tagging. [CONFIG]
