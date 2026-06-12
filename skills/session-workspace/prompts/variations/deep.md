# Deep variation — verified dispatch (depth=deep)

Use when the lifecycle moment is ambiguous, spans a boundary (bootstrap vs.
protocol, pre-compact vs. end-cleanup, manager-write vs. protocol-read), or when
a wrong route would be costly (e.g. an unauthorized `.specify/context.json`
write).

## Procedure
1. **Discover** — restate the request; enumerate every candidate topic that could
   plausibly apply, each with a one-line reason and an Alfa-core tag.
2. **Analyze (adversarial)** — for each candidate, state the discriminator that
   *excludes* it or *confirms* it. Apply the boundary rulings:
   - Any write/compute of `.specify/context.json` stage → forces `session-manager`.
   - "Safe to begin?" (no closure of old tasks) → `session-start-bootstrap`.
   - Load→recover→close→next, including pending-task closure → `session-protocol`.
   - Preserve *unfinished* work across compaction/`/clear` → `pre-compact-context`.
   - Close a *finished/paused* session with durable handoff → `session-end-cleanup`.
   If more than one survives, STOP — ask exactly one clarifying question and mark
   the residual ambiguity `[OPEN]`.
3. **Execute** — Read the single winning `references/<topic>.md`; pass
   `depth=deep` so the playbook runs its per-step verification and full
   `scripts/check.sh` gate.
4. **Validate (per-step)** — run the meta-prompt checklist (`prompts/meta.md`):
   single-route, correct discrimination, anti-scope clean, tags one-family,
   Guardian emitted.

## Output
Candidate table (topic · include/exclude · evidence tag), the chosen route, the
Guardian decision with named gaps, and the next action handed to the playbook.

## Governance
Alfa-core tags one family; no prices; no PII; single brand; green never assumed —
unknown → `[OPEN]` → one clarifying question. [DOC]
