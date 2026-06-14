# Meta Prompt — lab-session (self-check before declaring done)

Use this to audit your own run of lab-session against the P08 contract before
returning. Answer each; any "no" blocks completion.

## Routing
- Did I confirm a real topic, or did I STOP and ask on an empty objective
  (never auto-filled a topic)?
- Did I resolve slug and Lab root explicitly, and surface any slug collision
  with a different topic instead of silently reusing the folder?

## Contract
- Are there **exactly four** files planned — `notas.md`, `hipotesis.md`,
  `referencias.md`, `decision.md` — not more, not fewer?
- Did I classify every path CREATE vs SKIP, and write only CREATE files?

## Safety
- Did every SKIP file stay byte-identical (mtime/bytes unchanged)?
- Did I avoid overwriting anything without an explicit, diff-reviewed `--force`?
- Did I refuse to create sibling/parent files or fall back to a surprise path?

## Content quality
- Is `hipotesis.md` falsifiable or an explicit stub?
- Does `decision.md` start `{POR_CONFIRMAR}` with no pre-written verdict?
- Does every reference entry and non-obvious note carry one Alfa-core tag, one
  spelling throughout?

## Hygiene
- ISO dates, offline, identical-inputs-identical-bytes?
- Single-brand JM Labs, with green never used as a success signal?
- Did I emit the `created=<n> skipped=<m>` summary line?

If any answer is "no", fix it before declaring done. Do not green-light a
partial scaffold.
