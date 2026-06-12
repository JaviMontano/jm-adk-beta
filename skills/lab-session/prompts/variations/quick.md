# Quick Variation — lab-session

Fast path for when the topic is clear and the Lab root is the current directory.

Run the spine without ceremony:

1. Derive `slug` (kebab-case) from the topic; use the current working dir as the
   Lab root.
2. Probe `<slug>/`; classify the four paths CREATE/SKIP.
3. `Write` only CREATE files with their canonical skeletons:
   - `notas.md` — one dated stub entry (ISO date).
   - `hipotesis.md` — the supplied claim, or `{HIPOTESIS_POR_DEFINIR}`.
   - `referencias.md` — empty tagged skeleton.
   - `decision.md` — `{POR_CONFIRMAR}`.
4. Re-list; emit `created=<n> skipped=<m>`.

Still non-negotiable: empty topic → STOP and ask; never overwrite a SKIP;
falsifiable-or-stub hypothesis; one Alfa-core tag per reference entry;
single-brand JM Labs.

Skip only the deep framing dialogue — not any safety or contract check.
