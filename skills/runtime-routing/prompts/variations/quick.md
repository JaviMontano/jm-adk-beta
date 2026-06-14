# Quick Variation — Runtime Routing (fast route)

For a clear task where the candidate set is small and evidence is at hand.

## Ask

"Given this task and its required capabilities, which runtime — and why —
lowest-permission, evidence-backed?"

## 4-line procedure

1. List required capabilities; note an evidence id for each (or mark pending).
2. Drop runtimes missing evidence for any required capability.
3. Pick the lowest permission level among survivors (tie → local + Markdown).
4. Emit: runtime + reason, one-line capability status, one-line fallback.

## Guardrails (do not skip even when fast)

- No evidence id for a required capability → that runtime is out; do not assume.
- Always include the local-first fallback, even as a single line.
- Keep secrets local; no remote runtime for a local-doable task.
- Tag claims `[DOC] [CONFIG] [CÓDIGO] [INFERENCE] [SUPUESTO]`.

## Example

"Run a lint+test+commit cycle in this repo." → **Codex / local CLI** — file edits
+ shell validators + `git` are repo-local and lowest-permission `[INFERENCE]`;
fallback = run validators locally + Markdown PR body if `gh` auth is unavailable
`[DOC]`.
