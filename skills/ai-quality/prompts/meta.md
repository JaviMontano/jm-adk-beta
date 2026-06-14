# Meta Prompt — ai-quality

Use this to reason about *how well the router itself is operating* before and
after a run. It governs routing quality, not any single topic's content.

## Pre-flight (before reading any playbook)
- Did I map the request to **exactly one** topic enum, or am I tempted to load
  two "to be safe"? Loading >1 playbook is a defect — stop. [SUPUESTO]
- Is there a real tie between two topics? If yes, ask one targeted clarifying
  question. If no, resolve silently and proceed. [INFERENCIA]
- Did I run the disambiguation rules for the known collisions (score vs write vs
  review; AI vs human review; strategy vs execution; detection vs evaluation)? [DOC]
- Is `depth` set to match the stakes (quick vs deep)? [CONFIG]

## In-flight
- Am I answering from the router instead of the playbook? If so, stop and read
  the playbook. [SUPUESTO]
- Is every claim carrying one Alfa tag, one family? Any `[CÓDIGO]` without an
  inspected referent must downgrade to `[SUPUESTO]`. [DOC]
- Am I about to assert a test/eval/runtime result without an executed command or
  a captured check? That is forbidden — mark `needs-verification`. [DOC]

## Post-flight (self-audit)
- Did the validation gate actually run, or am I about to call "done" on vibes? [DOC]
- Am I reporting a green check as a safety/correctness guarantee? Reword to
  "well-formed", never "safe". [INFERENCIA]
- Would a second router, given the same request, resolve the same topic? If not,
  my justification is too weak — strengthen or re-resolve. [INFERENCIA]

## Improvement signal
If the same request type keeps causing a tie, propose a sharpening of the
disambiguation rule in `SKILL.md` and `knowledge/body-of-knowledge.md` — do not
keep guessing the same ambiguity each run. [SUPUESTO]
