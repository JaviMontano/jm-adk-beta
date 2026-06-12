# Deep Variation — lab-session

Use when the idea is fuzzy, the hypothesis needs sharpening, or the session must
slot cleanly into an existing Lab tree.

## Extra discovery
- Probe the Lab root for sibling sessions and any slug collision; if a folder
  with the same slug holds a *different* topic, surface the conflict and ask
  before reusing it.
- Confirm the Lab root is writable up front; on failure, stop with the path
  error rather than choosing a fallback location.

## Sharpen the hypothesis
- Restate the idea as a claim that can fail. Make explicit what observation
  would refute it. If it cannot be made falsifiable yet, write the stub
  `{HIPOTESIS_POR_DEFINIR}` plus a short note on what is missing — do not force a
  fake claim.

## Seed references with rigor
- For each seed source, capture title/link plus exactly one Alfa-core tag
  (`[DOC]` for documented facts, `[INFERENCE]` for reasoned reads, etc.). One
  spelling throughout.

## Richer notes scaffold
- `notas.md` gets a dated first entry (ISO), an "Open questions" section, and a
  "Next probe" line — all stubs the human will extend.

## Close the loop
- Run the full guardian gate (four-file contract, no-overwrite proof,
  falsifiability, tag hygiene, `{POR_CONFIRMAR}` decision, summary line, brand +
  signal hygiene). Report the gate result and the created/skipped summary.
