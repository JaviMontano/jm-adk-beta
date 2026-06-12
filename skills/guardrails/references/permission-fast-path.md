<!-- distilled from alfa skills/permission-fast-path -->
<!-- > -->
# Permission Fast Path
> "Method over hacks."
## TL;DR
Auto-approve read-only operations to cut human-in-the-loop overhead; route every state-changing op through explicit approval. [DOC]

## Classification
The whole guardrail reduces to: read-only → auto-approve; mutating, costly, or exfiltrating → ask. When unsure, treat as mutating. [INFERENCIA]

**Auto-approve (read-only, idempotent, local):**
- File reads, `ls`/`find`/`grep`/`cat`, status/diff/log inspection. [CONFIG]
- Dry-run/preview flags (`--dry-run`, `--check`, plan-only). [CONFIG]

**Always ask (never fast-path):**
- Writes/deletes/moves, `git push`/commit, package installs. [CONFIG]
- Network egress with payloads, credential or secret reads. [CONFIG]
- Anything billable, irreversible, or outside the working dir. [SUPUESTO]

## Procedure
1. **Classify** the op against the two lists above. [DOC]
2. **Default-deny on ambiguity** — unknown command or mixed read+write → ask. [INFERENCIA]
3. **Execute**; tag each action with its evidence source. [DOC]
4. **Validate** against the acceptance criteria below. [DOC]

## Acceptance Criteria
- [ ] Every auto-approved op is provably read-only and in-scope. [DOC]
- [ ] No write/network/billing op was auto-approved. [DOC]
- [ ] Ambiguous ops were escalated, not guessed. [INFERENCIA]
- [ ] Evidence tags use the Alfa core set, one spelling throughout. [CONFIG]

## Trade-off
Allowlist (this design) over denylist: a missed allowlist entry costs one extra
prompt; a missed denylist entry auto-approves a mutation. Fail toward asking. [INFERENCIA]

## Usage

Example invocations:

- "/permission-fast-path" — Run the full permission fast path workflow
- "permission fast path on this project" — Apply to current context

## Assumptions & Limits
- Assumes the working dir is the trust boundary; ops touching paths outside it are never fast-pathed. [SUPUESTO]
- Classification is best-effort on command text; obfuscated/piped commands (`sh -c`, base64) default to ask. [INFERENCIA]
- Does not replace human judgment for irreversible or billable actions. [DOC]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Read command that writes a side-effect (e.g. `tee`, `>`) | Treat as mutating; ask |
| Compound command (read `&&` write) | Classify by the strongest effect; ask |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope / outside working dir | Redirect to appropriate skill or escalate |
