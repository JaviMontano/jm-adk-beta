# Meta Prompt — data-platform (self-check)

Use this to audit a data-platform run before declaring done. Answer each; any
"no" sends the run back to the responsible agent.

## Routing integrity
- Did I resolve `topic` to a single value in the 8-enum? [EXPLICIT]
- Did I load **exactly one** playbook, and only after fixing `topic`? Loading
  >1 route, or reading a playbook before fixing `topic`, is an anti-pattern. [INFERENCE]
- If two topics were plausible, did I run the dominant and name the deferred? [INFERENCE]

## Application integrity
- Does the output address the user's concrete task, not the topic in the
  abstract?
- For ETL/migration: are loads idempotent, and is the watermark advanced only
  post-commit? [EXPLICIT]
- For migration: did I respect the Firestore 500-writes/batch cap and emit a
  `batch_id` per chunk? [CONFIG]
- For schema changes: additive or planned-with-sign-off, never a surprise
  break? [EXPLICIT]

## Gate integrity
- Does every destructive op carry a rollback path stated before execution? [ASSUMPTION]
- Does reconciliation (counts + key checksum) pass within tolerance, with no
  duplicate/NULL keys at grain? [EXPLICIT]
- Is every claim tagged with one Alfa-core family tag — one family, one
  spelling? [DOC]
- Did I avoid green-as-success: every gate item actually exercised, not assumed?
