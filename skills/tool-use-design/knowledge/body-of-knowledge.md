# Body of Knowledge — Tool Use Design

Domain knowledge for designing tool descriptions as deterministic routing contracts.

## Key concepts

- **Routing contract.** A tool description that lets a planner pick the tool from the description *alone* — no hidden context, no clarifying question. Fixes purpose, input format, output shape, examples, boundary. [DOC]
- **Decisión inmediata.** The unit of value: given only the descriptions, the model routes correctly without guessing or asking. [INFERENCIA]
- **Overloading.** Two tools whose purposes overlap such that a human would confuse them. The model confuses them too. [INFERENCIA]
- **Reciprocal boundary.** A bidirectional delegation: X says "for B use Y" and Y says "for A use X". Unidirectional mentions are defects. [DOC]
- **Repo strategy `Grep → Read → Edit`.** Locate cheaply with Grep/Glob, read only justified hits with Read, mutate precisely with Edit. [DOC]
- **Edit failure mode.** `old_string` must be unique; a non-unique anchor makes `Edit` fail. [CÓDIGO]
- **Full-rewrite fallback.** When the anchor cannot be isolated, `Read` the file then `Write` the whole new content. [CÓDIGO]

## Standards / decision rules

1. **Reject generic verbs.** `analyze`, `process`, `handle` declare neither input nor boundary → automatic reject. [DOC]
2. **Split, don't narrate.** Resolve overload with `rename_split`, never with a longer paragraph. The model routes by name + boundary, not by nuance under context pressure. [INFERENCIA]
3. **No read-all upfront.** Ban `Glob("**/*") + Read all`; it saturates the window (~200k tokens in mid repos) and degrades reasoning. Load only what a Grep hit justifies. [SUPUESTO] — measure tokens on the target repo before ever adopting read-all.
4. **Prefer Edit over Write.** Minimal blast radius. Fall to Write full-rewrite only when the anchor cannot be isolated — never the reverse for convenience. [CÓDIGO]
5. **Determinism flags required.** `offline=true`, `network_required=false`, `deterministic=true` on every valid report. [DOC]
6. **Single evidence-tag family.** One Alfa-core family (`[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`) per output; mixing families fails the gate. [CONFIG]

## Failure-mode catalog

| Symptom | Root cause | Repair |
|---|---|---|
| Agent asks "which tool?" | Missing reciprocal boundary | Add bidirectional delegation [DOC] |
| Wrong tool chosen | Overloaded surface | `rename_split` on responsibility axis [INFERENCIA] |
| Context window saturated | read-all upfront | Switch to `Grep → Read` selective [SUPUESTO] |
| `Edit` fails silently | Non-unique `old_string` | Expand anchor or `Read + Write` [CÓDIGO] |
| Description says nothing | Generic verb | Rewrite as contract [DOC] |

## Acceptance gate (offline, no network)

≥2 contracts each with purpose/input/examples/boundary · reciprocal delegation · overload = `rename_split` · repo sequence `grep, read, edit` · `read_all_upfront=false` · `glob_all_then_read_all=false` · `unique_anchor_required=true` + `read_write_full_rewrite` fallback · `offline=true`, `network_required=false`, `deterministic=true`. [DOC]

## Related practice

Katas `katas-21`, `katas-23`; skills `katas-tool-description-quality`, `katas-builtin-tool-selection`.
