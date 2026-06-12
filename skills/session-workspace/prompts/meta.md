# Meta prompt — session-workspace router self-check

Use this to audit a dispatch decision before it is finalized. Answer each as
pass/fail with the evidence.

## Routing integrity
- Did I Read exactly ONE `references/<topic>.md`? (Any sibling loaded = fail.)
- Is the chosen `topic` one of the seven enum values?
- Did I route by lifecycle *intent*, not by the literal word "session"
  (e.g. a login-session question is out of scope)?

## Discrimination correctness
- bootstrap vs. protocol: did I pick bootstrap only for "safe-state check" and
  protocol for the full load→recover→close→next sequence?
- manager vs. protocol: any *write* to `.specify/context.json` must route to
  `session-manager`; protocol only *reads* the stage.
- pre-compact vs. end-cleanup: pre-compact preserves *unfinished* work across a
  compaction; end-cleanup closes a *finished/paused* session.

## Anti-scope
- No content authoring performed by the router itself?
- No multi-topic merge / fan-out across playbooks?
- No `.specify/context.json` write outside the manager route?

## Governance & evidence
- Every routing claim carries one Alfa-core tag, one family, consistent spelling?
- No invented prices, no PII, single brand?
- On ambiguity, did I ask exactly ONE clarifying question instead of guessing?

## Guardian
- Did I emit a decision (`proceed` | `blocked` | `needs-confirmation`) and, when
  not `proceed`, name the failing gate and the corrective next step?

If any answer is fail, do not declare done — correct or escalate to the user.
