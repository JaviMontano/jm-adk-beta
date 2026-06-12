# Assets — lab-session

Supporting data files for the P08 Lab-session scaffold. Each is referenced from
`assets/manifest.json` with its `used_by` target.

## Files

- **`quality-rubric.json`** — the P08 acceptance criteria as machine-readable
  blocker checks. The guardian agent (`agents/guardian.md`) runs these as the
  validation gate; `SKILL.md` points here for the gate definition.

- **`file-skeletons.json`** — the canonical starting state for each of the four
  files (`notas.md`, `hipotesis.md`, `referencias.md`, `decision.md`),
  including required sections and the tag set. The specialist
  (`agents/specialist.md`) specs from it and support (`agents/support.md`)
  writes the skeletons verbatim.

## Conventions

- Tags are the Alfa core set, EN spelling: `[CODE]` / `[CONFIG]` / `[DOC]` /
  `[INFERENCE]` / `[ASSUMPTION]`.
- Skeleton placeholders in `{BRACES}` are human-filled stubs; the skill never
  invents a topic or writes a keep/pivot/kill verdict.
- `manifest.json` is the index; keep `used_by` targets pointing at files that
  actually exist.
