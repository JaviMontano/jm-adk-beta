# Deep variation — project-create

Thorough path for ambiguous intents, collision risk, or partial scaffolds.

## Steps

1. **Discover with care** — derive the slug and validate it against
   `^[a-z0-9]+(-[a-z0-9]+)*$`. Read the registry; compute the next free `P-NNN`.
   Read the parent sector `CLAUDE.md` and confirm the sector if the name implies
   one other than the `III Core` default `[ASSUMPTION]`. [CONFIG]
2. **Collision analysis** — if the slug exists under a different `P-NNN`, surface
   both and ask which to reuse/rename. If the id is taken, advance to the next
   free id and record the substitution. [INFERENCE]
3. **Partial-scaffold handling** — if 1–2 of the three files already exist, fill
   only the missing ones; never touch the present ones. Re-read each present file
   before deciding. [DOC]
4. **Rule-9 construction** — draft `CLAUDE.md` as a router; if it would exceed 70
   lines, factor detail into `MEMORY.md`/links before writing. [INFERENCE]
5. **Register & validate** — confirm the unique `P-NNN ↔ slug ↔ path` triple
   idempotently; run the full acceptance gate and report each check. [DOC]

## Reporting

Use `templates/output.md` and include collision/substitution notes, the
files-written-vs-skipped breakdown, and the per-check gate verdict. [DOC]
