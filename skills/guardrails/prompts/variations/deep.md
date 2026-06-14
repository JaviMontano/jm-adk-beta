# Deep variation — guardrails

`depth=deep`. Apply one guard exhaustively through the full
Discover → Analyze → Execute → Validate loop, verifying each step.

## Discover
- Resolve `topic` to one value; record why competing topics were rejected
  (cite `routes.json` `desc`). Read that single playbook and load every JSON
  policy asset it names. [EXPLICIT]

## Analyze
- Normalize the target: path traversal/symlinks/`~` for paths; segment a compound
  command; identify artifact type and declared contract. [INFERENCE]
- Walk the fail-closed precedence top-down and note the first match. [EXPLICIT]

## Execute
- Run the named validator AND `scripts/check.sh` over positive and negative
  fixtures. Assemble the full packet; aggregate ALL violations, never short-circuit
  at the first. Mask every secret (`path:line` + masked token). [CODE]

## Validate
- Self-application: the packet validates against its own schema where one exists.
- Confirm no `pass` while any required check is fail/blocked; no `allow` without
  evidence; no `block` without a reason; exactly one playbook read; tags single
  family. [EXPLICIT]
- Re-run the script to confirm byte-identical determinism. [EXPLICIT]

## Deliver
Verdict + per-check table + violations + remediation (each repair: exact target +
exact edit) + masked evidence, per `templates/output.md`. Cite the triggering
gate rule. [DOC]
