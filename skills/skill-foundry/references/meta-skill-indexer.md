<!-- distilled from alfa skills/meta-skill-indexer -->
<!-- Regenerates skills_index.json by scanning all SKILL.md files. Extracts frontmatter metadata for BM25 search. [EXPLICIT] -->
# meta-skill-indexer {Meta} (v1.1)

> **"Skills that create, review, search, and deploy other skills."**

## Purpose
Generates the `skills_index.json` catalog from SKILL.md YAML frontmatter; consumed by meta-skill-searcher for BM25 search. [EXPLICIT]

**When to use:** After any create / delete / rename / frontmatter edit of a skill. Run `python .agent/scripts/generate_index.py`. [EXPLICIT]
**Anti-scope:** Does NOT lint frontmatter, validate schema correctness, or fix malformed skills — it only extracts and catalogs. Body content below frontmatter is never indexed. [INFERRED]

## Core Principles
1. **Single Source:** `skills_index.json` is auto-generated, never hand-edited; manual edits are overwritten on next run. [EXPLICIT]
2. **Frontmatter contract:** Index extracts exactly `name, description, version, status, tags`. Missing key → field emitted as `null`/`[]`, not a crash. [EXPLICIT]
3. **Freshness:** Stale index = silent search misses. Re-index after every skill change. [EXPLICIT]
4. **Determinism:** Same tree → byte-identical output (sorted ids) so diffs are reviewable. [INFERRED]

## Core Process
- **Phase 1 — Walk:** Recurse `.agent/skills/` for every `SKILL.md`. Symlinks not followed; hidden dirs skipped. [INFERRED]
- **Phase 2 — Parse:** Read leading `---` YAML block of each file. On malformed YAML, skip that file and record a warning (one bad skill must not abort the run). [INFERRED]
- **Phase 3 — Write:** Emit `skills_index.json` with `{id, path, name, description, version, status, tags}` per skill, sorted by `id`.

### Output schema (per entry) [INFERRED]
| field | source | on-missing |
|-------|--------|-----------|
| `id` | slug of `name` or dir name | derive from path |
| `path` | relative path to SKILL.md | always present |
| `name`/`description`/`version`/`status`/`tags` | frontmatter | `null` / `[]` |

### Worked example
Input frontmatter → index entry:
```yaml
# .agent/skills/pdf-export/SKILL.md
name: pdf-export
description: Render docs to PDF
version: 2.0
status: production
tags: [export, pdf]
```
```json
{ "id": "pdf-export", "path": ".agent/skills/pdf-export/SKILL.md",
  "name": "pdf-export", "description": "Render docs to PDF",
  "version": "2.0", "status": "production", "tags": ["export","pdf"] }
```

## Validation Gate
- [ ] Script exited 0; entry count == number of `SKILL.md` files found minus skipped
- [ ] `skills_index.json` updated and re-parses as valid JSON
- [ ] `context.json` reflects current state
- [ ] No stack violations (R-002, R-003)
- [ ] Skipped-file warnings reviewed (none silently lost) [INFERRED]

## 4. Self-Correction Triggers
> [!WARNING]
> IF `skills_index.json` is stale THEN regenerate before searching.
> IF deploying a skill with `status != production` THEN WARN user.
> IF entry count dropped unexpectedly THEN a SKILL.md failed to parse — inspect warnings before committing. [INFERRED]

## Failure Modes [INFERRED]
| Symptom | Cause | Fix |
|---------|-------|-----|
| Search misses a known skill | Stale index | Re-run indexer |
| Skill absent from index | Malformed/missing frontmatter | Fix YAML, re-run |
| Field is `null` | Key absent in frontmatter | Add key to SKILL.md |
| Run aborts | I/O or non-skippable error | Check path perms; rerun |

## Usage
Example invocations:
- "/meta-skill-indexer" — Run the full meta skill indexer workflow
- "meta skill indexer on this project" — Apply to current context

## Assumptions & Limits
- Assumes read access to `.agent/skills/` artifacts (code, docs, configs). [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Indexes frontmatter only — not skill body, examples, or referenced files. [INFERRED]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Duplicate `name` across skills | Disambiguate `id` by path; warn on collision |
| Malformed YAML frontmatter | Skip file, record warning, continue run |
| Empty `.agent/skills/` tree | Emit valid empty index `[]`, not an error |
