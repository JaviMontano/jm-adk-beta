# Quick variation — guardrails

`depth=quick`. Run the essentials of one guard and return the verdict fast.

1. Resolve `topic` to one value (ask only if genuinely ambiguous).
2. Read that single playbook.
3. Run its named validator + `scripts/check.sh`.
4. Emit verdict: `allow|approve|block` (pre) or `pass|fail|blocked` (post/gate)
   with exit_code where applicable, a one-line reason, and the triggering rule.

Quick still enforces every MANDATORY check — `quick` only narrows optional
coverage, it never skips a hard gate. Missing evidence ⇒ block/fail, never pass.
Every claim carries one Alfa-core tag; secrets masked. [EXPLICIT]

Example: proposed `rm -rf build/ && cat .env` → `block`, `exit_code: 2`, reason
"`.env` secret read + `rm -rf` destructive (worst segment governs)". [INFERENCE]
