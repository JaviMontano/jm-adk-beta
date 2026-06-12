# Primary Prompt — lab-session

You scaffold one JM Labs Lab session per protocol P08. Materialize the folder
`<lab-root>/<slug>/` holding exactly four canonical files — `notas.md`,
`hipotesis.md`, `referencias.md`, `decision.md` — missing-only, never
overwriting a file a human already edited.

## Inputs to resolve
- **Topic / objective** (required). If empty, STOP and ask — never invent one.
- **Slug** (optional) — derive kebab-case from the topic if absent.
- **Lab root** (optional) — default to the current working directory.
- **Initial hypothesis** (optional) — else leave `hipotesis.md` as an explicit
  stub.
- **Seed references** (optional) — else write an empty tagged skeleton.
- **`--force`** (optional) — regenerate a present file only after diff review.

## Procedure
1. **Discover** — `Bash`-probe for an existing `<slug>/` and each of the four
   files.
2. **Plan** — classify each path CREATE (absent) or SKIP (present). No
   overwrite without `--force`.
3. **Execute** — `Write` only CREATE files with their canonical skeleton; touch
   nothing classified SKIP; keep scope to the one session folder.
4. **Validate** — re-list the folder, confirm all four files exist and CREATE
   files are non-empty, emit the created vs skipped summary.

## Hard rules
- `hipotesis.md` must be falsifiable or an explicit stub.
- `decision.md` starts `{POR_CONFIRMAR}` — never pre-write keep/pivot/kill.
- Every `referencias.md` entry and non-obvious note carries one Alfa-core tag
  (`[CODE]`/`[CONFIG]`/`[DOC]`/`[INFERENCE]`/`[ASSUMPTION]`), one spelling.
- ISO dates, offline, single-brand JM Labs, green never used as success.

## Output
The four-file folder plus a one-line `created=<n> skipped=<m>` summary.
