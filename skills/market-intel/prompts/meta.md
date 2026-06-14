# Meta prompt — market-intel (self-check & reasoning)

Use before emitting. This governs *how* the router reasons about routing and
evidence, independent of which topic was chosen.

## Routing self-interrogation

- Did I land on **exactly one** topic ∈ enum? If I felt the urge to load two
  playbooks "to be safe", that is a routing failure — pick the dominant
  decision-value topic and defer the other.
- Is the topic genuinely ambiguous (two readings → two different playbooks)? If
  yes, ask one question. If the user gave a disambiguator (URL, ticker, sector,
  role), do **not** ask — state the chosen reading.
- Is the request actually out of scope (product spec, GTM execution, DCF/unit
  economics, implementation)? If so, re-route instead of forcing a topic.

## Evidence self-interrogation

- Am I using the **loaded playbook's** tag family — and only that one? No mixing
  Alfa `[..]` with OSINT `[EXPLICIT]/[INFERRED]/[OPEN]`.
- For every quantitative claim: do I have a source + date? If not, did I
  downgrade the tag (to `[INFERENCIA]`/`[INFERRED]`/`[OPEN]`) rather than
  asserting?
- Did any vendor self-positioning sneak in as verified fact? Re-tag it as a
  claim.
- One tag per claim; weakest applicable when two compete; over-tagging the
  obvious is forbidden.

## Governance self-interrogation

- Did a concrete price leak anywhere? Replace with a range/placeholder.
- One brand only? Correct token set?
- Any client PII or non-public contact data? Reduce to public-channel
  equivalents.
- Did `depth=deep` actually run the playbook's Validate step?

If any answer fails, fix before output — do not ship and annotate.
